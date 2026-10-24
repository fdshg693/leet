# 共通ノート

問題をまたいで使う知識をまとめる場所。解答言語は Python。

## 分類

| フォルダ | 中身 | 例 |
| --- | --- | --- |
| [python/](python/) | Python の書き方・標準ライブラリ | ソート、`collections`、`heapq` |
| [patterns/](patterns/) | 「こういう問題はこう解く」という典型パターン | ハッシュマップで補数を探す、二分探索で答えを決め打つ |
| [algorithms/](algorithms/) | アルゴリズム・データ構造の仕組み | 二分探索、BFS/DFS、Union-Find |

## 一覧

<!-- ノートを追加したらここに 1 行足す -->

### python/

- [sort.md](python/sort.md) — 配列のソート（`sort` / `sorted` / `key` / 安定ソート）

### patterns/

- [hashmap-lookup.md](patterns/hashmap-lookup.md) — 「見たものを覚えておく」ハッシュマップ
- [two-pointers.md](patterns/two-pointers.md) — 二ポインタ（尺取り法）: ソート済み配列の両端から寄せる

### algorithms/

- [binary-search.md](algorithms/binary-search.md) — 二分探索の仕組みと境界の書き方

## ノートの書き方

- 1 ファイル 1 トピック。ファイル名は英語の kebab-case（例: `two-pointers.md`）
- 末尾に「関連問題」を置き、`problems/` のフォルダへリンクする
