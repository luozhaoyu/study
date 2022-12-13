"""
run time complexity should be O(log(m+n))

num1 = []
num2 = []

* total_len = len(num1) + len(num2)
* i = min[len(num1), total_len / 2]
* pick random index i in num1, d = num1[i], it should be the median for, j = total_len / 2 - i,  num[j], and d <= num[j + 1]

if j < 0: 
if j exceeds:

if total_len / 2 - i < 0 -> decrease i
if total_len / 2 - i > len(num2) -> increase i

if d > num[total_len / 2 -i]

"""
