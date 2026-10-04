#!/usr/bin/env python3
"""dogfooding 手順 §4.2 の「機械的な抽出」を行う。

対象文書（プレーンテキスト）を1行ずつ走査し、空間語の出現を1出現1行で書き出す。
検索語は次の4種で、すべて pilot/part0-annexes.md から実行時に読み込む
（辞書の版と検索語の版を一致させるため、語をこのスクリプトに書き写さない）。

  A    附属書A の現場語と、同義・異表記の列
  G1   附属書G.1 の和文名
  G2   附属書G.2 の主名称（英）
  方向 手順書 §4.2 の目視用方向語（これだけは手順書の列挙を写している）

1行の中では長い語を優先し、重なる短い語は数えない（「搬送安定姿勢」を
「姿勢」としても数えると出現数が膨らむため）。
1文字の方向語（上、下、前、後、表、裏、正、逆）は「以上」「下記」のような
非空間の用法を多く拾うため、区分を「方向?」として出し、目視で残すか決める。

出力は記録ファイル（手順書 §6）の出現一覧にそのまま貼れる Markdown 表で、
主語・参照枠・代表形・区分の列は空欄にしておく（§4.3〜§4.5 は人が埋める）。
対象文書の原文はリポジトリに置かないため、抜粋は前後数文字に限る。

使い方:
  python3 review/dogfooding/extract.py <対象文書.txt> [--context N] [--no-single]
"""

import argparse
import pathlib
import re
import sys

ANNEX = pathlib.Path(__file__).resolve().parents[2] / "pilot" / "part0-annexes.md"

# 手順書 §4.2 の目視用方向語
DIRECTION_WORDS = [
    "右", "左", "前", "後", "手前", "奥", "上", "下", "上流", "下流",
    "表", "裏", "正", "逆", "正面", "背面", "内側", "外側",
]


def _clean(cell):
    cell = re.sub(r"\*\*|★|`", "", cell)
    cell = re.sub(r"[（(][^）)]*[）)]", "", cell)  # 「（本アーキテクチャ内の呼称）ハブ」の注記を落とす
    return cell.strip()


def _table_rows(lines, start_heading):
    """start_heading で始まる節の、最初の表のデータ行をセルの列として返す。"""
    in_section = False
    seen_table = False
    for line in lines:
        if line.startswith("#"):
            if in_section and seen_table:
                return
            in_section = line.startswith(start_heading)
            continue
        if not in_section:
            continue
        if line.startswith("|"):
            seen_table = True
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if re.fullmatch(r":?-+:?", cells[0]) or cells[0] in ("現場語ID", "和文名", "主名称（英）"):
                continue
            yield cells
        elif seen_table:
            return


def load_terms():
    lines = ANNEX.read_text(encoding="utf-8").splitlines()
    terms = {}  # 語 -> 出典の集合

    def add(word, source):
        word = _clean(word)
        if len(word) >= 1 and not re.fullmatch(r"[\s\-—$\[\]_,]*", word):
            terms.setdefault(word, set()).add(source)

    for cells in _table_rows(lines, "## 附属書A"):
        add(cells[1], "A")
        for syn in re.split(r"[／、]", cells[4]):
            add(syn, "A")
    for cells in _table_rows(lines, "### G.1"):
        add(cells[0], "G1")
    for cells in _table_rows(lines, "### G.2"):
        add(cells[0], "G2")
    for word in DIRECTION_WORDS:
        add(word, "方向")
    return terms


def scan(text, terms, context, keep_single):
    # 長い語から順に照合する。英字の語は大小文字を区別せず、単語境界で照合する。
    ordered = sorted(terms, key=len, reverse=True)
    patterns = []
    for word in ordered:
        if re.search(r"[A-Za-z]", word):
            patterns.append((word, re.compile(r"(?<![A-Za-z])" + re.escape(word) + r"(?![A-Za-z])", re.I)))
        else:
            patterns.append((word, re.compile(re.escape(word))))

    for lineno, line in enumerate(text.splitlines(), 1):
        taken = [False] * len(line)
        hits = []
        for word, pat in patterns:
            for m in pat.finditer(line):
                if any(taken[m.start():m.end()]):
                    continue
                for i in range(m.start(), m.end()):
                    taken[i] = True
                hits.append((m.start(), m.end(), word))
        for start, end, word in sorted(hits):
            sources = terms[word]
            single = sources == {"方向"} and len(word) == 1
            if single and not keep_single:
                continue
            excerpt = line[max(0, start - context):end + context].strip().replace("|", "\\|")
            label = "方向?" if single else "・".join(sorted(sources))
            yield lineno, line[start:end], label, excerpt


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("document", help="対象文書のプレーンテキスト（リポジトリ外に置く）")
    ap.add_argument("--context", type=int, default=8, help="抜粋に含める前後の文字数（既定 8）")
    ap.add_argument("--no-single", action="store_true", help="1文字の方向語を出力しない")
    args = ap.parse_args()

    terms = load_terms()
    text = pathlib.Path(args.document).read_text(encoding="utf-8")

    print("| # | 箇所 | 語 | 検索語の出典 | 抜粋 | 主語（附属書D #） | 参照枠 | 代表形 EED-ID | 区分 | メモ、起票ID |")
    print("| ---: | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    n = 0
    for lineno, word, label, excerpt in scan(text, terms, args.context, not args.no_single):
        n += 1
        print(f"| {n} | {lineno}行目 | {word} | {label} | {excerpt} |  |  |  |  |  |")
    print(f"\n検索語 {len(terms)} 語、出現 {n} 件（{ANNEX.name} から読み込み）", file=sys.stderr)


if __name__ == "__main__":
    main()
