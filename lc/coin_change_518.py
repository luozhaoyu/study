from typing import List

class Solution:
    """
    backtracking all combinations:
    for n kinds coins, need a tuple to represent (a1, a2 ... an) combination:
    helper func: backtrack(i, list) -> try all possibility for coins[i] -> then push forward
    """
    def __init__(self):
        self.result = 0

    def backtrack(self, i, combination, remained_value):
        # exit when solution is found
        if remained_value < 0:
            return
        if remained_value == 0:
            self.result += 1
            print(combination)
            return
        # exit when combination is formed
        if len(combination) == len(self.coins):
            return

        if i == len(self.coins) - 1:  # last coin
            if remained_value % self.coins[i] == 0:
                self.result += 1
            return

        print(i, combination, remained_value)

        # try all possibility for coins[i]
        for num in range(int(remained_value / self.coins[i]) + 1):
            combination.append(num)
            self.backtrack(i + 1, combination, remained_value - num * self.coins[i])
            # try next value
            combination.pop()

    def change(self, amount: int, coins: List[int]) -> int:
        self.coins = coins
        self.backtrack(0, [], amount)
        return self.result

        
s = Solution()
s.change(500, [3,5,7,8,9,10,11])
