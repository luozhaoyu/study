"""
# Exercise 5: Blockchain Ledger
*Highly relevant to Coinbase - tests linked structures and validation.*

### Level 1: Linear Transaction Chain
Build a simple blockchain.
- **Operations:** `["ADD_BLOCK", "transaction_data"]`
- **Logic:**
  - Each block has: index, data, previous_block_hash, timestamp
  - Hash = simple string like `"block_{index}_{data}_{prev_hash}"`
  - Genesis block (index 0) has previous_hash = `"0"`
- **Return:** The hash of the newly added block
- **New Operation:** `["VERIFY"]` returns `"valid"` if the chain is intact

### Level 2: Mining with Proof-of-Work
Add difficulty requirement.
- **New Format:** `["ADD_BLOCK", "transaction_data", "difficulty"]`
- **Logic:**
  - Hash must start with `difficulty` number of zeros
  - Add a `nonce` field that increments until hash satisfies the requirement
  - Example: difficulty=2 means hash must start with "00"
  - Simulate mining: increment nonce from 0 until condition met
- **Return:** `"block_mined:{hash}:{nonce_used}"`
- **Optimization:** For Level 2, brute force is fine

### Level 3: Transaction Validation and Balances
Blocks now contain multiple transactions.
- **New Format:** `["ADD_BLOCK", [["SEND", "alice", "bob", "50"], ["SEND", "bob", "charlie", "20"]]]`
- **Logic:**
  - Track balances for all users
  - Each user starts with 1000 coins
  - Reject blocks where any transaction would result in negative balance
  - Hash calculation now includes ALL transactions in the block
- **New Operations:**
  - `["GET_BALANCE", "user"]` returns current balance
  - `["GET_TRANSACTION_HISTORY", "user"]` returns all transactions involving that user
- **Validation:** `VERIFY` now also checks that no transaction violated balance constraints

### Level 4: Forking and Consensus
Handle competing chains (blockchain splits).
- **New Concept:** Multiple miners can add blocks simultaneously
- **New Format:** `["ADD_BLOCK", "branch_id", "transaction_data"]`
- **Logic:**
  - Support multiple branch chains from the same parent block
  - `["GET_LONGEST_CHAIN"]` returns the branch with most blocks (consensus rule)
  - `["RESOLVE_FORK"]` adopts the longest chain as canonical and discards others
  - All balance queries use the canonical chain
- **New Operations:**
  - `["GET_BRANCHES"]` lists all active branches
  - `["GET_CHAIN_HEIGHT", "branch_id"]` returns number of blocks
- **Challenge:** Use a tree structure or graph to represent branches, with efficient traversal to find longest path
"""