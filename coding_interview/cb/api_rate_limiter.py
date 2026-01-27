"""
# Exercise 6: API Rate Limiter
*Common system design problem for financial APIs.*

### Level 1: Fixed Window Counter
Implement rate limiting per user.
- **Input:** `["REQUEST", "user_id", "timestamp"]`
- **Logic:**
  - Allow maximum 10 requests per minute
  - Use timestamp to determine which minute window we're in
  - Window resets at :00 seconds of each minute
- **Return:** `"allowed"` or `"rate_limit_exceeded"`

### Level 2: Sliding Window Log
More accurate rate limiting.
- **Logic:**
  - Instead of fixed windows, track exact timestamps of last N requests
  - Check if the oldest request in the log is within 60 seconds
  - If user has made 10 requests in the last 60 seconds, deny
- **Data Structure:** Queue or list per user storing timestamps
- **New Operation:** `["GET_REQUEST_COUNT", "user_id", "timestamp"]` returns requests in last 60 seconds

### Level 3: Token Bucket Algorithm
More flexible rate limiting with burst capacity.
- **Logic:**
  - Each user has a bucket with 10 tokens, refills at 1 token/6 seconds (10 per minute)
  - Each request consumes 1 token
  - Tokens accumulate up to max capacity (10)
  - If no tokens available, deny request
- **New Format:** `["REQUEST", "user_id", "timestamp", "cost"]` where cost = tokens needed
- **Operations:**
  - `["GET_TOKENS", "user_id", "timestamp"]` returns available tokens
  - Heavy requests (cost=3) allow you to "spend" multiple tokens at once

### Level 4: Tiered Limits with Quota Reset
Different user tiers with monthly quotas.
- **New Operations:**
  - `["SET_TIER", "user_id", "tier"]` where tier = "free" (100/day, 1000/month), "premium" (1000/day, 50000/month), "enterprise" (unlimited)
  - `["RESET_QUOTA", "user_id", "period"]` where period = "daily" or "monthly"
- **Logic:**
  - Track both per-minute (sliding window), daily, and monthly limits
  - Request denied if ANY limit is exceeded
  - Daily quota resets at midnight, monthly at first of month
  - Add `["UPGRADE_USER", "user_id", "new_tier", "timestamp"]` - immediately apply new limits
- **New Operation:** `["GET_QUOTA_STATUS", "user_id"]` returns `{daily_used, daily_limit, monthly_used, monthly_limit, next_reset}`
- **Challenge:** Efficiently track multiple time windows per user

---

# Time Management Tips

For 90-minute assessments with 4 levels:

- **Level 1:** 10-15 minutes (get something working quickly)
- **Level 2:** 20-25 minutes (refactor Level 1 code into cleaner structure)
- **Level 3:** 25-30 minutes (major new feature, likely new data structure)
- **Level 4:** 25-30 minutes (complexity spike, optimization needed)
- **Buffer:** 10 minutes for debugging

**Key Strategy:** Don't try to predict Level 4 requirements. Code Level 1 cleanly but simply. When Level 3 introduces a sorted requirement, THEN refactor to use a TreeMap. The test measures your ability to adapt, not to predict the future.

11:54
12:13 -> 19 mins
12:38 -> 25 mins
2:33
2:49 -> 16 mins
3:33 -> 44 mins
"""
import time


class Counter:
    """counter per user
    counter supports sliding window


    Attributes:
        limit: counter limit
        queue: [timestamp, ]
    """
    def __init__(self, limit):
        self.limit = limit
        self.queue = []

    def bump(self, timestamp):
        """
        1. calculate allow_time = timestamp - 60
        2. find how many timestamps after allow_time
        Returns:
            allowed or deny
        """
        allow_time = timestamp - 60

        # remove older timestamp, they are irrelevant now
        while self.queue and self.queue[0] < allow_time:
            self.queue.pop(0)

        # now all timestamp is within 60 seconds
        if len(self.queue) + 1 > self.limit:  # plus current stamp would exceed limit
            return "rate_limit_exceeded"
        # still good
        self.queue.append(timestamp)
        return "allowed"

    def __str__(self):
        return str(self.queue)

    def __repr__(self):
        return str(self)


class RateLimiter:
    """
    Attributes:
        limit: 10 RequestPerMinute
        counter: {
            "user_id": [counter, current_min]
        }
    """
    def __init__(self, limit = 10):
        self.limit = limit
        self.counter = {}

    def request(self, user_id, timestamp):
        """
        1. determine current min
        2. bump counter
        3. check limit
        """
        if user_id not in self.counter:
            self.counter[user_id] = [0, 0]

        request_min = timestamp // 60
        # print(timestamp, self.counter, self.current_min)
        user_counter = self.counter[user_id]
        if request_min == user_counter[1]:  # same minute
            user_counter[0] += 1
        else:  # new minute -> reset
            user_counter[0] = 1
            user_counter[1] = request_min

        # check limit
        if user_counter[0] > self.limit:
            return "rate_limit_exceeded"

        return "allowed"

    def apply(self, operation):
        action = operation[0]
        if action == "REQUEST":
            return self.request(operation[1], operation[2])


class RateLimiterL2(RateLimiter):
    def get_request_count(self, user_id, timestamp):
        """
        """
        if user_id not in self.counter:
            return 0

        user_counter = self.counter[user_id]
        allow_time = timestamp - 60
        result = 0
        while result < len(user_counter.queue) and user_counter.queue[-result-1] >= allow_time:
            result += 1
        return result

    def request(self, user_id, timestamp):
        """
        1. determine current min
        2. bump counter
        3. check limit
        """
        if user_id not in self.counter:
            self.counter[user_id] = Counter(self.limit)

        return self.counter[user_id].bump(timestamp)

    def apply(self, operation):
        action = operation[0]
        if action == "GET_REQUEST_COUNT":
            return self.get_request_count(operation[1], operation[2])
        return super().apply(operation)

class RateLimiterL3(RateLimiterL2):
    """
    cost = token
    new token for each user, calculate new upon new request

    Attributes:
        token: {
            user_id: [token_number, timestamp]
        }
    """
    def __init__(self):
        self.token = {}

    def request(self, user_id, timestamp, cost):
        """
        1. get now how many tokens
        2. deny or allow it to proceed
        """
        token = self.get_tokens(user_id, timestamp)
        if token >= cost:  # good to go
            self.token[user_id][0] -= cost
            self.token[user_id][1] = timestamp
            return "allowed"
        return "rate_limit_exceeded"

    def get_tokens(self, user_id, timestamp):
        """
        1. calculate the time elapsed since last token calculation
        2. refill token
        """
        # init token
        if user_id not in self.token:
            self.token[user_id] = [10, timestamp]
            return self.token[user_id][0]

        time_elapsed = timestamp - self.token[user_id][1]
        # every 6 seconds
        refill_token = time_elapsed // 6
        self.token[user_id][0] += refill_token
        self.token[user_id][0] = min(10, self.token[user_id][0])
        self.token[user_id][1] += timestamp
        return self.token[user_id][0]

    def apply(self, operation):
        action = operation[0]
        if action == "REQUEST":
            return self.request(operation[1], operation[2], operation[3])
        elif action == "GET_TOKENS":
            return self.get_tokens(operation[1], operation[2])
        return super().apply(operation)

class RateLimiterL4(RateLimiterL3):
    """
    limit: per-minute, daily, monthly
    per-minute is already handled

    Attributes:
        tier: {
            "user_id": "tier"
        }
        daily: {
            user_id: [count, timestamp]
        }
        monthly: {
            user_id: [count, timestamp]
        }
    """
    def __init__(self):
        self.tier = {}
        self.daily = {}
        self.monthly = {}
        super().__init__()

    def request(self, user_id, timestamp, cost):
        """
        1. check daily
        2. check monthly
        3. execute per-minute
        4. adjust daily, monthly counter
        """
        check = self.check_limit(user_id, timestamp, cost)
        if check == "rate_limit_exceeded":
            return "rate_limit_exceeded"

        # good to check
        result = super().request(user_id, timestamp, cost)
        if result == "rate_limit_exceeded":
            return "rate_limit_exceeded"

        self.daily[user_id][0] += cost
        self.monthly[user_id][0] += cost
        self.daily[user_id][1] = timestamp
        self.monthly[user_id][1] = timestamp
        return "allowed"

    def check_limit(self, user_id, timestamp, cost):
        """
        Returns:
            boolean: whether it is within limit or not
        """
        tier = self.tier[user_id]
        if tier == "premium":
            return "allowed"

        daily_used, daily_limit, monthly_used, monthly_limit, next_reset = self.get_quota_status(user_id)

        if timestamp >= next_reset:  # if it is next reset time, then reset
            self.reset_quota(user_id, "daily")
            self.reset_quota(user_id, "monthly")

        # right quota now
        if daily_limit != -1:  # has limit
            if daily_used + cost > daily_limit: 
                return "rate_limit_exceeded"
        if monthly_limit != -1:  # has limit
            if monthly_used + cost > monthly_limit: 
                return "rate_limit_exceeded"
        return "allowed"

    def set_tier(self, user_id, tier):
        self.tier[user_id] = tier

        if user_id not in self.daily:
            self.daily[user_id] = [0, 0]
        if user_id not in self.monthly:
            self.monthly[user_id] = [0, 0]
        return tier

    def reset_quota(self, user_id, period):
        tier = self.tier[user_id]
        if period == "daily":
            if tier == "free" or tier == "premium":
                self.daily[user_id] = [0, 0]
        elif period == "monthly":
            if tier == "free" or tier == "premium":
                self.monthly[user_id] = [0, 0]

    def upgrade_user(self, user_id, new_tier, timestamp):
        """
        1. set new tier
        2. apply new limit
        """
        self.set_tier(user_id, new_tier)

        daily_used, daily_limit, monthly_used, monthly_limit, next_reset = self.get_quota_status(user_id)

    def get_quota_status(self, user_id):
        daily = self.daily[user_id]
        monthly = self.monthly[user_id]
        daily_used = daily[0]
        monthly_used = monthly[0]

        tier = self.tier[user_id]
        if tier == "free":
            daily_limit = 100
            monthly_limit = 1000
        elif tier == "premium":
            daily_limit = 1000
            monthly_limit = 50000
        else:
            daily_limit = -1
            monthly_limit = -1
        daily_next_reset = (daily[1] // (24 * 3600) + 1) * 24 * 3600

        return daily_used, daily_limit, monthly_used, monthly_limit, daily_next_reset

    def apply(self, operation):
        action = operation[0]
        if action == "SET_TIER":
            return self.set_tier(operation[1], operation[2])
        elif action == "RESET_QUOTA":
            return self.reset_quota(operation[1], operation[2])
        elif action == "UPGRADE_USER":
            return self.upgrade_user(operation[1], operation[2])
        elif action == "GET_QUOTA_STATUS":
            return self.get_quota_status(operation[1])
        return super().apply(operation)


def assert_equal(a, b):
    if a != b:
        print(f"Error: {a} != {b}")
        raise

def test_level1():
    limiter = RateLimiter(2)
    assert_equal(limiter.apply(["REQUEST", "a", 1]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 2]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 59]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 59]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 61]), "allowed")
    print("passed level 1!")

test_level1()


def test_level2():
    limiter = RateLimiterL2(2)
    assert_equal(limiter.apply(["REQUEST", "a", 1]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 2]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 59]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 59]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 61]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 62]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 120]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 120]), "rate_limit_exceeded")
    print("passed level 2!")

test_level2()


def test_level3():
    limiter = RateLimiterL3()
    assert_equal(limiter.apply(["REQUEST", "a", 1, 4]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 1, 4]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 1, 4]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 30, 4]), "allowed")
    print("passed level 3!")

test_level3()


def test_level4():
    limiter = RateLimiterL4()
    assert_equal(limiter.apply(["SET_TIER", "a", "free"]), "free")
    assert_equal(limiter.apply(["REQUEST", "a", 1, 6]), "allowed")
    assert_equal(limiter.apply(["REQUEST", "a", 1, 6]), "rate_limit_exceeded")
    assert_equal(limiter.apply(["REQUEST", "a", 30, 6]), "allowed")
    print(limiter.apply(["GET_QUOTA_STATUS", "a"]))
    print("passed level 4!")

test_level4()