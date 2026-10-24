# Leet Code 学習プロジェクト

https://leetcode.com

## 学習の流れ

1. 問題を取得してフォルダを作る

   ```sh
   uv run leet2md.py https://leetcode.com/problems/two-sum/ -o problems
   ```

2. `problem.md` で問題を読む
3. `approach.md` に方針（アイデア・計算量）を書く
4. `solution-1.py` にコードを書く。別の解き方を試すときは解答ファイルを追加する

   ```sh
   uv run leet2md.py two-sum -o problems --solution hashmap
   ```

5. AI に講評を頼む。各ファイル末尾の「AI 講評」欄に追記してもらう
6. 問題をまたいで使える知識（Python の書き方・解き方のパターン・アルゴリズムの仕組み）は [notes/](notes/) にまとめる

## フォルダ構成

```
problems/
└── 0001-two-sum/
    ├── problem.md          問題文 + AI 講評
    ├── approach.md         解答方針の検討 + AI 講評
    ├── solution-1.py       解法 1 のコード + AI 講評
    └── solution-hashmap.py 解法 2 のコード + AI 講評
notes/                      共通ノート（索引は notes/README.md）
├── python/                 Python の書き方・標準ライブラリ
├── patterns/               典型パターン
└── algorithms/             アルゴリズム・データ構造の仕組み
```
