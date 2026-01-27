# Interview Preparation Guide

## Research Summary

**Sources Checked:**
- 1point3acres.com (地里) - Multiple interview experiences (2024-2025)
- Blind (teamblind.com) - CodeSignal specific experiences
- Glassdoor, LeetCode, Interview platforms
- Date Range: Last 12-24 months (2024-2026)

**Key Patterns Observed:**

1. **Platform:** CodeSignal (previously Replit)
2. **Duration:** 60-90 minutes (live interview or asynchronous)
3. **Question Bank:** Very small (~6 questions total)
4. **Most Common Question:** Web Crawler implementation (BFS-based)
5. **Second Most Common:** In-memory database/API with progressive rounds (4 rounds in 90 mins)
6. **Language:** Primarily Python
7. **Difficulty:** Not standard LeetCode-style; more practical and open-ended
8. **Main Challenge:** **TIME PRESSURE** - speed is critical, not complexity

**Interview Format Notes:**
- **NOT** traditional algorithm problems
- Emphasis on **practical, production-ready code**
- Focus on **code quality, scalability, and async/concurrent programming**
- Progressive rounds: start simple, add features incrementally
- Get tests passing first, then optimize
- AI tools strictly prohibited during live sessions

**Critical Success Factors:**
- ⚡ **Speed:** Complete all rounds within time limit
- ✅ **Test Coverage:** Pass all test cases (often required for advancement)
- 🏗️ **Incremental Building:** Each round builds on previous
- 🔄 **Async/Concurrency:** Often required for optimization rounds
- 🎯 **Practical Focus:** Real-world engineering, not academic algorithms

---

## Exercise 1: Web Crawler with Domain Filtering

**Difficulty:** Medium-Hard  
**Time:** 45 minutes  
**Based on:** Most frequently asked the company question (confirmed multiple sources)

**Problem Statement:**

Implement a web crawler that discovers all pages within a given domain. Your crawler should:
- Start from a seed URL
- Extract all links from each page
- Only follow links within the same domain
- Avoid revisiting pages (deduplication)
- Return a list of all discovered URLs

**Round 1 (15 mins): Basic Synchronous Crawler**
```python
def crawl(seed_url: str, max_pages: int = 100) -> List[str]:
    """
    Crawl pages starting from seed_url, staying within same domain.
    
    Args:
        seed_url: Starting URL (e.g., "https://example.com/page1")
        max_pages: Maximum pages to crawl
    
    Returns:
        List of all discovered URLs
    """
    pass
```

**Round 2 (10 mins): Add Filtering and Statistics**
```python
def crawl_with_stats(seed_url: str, max_pages: int = 100) -> Dict[str, Any]:
    """
    Returns:
        {
            "urls": List[str],           # All discovered URLs
            "total_pages": int,           # Number of pages crawled
            "total_links": int,           # Total links found
            "broken_links": List[str]     # URLs that returned errors
        }
    """
    pass
```

**Round 3 (15 mins): Async/Concurrent Implementation**
```python
async def crawl_concurrent(seed_url: str, max_pages: int = 100, 
                          max_concurrent: int = 10) -> List[str]:
    """
    Implement concurrent crawling using asyncio or threading.
    Control concurrency with max_concurrent parameter.
    """
    pass
```

**Round 4 (5 mins): Politeness and Rate Limiting**
```python
async def crawl_polite(seed_url: str, max_pages: int = 100,
                      max_concurrent: int = 10,
                      delay_seconds: float = 1.0) -> List[str]:
    """
    Add rate limiting to be a polite crawler.
    Respect robots.txt (bonus).
    """
    pass
```

**Input/Output Examples:**

```python
# Example 1: Simple domain
seed_url = "https://example.com/page1"
# page1 contains links to: page2, page3, https://other.com/page4
# page2 contains links to: page1, page3
# page3 contains links to: page1

result = crawl(seed_url)
# Output: [
#   "https://example.com/page1",
#   "https://example.com/page2", 
#   "https://example.com/page3"
# ]
# Note: https://other.com/page4 excluded (different domain)

# Example 2: With stats
result = crawl_with_stats(seed_url)
# Output: {
#   "urls": ["https://example.com/page1", ...],
#   "total_pages": 3,
#   "total_links": 6,
#   "broken_links": []
# }
```

**Constraints:**
- 1 <= max_pages <= 1000
- URLs are well-formed HTTP/HTTPS
- Handle network errors gracefully
- Detect and handle cycles in link graph
- Same domain means same scheme + netloc (e.g., https://example.com)

**Why This Matters for the company:**

This is THE most common the company question. It tests:
- **Graph traversal** (BFS for web crawling)
- **Deduplication** (set/dict for visited URLs)
- **URL parsing** (extracting domain, normalizing)
- **Async programming** (critical for Claude API infrastructure)
- **Production concerns** (rate limiting, error handling, politeness)

the company builds LLM APIs that crawl and process web content, so understanding web infrastructure is crucial.

**Expected Approach:**
- Use BFS (queue) not DFS (stack) for level-order traversal
- Use `urllib.parse` or `urlparse` for URL manipulation
- Use `set` for visited URLs (O(1) lookup)
- Use `requests` or `httpx` for HTTP calls
- For async: `asyncio` + `aiohttp` or `httpx.AsyncClient`
- For threading: `ThreadPoolExecutor` with `concurrent.futures`
- Target Complexity: O(V + E) time where V=pages, E=links; O(V) space

**Common Pitfalls:**
- Not normalizing URLs (trailing slash, fragments, query params)
- Not handling redirects properly
- DFS instead of BFS (causes deep recursion)
- Race conditions in concurrent version
- Not limiting queue size (memory issues)

**Follow-up Questions:**

1. **Scaling:** How would you distribute this across multiple machines? How would you handle a queue of millions of URLs?
   - *Hint: Distributed queue (Redis, Kafka), consistent hashing for URL assignment*

2. **Production:** How would you handle failures? What if a domain goes down mid-crawl?
   - *Hint: Checkpoint progress, retry logic with exponential backoff, circuit breakers*

3. **Optimization:** Threading vs. Multiprocessing vs. Async - which is best and why?
   - *Hint: Async is best for I/O-bound (network calls), GIL doesn't matter*

4. **Politeness:** How do you ensure you don't overload target servers?
   - *Hint: robots.txt, rate limiting per domain, exponential backoff on errors*

5. **Detection:** How would you detect infinite loops or crawler traps?
   - *Hint: Max depth per path, URL pattern detection, time limits*

---

## Exercise 2: In-Memory Database with Progressive Features

**Difficulty:** Medium  
**Time:** 45 minutes  
**Based on:** Second most common the company question pattern (4-round progressive build)

**Problem Statement:**

Build an in-memory key-value database with a clean API. Each round adds new features.

**Round 1 (10 mins): Basic GET/SET/DELETE**

```python
class InMemoryDB:
    def set(self, key: str, value: Any) -> None:
        """Set a key-value pair."""
        pass
    
    def get(self, key: str) -> Optional[Any]:
        """Get value by key. Returns None if not found."""
        pass
    
    def delete(self, key: str) -> bool:
        """Delete a key. Returns True if existed, False otherwise."""
        pass
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass
```

**Round 2 (10 mins): Transactions (BEGIN/COMMIT/ROLLBACK)**

```python
class InMemoryDB:
    # ... previous methods ...
    
    def begin_transaction(self) -> None:
        """Start a new transaction."""
        pass
    
    def commit(self) -> None:
        """Commit current transaction."""
        pass
    
    def rollback(self) -> None:
        """Rollback current transaction."""
        pass
```

**Round 3 (15 mins): Nested Transactions**

```python
# Support multiple levels of nested transactions
# Each ROLLBACK only affects the innermost transaction
# COMMIT applies changes to parent transaction (not main DB until outermost commits)

db = InMemoryDB()
db.set("x", 1)
db.begin_transaction()
db.set("x", 2)
db.begin_transaction()
db.set("x", 3)
db.rollback()  # x should be 2 in transaction
db.get("x")     # Returns 2
db.commit()     # x is now 2 in main DB
```

**Round 4 (10 mins): Expiration/TTL**

```python
class InMemoryDB:
    # ... previous methods ...
    
    def set_with_ttl(self, key: str, value: Any, ttl_seconds: int) -> None:
        """Set key with time-to-live in seconds."""
        pass
    
    def get(self, key: str) -> Optional[Any]:
        """Get value. Returns None if expired or not found."""
        pass
```

**Input/Output Examples:**

```python
# Example 1: Basic operations
db = InMemoryDB()
db.set("name", "Claude")
db.get("name")          # Returns "Claude"
db.exists("name")       # Returns True
db.delete("name")       # Returns True
db.get("name")          # Returns None

# Example 2: Transactions
db.set("balance", 100)
db.begin_transaction()
db.set("balance", 50)
db.get("balance")       # Returns 50 (in transaction)
db.rollback()
db.get("balance")       # Returns 100 (rollback successful)

# Example 3: Nested transactions
db.set("x", 1)
db.begin_transaction()
db.set("x", 2)
db.begin_transaction()
db.set("x", 3)
db.commit()             # Commit inner
db.get("x")             # Returns 3
db.rollback()           # Rollback outer
db.get("x")             # Returns 1

# Example 4: TTL
db.set_with_ttl("session", "abc123", ttl_seconds=2)
db.get("session")       # Returns "abc123"
time.sleep(3)
db.get("session")       # Returns None (expired)
```

**Constraints:**
- Keys are strings, values can be any Python object
- Transaction nesting depth <= 10
- TTL precision: seconds (not milliseconds)
- No persistence required (in-memory only)

**Why This Matters for the company:**

the company's Claude API requires:
- **Fast in-memory caching** for conversation context
- **Transaction semantics** for atomic operations
- **TTL/Expiration** for session management
- **Clean API design** for SDK development

This tests your ability to design production-ready data structures with complex state management.

**Expected Approach:**
- Use dict for main storage: O(1) get/set/delete
- For transactions: Stack of dicts (copy-on-write or delta logs)
- For TTL: Store `(value, expiration_time)` tuples, check on get
- Alternative: Background thread to clean expired keys
- Target Complexity: O(1) for basic ops, O(n) for rollback where n=keys modified

**Common Pitfalls:**
- Shallow vs. deep copy of values in transactions
- Forgetting to check expiration on exists()
- Not handling commit without begin_transaction
- Incorrect nested transaction isolation
- Memory leak from not cleaning expired keys

**Follow-up Questions:**

1. **Concurrency:** How would you make this thread-safe for multiple clients?
   - *Hint: Read-write locks, per-key locks, lock-free data structures*

2. **Persistence:** How would you add persistence without sacrificing performance?
   - *Hint: Write-ahead log (WAL), snapshots + deltas, background flush*

3. **Memory:** How would you implement an LRU eviction policy?
   - *Hint: OrderedDict or doubly-linked list + hashmap*

4. **Distribution:** How would you shard this across multiple machines?
   - *Hint: Consistent hashing, partition by key range, replication*

5. **Complex Queries:** How would you add support for range queries or pattern matching?
   - *Hint: B-tree/sorted containers for ranges, trie for prefix matching*

---

## Exercise 3: Rate Limiter API

**Difficulty:** Medium  
**Time:** 40 minutes  
**Based on:** Common pattern in the company interviews (API design with constraints)

**Problem Statement:**

Design and implement a rate limiter for an API service. Support multiple rate limiting strategies.

**Round 1 (12 mins): Fixed Window Rate Limiter**

```python
class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Window size in seconds
        """
        pass
    
    def allow_request(self, user_id: str) -> bool:
        """
        Returns True if request should be allowed, False if rate limit exceeded.
        """
        pass
    
    def get_remaining(self, user_id: str) -> int:
        """
        Returns number of remaining requests in current window.
        """
        pass
```

**Round 2 (12 mins): Sliding Window Log**

```python
class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int, window_seconds: int):
        """
        More accurate than fixed window - tracks each request timestamp.
        """
        pass
    
    def allow_request(self, user_id: str, timestamp: Optional[float] = None) -> bool:
        """
        Args:
            user_id: User identifier
            timestamp: Optional timestamp (defaults to time.time())
        """
        pass
```

**Round 3 (10 mins): Token Bucket Algorithm**

```python
class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate: float):
        """
        Args:
            capacity: Maximum tokens in bucket
            refill_rate: Tokens added per second
        """
        pass
    
    def allow_request(self, user_id: str, tokens: int = 1) -> bool:
        """
        Args:
            tokens: Number of tokens to consume (default 1)
        """
        pass
```

**Round 4 (6 mins): Distributed Rate Limiting**

```python
# Design discussion: How would you implement this with Redis?
# Provide pseudo-code or algorithm description

def distributed_rate_limiter_design() -> str:
    """
    Describe how you'd implement this using Redis.
    Include:
    - Data structures used
    - Redis commands
    - Race condition handling
    - TTL management
    """
    pass
```

**Input/Output Examples:**

```python
# Example 1: Fixed Window (5 requests per 10 seconds)
limiter = RateLimiter(max_requests=5, window_seconds=10)

for i in range(7):
    allowed = limiter.allow_request("user123")
    print(f"Request {i+1}: {'allowed' if allowed else 'denied'}")

# Output:
# Request 1: allowed
# Request 2: allowed
# Request 3: allowed
# Request 4: allowed
# Request 5: allowed
# Request 6: denied   <- rate limit hit
# Request 7: denied

time.sleep(10)  # Wait for window to reset
limiter.allow_request("user123")  # Returns True

# Example 2: Token Bucket (capacity=10, refill=2/second)
limiter = TokenBucketRateLimiter(capacity=10, refill_rate=2.0)

# Burst of 10 requests
for i in range(10):
    limiter.allow_request("user123")  # All allowed

limiter.allow_request("user123")  # False (bucket empty)

time.sleep(3)  # 6 tokens refilled (2/sec * 3 sec)

for i in range(6):
    limiter.allow_request("user123")  # First 6 allowed
```

**Constraints:**
- Support up to 1M concurrent users
- Window sizes: 1 second to 1 hour
- Requests per window: 1 to 10,000
- Must be memory efficient
- Thread-safe for concurrent requests

**Why This Matters for the company:**

Claude API must:
- **Rate limit API calls** per user/organization
- **Protect infrastructure** from abuse and overload
- **Fair resource allocation** across customers
- **Handle burst traffic** gracefully

Rate limiting is critical for any production API at scale.

**Expected Approach:**
- Fixed Window: Dict of `{user_id: (count, window_start)}`
- Sliding Window: Dict of `{user_id: deque(timestamps)}`
- Token Bucket: Dict of `{user_id: (tokens, last_refill_time)}`
- Clean up expired entries periodically or lazily
- Target Complexity: O(1) for fixed/token, O(n) for sliding window cleanup

**Common Pitfalls:**
- Fixed window edge case: burst at window boundary
- Not cleaning old timestamps in sliding window (memory leak)
- Token bucket: incorrect refill calculation with time drift
- Race conditions in multi-threaded environment
- Not handling clock skew in distributed system

**Follow-up Questions:**

1. **Distributed:** Implement this using Redis. How do you handle race conditions?
   - *Hint: Lua scripts for atomic operations, Redis sorted sets for sliding window*

2. **Fairness:** What if you need different limits for different tiers (free/pro/enterprise)?
   - *Hint: Multiple rate limiters per user, hierarchical limits*

3. **Graceful Degradation:** How would you handle rate limiter service failure?
   - *Hint: Fail open vs. fail closed, circuit breakers, fallback to local limits*

4. **Analytics:** How would you track and report rate limit violations?
   - *Hint: Metrics aggregation, async logging, time-series database*

5. **Algorithms:** Compare Fixed Window, Sliding Window, Token Bucket, Leaky Bucket - which is best?
   - *Hint: Trade-offs between accuracy, memory, implementation complexity*

---

## Exercise 4: Event Stream Processor

**Difficulty:** Medium-Hard  
**Time:** 45 minutes  
**Based on:** Real-world system patterns (async processing, streaming)

**Problem Statement:**

Build an event stream processor that handles high-volume events with filtering, transformation, and aggregation.

**Round 1 (10 mins): Basic Event Processor**

```python
from typing import Callable, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Event:
    event_type: str
    user_id: str
    timestamp: datetime
    data: Dict[str, Any]

class EventProcessor:
    def __init__(self):
        pass
    
    def subscribe(self, event_type: str, handler: Callable[[Event], None]) -> None:
        """Register a handler for specific event type."""
        pass
    
    def publish(self, event: Event) -> None:
        """Publish an event to all subscribed handlers."""
        pass
```

**Round 2 (10 mins): Filtering and Chaining**

```python
class EventProcessor:
    # ... previous methods ...
    
    def filter(self, predicate: Callable[[Event], bool]) -> 'EventProcessor':
        """Return new processor that only processes events matching predicate."""
        pass
    
    def map(self, transformer: Callable[[Event], Event]) -> 'EventProcessor':
        """Return new processor that transforms each event."""
        pass
```

**Round 3 (15 mins): Windowed Aggregation**

```python
class EventProcessor:
    # ... previous methods ...
    
    def window(self, 
               window_seconds: int,
               aggregator: Callable[[List[Event]], Any]) -> 'EventProcessor':
        """
        Aggregate events within sliding time windows.
        
        Args:
            window_seconds: Window size
            aggregator: Function to aggregate events in window
        
        Returns:
            New processor that emits aggregated results
        """
        pass
```

**Round 4 (10 mins): Async Processing and Backpressure**

```python
class AsyncEventProcessor:
    async def publish(self, event: Event) -> None:
        """Async publish with backpressure handling."""
        pass
    
    def set_max_queue_size(self, size: int) -> None:
        """Set maximum queue size for backpressure."""
        pass
```

**Input/Output Examples:**

```python
# Example 1: Basic pub/sub
processor = EventProcessor()

def handle_login(event: Event):
    print(f"User {event.user_id} logged in")

processor.subscribe("login", handle_login)

event = Event("login", "user123", datetime.now(), {})
processor.publish(event)
# Output: "User user123 logged in"

# Example 2: Filtering and mapping
processor = EventProcessor()
filtered = processor.filter(lambda e: e.user_id.startswith("premium_"))
transformed = filtered.map(lambda e: Event(
    event_type=f"{e.event_type}_premium",
    user_id=e.user_id,
    timestamp=e.timestamp,
    data=e.data
))

# Example 3: Windowed aggregation (count events per 60 seconds)
processor = EventProcessor()
windowed = processor.window(
    window_seconds=60,
    aggregator=lambda events: len(events)
)

# Publish 100 events over time
# Every 60 seconds, windowed processor emits count
```

**Constraints:**
- Handle 10,000+ events per second
- Support multiple subscribers per event type
- Windowed aggregation: handle overlapping windows
- Memory efficient (don't store all events)
- Thread-safe or async-safe

**Why This Matters for the company:**

Claude API processes:
- **High-volume request streams**
- **Real-time analytics** (usage metrics, billing)
- **Event-driven architectures** (webhooks, notifications)
- **Stream processing** (conversation flows, context management)

This tests ability to design scalable, reactive systems.

**Expected Approach:**
- Use dict of lists for subscribers: `{event_type: [handlers]}`
- Filter/map: Chain processors or decorator pattern
- Windowing: Circular buffer or deque with timestamps
- Async: `asyncio.Queue` with `maxsize` for backpressure
- Target Complexity: O(1) for publish, O(k) where k=subscribers

**Common Pitfalls:**
- Not handling exceptions in handlers (one bad handler kills all)
- Memory leak in windowing (not removing old events)
- Race conditions with concurrent publishers
- Blocking I/O in handlers (use async or thread pool)
- Not handling backpressure (unbounded queue growth)

**Follow-up Questions:**

1. **Ordering:** How do you guarantee event ordering across distributed system?
   - *Hint: Vector clocks, sequence numbers, partition by key*

2. **Fault Tolerance:** What if a handler crashes? How do you retry?
   - *Hint: Dead letter queue, exponential backoff, circuit breakers*

3. **Scalability:** How would you distribute this across multiple machines?
   - *Hint: Kafka/Kinesis, partition by user_id, exactly-once semantics*

4. **Monitoring:** How do you monitor lag, throughput, and error rates?
   - *Hint: Metrics per event type, consumer lag monitoring, alerting*

5. **Testing:** How would you test this system, especially windowing logic?
   - *Hint: Inject fake clock, property-based testing, integration tests*

---

## Exercise 5: API Request Batching and Deduplication

**Difficulty:** Medium  
**Time:** 40 minutes  
**Based on:** Practical optimization pattern (mentioned in API design rounds)

**Problem Statement:**

Design a system that batches and deduplicates API requests to reduce load on downstream services.

**Round 1 (12 mins): Request Deduplication**

```python
from typing import Any, Callable
import asyncio

class RequestDeduplicator:
    def __init__(self):
        pass
    
    async def fetch(self, key: str, fetcher: Callable[[str], Any]) -> Any:
        """
        Fetch data for key. If another request for same key is in-flight,
        wait for that result instead of making duplicate request.
        
        Args:
            key: Request identifier
            fetcher: Async function to fetch data
        
        Returns:
            Result from fetcher (shared if deduplicated)
        """
        pass
```

**Round 2 (12 mins): Automatic Batching**

```python
class BatchingClient:
    def __init__(self, 
                 batch_size: int = 10,
                 max_wait_ms: int = 100):
        """
        Args:
            batch_size: Maximum items per batch
            max_wait_ms: Maximum time to wait before sending batch
        """
        pass
    
    async def fetch(self, key: str) -> Any:
        """
        Fetch data for key. Automatically batches requests.
        """
        pass
    
    async def _batch_fetcher(self, keys: List[str]) -> Dict[str, Any]:
        """Override this to implement actual batch API call."""
        pass
```

**Round 3 (10 mins): Caching Layer**

```python
class CachedBatchingClient(BatchingClient):
    def __init__(self, 
                 batch_size: int = 10,
                 max_wait_ms: int = 100,
                 cache_ttl_seconds: int = 300):
        """Add LRU cache with TTL to batching client."""
        pass
    
    async def fetch(self, key: str, bypass_cache: bool = False) -> Any:
        """Fetch with automatic caching."""
        pass
```

**Round 4 (6 mins): Error Handling and Retries**

```python
# Add:
# - Per-key error handling (one failure doesn't fail whole batch)
# - Exponential backoff retries
# - Circuit breaker for downstream service
```

**Input/Output Examples:**

```python
# Example 1: Deduplication
dedup = RequestDeduplicator()

async def slow_fetch(key):
    await asyncio.sleep(1)  # Simulate slow API
    return f"data_{key}"

# Make 5 concurrent requests for same key
results = await asyncio.gather(
    dedup.fetch("user123", slow_fetch),
    dedup.fetch("user123", slow_fetch),
    dedup.fetch("user123", slow_fetch),
    dedup.fetch("user123", slow_fetch),
    dedup.fetch("user123", slow_fetch),
)
# Only 1 actual call to slow_fetch, all 5 get same result
# Total time: ~1 second (not 5)

# Example 2: Batching
client = BatchingClient(batch_size=10, max_wait_ms=100)

# Make 25 requests within 50ms
tasks = [client.fetch(f"key_{i}") for i in range(25)]
results = await asyncio.gather(*tasks)

# Results in 3 batch API calls:
# - Batch 1: keys 0-9 (batch_size=10)
# - Batch 2: keys 10-19 (batch_size=10)
# - Batch 3: keys 20-24 (timeout after max_wait_ms)
```

**Constraints:**
- Support 1000+ concurrent requests
- Batch size: 1-100 items
- Max wait time: 10-1000ms
- Handle partial batch failures
- Thread-safe/async-safe

**Why This Matters for the company:**

Claude API benefits from:
- **Batching embeddings API calls** (efficiency)
- **Deduplicating identical requests** (cost reduction)
- **Caching frequently accessed data** (latency)
- **Graceful degradation** under load

This demonstrates understanding of production optimization techniques.

**Expected Approach:**
- Deduplication: Dict of `{key: Future/Event}` for in-flight requests
- Batching: Queue + background task that flushes on size/timeout
- Caching: LRU cache (`functools.lru_cache` or custom with TTL)
- Use `asyncio.gather` or `asyncio.wait_for` for coordination
- Target Complexity: O(1) per request, O(n) for batch where n=batch_size

**Common Pitfalls:**
- Race condition in deduplication (double-fetch)
- Not waking up waiting tasks after fetch completes
- Batching: not handling timeout vs. batch size trigger
- Memory leak from abandoned requests in queue
- Not propagating errors correctly to individual requests

**Follow-up Questions:**

1. **Partial Failures:** If 1 item in batch fails, how do you handle the other 9?
   - *Hint: Return dict with successes and errors, retry only failures*

2. **Priority:** How would you prioritize certain requests over others?
   - *Hint: Priority queue, multiple batch queues, preemption*

3. **Monitoring:** What metrics would you track?
   - *Hint: Batch size distribution, wait time, deduplication rate, cache hit rate*

4. **Adaptive Batching:** How would you dynamically adjust batch size based on load?
   - *Hint: Monitor latency, adjust batch_size and max_wait_ms automatically*

5. **Distributed:** How would this work across multiple API servers?
   - *Hint: Shared cache (Redis), coordination service, or accept some duplication*

---

## Practice Strategy Recommendations

### Priority Order

**Week 1-2: Core Patterns (Complete these first)**
1. ✅ **Exercise 1: Web Crawler** - This is THE most common question
2. ✅ **Exercise 2: In-Memory Database** - Second most common
3. ✅ **Exercise 3: Rate Limiter** - Common API design pattern

**Week 3-4: Advanced Topics**
4. ✅ **Exercise 4: Event Stream Processor** - Async/streaming practice
5. ✅ **Exercise 5: Request Batching** - Optimization techniques

### Time Management Tips

**⚡ SPEED IS CRITICAL at the company**

1. **Round 1 First (15 mins):** Get basic solution working and tests passing
   - Don't aim for perfection
   - Use simple data structures
   - Get to green tests FAST

2. **Progressive Refinement (10 mins per round):** Add features incrementally
   - Each round builds on previous
   - Don't refactor Round 1 when doing Round 3
   - Copy-paste and extend if needed

3. **Time Boxing (Strict):**
   - Set timer for each round
   - Move on even if not perfect
   - Partial credit > no credit

4. **Testing Strategy:**
   - Run provided tests after each round
   - Fix failures immediately
   - Don't over-test (time constraint!)

### Key Topics to Review

**Must-Know Python:**
- ✅ `asyncio` and `async`/`await` patterns
- ✅ `threading` and `concurrent.futures`
- ✅ `collections.deque`, `defaultdict`, `OrderedDict`
- ✅ `urllib.parse` for URL manipulation
- ✅ `time`, `datetime` for time-based features
- ✅ Context managers (`with` statements)
- ✅ Decorators and functional programming

**Data Structures:**
- ✅ Hash tables (dict) - O(1) operations
- ✅ Queues (deque) - BFS, buffering
- ✅ Sets - deduplication
- ✅ Heaps - priority queues
- ✅ Tries - prefix matching (bonus)

**Patterns:**
- ✅ BFS vs. DFS (when to use each)
- ✅ Producer-Consumer pattern
- ✅ Observer/Pub-Sub pattern
- ✅ Decorator/Wrapper pattern
- ✅ State management (FSM basics)

**System Design Concepts:**
- ✅ Caching strategies (LRU, TTL)
- ✅ Rate limiting algorithms
- ✅ Concurrency control
- ✅ Backpressure handling
- ✅ Graceful degradation

### the company-Specific Tips

**Do's:**
- ✅ **Ask questions early** - show engagement
- ✅ **Think out loud** - explain your approach
- ✅ **Start simple, iterate** - progressive problem solving
- ✅ **Write clean, readable code** - production quality matters
- ✅ **Handle errors gracefully** - show production mindset
- ✅ **Test as you go** - run tests after each round
- ✅ **Discuss trade-offs** - show senior-level thinking

**Don'ts:**
- ❌ Don't use AI tools (strictly prohibited)
- ❌ Don't aim for perfect solution in Round 1
- ❌ Don't over-engineer early rounds
- ❌ Don't ignore time limits
- ❌ Don't forget to handle edge cases
- ❌ Don't write overly clever code (readability > cleverness)
- ❌ Don't skip testing (passing tests is critical)

**Interview Day:**
- ☕ Use a larger monitor (recommended by candidates)
- 💻 Test CodeSignal platform beforehand
- 🐍 Be comfortable with Python REPL for quick testing
- ⏰ Keep an eye on time - use timer
- 📝 Read problem statement carefully (all rounds at once if provided)
- 🗣️ Communicate constantly with interviewer

### Mock Interview Practice

**Simulate Real Conditions:**
1. Set 90-minute timer for all 4 rounds
2. Use CodeSignal practice assessments
3. No AI tools, no Google (syntax docs OK)
4. Track completion time per round
5. Review and identify bottlenecks

**Target Scores:**
- Round 1: 100% tests passing (baseline)
- Round 2: 100% tests passing (features)
- Round 3: 100% tests passing (optimization)
- Round 4: 80%+ (time permitting)

**Success Criteria:**
- Complete all 4 rounds in 90 minutes
- All tests passing for Rounds 1-3
- Clean, production-ready code
- Good error handling
- Clear variable names and structure

---

## Additional Resources

**Practice Platforms:**
- [CodeSignal Practice Assessments](https://app.codesignal.com/assessments/practice) - **MUST DO**
- LeetCode: Focus on Medium problems, not Hard
- Real Python: Async/concurrency tutorials
- Python asyncio documentation

**the company Research:**
- Read the company's engineering blog
- Understand Claude API architecture
- Review API rate limiting documentation
- Study AI safety and responsible AI practices (for culture fit)

**Python Async Resources:**
- "Fluent Python" by Luciano Ramalho (asyncio chapters)
- Python asyncio official docs
- Real Python asyncio tutorials
- Understanding GIL and when it matters

---

## Final Checklist

**Before Interview:**
- [ ] Completed all 5 exercises under time constraints
- [ ] Practiced on CodeSignal platform
- [ ] Reviewed asyncio/threading patterns
- [ ] Can implement BFS web crawler in 15 minutes
- [ ] Can build basic in-memory DB in 10 minutes
- [ ] Comfortable with progressive problem-solving
- [ ] Prepared questions about the company's tech stack
- [ ] Setup: Large monitor, quiet space, stable internet

**Day Before:**
- [ ] Good night's sleep (speed requires focus!)
- [ ] Review Python async syntax one more time
- [ ] Quick review of common data structures
- [ ] Prepare water, snacks for interview
- [ ] Test CodeSignal in your browser

**During Interview:**
- [ ] Read entire problem before the company
- [ ] Ask clarifying questions upfront
- [ ] Think out loud - explain approach
- [ ] Get Round 1 working ASAP
- [ ] Run tests after each round
- [ ] Watch the clock - strict time boxing
- [ ] Stay calm if stuck - move on and come back

---

## Good Luck! 🚀

Remember: **the company values practical, production-ready code over algorithmic tricks.**

Focus on:
- **Speed** (finish all rounds)
- **Quality** (clean, readable code)
- **Testing** (pass all test cases)
- **Communication** (think out loud)

You've got this! 💪
