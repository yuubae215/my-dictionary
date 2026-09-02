# TECHNICAL SPECIFICATION（試作版 / Pilot）

# 空間データを扱うモデリングの概念辞書 — 第2編: 空間統合 (Integration層)
Conceptual vocabulary for spatial-data modelling — Part 2: Spatial integration (Integration layer)

**文書番号（仮）:** STD-EED-0001-2
**版:** 0.1.0-pilot（原辞書 v0.17.0 からの変換試作）
**変換日:** 2026-08-21
**変換範囲:** 原辞書 第II部（2.01〜2.16、概念16件・現場語24語）

---

## 前書き (Foreword)

本仕様書は、第1編（物理資産／Asset層、STD-EED-0001-1）に続く、空間データを扱うモデリングにおける概念語彙の自主技術仕様書である。用語エントリの構造・記述フォーマット・変換方針は第1編と同一であり、詳細は第1編前書きを参照。以下は本編（第2編）固有の申し合わせである。

- 原辞書の**恒久ID（IRDI）は一切変更していない**。第II部の概念採番（原 `2.01`〜`2.16`）は本仕様書の `3.1`〜`3.16` に**欠番なく1対1で対応**する（附属書E.1）。第1編で発生した概念分離（原1.07 → 3.7／3.8）のような番号のずれは、本編には生じていない。
- 第1編の申し合わせどおり、**エントリ本文には IRDI のみを残し、その他のメタデータは附属書Bに集約**する。
- **概念間関係には第1編で定義した4型（is-a／part-of／refers-to／constrained-by）に加え、本編で新たに `transforms` 型を導入する**（附属書C.1）。第1編附属書C.1 NOTE 1 で予告した4型のうち、`transforms` は 3.12（座標変換）が 3.7（ローカル空間）の値を 3.8（ワールド空間）の値へ変換するという操作関係を表すために確定使用した。`calibrated-from`・`aligns-with`・`mates-to` は本編でも根拠となりうる候補箇所が見つかったが、確信度が is-a／transforms ほど高くないため、各該当エントリの Note に**候補**として明記するにとどめ、正式な型としては採用していない（確定は全編化時のレビューに委ねる。詳細は `decisions.md` D-2026-08-21-03）。
- **写像作業（定義文の逐語読み直し）による検証の結果、本編16概念に、第1編1.07（eed:0007）のような概念ドリフト（定義文と命名意図の乖離）は確認されなかった（0/16）。** 英語主名称・旧恒久ID（`term.*` スラグ）・定義文の三者は全エントリで整合していた。
- **原辞書の記述に、部立て説明文（4.2節相当）の件数・範囲の誤記を1件発見した。** 原辞書該当箇所（前文592行目付近）は「II-B 位置・姿勢という値（2.05〜2.09、4件）」「II-D 空間に設置される意味づけられた要素（2.13〜2.16、3件）」と記すが、実際の本文見出し・エントリ配置は II-B が `2.05`〜`2.10`（6件、見出し自体は「位置・姿勢・**隔たり**という値」と正しく `2.10` を含意している）、II-D が `2.13`〜`2.16`（4件）である。本仕様書 Clause 5 では実体に合わせて是正した表記を採用する（`decisions.md` D-2026-08-21-01）。
- 原辞書 3章「基礎規約」は、第1編附属書E.3が定めた変換計画（「3章 基礎規約 → 第2編（Integration層）の Clause 4 として規定」）に従い、本編 **Clause 4** として収録する。第1編には基礎規約に相当するClauseがなかったため、本編で初めて登場する（`decisions.md` D-2026-08-21-02）。この配置替えに伴い、第1編で Clause 4 だった「概念体系」は本編では **Clause 5** に繰り下がる。
- 原辞書の独自コンテンツ（登場人物対応表の該当抜粋）は、第1編と同様に informative な附属書Dとして保全する。

## 序文 (Introduction)

第II部が扱うのは、物理世界（第1編／Asset層）を計算可能な仮想表現へ橋渡しする関心事である。物理資産そのものではなく、その位置・向き・隔たりを、数値として一意に読み書きできるようにする仕組みを定義する。

```mermaid
flowchart TD
    OBJ["第1編の物理実体<br/>ワーク・治具・設備・人"]
    RULE["Clause 4 基礎規約<br/>右手系・SI単位・クォータニオン"]
    CS["座標系そのもの (Clause 3, II-A)"]
    VAL["位置・姿勢・隔たりという値 (II-B)"]
    OP["変換という操作 (II-C)"]
    ELEM["空間に設置される意味づけられた要素 (II-D)"]

    OBJ -->|"仮想表現へ写像"| CS
    RULE -.->|"数値化の前提を固定"| CS
    CS -->|"上に成り立つ"| VAL
    VAL -->|"座標系間を行き来する"| OP
    CS -->|"意味づけられた点・領域が設置される"| ELEM
    ELEM -->|"位置決め・校正の基準になる"| VAL
```

## 1 適用範囲 (Scope)

本仕様書は、空間データを扱うモデリングにおいてステークホルダー間の共通言語を確立するための概念語彙のうち、**物理世界を計算可能な仮想表現へ橋渡しする関心事（Integration層）に属する用語、定義、および概念間関係のセマンティクス**について規定します。

適用範囲は以下の通りです：

* 座標系そのものの定義・基準・手性・尺度（II-A）
* 位置・姿勢・隔たりという値とその表現規約（II-B）
* 座標系間の変換という操作（II-C）
* 空間に設置される意味づけられた要素（基準フィーチャー・キャリブレーション基準・干渉禁止領域・アプローチ方向）（II-D）

特定のプログラミング言語、ファイル形式、通信規格、製品、リポジトリには依存しません。実装（TFツリー実装、URDF、OPC UA情報モデル等）へのマッピングは、本仕様書を下敷きにした別工程として扱います。

## 2 参照標準・参考文献 (References)

第1編と同一の参照群に加え、本編では以下を主に参照・活用しています：

* ISO 704:2009, Terminology work — Principles and methods
* ROS REP-103, Standard Units of Measure and Coordinate Conventions
* ISO 10303 (STEP AP242), Industrial automation systems and integration — Product data representation and exchange
* ISO 5459 / ISO 10303-242, Geometrical product specifications (GD&T / PMI) — Datums
* ISO 9787, Robots and robotic devices — Coordinate systems and motion nomenclatures
* OPC UA for Robotics（ロボットの姿勢表現・負荷特性の標準データモデル）
* DIN SPEC 91345:2016-04, Reference Architecture Model Industrie 4.0 (RAMI 4.0)

## 3 用語及び定義 (Terms and Definitions)

各エントリは、用語（英語主名称・和文名・admitted term）、恒久ID（IRDI）、定義文、適用例（EXAMPLE）、およびエントリ注記（Note 1: コアイメージ／Note 2: 概念間関係／Note 3以降: 用法上の注意）で構成されます。分類メタデータは附属書Bに集約しています。

**サブグループ（区分基準＝主題。原辞書の件数誤記を是正、`decisions.md` D-2026-08-21-01）:** II-A 座標系そのもの（3.1〜3.4、4件）／ II-B 位置・姿勢・隔たりという値（3.5〜3.10、6件）／ II-C 変換という操作（3.11〜3.12、2件）／ II-D 空間に設置される意味づけられた要素（3.13〜3.16、4件）。

**II-A. 座標系そのもの**

### 3.1
**coordinate system**
座標系
IRDI: `eed:0008#001`

空間上の点の位置・向きを、1つの原点と、互いに直交する軸（本仕様書ではClause 4に従い右手系のX, Y, Z軸）に対する数値の組として表現するための、最も基本的な枠組み。本編の他のエントリ（3.2、3.7、3.8等）は、いずれもこの枠組みが具体的にどこに設置され、他の座標系とどう関係するかを規定する下位概念である。

EXAMPLE （生産・CAD共通）Clause 4 に定めるROS REP-103準拠の右手直交座標系（+X前方、Y左、Z上）。あらゆる位置・姿勢データは、最終的にこの座標系上の数値の組として表現される。

Note 1 to entry: Core image：空間内のあらゆる位置を、原点からの数値の組（X, Y, Z）として一意に読み取れるようにする、物差しと目盛りの枠組みそのもの。

Note 2 to entry: Concept relations:
— refers-to 3.3 (handedness)
— refers-to 3.7 (local space), 3.8 (world space)
— refers-to 3.9 (hierarchical coordinate structure)
— refers-to 3.10 (distance metric convention)

### 3.2
**reference coordinate frame**
参照座標系
IRDI: `eed:0009#001`

座標系（3.1）のうち、ある親座標系（またはワールド座標系）からの相対的な位置と向きによって定義される、局所的な基準座標系。

EXAMPLE 1 （生産）製品基準座標系（MCS）。データムフィーチャーの交点として定義され、すべての把持点・配置基準点がこの座標系からの相対値として表現される。

EXAMPLE 2 （CAD）親を持ち木構造を成す座標フレーム。並進と回転を持つ。

Note 1 to entry: Core image：空間のどこかに立てられた、それ自身の見取り図の原点を持つ旗。

Note 2 to entry: Concept relations:
— is-a 3.1 (coordinate system)
— refers-to 3.3 (handedness), 3.4 (unit scale convention), 3.5 (pose), 3.7 (local space), 3.8 (world space), 3.11 (homogeneous transformation matrix), 3.12 (coordinate transformation)
— refers-to 3.9 (hierarchical coordinate structure) ※階層座標構造を構成する各ノードは参照座標系であり、part-of（3.2 が 3.9 の部分）の候補。確信度は is-a ほど高くなく、全編化時に精密化する
— refers-to 3.13 (datum reference feature) ※constrained-by（拘束）の候補。3-2-1データム拘束によって参照座標系（例：製品基準座標系）が確立される関係にあたる
— refers-to 3.14 (calibration reference) ※calibrated-from の候補。2つの参照座標系間の未知変換がキャリブレーション基準によって解かれる関係にあたる

### 3.3
**handedness**
座標系のハンドネス
admitted term: right-handed / left-handed
IRDI: `eed:0010#001`

座標系の3軸（X, Y, Z）の向きの組み合わせが、右手系（$X \times Y = Z$）と左手系（$X \times Y = -Z$）のどちらの規約に従うかという区別。軸のラベル（前方・左・上等）が一致していても、ハンドネスが異なれば回転の正負や外積の結果が反転する。

EXAMPLE 1 （生産）ROS REP-103に基づく右手系を全社的な規約として採用（Clause 4）。

EXAMPLE 2 （CAD）一部のCADソフトウェアやゲームエンジンはY-up左手系をデフォルトとするため、外部データ取り込み時にハンドネス変換（Z軸反転等）が必要になる。

Note 1 to entry: Core image：右手でも左手でも「X軸→Y軸→Z軸」という並びの名前は同じに見えるが、実際に指を折ってみると、Z軸が上を向くか下を向くかが逆になる。

Note 2 to entry: Concept relations:
— refers-to 3.1 (coordinate system), 3.2 (reference coordinate frame)
— refers-to 3.7 (local space), 3.8 (world space)
— refers-to 3.6 (rotation representation convention)

### 3.4
**unit scale convention**
尺度定義
admitted term: scale factor（スケールファクタ）
IRDI: `eed:0011#001`

モデル内部で扱う数値が、どの物理単位（またはどの縮尺）を1として表現されているかを明示し、実データがその規約通りの尺度で保存・送受信されているかを保証する考え方。

EXAMPLE 1 （生産）異なるCADシステム間でファイルを受け渡す際、内部単位がmmかcmかを確認せずインポートし、ワークが1000倍の大きさで配置されてしまう不具合とその防止策。

EXAMPLE 2 （CAD）シーンファイルの単位設定（メートル法／インペリアル）を読み込み時に検証し、規約と異なる場合は自動変換または警告を発する仕組み。

Note 1 to entry: Core image：図面に書かれた「10」という数値が、mm単位なのかcm単位なのか、それとも単位のない相対値なのかによって、実際の大きさが最大1000倍も変わってしまう取り違えの罠。

Note 2 to entry: Concept relations:
— refers-to 3.2 (reference coordinate frame)
— refers-to 3.11 (homogeneous transformation matrix)

Note 3 to entry: 単位系そのものの規定はClause 4が担う。本エントリは、個々のCADファイル・センサデータ・通信メッセージが実際にその規約を守れているかを検証・変換する運用側の責務を指す。

**II-B. 位置・姿勢・隔たりという値**

### 3.5
**pose**
姿勢
IRDI: `eed:0012#001`

位置（並進）と向き（回転）を組み合わせた空間的状態。

EXAMPLE 1 （生産）把持目標姿勢、搬送安定姿勢。

EXAMPLE 2 （CAD）立体の主要状態（原点位置と向き）。

Note 1 to entry: Core image：「どこにいて、どちらを向いているか」を一組で表す1枚のスナップショット。

Note 2 to entry: Concept relations:
— refers-to 1.04 (stable pose, 第1編 3.4), 1.05 (resolution, 第1編 3.5)
— refers-to 3.2 (reference coordinate frame), 3.6 (rotation representation convention), 3.10 (distance metric convention), 3.11 (homogeneous transformation matrix), 3.16 (approach vector)
— refers-to 3.9 (grasp specification and synthesis, 第3編), 3.10 (symmetry rule, 第3編)

### 3.6
**rotation representation convention**
回転表現規約
IRDI: `eed:0013#001`

回転をどの形式で表現するか、およびその形式に付随する曖昧さをどう固定するかの取り決め。クォータニオン・回転行列・回転ベクトル（軸角）は表現として一意だが人が直感的に読めない。オイラー角は読める代わりに、次の2つを併記しなければ姿勢が一意に定まらない。(1) **回転順序**：どの軸をどの順に回すか（Z-Y-X、X-Y-Z など全12通り）。(2) **内因性 / 外因性**：各回転を、直前の回転で一緒に動いた軸まわりに行う内因性（intrinsic / rotated axes）か、常に固定された基準軸まわりに行う外因性（extrinsic / static axes）か。

EXAMPLE 1 （生産）ロボットティーチングペンダントに表示されるRPY値。メーカーごとに内因性・外因性と順序が異なり、同じ数値でも別の姿勢を指す。

EXAMPLE 2 （CAD）外部フォーマットからオイラー角を取り込む際、順序と内因性・外因性を確定させないとクォータニオンへ変換できない。

Note 1 to entry: Core image：「Z→Y→X の順に回す」と言われても、軸が回転に連れて一緒に動くのか、床に描いた線のように固定されたままなのかで、行き着く姿勢はまったく別物になる。

Note 2 to entry: Concept relations:
— refers-to 3.3 (handedness), 3.5 (pose), 3.11 (homogeneous transformation matrix)

Note 3 to entry: ジンバルロックはオイラー角に固有の縮退であり、表現形式の選択理由になる。Clause 4 は本アーキテクチャの既定値（クォータニオン、外因性X→Y→Z）を定めるが、外部から受け取るデータがその規約に従っている保証はないため、取り込み時に必ず順序と内因性・外因性を確認する。

### 3.7
**local space**
ローカル空間
IRDI: `eed:0014#001`

ある参照座標系（3.2）を基準とした相対位置・相対姿勢として表現される空間。親フレームからの相対値であり、親フレーム自体が動いても局所的な値は変化しない。

EXAMPLE 1 （生産）すべての位置・姿勢データに参照座標系を明示する基礎規約（Clause 4）における、親フレーム相対の表現。

EXAMPLE 2 （CAD）オブジェクトの原点位置・向きを親フレーム基準で保持する型システム。

Note 1 to entry: Core image：「自分の部屋の中での位置」。部屋（親フレーム）が動けば、部屋の中の物の見え方は変わらないまま一緒に動く。

Note 2 to entry: Concept relations:
— refers-to 3.1 (coordinate system), 3.2 (reference coordinate frame), 3.3 (handedness)
— refers-to 3.8 (world space) ※対比ペア。3.4節参照
— refers-to 3.12 (coordinate transformation)

Note 3 to entry: 対になるワールド空間（3.8）と暗黙に混同してはならない（Clause 4 の規約）。原辞書2.4節「対比によって識別される語彙ペア」の一組（ローカル空間／ワールド空間）にあたる。

### 3.8
**world space**
ワールド空間
IRDI: `eed:0015#001`

シーン全体（ルートとなる座標系）を基準とした絶対的な空間。ローカル空間（3.7）の値を、階層座標構造（3.9）に沿って親から親へと座標変換（3.12）することで得られる。

EXAMPLE 1 （生産）搬送経路計画で、複数のロボット・治具の位置を1つの共通基準で比較する際に必要になる表現。

EXAMPLE 2 （CAD）ワールド座標キャッシュが保持する、シーン全体基準の座標値。

Note 1 to entry: Core image：「街全体の地図での位置」。どの建物（親フレーム）に属していても、同じ1枚の地図上の1点として表せる。

Note 2 to entry: Concept relations:
— refers-to 3.1 (coordinate system), 3.2 (reference coordinate frame), 3.3 (handedness)
— refers-to 3.7 (local space) ※対比ペア。3.4節参照
— refers-to 3.9 (hierarchical coordinate structure), 3.12 (coordinate transformation) ※定義文が「階層座標構造（3.9）に沿って親から親へと座標変換（3.12）することで得られる」と両者を名指ししている（3.9 は第M編附属書F.4 で追加）
— refers-to 3.11 (self-validating freshness guarantee, 第M編)

### 3.9
**hierarchical coordinate structure**
階層座標構造
IRDI: `eed:0016#001`

複数の参照座標系を木構造として組み上げ、上位フレームの変化が下位フレームに伝播する構造。

EXAMPLE 1 （生産）アセンブリの親子構成関係や、ロボットのTFツリー。

EXAMPLE 2 （CAD）座標フレームの親子関係、ロボットのベースフレームとTCPフレームという2ノード構造。

Note 1 to entry: Core image：体の各部位が親子関係でつながった骨格アニメーションの骨。

Note 2 to entry: Concept relations:
— refers-to 3.1 (coordinate system), 3.2 (reference coordinate frame) ※3.2は3.9の構成要素である可能性（part-of候補、全編化時に精密化）
— refers-to 3.11 (homogeneous transformation matrix), 3.12 (coordinate transformation)
— refers-to 3.7 (typed relation, 第3編)

### 3.10
**distance metric convention**
距離定義規約
admitted term: metric／Minkowski距離（L1・L2・L∞）
IRDI: `eed:0017#001`

2点間の隔たりをどう測るかという取り決め。同じ2点であっても採る距離の定義が変われば数値が変わるため、距離を数値として扱う場面では、どの定義によるかを併記しなければ一意にならない。

EXAMPLE 1 （生産）直交機構（門型ローダやガントリ）の各軸を順に動かす移動時間は、軸ごとの移動量の和（マンハッタン距離）に比例する。一方、同時5軸で補間しながら動く場合は直線距離（ユークリッド距離）に近い。同じ2点でも、機構が違えば「近い」の意味が変わる。

EXAMPLE 2 （CAD・ロボティクス）干渉判定のクリアランスはユークリッド距離、格子状のパス探索コストはマンハッタン距離、バウンディングボックスの重なり判定はチェビシェフ距離が自然になる。

Note 1 to entry: Core image：「2点間の距離は5」と言われても、まっすぐ突っ切った5なのか、縦と横に分けて足した5なのかで、意味も所要時間もまったく違う。

Note 2 to entry: Concept relations:
— refers-to 3.1 (coordinate system), 3.5 (pose)
— refers-to 3.2 (measurement, 第4編)
— refers-to 3.4 (unit scale convention), 3.6 (rotation representation convention) ※Note 3 が名指しする「同じ型の落とし穴」の2件（第M編附属書F.4 で追加）

Note 3 to entry: 3.4（尺度定義）、3.6（回転表現規約）と同じ型の落とし穴である。いずれも「技術的には他の選択肢でも成立するが、どれを採ったかを書かなければ受け手が復元できない」取り決めであり、書き忘れても数値としては通ってしまう。

**II-C. 変換という操作**

### 3.11
**homogeneous transformation matrix**
同次変換行列
IRDI: `eed:0018#001`

回転行列と並進ベクトルを1つの4×4正方行列にまとめ、複数の座標変換を単純な行列積の連鎖として合成できるようにする数学的表現。

EXAMPLE 1 （生産）ロボットのベースフレームからTCPフレームへの変換を表す4×4行列。TFツリー（3.9）のノード間変換の実体。

EXAMPLE 2 （CAD）座標フレームの親子関係を辿って、あるオブジェクトのワールド座標を求める際に内部で連鎖させる変換行列。

Note 1 to entry: Core image：「回転」と「平行移動」という別々の操作を、1回の掛け算だけで連続的につなげられるようにする、4×4の計算専用の箱。

Note 2 to entry: Concept relations:
— refers-to 3.2 (reference coordinate frame), 3.4 (unit scale convention), 3.5 (pose), 3.6 (rotation representation convention), 3.9 (hierarchical coordinate structure), 3.12 (coordinate transformation)
— refers-to 3.14 (calibration reference) ※calibrated-from の候補。キャリブレーションで得られた変換行列である場合に成立する関係であり、全ての同次変換行列がこの由来を持つわけではない

Note 3 to entry: 姿勢（3.5）が「位置と向きという値そのもの」を指すのに対し、本エントリはその値を座標変換の計算に使える形に変換した**表現手段**を指す。

### 3.12
**coordinate transformation**
座標変換
IRDI: `eed:0019#001`

ある参照座標系で表現された位置・姿勢の値を、別の参照座標系（親・子・ワールド等）で表現された値へと変換する操作。設計段階の幾何（Type）にも、実機の姿勢計算（Instance）にも同じ操作が成立する。

EXAMPLE 1 （生産）製品基準座標系（MCS）で定義された把持点を、ロボットのベースフレーム基準の値へ変換してロボットに渡す処理。

EXAMPLE 2 （CAD）親フレームのローカル座標をワールド座標へ変換してレンダリングする処理（ワールド座標キャッシュ）。

Note 1 to entry: Core image：「自分の部屋の中での位置」を「街全体の地図での位置」に翻訳する、変換という作業そのもの。

Note 2 to entry: Concept relations:
— transforms 3.7 (local space) → 3.8 (world space) ※本編で確定した最初の transforms 型。ローカル空間の値を、階層座標構造（3.9）に沿ってワールド空間の値へ変換する操作関係を表す
— refers-to 3.2 (reference coordinate frame), 3.9 (hierarchical coordinate structure), 3.11 (homogeneous transformation matrix), 3.14 (calibration reference)
— refers-to 3.11 (self-validating freshness guarantee, 第M編)

Note 3 to entry: 階層座標構造（3.9）が座標系同士の木構造そのものを指すのに対し、本エントリはその木を辿って値を実際に計算する**動作**を指す。

**II-D. 空間に設置される意味づけられた要素**

### 3.13
**datum reference feature**
基準フィーチャー
IRDI: `eed:0020#001`

位置決め・原点定義・意味的な基準点となる、面・穴・中心線・結節点などの幾何要素。

EXAMPLE 1 （生産）データムフィーチャーおよび位置決めフィーチャー（治具の基準ピン穴・突き当て面）。

EXAMPLE 2 （CAD）空間注記における「ハブ」（結節点・基準点：交差点、出入口、基準穴、治具固定点）。この役割は一般には**ランドマーク**と呼ばれ、校正基準としての側面は 3.14（キャリブレーション基準）が扱う。

Note 1 to entry: Core image：測るときに誰もが指を置く物差しの起点。

Note 2 to entry: Concept relations:
— refers-to 1.02 (topology, 第1編 3.2)
— refers-to 3.2 (reference coordinate frame) ※constrained-by の候補（3.2 のNote 2参照）
— refers-to 3.14 (calibration reference) ※aligns-with の候補。カメラ座標系とロボットベース座標系はランドマーク（3.14）で結び、ロボットとワーク座標系は本エントリ（データム）を実測して結ぶという、2つの位置合わせ手段が連鎖する関係にあたる
— refers-to 3.7 (typed relation, 第3編), 3.8 (spatial element classification, 第3編)

### 3.14
**calibration reference**
キャリブレーション基準
admitted term: calibration target
IRDI: `eed:0021#001`

**既知の幾何**（寸法・形状・特徴点の配置）を持ち込むことで、2つの座標系のあいだの未知の変換を解けるようにするための基準物または基準特徴。既知量がなければ観測値と真値の差を取れないため、既知の幾何を含むことが本質的な要件であり、単に「目印になる」だけでは足りない。

EXAMPLE 1 （生産）チェッカーボード（格子ピッチが既知）、ARマーカー（辺長と符号が既知）、基準球（直径が既知、3Dスキャナ用）、校正治具（穴位置が既知）。ハンドアイキャリブレーションでは、ロボットのTCPの既知幾何そのものが基準になる。

EXAMPLE 2 （CAD・ロボティクス）校正結果はカメラ座標系からロボットベース座標系への同次変換行列（3.11）として保存される。

Note 1 to entry: Core image：寸法が分かっているものを1つ置いてやると、カメラとロボットが「同じ世界の話をしている」と初めて言えるようになる。

Note 2 to entry: Concept relations:
— refers-to 1.05 (resolution, 第1編 3.5)
— refers-to 3.2 (reference coordinate frame) ※calibrated-from の候補（3.2 のNote 2参照）
— refers-to 3.11 (homogeneous transformation matrix) ※calibrated-from の候補（3.11 のNote 2参照）
— refers-to 3.12 (coordinate transformation)
— refers-to 3.13 (datum reference feature) ※aligns-with の候補（3.13 のNote 2参照）
— refers-to 3.8 (spatial element classification, 第3編)

Note 3 to entry: 3.13（基準フィーチャー）とは役割が異なるが、実務では**連鎖して使う**。カメラ座標系とロボットベース座標系はランドマークや校正ボード（本エントリ）で結び、ロボットとワーク座標系はデータム（3.13）を実測して結ぶ。どちらか一方だけでは、カメラで見た点をワークのどこかとして語れない。読み取れる細かさは 1.05（分解能、第1編 3.5）が上限を決める。

### 3.15
**exclusion zone**
干渉禁止領域
IRDI: `eed:0022#001`

ツールや治具が接触・侵入してはならないと定義された幾何領域。

EXAMPLE （生産）鏡面加工部・センサ受光部など、把持ツールの接触が禁止される領域。安全マージンを必ず持つ。

Note 1 to entry: Core image：「ここに触れるな」という見えない立入禁止テープ。

Note 2 to entry: Concept relations:
— refers-to 3.9 (grasp specification and synthesis, 第3編)

### 3.16
**approach vector**
アプローチ方向
IRDI: `eed:0023#001`

把持や接触の直前に、ツールが対象へ近づく方向を表す単位ベクトル。

EXAMPLE 1 （生産）把持目標姿勢に付随する許容アプローチ方向。

EXAMPLE 2 （CAD）エンドエフェクタのフレームから導出される進入ベクトル。

Note 1 to entry: Core image：手を伸ばす最後の一瞬、どの向きから近づくか。

Note 2 to entry: Concept relations:
— refers-to 3.5 (pose)
— refers-to 3.9 (grasp specification and synthesis, 第3編)

## 4 基礎規約 (Foundational Physical & Mathematical Rules)

原辞書3章「基礎規約」を、第1編附属書E.3の変換計画に従い本編Clauseとして収録したものである（`decisions.md` D-2026-08-21-02）。本章は規約そのものを定める。**規約が実データ上で実際にどう扱われるか**（変換・尺度検証・軸の向きの取り違え防止）はClause 3の各エントリ（3.1〜3.12）が扱う。ただし計測限界（分解能）は計測装置という物理資産そのものの限界であるため、第1編3.5（Resolution）にある。

| 項目 | 規定仕様 | 準拠規格 / 備考 |
| :--- | :--- | :--- |
| **空間座標系** | $+X$ 前方、$Y$ 左、$Z$ 上、右手直交座標系 | ROS REP-103 準拠 → 3.1, 3.3 |
| **長さ・距離** | $\text{mm}$ (ミリメートル) | SI単位系 → 3.4, 3.10 |
| **角度** | $\text{deg}$ (度) または $\text{rad}$ (ラジアン) | 内部処理は $\text{rad}$、UI/対話は $\text{deg}$ → 3.6 |
| **質量 / 慣性** | $\text{kg}$ / $\text{kg}\cdot\text{m}^2$ | IEC 61360 → 第1編 3.3 |
| **力 / トルク** | $\text{N}$ / $\text{N}\cdot\text{m}$ | 把持力・締結トルク（第3編 把持宣言と解決で使用） |
| **回転姿勢** | クォータニオン $[q_x, q_y, q_z, q_w]$ ($q_w$ は実部) | 補助表示としてオイラー角を併記する場合は、**外因性（extrinsic・固定軸）$X$→$Y$→$Z$**（ROS REP-103のroll-pitch-yaw、内因性 $Z$-$Y$-$X$ と等価）と明示する。順序と内因性・外因性の指定を欠いた「RPY」表記は姿勢を一意に定めない → 3.6 |
| **空間参照** | 親フレーム中心からの相対オフセット | ローカル空間とワールド空間の混同を禁止 → 3.7, 3.8 |

## 5 概念体系 (Concept System)

本編の16概念は、主題により4つのサブグループに区分されます（区分基準＝主題。原辞書の件数・範囲の誤記を是正、`decisions.md` D-2026-08-21-01）。

```mermaid
flowchart TB
    P2["第2編 Integration層（16概念）"]
    P2 --> A["II-A 座標系そのもの"]
    P2 --> B["II-B 位置・姿勢・隔たりという値"]
    P2 --> C["II-C 変換という操作"]
    P2 --> D["II-D 空間に設置される意味づけられた要素"]

    A --> A1["3.1 coordinate system"]
    A --> A2["3.2 reference coordinate frame"]
    A --> A3["3.3 handedness"]
    A --> A4["3.4 unit scale convention"]
    B --> B1["3.5 pose"]
    B --> B2["3.6 rotation representation convention"]
    B --> B3["3.7 local space"]
    B --> B4["3.8 world space"]
    B --> B5["3.9 hierarchical coordinate structure"]
    B --> B6["3.10 distance metric convention"]
    C --> C1["3.11 homogeneous transformation matrix"]
    C --> C2["3.12 coordinate transformation"]
    D --> D1["3.13 datum reference feature"]
    D --> D2["3.14 calibration reference"]
    D --> D3["3.15 exclusion zone"]
    D --> D4["3.16 approach vector"]

    A2 -->|is-a| A1
    C2 -->|transforms| B3
    C2 -->|transforms| B4
    B3 <-->|"対比ペア"| B4
    D1 -.->|"aligns-with 候補"| D2
    A2 -.->|"calibrated-from 候補"| D2
    A2 -.->|"constrained-by 候補"| D1
```

図の見方：実線矢印は本編で確定した関係型（is-a・transforms）、点線矢印は根拠はあるが確信度が十分でないため候補にとどめた関係型（`decisions.md` D-2026-08-21-03）。

---

## 附属書A (informative) 現場語・通称対応表 (Shopfloor & Colloquial Terms Mapping)

本編で定義された概念（Clause 3）と、現場で実際に使われる通称・俗称（Shopfloor Terms）との対比表です。各現場語は**ちょうど1つの代表形（概念）**と**ちょうど1つの主語（登場人物、附属書D）**を持ちます。

| 現場語ID | 代表形（概念） | 現場語 (JP) | 主語（登場人物） | 現場での使用場面例 | 同義・異表記 |
|---|---|---|---|---|---|
| `eed:0072#001` | 3.2 reference coordinate frame | 製品基準座標系 | ワーク（被加工物・部品・製品） | 製品設計・データムの交点として定義し、把持点や配置基準点の相対原点にする | MCS／ワーク原点 |
| `eed:0073#001` | 3.2 reference coordinate frame | データム系 | ワーク（被加工物・部品・製品） | 一次・二次・三次の3つのデータム平面で6自由度を拘束し、ワーク座標系を確立する（3-2-1拘束） | DRF／datum reference frame／データム参照系 |
| `eed:0074#001` | 3.2 reference coordinate frame | 座標フレーム | 架台・ベースプレート・床 | CAD・親を持ち木構造を成す局所座標 | フレーム／ノード座標系 |
| `eed:0075#001` | 3.6 rotation representation convention | クォータニオン | 産業用ロボット（多関節マニピュレータ） | 内部処理・補間と合成に使う一意な表現 | 四元数／$[q_x, q_y, q_z, q_w]$ |
| `eed:0076#001` | 3.6 rotation representation convention | 回転行列 | 産業用ロボット（多関節マニピュレータ） | 座標変換の計算に使う$3 \times 3$表現 | 姿勢行列／DCM |
| `eed:0077#001` | 3.6 rotation representation convention | 回転ベクトル | 産業用ロボット（多関節マニピュレータ） | 一部のロボットメーカーが姿勢指令に使う軸角表現 | 軸角／Rodriguesベクトル |
| `eed:0078#001` | 3.6 rotation representation convention | オイラー角 | 産業用ロボット（多関節マニピュレータ） | UI表示と人手ティーチング。順序と内因性・外因性の併記が必須 | RPY／ロール・ピッチ・ヨー／ABC角 |
| `eed:0079#001` | 3.6 rotation representation convention | 内因性・外因性 | 産業用ロボット（多関節マニピュレータ） | オイラー角の解釈を確定させる指定 | intrinsic／extrinsic、rotated axes／static axes、可動軸／固定軸 |
| `eed:0080#001` | 3.9 hierarchical coordinate structure | TFツリー | 産業用ロボット（多関節マニピュレータ） | ロボティクス・ベースからTCPまでの座標系の木 | 座標変換ツリー／TF |
| `eed:0081#001` | 3.9 hierarchical coordinate structure | アセンブリ親子構成 | ワーク（被加工物・部品・製品） | 製品設計・部品の組み付け階層 | BOM構造／構成ツリー |
| `eed:0082#001` | 3.10 distance metric convention | ユークリッド距離 | ワーク（被加工物・部品・製品） | 2点を直線で結んだときの隔たり。クリアランスや公差の評価 | 直線距離／L2ノルム |
| `eed:0083#001` | 3.10 distance metric convention | マンハッタン距離 | 工作機械・専用機（CNC、プレス、溶接機など） | 軸ごとの移動量を足し合わせた隔たり。直交機構の移動コスト評価 | 市街地距離／L1ノルム |
| `eed:0084#001` | 3.10 distance metric convention | チェビシェフ距離 | ワーク（被加工物・部品・製品） | 各軸の差の最大値。AABB同士の隔たり判定 | L∞ノルム／最大値ノルム |
| `eed:0085#001` | 3.11 homogeneous transformation matrix | 4×4変換行列 | 産業用ロボット（多関節マニピュレータ） | ロボティクス・ベースからTCPへの変換の実体 | 同次行列／変換マトリクス |
| `eed:0086#001` | 3.13 datum reference feature | データムフィーチャー | ワーク（被加工物・部品・製品） | 製品設計・GD&T（ISO 5459）における測定と位置決めの起点 | データム／基準面・基準穴 |
| `eed:0087#001` | 3.13 datum reference feature | 位置決めフィーチャー | 治具（ジグ）・位置決めピン・突き当て面 | 設備制御・治具側でワークを毎回同じ姿勢に決める要素 | 基準ピン穴／突き当て面 |
| `eed:0088#001` | 3.13 datum reference feature | データム | ワーク（被加工物・部品・製品） | データムフィーチャーから導かれる、理論的に完全な点・軸・平面 | 理論データム／datum |
| `eed:0089#001` | 3.14 calibration reference | ランドマーク | 架台・ベースプレート・床 | ビジョン系の校正・自己位置推定で、既知の位置に固定して座標系どうしを対応づける | 校正基準／（本アーキテクチャ内の呼称）ハブ |
| `eed:0090#001` | 3.14 calibration reference | チェッカーボード | ビジョンカメラ・3Dスキャナ | カメラ内部パラメータと外部パラメータの同時校正 | 校正ボード／格子パターン |
| `eed:0091#001` | 3.14 calibration reference | ARマーカー | ビジョンカメラ・3Dスキャナ | 辺長既知の平面マーカーで単眼から姿勢を得る | ArUco／AprilTag／基準マーカー |
| `eed:0092#001` | 3.14 calibration reference | 基準球 | ビジョンカメラ・3Dスキャナ | 直径既知の球で3Dスキャナ間の位置合わせを行う | 校正球／ターゲットスフィア |
| `eed:0093#001` | 3.14 calibration reference | 校正治具 | 治具（ジグ）・位置決めピン・突き当て面 | 穴位置が既知の治具でロボットとワーク座標系を対応づける | キャリブレーションジグ／マスタージグ |
| `eed:0094#001` | 3.15 exclusion zone | 接触禁止領域 | ワーク（被加工物・部品・製品） | 生産・鏡面加工部やセンサ受光部など触れてはならない面 | タッチ禁止面／NGエリア |
| `eed:0095#001` | 3.16 approach vector | 許容アプローチ方向 | エンドエフェクタ（ハンド・グリッパ・吸着パッド） | ロボティクス・把持直前の進入向き | 進入ベクトル／アプローチベクトル |

NOTE 3.1（座標系）、3.2の別表現、3.3（ハンドネス）、3.4（尺度定義）、3.5（姿勢）、3.7（ローカル空間）、3.8（ワールド空間）、3.12（座標変換）に対応する現場語は未抽出（原辞書の記載を保存。存在しない現場語を創作しない）。

## 附属書B (informative) 概念メタデータ一覧 (Concept Metadata Registry)

- **Hier. Level / Life Cycle**: RAMI 4.0 の Hierarchy Levels 軸・Life Cycle 軸。**Layers 軸の欄は設けない**（編構成と一対一に対応するため。本編収録の全概念は `Integration`）。
- **Provider / Consumer**: 責務タグ。ロール名は第1編と同じ（ProductDesign／MfgRobotics／StationControl／ShopfloorIT／MetaArchitecture＝共通アーキテクチャ）。
- **語彙区分**: 標準／業界一般／独自の3値。
- **カバレッジ**: 実例を確認済みの分野（生産 / CAD・ロボティクス）。`—` は未確認。

| 採番 | 用語 | IRDI | 旧ID | Hier. Level | Life Cycle | Provider | Consumer | 語彙区分 | カバレッジ |
|---|---|---|---|---|---|---|---|---|---|
| 3.1 | coordinate system | `eed:0008#001` | `term.coordinate-system` | N/A（メタ概念） | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl, ShopfloorIT | 標準（数学・ROS REP-103） | 生産 ◯ / CAD ◯ |
| 3.2 | reference coordinate frame | `eed:0009#001` | `term.reference-frame` | Product | Type | ProductDesign | MfgRobotics, StationControl, ShopfloorIT | 標準（ROS REP-103、ISO 10303-242） | 生産 ◯ / CAD ◯ |
| 3.3 | handedness | `eed:0010#001` | `term.handedness` | Product | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl | 標準（数学・CG） | 生産 ◯ / CAD ◯ |
| 3.4 | unit scale convention | `eed:0011#001` | `term.scale-factor` | Product | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl | 業界一般 | 生産 ◯ / CAD ◯ |
| 3.5 | pose | `eed:0012#001` | `term.pose` | Product | Type & Instance | ProductDesign, MfgRobotics | StationControl, ShopfloorIT | 標準（ISO 9787、OPC UA for Robotics） | 生産 ◯ / CAD ◯ |
| 3.6 | rotation representation convention | `eed:0013#001` | `term.rotation-convention` | Product | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl | 標準（ROS REP-103） | 生産 ◯ / CAD ◯ |
| 3.7 | local space | `eed:0014#001` | `term.local-space` | Product | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl | 業界一般 | 生産 ◯ / CAD ◯ |
| 3.8 | world space | `eed:0015#001` | `term.world-space` | Product | Type | MetaArchitecture | ProductDesign, MfgRobotics, StationControl | 業界一般 | 生産 ◯ / CAD ◯ |
| 3.9 | hierarchical coordinate structure | `eed:0016#001` | `term.coordinate-hierarchy` | Product | Type & Instance | ProductDesign, MfgRobotics | StationControl, ShopfloorIT | 業界一般（シーングラフ、ROSのTFツリー） | 生産 ◯ / CAD ◯ |
| 3.10 | distance metric convention | `eed:0017#001` | `term.distance-metric` | N/A（メタ概念） | Type | MetaArchitecture | MfgRobotics, StationControl, ProductDesign | 標準（数学の距離空間） | 生産 ◯ / CAD ◯ |
| 3.11 | homogeneous transformation matrix | `eed:0018#001` | `term.homogeneous-transform` | Product | Type | ProductDesign, MfgRobotics | StationControl, ShopfloorIT | 標準（線形代数・ロボティクス） | 生産 ◯ / CAD ◯ |
| 3.12 | coordinate transformation | `eed:0019#001` | `term.coordinate-transformation` | Product | Type & Instance | ProductDesign, MfgRobotics | StationControl, ShopfloorIT | 標準（線形代数・ロボティクス） | 生産 ◯ / CAD ◯ |
| 3.13 | datum reference feature | `eed:0020#001` | `term.datum-feature` | Field Device | Type | ProductDesign | MfgRobotics, StationControl | 標準（ISO 5459、ISO 10303-242） | 生産 ◯ / CAD ◯ |
| 3.14 | calibration reference | `eed:0021#001` | `term.calibration-reference` | Control Device | Type | StationControl | MfgRobotics, ProductDesign | 業界一般 | 生産 ◯ / CAD ◯ |
| 3.15 | exclusion zone | `eed:0022#001` | `term.exclusion-zone` | Field Device | Type | ProductDesign, MfgRobotics | StationControl | 独自 | 生産 ◯ / CAD — |
| 3.16 | approach vector | `eed:0023#001` | `term.approach-vector` | Field Device | Type | MfgRobotics | StationControl | 業界一般 | 生産 ◯ / CAD ◯ |

NOTE 本編で Hierarchy Level が `N/A` なのは `eed:0008`（3.1 座標系、原辞書表記 `N/A（メタ概念）`）と `eed:0017`（3.10 距離定義規約、原辞書表記 `N/A`）の**2件**である。いずれも数学的な取り決めであり設備階層に依存しない。原辞書4.3節 軸1×軸2 クロス表の Integration 行はこのセルを1件としており、行計も16ではなく15になっている（`decisions.md` D-2026-08-22-15）。

## 附属書C (informative) 関係型セマンティクス (Relational Semantics)

### C.1 概念間関係型

第1編で導入した4型に加え、本編で `transforms` 型を確定使用した。

| 関係型 | 意味 | ISO 704 分類 | 本編での使用 |
|---|---|---|---|
| is-a | 上位概念・下位概念関係（Taxonomic Specialization） | 類種関係 (generic) | 3.2 → 3.1（1件） |
| part-of | 全体・部分構成関係（Aggregation / Composition） | 部分関係 (partitive) | 未確定使用（3.2/3.9 は候補にとどめる） |
| refers-to | 参照・パラメータ関連付け（Semantic Reference） | 連想関係 (associative) | 大多数の関係 |
| constrained-by | 幾何条件・境界拘束（Constraint Enforcement） | 連想関係 (associative) | 未確定使用（3.2/3.13 は候補にとどめる） |
| **transforms** | ある空間・座標系上の値を、別の空間・座標系上の値へ変換する操作関係（本編で新規確定） | 連想関係 (associative) | 3.12 → 3.7, 3.8（1組） |
| calibrated-from | 未知の変換が、既知幾何を持つ基準物によって解かれた、という由来関係（提案・未確定） | 連想関係 (associative) | 候補：3.2↔3.14、3.11↔3.14 |
| aligns-with | 異なる位置合わせ手段が、同じ2座標系間の対応づけを目的として連鎖的に使われる関係（提案・未確定） | 連想関係 (associative) | 候補：3.13↔3.14 |
| ~~mates-to~~ | 嵌合・作業一致を表す関係（第1編で予告） | 連想関係 (associative) | 本編でも未出現。第3〜5編・第M編でも出現せず、**廃止**（第M編附属書C.1 NOTE 3） |

NOTE 1 `calibrated-from`・`aligns-with` を候補にとどめた理由：どちらも実務上の連携（キャリブレーションのワークフロー、位置合わせ手段の使い分け）としては明確だが、概念定義そのものが相手概念を前提とする関係（is-aやtransformsのように定義文が直接その関係を述べている）ではなく、**エントリの用法上の注意・具体例が間接的に示す運用上の関係**にとどまる。ISO 704の連想関係は本来幅広い実務上の関連付けを許容するため、全編化時のレビューで正式採用してよい候補である（`decisions.md` D-2026-08-21-03）。

NOTE 2 `transforms` の方向は「操作 → 操作対象（変換前・変換後）」で統一する。3.12 の場合、変換前（3.7）・変換後（3.8）の両方を transforms の対象として記載した。

### C.2 OWL / RDF ナレッジグラフ記述例 (Turtle形式)

```turtle
@prefix eed:   <http://example.org/eed/vocab/> .
@prefix rami:  <http://www.plattform-i40.de/rami/ontology#> .
@prefix owl:   <http://www.w3.org/2002/07/owl#> .
@prefix rdfs:  <http://www.w3.org/2000/01/rdf-schema#> .
@prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

eed:ReferenceCoordinateFrame a owl:Class ;
    rdfs:label "reference coordinate frame"@en , "参照座標系"@ja ;
    eed:irdi "eed:0009#001"^^xsd:string ;
    rdfs:subClassOf eed:CoordinateSystem ;   # is-a
    rami:layer rami:IntegrationLayer ;
    rami:hierarchyLevel rami:ProductLevel ;
    rami:lifeCycleStage rami:TypeStage .

eed:CoordinateTransformation a owl:Class ;
    rdfs:label "coordinate transformation"@en , "座標変換"@ja ;
    eed:irdi "eed:0019#001"^^xsd:string ;
    eed:transforms eed:LocalSpace , eed:WorldSpace ;  # transforms（本編で新規確定）
    rami:layer rami:IntegrationLayer .

eed:LocalSpace a owl:Class ;
    rdfs:label "local space"@en , "ローカル空間"@ja ;
    eed:irdi "eed:0014#001"^^xsd:string ;
    eed:contrastsWith eed:WorldSpace ;   # 対比ペア（2.4節）。正式な関係型ではなく注記レベルの対応
    rami:layer rami:IntegrationLayer .
```

---

## 附属書D (informative) 登場人物対応表 — 本編の概念で語られる実在物

原辞書1.2節の趣旨を保全する附属書です。以下は本編（Integration層）の16概念に接続する登場人物の抜粋です。

| 登場人物 | 一言でいうと | 本編ではどう語られるか |
|---|---|---|
| 産業用ロボット（多関節マニピュレータ） | 掴んで運ぶ・組み付ける腕 | ベースからTCPまでの関節連鎖は3.9、その計算は3.11・3.12、手先の位置と向きは3.5、向きの形式は3.6 |
| 架台・ベースプレート・床 | 設備が据え付けられる土台 | そもそもの物差しの枠組みは3.1、シーン全体基準の3.8、そこからの親子関係は3.9、ランドマーク（3.14）の設置場所 |
| 治具（ジグ）・位置決めピン・突き当て面 | ワークを毎回同じ位置・姿勢に固定する道具 | 基準となる穴や面そのものは3.13、そこから立つ座標系は3.2、校正治具としては3.14 |
| ビジョンカメラ・3Dスキャナ | ワークがどこにどの向きであるかを見つける目 | 出力そのものは3.5、カメラとロボットの座標系を対応づけるのは3.14 |
| 無人搬送車（AGV／AMR） | 床を走ってワークを別の場所へ運ぶ | 走行して基準が動くため3.7と3.8の区別が要になる |
| 工作機械・専用機（CNC、プレス、溶接機など） | ワークの形そのものを変える設備 | 軸ごとに順に動かす移動量の見積もりは3.10（マンハッタン距離） |
| エンドエフェクタ（ハンド・グリッパ・吸着パッド） | ロボットの手先。実際にワークに触れる部分 | 最後に近づく向きは3.16、触れてはいけない場所は3.15 |
| 安全柵・ライトカーテン | 人と機械を隔てる境界 | 立ち入ってはいけない空間として3.15 |
| CADシステム・PLM | 設計データの出どころ | 他システムへ渡す際の軸の向きと単位の食い違いは3.3・3.4 |

## 附属書E (informative) 変換対応表 (Conversion Mapping)

### E.1 採番対応

| 本仕様書 | 原辞書採番 | 恒久ID (IRDI) | English Name |
|---|---|---|---|
| 3.1 | 2.01 | `eed:0008#001` | coordinate system |
| 3.2 | 2.02 | `eed:0009#001` | reference coordinate frame |
| 3.3 | 2.03 | `eed:0010#001` | handedness |
| 3.4 | 2.04 | `eed:0011#001` | unit scale convention |
| 3.5 | 2.05 | `eed:0012#001` | pose |
| 3.6 | 2.06 | `eed:0013#001` | rotation representation convention |
| 3.7 | 2.07 | `eed:0014#001` | local space |
| 3.8 | 2.08 | `eed:0015#001` | world space |
| 3.9 | 2.09 | `eed:0016#001` | hierarchical coordinate structure |
| 3.10 | 2.10 | `eed:0017#001` | distance metric convention |
| 3.11 | 2.11 | `eed:0018#001` | homogeneous transformation matrix |
| 3.12 | 2.12 | `eed:0019#001` | coordinate transformation |
| 3.13 | 2.13 | `eed:0020#001` | datum reference feature |
| 3.14 | 2.14 | `eed:0021#001` | calibration reference |
| 3.15 | 2.15 | `eed:0022#001` | exclusion zone |
| 3.16 | 2.16 | `eed:0023#001` | approach vector |

NOTE 第1編と異なり、本編には概念分離・新設は発生していない。原辞書の採番（`2.01`〜`2.16`）と本仕様書の採番（`3.1`〜`3.16`）は欠番なく1対1で対応する。

NOTE（2026-09-02追補） 本編の Note 2（Concept relations）が編をまたいで参照する箇所は、**参照先の編の採番と編番号を必ず含む**（例：`3.3 (work interface, 第4編)`。原採番を併記している箇所もある — 例：`1.04 (stable pose, 第1編 3.4)`）。第4編のみ原辞書の採番と本仕様書の採番が一致しないため（原 `4.02` → 第4編 `3.3` 等）、原採番との対応は第4編附属書E.1 を参照すること。他の編は原採番と1対1で対応する（第1編は `1.0N` → `3.N`）。

### E.2 欄の写像規則

第1編附属書E.2と同一の規則を適用した。変更なし。

### E.3 原辞書の章とISO構成の対応（本編での実現状況）

| 原辞書 | 第1編附属書E.3の計画 | 本編（第2編）での実現 |
|---|---|---|
| 3章 基礎規約 | 第2編（Integration層）の Clause 4 として規定 | Clause 4 として実現。第1編ではこの内容に相当するClauseがなかったため、本編で初めて登場する |
| 4章 分類軸・MECE検証・空セル一覧 | 附属書F (informative)（全編化時。集計元は附属書B） | 未実施（全編化時に対応） |
| 5章 用語及び定義 | 各編の Clause 3 | Clause 3（3.1〜3.16）として実現 |

NOTE Clause 4 を基礎規約に割り当てたことに伴い、第1編で Clause 4 だった「概念体系」は本編では **Clause 5** に繰り下がる。この繰り下げは編ごとの構成差であり、恒久IDやエントリ内容には影響しない。
