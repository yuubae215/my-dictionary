# dogfooding 記録：データ交換・座標規約（2026-10-04）

- 対象文書：ROS Enhancement Proposal 105「Coordinate Frames for Mobile Platforms」（Wim Meeussen）。作成 2010-10-27、最終変更 2024-03-15（`ros-infrastructure/rep` の `rep-0105.rst`、コミット `d44bebad5c9f8c52d0f0ad100d03566f97f081d1`）。パブリックドメイン
- 文書の種類：手順書 §3 の優先4（下流のソフトウェアへのデータ交換規約）に近い。移動ロボットの base_link／odom／map／earth の4フレームの意味と親子関係、地図の向きと原点の取り方を定める
- 辞書の版：コミット `4aa70a2`（`pilot/` は `9ad96b8` から変更なし）
- 実施者：Claude（書き手）、リポジトリの持ち主（書き手以外）

## 対象文書の選定

日本語の公開文書は、環境のネットワーク制限で取得できなかった。
持ち主の了承を得て、GitHub から取得できる英語の公開文書から選んだ。

最初は REP 103（単位と座標系の規約）を選んだが、抽出の後で取り下げた。
REP 103 は辞書自身の典拠であり、原辞書で12回、第2編で12回引用され、第2編 Clause 4 の座標系規約は REP 103 をそのまま写している。
辞書の方がこの文書に合わせて書かれているため、判定は一致に偏り、仮説 H1〜H4 の反証にならない。
手順書 §3 条件1 が書き下ろしの文書を除くのと同じ理由である。
REP 105 は原辞書、`pilot/`、`decisions.md` のどこにも引用がないことを確かめてから選んだ（`grep` で `REP-105`、`REP 105`、`odom`、`base_link` が0件）。
REP 105 自身は REP 103 に準拠すると宣言している（261行目）が、本文が定めるのは REP 103 にないフレームの意味と親子関係である。

## 手順書からの逸脱

| 項目 | 手順書 | 本記録 | 理由 |
| :--- | :--- | :--- | :--- |
| 文書の言語 | 規定なし（日本語の社内文書を想定） | 英語 | 上記のとおり |
| 対訳 | なし | 空間語ごとに語の対訳を付け、両実施者の共有の入力とする | 附属書A は日本語の現場語で引くため。対訳は語の置き換えにとどめ、主語や参照枠の判断を含めない。対訳の誤りは判定とは別に記録する |
| 原文の扱い | 原文をリポジトリに置かない | 抜粋を1文単位で載せる | パブリックドメインであり、社内文書の秘匿の理由が当たらない |
| 条件1（実務で使われた文書） | 実務で使われた文書 | ROS のソフトウェア群が準拠する規約文書 | 工場の現場文書ではない。現場語（附属書A）に当たりにくいことは結果の読み方に含める |
| 出現の数え方 | 1出現を1行 | 1文の中の同じ語は1行にまとめる。フレーム名（`base_link`、`odom`、`map`、`earth`）は定義節の初出だけを1行とする | フレーム名は本文中に計80回以上現れ、どれも定義節で意味が固定された識別子である。以降の出現で（語, 主語）が変わる余地がないため、行を増やしても判定の分布は変わらない |

## 抽出（§4.2、共有）

抽出は Claude が行い、持ち主の確認を経て両者共通の入力とする。
空間語として、方向、位置、姿勢、座標系、原点、基準、高さ、移動、フレームの親子関係に関わる語を拾った。
Mermaid の図（150〜157行目、185〜194行目）、図の代替テキスト、参考文献は、本文と同じ語を繰り返すだけなので拾っていない。
`extract.py` は日本語の検索語で照合するため、本文書には使っていない。全件を目視で抽出した。

| # | 箇所 | 語（原文） | 対訳（共有） | 抜粋 |
| ---: | :--- | :--- | :--- | :--- |
| 1 | 2行目 | Coordinate Frames | 座標フレーム | Title: Coordinate Frames for Mobile Platforms |
| 2 | 15行目 | coordinate frames | 座標フレーム | naming conventions and semantic meaning for coordinate frames of mobile platforms |
| 3 | 22行目 | coordinate frames | 座標フレーム | need a shared convention for coordinate frames |
| 4 | 28行目 | localization | 自己位置推定 | the frames necessary for writing a new localization component |
| 5 | 29行目 | mobile base | 移動台車（モバイルベース） | frames that can be used to refer to the mobile base of a robot |
| 6 | 42行目 | base_link | base_link（台車フレーム） | The coordinate frame called base_link is rigidly attached to the mobile robot base. |
| 7 | 42行目 | rigidly attached | 剛に固定 | is rigidly attached to the mobile robot base |
| 8 | 44行目 | position or orientation | 位置または向き | can be attached to the base in any arbitrary position or orientation |
| 9 | 46行目 | point of reference | 基準点 | a different place on the base that provides an obvious point of reference |
| 10 | 47行目 | preferred orientation | 推奨される向き | REP 103 specifies a preferred orientation for frames |
| 11 | 52行目 | odom | odom（オドメトリフレーム） | The coordinate frame called odom is a world-fixed frame. |
| 12 | 52行目 | world-fixed frame | ワールド固定フレーム | odom is a world-fixed frame |
| 13 | 52行目 | pose | 位置姿勢 | The pose of a mobile platform in the odom frame can drift over time |
| 14 | 53行目 | drift | ドリフト | can drift over time, without any bounds |
| 15 | 55行目 | global reference | 大域的な基準 | useless as a long-term global reference |
| 16 | 56行目 | continuous | 連続 | the pose of a robot in the odom frame is guaranteed to be continuous |
| 17 | 58行目 | discrete jumps | 不連続な跳び | evolves in a smooth way, without discrete jumps |
| 18 | 60行目 | odometry | オドメトリ | the odom frame is computed based on an odometry source, such as wheel odometry, visual odometry |
| 19 | 64行目 | local reference | 局所的な基準 | useful as an accurate, short-term local reference |
| 20 | 70行目 | map | map（地図フレーム） | The coordinate frame called map is a world fixed frame |
| 21 | 70行目 | world fixed frame | ワールド固定フレーム | map is a world fixed frame |
| 22 | 71行目 | Z-axis pointing upwards | Z軸が上向き | with its Z-axis pointing upwards |
| 23 | 71行目 | relative to the map frame | map フレームに対する | The pose of a mobile platform, relative to the map frame, should not significantly drift |
| 24 | 77行目 | robot pose | ロボットの位置姿勢 | re-computes the robot pose in the map frame based on sensor observations |
| 25 | 81行目 | long-term global reference | 長期的な大域基準 | The map frame is useful as a long-term global reference |
| 26 | 82行目 | reference frame | 参照フレーム | a poor reference frame for local sensing and acting |
| 27 | 87行目 | referenced globally | 大域的に参照 | Map coordinate frames can either be referenced globally or to an application specific position. |
| 28 | 87行目 | application specific position | 用途固有の位置 | or to an application specific position |
| 29 | 88行目 | Mean Sea Level | 平均海面 | Mean Sea Level according to EGM1996 |
| 30 | 88行目 | z position | z位置 | the z position in the map frame is equivalent to meters above sea level |
| 31 | 88行目 | meters above sea level | 海抜（メートル） | equivalent to meters above sea level |
| 32 | 89行目 | reference position | 基準位置 | the choice of reference position is clearly documented |
| 33 | 91行目 | earth | 地球 | with respect to a global reference like the earth |
| 34 | 92行目 | x-axis east | x軸 東 | align the x-axis east, y-axis north, and the z-axis up |
| 35 | 92行目 | y-axis north | y軸 北 | align the x-axis east, y-axis north, and the z-axis up |
| 36 | 92行目 | z-axis up | z軸 上 | align the x-axis east, y-axis north, and the z-axis up |
| 37 | 92行目 | origin | 原点 | at the origin of the coordinate frame |
| 38 | 93行目 | height | 高さ | zero at the height of the WGS84 ellipsoid |
| 39 | 97行目 | compass | コンパス（方位計） | an external reference device such as a GPS, compass, nor altimeter |
| 40 | 98行目 | current location | 現在位置 | initialize the map at its current location |
| 41 | 98行目 | z axis upward | z軸 上向き | with the z axis upward |
| 42 | 100行目 | compass heading | 方位（ヘディング） | If the robot has a compass heading as startup |
| 43 | 100行目 | x east, y north | x 東、y 北 | it can then also initialize x east, y north |
| 44 | 102行目 | height at MSL | 平均海面での高さ | initialize the height at MSL |
| 45 | 104行目 | unstructured environments | 非構造化環境 | strongly recommended for unstructured environments |
| 46 | 108行目 | aligning the map with the environment | 地図を環境に合わせる | In structured environments aligning the map with the environment may be more useful. |
| 47 | 109行目 | rectilinear | 直交（直線的） | an office building interior, which is commonly rectilinear |
| 48 | 109行目 | aligning the map with the building | 地図を建物に合わせる | aligning the map with the building is recommended |
| 49 | 109行目 | building layout | 建物のレイアウト | especially if the building layout is known apriori |
| 50 | 110行目 | floor level | 床面の高さ | align the map at floor level |
| 51 | 111行目 | multiple floors | 複数の階 | operating on multiple floors ... multiple coordinate frames, one for each floor |
| 52 | 119行目 | earth | earth（地球フレーム） | The coordinate frame called earth is the origin of ECEF. |
| 53 | 119行目 | origin of ECEF | ECEF の原点 | is the origin of ECEF |
| 54 | 121行目 | map frames | 地図フレーム | the interaction of multiple robots in different map frames |
| 55 | 123行目 | customized for each robot | ロボットごとに個別化 | map and odom and base_link frames will need to be customized for each robot |
| 56 | 124行目 | frame_ids | フレームID | the transform frame_ids can remain standard on each robot if the other robots' frame_ids are rewritten |
| 57 | 126行目 | globally referenced | 大域的に参照 | If the map frame is globally referenced |
| 58 | 126行目 | static transform | 静的な変換 | can be a static transform publisher |
| 59 | 127行目 | global position | 大域位置 | the estimate of the current global position |
| 60 | 127行目 | estimated pose of the origin of the map | 地図原点の推定位置姿勢 | to get the estimated pose of the origin of the map |
| 61 | 129行目 | absolute position | 絶対位置 | the map frame's absolute positon is unknown |
| 62 | 136行目 | tangential map frame | 接平面の map フレーム | Earth Centered Earth Fixed with a tangential map frame |
| 63 | 143行目 | tree representation | 木構造による表現 | We have chosen a tree representation to attach all coordinate frames |
| 64 | 145行目 | parent coordinate frame | 親座標フレーム | each coordinate frame has one parent coordinate frame |
| 65 | 145行目 | child coordinate frames | 子座標フレーム | and any number of child coordinate frames |
| 66 | 160行目 | parent | 親 | The map frame is the parent of odom, and odom is the parent of base_link. |
| 67 | 162行目 | attached to | 〜に取り付け（親にする） | both map and odom should be attached to base_link |
| 68 | 167行目 | graph | グラフ | the minimal representation of this graph |
| 69 | 168行目 | topology | トポロジー | The basic topology should stay the same |
| 70 | 172行目 | pressure altitude | 気圧高度 | a frame to represent pressure altitude for flying vehicles |
| 71 | 175行目 | drift vertically | 垂直方向にドリフト | It may drift in time like odometry but will only drift vertically. |
| 72 | 176行目 | inserted between | 間に挿入 | a pressure_altitude frame could be inserted between the inertially consistent odom frame and the map frame |
| 73 | 176行目 | inertially consistent | 慣性的に一貫 | the inertially consistent odom frame |
| 74 | 177行目 | offset | オフセット | estimate the offset of the pressure_altitude from the map |
| 75 | 196行目 | tf tree | tf ツリー | an example of a tf tree with two robots using different maps |
| 76 | 196行目 | common frame | 共通フレーム | having a common frame earth |
| 77 | 199行目 | canonical frame ids | 正準フレームID | use the canonical frame ids on each robot |
| 78 | 200行目 | remapped | 付け替え | the frame ids should be remapped to disambiguate which robot |
| 79 | 207行目 | transform | 変換 | The transform from odom to base_link is computed and broadcast by one of the odometry sources. |
| 80 | 210行目 | localization component | 自己位置推定コンポーネント | The transform from map to base_link is computed by a localization component. |
| 81 | 214行目 | broadcast the transform | 変換を配信 | uses this information to broadcast the transform from map to odom |
| 82 | 216行目 | statically published | 静的に配信 | The transform from earth to map is statically published |
| 83 | 218行目 | initial position | 初期位置 | use the initial position of the vehicle as the origin of the map frame |
| 84 | 219行目 | origin of the map frame | map フレームの原点 | as the origin of the map frame |
| 85 | 220行目 | georeferenced | 地理参照された | If the map is not georeferenced |
| 86 | 220行目 | estimated offset | 推定オフセット | publishing the estimated offset from the map to the odom frame |
| 87 | 225行目 | transition between maps | 地図間の移行 | it will need to transition between maps |
| 88 | 226行目 | euclidian approximation | ユークリッド近似 | map coordinate frame is a euclidian approximation of a vicinity |
| 89 | 226行目 | curvature of the earth | 地球の曲率 | breaks down at longer distances due to the curvature of the earth |
| 90 | 227行目 | new floor | 別の階 | the robot is on a new floor of a building |
| 91 | 229行目 | reparent | 親の付け替え | reparent the odom frame appropriately when moving between maps |
| 92 | 230行目 | localization fix | 測位結果 | subtracting the odom to base_link from the localization fix map to base_link |
| 93 | 234行目 | odometric frame | オドメトリフレーム | the odometric frame should not be affected |
| 94 | 235行目 | distant data | 遠方のデータ | old or distant data is discarded |
| 95 | 235行目 | integrated position error | 積算位置誤差 | before the integrated position error accumulates |
| 96 | 236行目 | rate of drift | ドリフト率 | a much lower rate of drift |
| 97 | 236行目 | high resolution encoders | 高分解能エンコーダ | multiple redundant high resolution encoders |
| 98 | 238行目 | moved by external motivators | 外力で動かされる | the robot being moved by external motivators |
| 99 | 239行目 | elevator | エレベータ | a robot in an elevator, where the environment outside has changed |
| 100 | 240行目 | inertial frame | 慣性フレーム | observations are in the same inertial frame as the robot |
| 101 | 242行目 | inertial odom frame | 慣性的な odom フレーム | the inertial odom frame should always remain continuous |
| 102 | 244行目 | origin | 原点 | the distance from the odom frame's origin to the vehicle |
| 103 | 244行目 | maximum floating point precision | 浮動小数点の最大精度 | approaches the maximum floating point precision |
| 104 | 246行目 | reset of the odom frame origin | odom フレーム原点のリセット | a systematic reset of the odom frame origin may be required |
| 105 | 247行目 | centimeter level accuracy | センチメートル精度 | If centimeter level accuracy is required the maximum distance ... is approximately 83km |
| 106 | 249行目 | obstacle data | 障害物データ | additional coordinate frames in which to persist obstacle data |

## 判定（§4.3〜§4.5）

各実施者が独立に付ける。両者が確定させるまで、ここには載せない（`review/dogfooding/README.md`）。

入力は Artifact の判定シート（持ち主のみ閲覧可）で行う。持ち主の判定はシートの共有データベースに保存され、Claude はそこから読む。

Claude の判定は 2026-10-04 に確定し、持ち主の判定より前に封をした。
判定ファイル（JSON、キーを整列し区切りの空白を除いた UTF-8）の SHA-256 は次のとおりである。
持ち主の確定後に同じファイルを公開し、このハッシュと一致することで、持ち主の判定を見てから書き換えていないことを示す。

```
be47311ec1853446378a08e5b9bedbfad65bb35acd3fe953064c824ebb7df050
```

## 3段判定（M6）

| 語 | 第1段 | 第2段 | 第3段 | 結論 | 起票ID |
| :--- | :--- | :--- | :--- | :--- | :--- |

## 集計

（両者の判定の確定後に §7 の表を書く）
