
from typing import List


class Solution:
    """
    No difference between tasks, so use greedy algorithm:
    1. count each task
    2. find the most task that is not in cooldown, if not, schedule idle

    remain_tasks = [["A", 3], ["B", 2], ["C", 1]]
    cooldown_task = {
        "A": 3,
        "B": 1,
    }
    """
    def __init__(self):
        self.cooldown_task = {}

    def count(self, tasks: List[str]):
        result = {}
        for task in tasks:
            if not task in result:
                result[task] = 0
            result[task] += 1
        
        result = sorted(result.items(), key=lambda x:x[1], reverse=True)
        result = [list(item) for item in result]
        return result

    def find_next_task_index(self, remain_tasks):
        i = 0
        while i < len(remain_tasks):
            task = remain_tasks[i][0]
            if task not in self.cooldown_task:  # first task not in cooldown
                return i
            i += 1
        return -1

    def decrease_cooldown(self):
        key_to_pop = []
        for key in self.cooldown_task:
            self.cooldown_task[key] -= 1
            if self.cooldown_task[key] == 0:
                key_to_pop.append(key)

        for key in key_to_pop:
            del self.cooldown_task[key]

    def leastInterval(self, tasks: List[str], n: int) -> int:
        remain_tasks = self.count(tasks)
        total_idle = 0
        while remain_tasks:
            print(remain_tasks)
            index = self.find_next_task_index(remain_tasks)
            if index > -1:  # find available task, then execute it
                task = remain_tasks[index]
                # this time would not cooldown
                self.cooldown_task[task[0]] = n + 1
                task[1] -= 1  # execute this one
                if task[1] == 0:  # finished
                    remain_tasks.pop(index)

                # keep remaining task in order
                remain_tasks = sorted(remain_tasks, key=lambda x:x[1], reverse=True)
                print(task, remain_tasks)
            else:  # idle this round
                total_idle += 1
                print("idle")
            # always decrease cooldown
            self.decrease_cooldown()
        return total_idle + len(tasks)


def test():
    s = Solution()
    test = ["A","A","A", "B","B","B"]
    print(s.leastInterval(test, 2))

test()


        