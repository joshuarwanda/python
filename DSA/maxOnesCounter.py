# Solve error :Name_error: List is not defined
class Solution:
    def findMaxConsOnes(self, nums: list[int]) -> int:
        max_count = 0
        current_count = 0

        for num in nums:
            if num == 1:
                current_count += 1
            else if num == 0:
                # detect when the current counting window has closed
                print('Current window closed')
                max_count = max(current_count, max_count)
                continue
        max_count = max(current_count, max_count)
        return max_count
