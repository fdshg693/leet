# 1. Two Sum — 解法: 1
# 方針:
# 計算量: 時間 O(?) / 空間 O(?)

class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        
        # 配列の長さ
        n = len(nums)
        
        # nums を昇順でソート（インデックスを復元できるようにタプルで一緒に記録）
        pairs = sorted((v, i) for i, v in enumerate(nums))
        
        # 2 ポインタを用意
        # 左右の端から動かす
        l = 0
        r = n-1
        while l < r:
            left_num , left_original_index = pairs[l]
            right_num , right_original_index   = pairs[r]            
            
            # 目的の解
            if left_num + right_num == target:
                return [left_original_index, right_original_index]
            # 合計がまだ小さいので左側を大きくする
            elif left_num + right_num < target:
                l+=1
                continue
            # 合計がまだ大きいので右側を小さくする
            elif left_num + right_num > target:
                r-=1
                continue

        # ここに来たということは、ループでtargetとの一致が見つけられなかった
        # 残るは、同じインデックスを足し合わせるときのみ
        if l != r:
            raise Exception("ありえないことが起きました")
        else:
            left_num , left_original_index = pairs[l]
            right_num , right_original_index   = pairs[r]
            if left_num + right_num == target:
                return [left_original_index, right_original_index]
            else:
                raise Exception("ありえないことが起きました")

# ============================================================
# AI 講評
# (AI が講評を追記する欄。日付見出し「--- YYYY-MM-DD ---」ごとに追記していく)
# ============================================================
