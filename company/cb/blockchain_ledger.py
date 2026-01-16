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

10:04
10:31 finish level 1
10:50 finish level 2
11:15 finish level 3
12:11 start level 4
12:43 finish level 4
"""
from typing import List, Tuple
from typing import *
import time

class BlockChainLedger:
    def __init__(self):
        """
        Attributes:
            ledger: [(i, data, prev_hash, hash, timestamp)], append only list
        """
        self.ledger: List[Tuple[int, str, str, float]] = []

    def _calculate_current_hash(self, ledger_index, data):
        """calculate current block hash

        It needs to refer previous hash
        """
        if ledger_index == 0:  # genesis block
            prev_hash = "0"
        else:
            prev_hash = self.ledger[ledger_index - 1][3]
        current_hash = f"block_{ledger_index}_{data}_{prev_hash}"
        return current_hash

    def add_block(self, data):
        new_index = len(self.ledger)
        prev_hash = self.ledger[new_index - 1][2] if new_index > 0 else "0"
        hash = self._calculate_current_hash(new_index, data)
        new_block = (len(self.ledger) + 1, data, prev_hash, hash, time.time())
        self.ledger.append(new_block)
        return self.ledger

    def verify(self):
        """
        1. go through each block
        2. get its prev hash, check hash
        """
        for i, block in enumerate(self.ledger):
            data = block[1]
            right_hash = self._calculate_current_hash(i, data)
            if right_hash != block[3]:  # hash doesn't match
                return "invalid"
        return "valid"

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_BLOCK":
            return self.add_block(operation[1])
        elif action == "VERIFY":
            return self.verify()

    def get_height(self):
        return len(self.ledger)


class BlockChainLedgerL2(BlockChainLedger):
    def add_block(self, data, difficulty):
        """
        1. still calculate the hash
        2. but prefix with nonce until satisfied
        """
        current_hash = self._calculate_current_hash(len(self.ledger), data)

        # count how many 0
        count_zero = 0
        while count_zero < len(current_hash) and current_hash[count_zero] == "0":
            count_zero += 1

        nonce = ""
        if count_zero < difficulty:  # need padding 0
            nonce = "0" * (difficulty - count_zero)
        current_hash = nonce + current_hash

        new_index = len(self.ledger)
        prev_hash = self.ledger[new_index - 1][2] if new_index > 0 else "0"
        new_block = (len(self.ledger) + 1, data, prev_hash, current_hash, time.time())
        self.ledger.append(new_block)
        return f"block_mined:{current_hash}:{nonce}"

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_BLOCK":
            return self.add_block(operation[1], operation[2])
        elif action == "VERIFY":
            return self.verify()


class BlockChainLedgerL3(BlockChainLedgerL2):
    """
    Attributes:
        account: {user: balance} quick check current balance
        history: {user: [transaction]} history list for each user
    """
    def __init__(self):
        super().__init__()
        self.account = {}
        self.history = {}

    def add_block(self, transactions: List[Tuple]):
        valid_transactions = []
        for transaction in transactions:
            result = self._process(transaction)
            if not result:
                continue
            valid_transactions.append(transaction)

        data = str(valid_transactions)
        return super().add_block(data, 0)


    def init_account_if_not_exist(self, user):
        if user not in self.account:
            self.account[user] = 1000
        if user not in self.history:
            self.history[user] = []

    def _process(self, transaction: Tuple):
        action, sender, receiver, amount = transaction
        amount = int(amount)
        self.init_account_if_not_exist(sender)
        self.init_account_if_not_exist(receiver)

        # validate it would not negative
        if self.account[sender] < amount:
            return False

        # proceed
        self.account[sender] -= amount
        self.account[receiver] += amount
        self.history[sender].append(transaction)
        self.history[receiver].append(transaction)
        return True

    def get_balance(self, user):
        if user not in self.account:
            return f"invalid user: {user}"
        return self.account[user]

    def get_transaction_history(self, user):
        if user not in self.history:
            return f"invalid history: {user}"
        return self.history[user]

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_BLOCK":
            return self.add_block(operation[1])
        elif action == "GET_BALANCE":
            return self.get_balance(operation[1])
        elif action == "GET_TRANSACTION_HISTORY":
            return self.get_transaction_history(operation[1])
        return super().apply(operation)


class BlockChainLedgerL4(BlockChainLedgerL3):
    """
    Idea:
        one chain becomes multiple chains
        ideally it should be a tree structure
        but the problem looks like a 2-dimension array

        for branch_id, find its corresponding ledger to serve

    Attributes:
        branch = {
            branch_id: BlockChainLedger
        }
    """
    def __init__(self):
        self.branch: Dict[str, BlockChainLedgerL3] = {}

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_BLOCK":
            return self.add_block(operation[1], operation[2])
        elif action == "GET_LONGEST_CHAIN":
            return self.get_longest_chain()
        elif action == "RESOLVE_FORK":
            return self.resolve_fork()
        elif action == "GET_BRANCHES":
            return self.get_branches()
        elif action == "GET_CHAIN_HEIGHT":
            return self.get_chain_height(operation[1])
        return super().apply(operation)

    def get_balance(self, user):
        """
        1. find the canonical chain
        2. return balance
        """
        canonical_ledger = self._find_canonical_chain()
        return canonical_ledger.get_balance(user)

    def get_transaction_history(self, user):
        canonical_ledger = self._find_canonical_chain()
        return canonical_ledger.get_transaction_history(user)

    def _find_canonical_chain(self)-> BlockChainLedgerL3:
        """
        1. find the longest chain, then discard
        """
        return self.branch[self.get_longest_chain()]

    def add_block(self, branch_id, transaction_data):
        """
        1. find the corresponding ledger first
        2. reuse the same ledger for accounting
        """
        if branch_id not in self.branch:
            self.branch[branch_id] = BlockChainLedgerL3()

        return self.branch[branch_id].add_block(transaction_data)

    def get_longest_chain(self):
        max_height = 0
        longest_chain = None
        for branch, ledger in self.branch.items():
            if ledger.get_height() > max_height:
                max_height = ledger.get_height()
                longest_chain = branch
        return longest_chain

    def resolve_fork(self):
        longest_chain = self.get_longest_chain()
        canonical_ledger = self.branch[longest_chain]
        # remove all other ledgers
        self.branch = {
            longest_chain: canonical_ledger
        }
        print(self.branch)

    def get_branches(self):
        return self.branch.keys()

    def get_chain_height(self, branch_id):
        if branch_id in self.branch:
            return self.branch[branch_id].get_height()
        return 0


def assert_equal(a, b):
    if a != b:
        print(f"{a} != {b}")
        raise

def test_level1():
    ledger = BlockChainLedger()
    print(ledger.add_block("a"))
    print(ledger.add_block("b"))
    assert_equal(ledger.verify(), "valid")
    print("level1 passed!")

test_level1()

def test_level2():
    ledger = BlockChainLedgerL2()
    print(ledger.add_block("a", 1))
    print(ledger.add_block("b", 2))
    print(ledger.add_block("c", 0))
    print("level2 passed!")

test_level2()

def test_level3():
    ledger = BlockChainLedgerL3()
    print(ledger.apply(["ADD_BLOCK", [["SEND", "alice", "bob", "50"], ["SEND", "bob", "charlie", "20"]]]))
    print(ledger.apply(["ADD_BLOCK", [["SEND", "alice", "bob", "5000"], ["SEND", "bob", "charlie", "20"]]]))
    print(ledger.apply(["GET_BALANCE", "alice"]))
    print(ledger.apply(["GET_BALANCE", "bob"]))
    print(ledger.apply(["GET_BALANCE", "charlie"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "alice"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "bob"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "charlie"]))
    print("level 3 passed!")

test_level3()


def test_level4():
    ledger = BlockChainLedgerL4()
    print(ledger.apply(["ADD_BLOCK", "b1", [["SEND", "alice", "bob", "50"]]]))
    print(ledger.apply(["ADD_BLOCK", "b2", [["SEND", "alice", "bob", "100"], ["SEND", "bob", "charlie", "20"]]]))
    print(ledger.apply(["ADD_BLOCK", "b3", [["SEND", "alice", "bob", "70"]]]))
    print(ledger.apply(["GET_BALANCE", "alice"]))
    print(ledger.apply(["GET_BALANCE", "bob"]))
    print(ledger.apply(["GET_BALANCE", "charlie"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "alice"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "bob"]))
    print(ledger.apply(["GET_TRANSACTION_HISTORY", "charlie"]))
    print(ledger.apply(["GET_LONGEST_CHAIN"]))
    print(ledger.apply(["GET_CHAIN_HEIGHT", "b3"]))
    print(ledger.apply(["RESOLVE_FORK"]))
    print(ledger.apply(["GET_CHAIN_HEIGHT", "b3"]))
    print("level 4 passed!")

test_level4()