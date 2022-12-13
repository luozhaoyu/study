from typing import List

class Solution:
    """
    Algorithm:
    current best solution = min(solution(amount-coin[1]) + 1, solution(amount-coin[2]))
    """
    def __init__(self):
        self.cache = {}

    def coinChange(self, coins: List[int], amount: int) -> int:
        if self.cache.get(amount):
            return self.cache[amount]

        if amount == 0:
            return 0

        result = -1
        for coin in coins:
            if amount >= coin:
                try_result = self.coinChange(coins, amount - coin)
                if try_result >= 0:  # has solution
                    if result == -1:
                        result = try_result + 1
                    else:
                        result = min(result, try_result + 1)
        self.cache[amount] = result
        return result

s = Solution()
for test in (
        ([1,2,5], 11),
        ([2], 3),
        ([1], 0),
        ([1], 1),
):
    coins, amount = test
    print(s.coinChange(coins, amount))
    s.cache = {}
    print(s.cache)
        
