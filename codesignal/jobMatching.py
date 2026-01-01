"""
For profits = [4, 10], skillsForJobs = [[true, false], [false, true]], and skillsOfCandidates = [[true, true], [true, false]], the output should be
solution(profits, skillsForJobs, skillsOfCandidates) = 14;

For profits = [5], skillsForJobs = [[true]], and skillsOfCandidates = [[true]], the output should be
solution(profits, skillsForJobs, skillsOfCandidates) = 5.
"""
import copy

def solution(profits, skillsForJobs, skillsOfCandidates):
    """
    if A works on 1, then the max profit is from non-A candidates on non-1 jobs

    1. determine (candidates, jobs): who can work on what
    2. recursively check: max_profit(qualifications with i, profits) = for each job i can do:
        result = max among profits[j] + max_profit(qualifications without i, profits without j)

    qualifications = {
        1: [1, 2]
        2: [3]
        3: []
        4: [2]
    }
    """
    def check_qualification(job_skill, candidate_skill):
        for i in range(len(job_skill)):
            if job_skill[i] and not candidate_skill[i]:  # candidate not have required skill
                return False
        return True

    def check_qualifications(skillsForJobs, skillsOfCandidates):
        qualifications = {}
        i = 0
        for candidate_skill in skillsOfCandidates:
            qualifications[i] = []
            j = 0
            for job_skill in skillsForJobs:
                if check_qualification(job_skill, candidate_skill):
                    qualifications[i].append(j)
                j += 1
            i += 1
        return qualifications
    
    def max_profit(candidate_set, job_set):
        f"""
        Calculate max profit for all qualifications given profits
        Args:
            candidate = (1, 2, 4)
            job_set = (1, 3)
        """
        if (tuple(candidate_set), tuple(job_set)) in state:
            return state[(tuple[int](candidate_set), tuple[int](job_set))]

        if not candidate_set or not job_set:  # no more candidate or no more profit
            return 0

        popped_candidate_set = copy.deepcopy(candidate_set)
        current_candidate = popped_candidate_set.pop()
        current_candidate_can_do = qualifications[current_candidate]
        # print("candidate can do", current_candidate, current_candidate_can_do, job_set)

        result = max_profit(popped_candidate_set, job_set)
        for job in current_candidate_can_do:
            if not job in job_set:  # the job can do is taken by others, then proceed
                continue

            rest_job = copy.deepcopy(job_set)
            rest_job.remove(job)
            potential_profit = profit_map[job] + max_profit(popped_candidate_set, rest_job)
            if potential_profit > result:
                result = potential_profit
        state[(tuple[int](candidate_set), tuple[int](job_set))] = result
        return result


    # store max_profit results
    state = {}
    qualifications = check_qualifications(skillsForJobs, skillsOfCandidates)
    # print(qualifications)
    profit_map = {}
    for i in range(len(profits)):
        profit_map[i] = profits[i]

    result = max_profit(set(range(len(skillsOfCandidates))), set(range(len(skillsForJobs))))
    # print(state)
    return result



def test():
    profits = [4, 10]
    skillsForJobs = [[True, False], [False, True]]
    skillsOfCandidates = [[False, False], [False, False]]
    result = solution(profits, skillsForJobs, skillsOfCandidates)
    print(result)
    print("passed test!")



test()