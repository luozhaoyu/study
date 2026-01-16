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

"""