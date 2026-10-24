# 配列のソート

## 基本

```python
nums = [3, 1, 2]

nums.sort()              # その場で並べ替え（戻り値は None）
new = sorted(nums)       # 新しいリストを返す（元は変わらない）。タプルや文字列にも使える

nums.sort(reverse=True)  # 降順
```

- `nums = nums.sort()` は `None` になるので注意
- 計算量は O(n log n)（Timsort）。すでにほぼ整列済みなら速い

## key で並べ替えの基準を指定する

```python
words = ["banana", "Apple", "cherry"]
sorted(words, key=len)              # 長さ順
sorted(words, key=str.lower)        # 大文字小文字を無視

pairs = [(1, "b"), (0, "c"), (1, "a")]
sorted(pairs, key=lambda p: p[1])   # 2 番目の要素で
sorted(pairs, key=lambda p: (-p[0], p[1]))  # 1 番目は降順、同点なら 2 番目は昇順
```

- タプルは先頭から順に比較されるので、複数キーはタプルで返すのが定番
- 数値キーを降順にしたいときは `-` を付ける

## 安定ソート

Python のソートは**安定**（キーが同じ要素は元の順序を保つ）。
「B で並べ、同点なら A の順」は、A で並べてから B で並べても実現できる。

## 元のインデックスを保ったままソートする

```python
nums = [30, 10, 20]
order = sorted(range(len(nums)), key=lambda i: nums[i])  # [1, 2, 0]
# あるいは
pairs = sorted((v, i) for i, v in enumerate(nums))       # [(10, 1), (20, 2), (30, 0)]
```

## 関連問題

- [0001 Two Sum](../../problems/0001-two-sum/) — ソート + 二ポインタで解く場合はインデックスを保持する必要がある
