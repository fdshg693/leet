# CLAUDE.md

LeetCode の学習用プロジェクト。問題文を Markdown で保存し、解答を書いていく。

**解答言語は Python に固定。** 講評・解説・ノートのコード例もすべて Python で書く（他言語との比較は求められたときだけ）。

## 構成

- `leet2md.py` — LeetCode の問題 URL（またはスラッグ）から問題文を取得し、学習用フォルダを作るスクリプト
- `problems/{4桁の問題番号}-{スラッグ}/` — 問題ごとのフォルダ（例: `problems/0001-two-sum/`）
  - `problem.md` — 問題文。末尾に「AI 講評」欄（問題の着眼点・典型パターン・関連問題）
  - `approach.md` — 解答方針の検討メモ。方針を複数並べられる。末尾に「AI 講評」欄
  - `solution-{名前}.{拡張子}` — 最終コード。解き方ごとに 1 ファイル（例: `solution-1.py`, `solution-hashmap.py`）。末尾のコメントブロックが「AI 講評」欄
- `notes/` — 問題をまたいで使う共通ノート。索引は `notes/README.md`
  - `python/` — Python の書き方・標準ライブラリ（例: ソート、`collections`、`heapq`）
  - `patterns/` — 典型パターン「こういう問題はこう解く」（例: ハッシュマップで相方を探す）
  - `algorithms/` — アルゴリズム・データ構造の仕組み（例: 二分探索、BFS/DFS）

## leet2md.py

```sh
uv run leet2md.py https://leetcode.com/problems/two-sum/            # 標準出力
uv run leet2md.py two-sum -o problems                               # 学習用フォルダを作成（既定 python3）
uv run leet2md.py two-sum -o problems --lang cpp                    # 解答ファイルの言語を指定
uv run leet2md.py two-sum -o problems --solution hashmap            # 解答ファイルを追加
```

- 依存は PEP 723 のインラインメタデータ（スクリプト先頭）で管理しているので、`uv run` で実行する。依存を追加するときもそこに書く
- 問題文は非公式の GraphQL API（`https://leetcode.com/graphql`）の `question(titleSlug)` で取得し、`markdownify` で HTML から Markdown に変換している
- `markdownify` に渡す前に `<sup>` / `<sub>` を `^` / `_` に置き換えている（そのままだと `10^4` が `104` になるため）
- 有料会員限定の問題は `content` が null で返ってくる
- `-o` 指定時、既存ファイルは上書きしない（ユーザーの解答・メモを守るため）

## AI 講評の書き方

ユーザーから講評を頼まれたら、対象ファイル末尾の「AI 講評」欄に追記する。

- 既存の講評は消さず、日付見出しで追記していく（Markdown は `### YYYY-MM-DD`、コードは `--- YYYY-MM-DD ---` のコメント行）
- ユーザーが書いた本文・コードは書き換えない。改善案は講評欄に書く
- 講評の観点:
  - `problem.md`: 問題の着眼点、典型パターン、関連問題
  - `approach.md`: 方針の妥当性、計算量の見積もりの正誤、見落としているエッジケース、別解のヒント
  - `solution-*`: 正しさ（反例があれば具体的に）、計算量、可読性・言語らしい書き方
- 答えをいきなり教えず、まずはヒントの形で書く（ユーザーが求めた場合は除く）
- 講評で触れたパターンやアルゴリズムに `notes/` のノートがあればリンクする（例: `[二分探索](../../notes/algorithms/binary-search.md)`）

## notes/ の書き方

「ソートってどうやるんだっけ」「この手の問題はどう解く」「〇〇法の仕組み」のような、特定の問題に依存しない知識はここに書く。

- 1 ファイル 1 トピック。ファイル名は英語の kebab-case（例: `two-pointers.md`）。置き場所は上の 3 分類から選ぶ
- 同じトピックのノートが既にあれば新しく作らず追記する。ノートを追加したら `notes/README.md` の一覧に 1 行足す
- 末尾に「関連問題」欄を置き、`problems/` のフォルダへ相対リンクする。問題を解いて関連が見つかったら追記していく
- ユーザーの質問に答えた内容を残す価値がありそうなら、ノートにするか提案する

## 環境

- Windows。シェルは Git Bash か PowerShell
- Python の実行と依存管理には uv を使う（pip や venv を直接使わない）
