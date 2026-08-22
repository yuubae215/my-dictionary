# my-dictionary

空間データを扱うモデリング（生産・ロボティクス・CAD・3Dソフトウェア全般）における概念辞書。原辞書（社内ドラフト、v0.17.0）を ISO 704 / ISO/IEC Directives Part 2 の記述規約に沿った自主技術仕様書（STD-EED-0001 シリーズ）へ、部（RAMI 4.0 の Layers 軸に対応）単位で段階的に変換している。

## 構成

| パス | 内容 |
| :--- | :--- |
| `source/dictionary_v0.17.0.md` | 変換元となる原辞書（全編）。読み取り専用の参照。編集しない。 |
| `pilot/part1-asset.md` | 第1編（物理資産／Asset層）ISO形式試作版。原辞書 第I部（1.01〜1.07）＋新設1件（interaction interface）に対応。 |
| `pilot/part2-integration.md` | 第2編（空間統合／Integration層）ISO形式試作版。原辞書 第II部（2.01〜2.16）に対応。 |
| `pilot/part3-information.md` | 第3編（意味・情報／Information層）ISO形式試作版。原辞書 第III部（3.01〜3.16）に対応。 |
| `decisions.md` | 変換過程で生じた判断の記録（改訂理由・命名判断・関係型の付与方針・検証で見つかった原辞書側の不整合など）。 |

## 変換の進め方

原辞書の部（第I部〜第V部、RAMI 4.0 Layers 軸に対応）を単位として、1部ずつ ISO 704 形式へ写像する。写像作業（定義文の逐語読み直し）はそれ自体が概念ドリフト検出器として機能するため、各部の変換時に次をセットで行う。

1. 定義文と命名意図（英語主名称・旧恒久ID・和文名）のズレ審査
2. 部立て説明文など、前文の件数・範囲の整合性チェック
3. 関連エントリへの関係型（is-a / part-of / refers-to / constrained-by / transforms / calibrated-from / aligns-with / mates-to）付与
4. 見つかった判断はすべて `decisions.md` に記録してから次の部へ進む

## 進捗

- [x] 第1編 物理資産（Asset層） — 概念7件（+新設1件）
- [x] 第2編 空間統合（Integration層） — 概念16件
- [x] 第3編 意味・情報（Information層） — 概念16件
- [ ] 第4編 機能・変換（Functional層） — 概念5件
- [ ] 第5編 契約・ガバナンス（Business層） — 概念1件
- [ ] メタ語彙編（M.01〜M.14、原辞書6.1節） — 全編化時に判断
- [ ] 附属書F以降（MECE検証・索引類） — 全編化時に追加
