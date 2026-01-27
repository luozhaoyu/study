## Coding Exercise Set for the company

### Research Summary
- **Sources Checked:** 1point3acres.com, LeetCode discuss, Blind, recent interview experiences
- **Date Range:** Last 12-24 months
- **Key Patterns Observed:** Strong emphasis on data serialization, in-memory storage systems, efficient data structures, API design, and scalability considerations for ML workloads
- **Interview Format Notes:** Virtual/onsite mix, 45-minute rounds, focus on clean code and system thinking

---

### Exercise 1: Custom Serialization Format for Nested API Responses

**Difficulty:** Medium  
**Time:** 35-40 minutes  
**Based on:** Common pattern at the company

**Problem Statement:**

Design and implement a serialization system for complex nested API response objects. Your system should support serializing and deserializing objects containing:
- Primitive types (integers, floats, strings, booleans, null)
- Nested dictionaries/objects
- Lists/arrays (which may contain any of the above types)
- Custom metadata fields that should be preserved

The serialized format should be space-efficient and human-readable. You need to implement:
- `serialize(obj) -> str`: Convert a Python object to your serialized format
- `deserialize(data: str) -> obj`: Reconstruct the original object

**Input/Output Examples:**

```
Example 1:
Input: {
    "model": "gpt-4",
    "usage": {"prompt_tokens": 100, "completion_tokens": 50},
    "choices": [{"text": "Hello", "index": 0}]
}
Output: (your serialized string format)

Example 2:
Input: {
    "data": [1, 2.5, "text", None, {"nested": True}],
    "metadata": {"version": "1.0"}
}
Output: (your serialized string format)
```

**Constraints:**
- Objects can be nested up to 10 levels deep
- String values may contain special characters including quotes and newlines
- Must handle circular references gracefully (detect and raise error)
- Serialized size should not exceed 2x the JSON representation
- Deserialization must produce exact copy of original structure

**Why This Matters for the company:**
The company's API infrastructure handles billions of requests with complex nested response structures. Efficient serialization impacts latency, bandwidth costs, and caching strategies.

**Expected Approach:**
- Consider different serialization formats (JSON-like, protocol buffer style, custom binary)
- Handle type information preservation
- Edge cases: escape characters, type coercion, number precision
- Target Complexity: O(n) time for both operations where n is total elements, O(n) space

**Follow-up Questions:**
1. How would you modify this to support streaming serialization for very large objects that don't fit in memory?
2. What changes would you make to optimize for repeated serialization of similar object structures?
3. How would you add versioning to handle schema evolution?
4. Compare your format to Protocol Buffers, MessagePack, and JSON - what are the trade-offs?

---

### Exercise 2: In-Memory Key-Value Store with Serialization Snapshots

**Difficulty:** Medium-Hard  
**Time:** 40-45 minutes  
**Based on:** Actual interview pattern at the company

**Problem Statement:**

Implement an in-memory key-value store that supports:
- `set(key: str, value: Any) -> None`: Store a key-value pair
- `get(key: str) -> Any`: Retrieve a value by key
- `delete(key: str) -> bool`: Remove a key-value pair
- `snapshot() -> bytes`: Serialize entire store state to bytes
- `restore(data: bytes) -> None`: Restore store from serialized snapshot

The store should handle various Python types (str, int, float, list, dict, set, tuple) and preserve type information across snapshots. Optimize for fast snapshot creation.

**Input/Output Examples:**

```
Example 1:
store = KVStore()
store.set("user:123", {"name": "Alice", "credits": 100})
store.set("model:gpt4", {"tokens": 8192, "temperature": 0.7})
snapshot_data = store.snapshot()
store.delete("user:123")
store.restore(snapshot_data)
assert store.get("user:123") == {"name": "Alice", "credits": 100}

Example 2:
store = KVStore()
store.set("list_data", [1, 2, [3, 4]])
store.set("set_data", {1, 2, 3})
snapshot_data = store.snapshot()
new_store = KVStore()
new_store.restore(snapshot_data)
assert new_store.get("list_data") == [1, 2, [3, 4]]
assert new_store.get("set_data") == {1, 2, 3}
```

**Constraints:**
- Store should support at least 1 million keys
- Snapshot operation should complete in O(n) time where n is data size
- Support concurrent reads during snapshot (bonus)
- Serialized format should be deterministic (same data = same bytes)
- Handle type preservation for all Python built-in types

**Why This Matters for the company:**
The company's serving infrastructure requires fast state snapshots for model caching, session management, and failover scenarios. Efficient serialization directly impacts recovery time and storage costs.

**Expected Approach:**
- Choose appropriate serialization format (pickle, msgpack, custom)
- Consider memory-efficient snapshot strategies (copy-on-write concepts)
- Handle type information encoding
- Target Complexity: O(n) snapshot time, O(1) get/set/delete, O(n) restore

**Follow-up Questions:**
1. How would you implement incremental snapshots to only serialize changed data?
2. What strategy would you use to support transactions across multiple operations?
3. How would you add TTL (time-to-live) for keys without impacting snapshot/restore?
4. Design an approach to compress snapshots while maintaining fast restore times.

---

### Exercise 3: Efficient Batch Request Serializer with Compression

**Difficulty:** Medium  
**Time:** 30-35 minutes  
**Based on:** Common pattern at the company

**Problem Statement:**

Design a system to efficiently serialize batches of similar structured requests. Given a list of request objects that share the same schema, create a compressed serialization format that:
- Stores the schema once
- Efficiently encodes repeated values
- Supports fast random access to individual requests after deserialization

Implement:
- `serialize_batch(requests: List[Dict]) -> bytes`: Serialize a batch
- `deserialize_batch(data: bytes) -> List[Dict]`: Deserialize entire batch
- `get_request_at(data: bytes, index: int) -> Dict`: Access single request without full deserialization

**Input/Output Examples:**

```
Example 1:
requests = [
    {"prompt": "Hello", "max_tokens": 100, "temperature": 0.7, "model": "gpt-4"},
    {"prompt": "World", "max_tokens": 100, "temperature": 0.7, "model": "gpt-4"},
    {"prompt": "Test", "max_tokens": 100, "temperature": 0.7, "model": "gpt-4"}
]
data = serialize_batch(requests)
# Should be significantly smaller than naive JSON serialization
assert deserialize_batch(data) == requests
assert get_request_at(data, 1) == requests[1]

Example 2:
requests = [
    {"user_id": 123, "action": "query", "timestamp": 1000000},
    {"user_id": 123, "action": "query", "timestamp": 1000001},
    {"user_id": 456, "action": "update", "timestamp": 1000002}
]
data = serialize_batch(requests)
```

**Constraints:**
- All requests in a batch share the same keys (schema)
- Batch size can be 1 to 100,000 requests
- Must achieve at least 30% compression compared to JSON for typical batches
- `get_request_at` should be O(1) or O(log n) without full deserialization
- Support all JSON-compatible types

**Why This Matters for the company:**
The company processes millions of API requests daily. Efficient batch serialization reduces storage costs for logging, improves cache hit rates, and speeds up data pipeline processing.

**Expected Approach:**
- Columnar storage format (store each field separately)
- Value deduplication/dictionary encoding
- Metadata for schema and offsets
- Target Complexity: O(n*m) serialize time (n requests, m fields), O(1) single-request access

**Follow-up Questions:**
1. How would you extend this to handle variable schemas within a batch?
2. What compression algorithms would you layer on top for additional space savings?
3. How would you modify this for append-only streaming scenarios?
4. Design a way to support filtering/searching within serialized batches without full deserialization.

---

### Exercise 4: Serialization-Aware LRU Cache with Persistence

**Difficulty:** Hard  
**Time:** 40-45 minutes  
**Based on:** System design pattern at the company

**Problem Statement:**

Implement an LRU cache that can persist its state to disk efficiently. The cache should:
- Store arbitrary Python objects as values
- Support standard LRU operations: `get(key)`, `put(key, value)`
- Implement `persist() -> str`: Serialize cache state to file path
- Implement `load(filepath: str)`: Restore cache state including LRU order
- Track serialization metadata (size of each value when serialized)

The cache should maintain LRU order across persist/load cycles and provide accurate memory usage based on serialized sizes.

**Input/Output Examples:**

```
Example 1:
cache = LRUCache(capacity=3)
cache.put("key1", {"data": "large_object", "size": 1000})
cache.put("key2", [1, 2, 3, 4, 5])
cache.put("key3", "simple_string")
cache.get("key1")  # Makes key1 most recent
filepath = cache.persist()
# Simulates restart
new_cache = LRUCache(capacity=3)
new_cache.load(filepath)
# LRU order preserved: key1 (most recent), key3, key2
new_cache.put("key4", "new")
# Should evict key2 (least recent)

Example 2:
cache = LRUCache(capacity=100)
# Load with 100 items
cache.persist()
# File size should be proportional to serialized content
```

**Constraints:**
- Cache capacity: 1 to 1,000,000 items
- Must preserve exact LRU order across persist/load
- `persist()` should be atomic (all or nothing)
- Support concurrent reads during persistence (bonus)
- Values can be any pickle-compatible Python object

**Why This Matters for the company:**
The company's model serving infrastructure uses extensive caching for embeddings and API responses. Persistent caches survive restarts, reducing cold-start times and improving user experience.

**Expected Approach:**
- LRU implementation with OrderedDict or custom doubly-linked list
- Efficient serialization format that includes order metadata
- File I/O considerations for atomicity
- Target Complexity: O(1) get/put, O(n) persist/load where n is cache size

**Follow-up Questions:**
1. How would you implement background persistence without blocking cache operations?
2. Design a strategy for partial cache warming during load (load most-recent items first).
3. How would you handle cache invalidation when persisted data becomes stale?
4. Extend this to support distributed LRU cache with consistent serialization across nodes.

---

### Exercise 5: Schema Evolution-Aware Data Migrator

**Difficulty:** Medium-Hard  
**Time:** 35-40 minutes  
**Based on:** Common pattern at the company

**Problem Statement:**

Build a serialization system that supports schema evolution. You need to:
- Define a schema format that describes object structure with version information
- Implement serialization that embeds schema version
- Implement deserialization that can read old versions and migrate to new schema
- Support these migrations: add field (with default), remove field, rename field, change type (with converter)

Implement:
- `define_schema(version: int, fields: Dict) -> Schema`: Create schema definition
- `serialize(obj: Dict, schema: Schema) -> bytes`: Serialize with schema
- `deserialize(data: bytes, target_schema: Schema, migrations: List[Migration]) -> Dict`: Deserialize and migrate

**Input/Output Examples:**

```
Example 1:
v1_schema = define_schema(1, {
    "name": str,
    "age": int
})
v2_schema = define_schema(2, {
    "name": str,
    "age": int,
    "email": str  # New field
})
migrations = [
    AddField("email", default="unknown@example.com", from_version=1)
]

old_data = serialize({"name": "Alice", "age": 30}, v1_schema)
new_obj = deserialize(old_data, v2_schema, migrations)
assert new_obj == {"name": "Alice", "age": 30, "email": "unknown@example.com"}

Example 2:
v1_schema = define_schema(1, {"score": int})
v2_schema = define_schema(2, {"score": float})
migrations = [
    ChangeType("score", converter=float, from_version=1)
]
old_data = serialize({"score": 100}, v1_schema)
new_obj = deserialize(old_data, v2_schema, migrations)
assert new_obj == {"score": 100.0}
```

**Constraints:**
- Support up to 100 schema versions
- Migration chain can be arbitrarily long
- Must detect incompatible migrations and raise errors
- Serialized data should include minimal schema information
- Support nested objects with independent schema versions

**Why This Matters for the company:**
The company's data models evolve rapidly (API schemas, training data formats, configuration structures). Backward-compatible serialization prevents data loss and enables smooth deployments.

**Expected Approach:**
- Version-aware serialization format
- Migration chain application in order
- Type checking and validation
- Target Complexity: O(n) serialization, O(n*m) deserialization (m migrations)

**Follow-up Questions:**
1. How would you optimize deserialization when many old-version objects need migration?
2. Design a way to validate migration chains for correctness before deployment.
3. How would you handle bidirectional migrations (downgrade support)?
4. Extend this to support structural changes (list to dict, flattening nested objects).

---

### Practice Strategy Recommendations

1. **Priority Order:** Start with Exercise 2 (most practical), then 1, 3, 4, and 5
2. **Time Management:** Practice each under strict 45-minute time limits. Focus on clean code structure first, optimization second
3. **Key Topics to Review:**
   - Python serialization modules: `pickle`, `json`, `struct`, `msgpack`
   - Data structure design for efficient serialization
   - File I/O and atomicity guarantees
   - Compression algorithms basics
   - Memory management and copy-on-write concepts

4. **Company-Specific Tips:**
   - Emphasize trade-offs in your explanations (time vs space, simplicity vs performance)
   - Consider scale from the start (million+ requests, multi-GB data)
   - Discuss production concerns: monitoring, error handling, backward compatibility
   - Be ready to pivot between different serialization formats based on requirements