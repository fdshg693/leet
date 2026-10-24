# 二分探索

## 仕組み

**ソート済み**（より一般には「ある位置を境に条件が False → True に切り替わる」）な範囲で、
真ん中を調べて探索範囲を半分ずつ捨てていく。長さ n なら O(log n) 回で終わる。

## 書き方（半開区間 `[lo, hi)` で「条件を満たす最初の位置」を探す）

```python
def first_true(lo, hi, ok):
    """ok(i) が False...False True...True と並ぶとき、最初の True の位置を返す。なければ hi。"""
    while lo < hi:
        mid = (lo + hi) // 2
        if ok(mid):
            hi = mid       # mid は答えの候補。右側を捨てる
        else:
            lo = mid + 1   # mid は答えではない。mid 以下を捨てる
    return lo
```

- 境界のバグを防ぐコツは「区間の意味（閉区間か半開区間か）を最初に決めて守る」こと
- ループ終了時 `lo == hi` が答え

## 標準ライブラリ `bisect`

```python
from bisect import bisect_left, bisect_right

a = [1, 2, 2, 2, 5]
bisect_left(a, 2)   # 1  … 2 以上が初めて現れる位置
bisect_right(a, 2)  # 4  … 2 より大きいものが初めて現れる位置
```

## 応用: 答えで二分探索

「答えが x 以下にできるか？」が x について単調なら、答えそのものを二分探索できる。

## 関連問題

- [0004 Median of Two Sorted Arrays](../../problems/0004-median-of-two-sorted-arrays/) — 分割位置を二分探索する
