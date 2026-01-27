"""
# Exercise 7: Wallet Address Book & Transfer System
*Simulates Coinbase's address management and withdrawal workflow.*

### Level 1: Address Book Management
Implement a wallet address book system.
- **Operations:**
  - `["ADD_ADDRESS", "user_id", "label", "address", "network"]` - add a whitelisted address
  - `["GET_ADDRESSES", "user_id"]` - returns all saved addresses for a user
  - `["DELETE_ADDRESS", "user_id", "label"]` - removes an address
- **Logic:**
  - Labels must be unique per user
  - If adding duplicate label, return `"label_exists"`
  - Network examples: "ETH", "BTC", "SOL"
- **Return:** `"success"` or appropriate error message

### Level 2: Address Validation & Cooling Period
Add security measures for new addresses.
- **New Format:** `["ADD_ADDRESS", "user_id", "label", "address", "network", "timestamp"]`
- **Logic:**
  - Validate address format per network:
    - ETH: starts with "0x", 42 characters total
    - BTC: starts with "1", "3", or "bc1", 26-35 characters
    - SOL: 32-44 characters, alphanumeric only
  - New addresses have 48-hour cooling period before they can receive transfers
  - `["GET_ADDRESS_STATUS", "user_id", "label", "timestamp"]` returns `"pending"` or `"active"`
- **Return:** `"invalid_address"` for bad format, `"added_pending"` for valid new address

### Level 3: Transfer Requests with Approval Workflow
Add transfer functionality with security rules.
- **New Operations:**
  - `["REQUEST_TRANSFER", "user_id", "label", "amount", "currency", "timestamp"]`
  - `["APPROVE_TRANSFER", "transfer_id"]`
  - `["REJECT_TRANSFER", "transfer_id"]`
  - `["GET_PENDING_TRANSFERS", "user_id"]`
- **Logic:**
  - Cannot transfer to addresses still in cooling period
  - Transfers over 1000 USD equivalent require manual approval (status = `"pending_approval"`)
  - Transfers under 1000 USD auto-approve (status = `"completed"`)
  - Track user balances per currency (start with 10000 of each)
  - If insufficient balance, return `"insufficient_funds"`
- **New Operation:** `["SET_PRICE", "currency", "usd_price", "timestamp"]` for USD conversion
- **Challenge:** Calculate USD equivalent using most recent price at transfer timestamp

### Level 4: Risk Scoring & Batch Transfers
Add fraud prevention and batch processing.
- **Risk Score Calculation:**
  - New address (< 7 days old): +30 points
  - Large transfer (> 5000 USD): +20 points
  - Multiple transfers in 1 hour: +10 points per extra transfer
  - First-time transfer to this address: +15 points
  - Score > 50: require 2FA (return `"2fa_required"`)
  - Score > 80: block transfer (return `"blocked_high_risk"`)
- **New Operations:**
  - `["BATCH_TRANSFER", "user_id", [["label1", "amount1", "currency1"], ["label2", "amount2", "currency2"]], "timestamp"]`
  - `["GET_RISK_SCORE", "user_id", "label", "amount", "currency", "timestamp"]`
  - `["VERIFY_2FA", "transfer_id", "code"]` - code must be "123456" to pass (simplified)
- **Logic:**
  - Batch transfers are atomic: if any single transfer fails, all fail
  - Calculate risk score for each transfer in batch; use highest score for the batch
  - Track transfer history per (user, address) pair for "first-time" detection
- **Return:** For batch: `"batch_completed"` with list of transfer IDs, or `"batch_failed:{reason}"`


10:07
10:18 -> 11 mins
10:34 -> 16 mins
10:47 paused -> 13 mins
11:02 resumed
11:36 -> 34 mins
"""
import bisect
from re import A


class AddressManagement:
    """
    Attributes:
        address = {
            user_id: {
                "l1": Dict{address, network}
            }
        }
    """
    def __init__(self):
        self.address = {}

    def add_address(self, user_id, label, address, network):
        if user_id not in self.address:
            self.address[user_id] = {}

        user_address = self.address[user_id]
        if label in user_address:  # label exists
            return "label_exists"

        user_address[label] = {
            "address": address,
            "network": network,
        }

    def get_addresses(self, user_id):
        if user_id not in self.address:
            return
        return self.address[user_id]

    def get_address(self, user_id, label):
        addresses = self.get_addresses(user_id)
        if addresses and label in addresses:
            return addresses[label]

    def delete_address(self, user_id, label):
        if user_id not in self.address:
            return
        
        if label not in self.address[user_id]:
            return
        del self.address[user_id][label]

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_ADDRESS":
            return self.add_address(operation[1], operation[2], operation[3], operation[4])
        elif action == "GET_ADDRESSES":
            return self.get_addresses(operation[1])
        elif action == "DELETE_ADDRESS":
            return self.delete_address(operation[1], operation[2])


class AddressManagementL2(AddressManagement):
    def add_address(self, user_id, label, address: str, network, timestamp):
        """
        1. validate address
        2. check 
        Returns:
            "invalid_address" | "added_pending"
        """
        # validation
        if network == "ETH":
            if not (address.startswith("0x") and len(address) == 42):
                return "invalid_address"
        elif network == "BTC":
            if not (len(address) >= 26 and len(address) <= 35 and (address.startswith("1") or address.startswith("3") or address.startswith("bc1"))):
                return "invalid_address"
        elif network == "SOL":
            if not (len(address) >= 32 and len(address) <= 44 and address.isalnum()):
                return "invalid_address"
        else:
            return "invalid_address"

        result = super().add_address(user_id, label, address, network)
        if result == "label_exists":
            return "label_exists"

        # need add timestamp
        self.address[user_id][label]["timestamp"] = timestamp
        return "added_pending"

    def get_address_status(self, user_id, label, timestamp):
        address_timestamp = self.address[user_id][label]["timestamp"]
        if timestamp - address_timestamp < 48 * 3600:
            return "pending"
        return "active"

    def apply(self, operation):
        action = operation[0]
        if action == "ADD_ADDRESS":
            return self.add_address(operation[1], operation[2], operation[3], operation[4], operation[5])
        elif action == "GET_ADDRESS_STATUS":
            return self.get_address_status(operation[1], operation[2], operation[3])
        return super().apply(operation)


class AddressManagementL3(AddressManagementL2):
    """
    Attributes:
        balance = {
            user_id: {
                eth: 100,
                btc: 1000,
            }
        }
        pending_transfer = {
            transfer_id: {
                user_id, label, amount, currency, timestamp
            }
        }
        price = {
            "eth": [(3, 100), (3.5, 200)]
        }
    """
    def __init__(self):
        super().__init__()
        self.balance = {}
        self.pending_transfer = {}
        self.price = {}

    def _init_user(self, user_id):
        if user_id in self.balance:
            return

        self.balance[user_id] = {
            "ETH": 10000,
            "SOL": 10000,
            "BTC": 10000,
        }

    def request_transfer(self, user_id, label, amount, currency, timestamp):
        """
        1. check balance
        2. determine usd equivalence
        3. process transfer
        """
        status = self.get_address_status(user_id, label, timestamp)
        if status == "pending":
            return "pending_address_cooling"

        self._init_user(user_id)

        if self.balance[user_id][currency] < amount:  # not enough balance
            return "insufficient_funds"

        transfer_id = f"{timestamp}-{user_id}"
        self.pending_transfer[transfer_id] = {
            "user_id": user_id,
            "label": label,
            "currency": currency,
            "amount": amount,
            "timestamp": timestamp,
        }
        usd_amount = self._get_usd_amount(currency, amount, timestamp)
        if usd_amount > 1000:  # need approval
            return "pending_approval"

        # all clear, proceed
        self._process_transfer(transfer_id)

        return "completed"

    def approve_transfer(self, transfer_id):
        """remove from pending_transfer"""
        return self._process_transfer(transfer_id)

    def reject_transfer(self, transfer_id):
        """delete this pending_transfer"""
        del self.pending_transfer[transfer_id]

    def get_pending_transfers(self, user_id):
        result = []
        for transfer in self.pending_transfer:
            if transfer["user_id"] == user_id:
                result.append(transfer)
        return result

    def _process_transfer(self, transfer_id):
        transfer = self.pending_transfer[transfer_id]
        user_id = transfer["user_id"]
        currency = transfer["currency"]
        amount = transfer["amount"]
        self.balance[user_id][currency] -= amount

        del self.pending_transfer[transfer_id]

    def _get_usd_amount(self, currency, amount, timestamp):
        """convert currency to usd amount using this timestamp

        1. find the first timestamp that <= timestamp
        """
        rates = self.price[currency]
        index = bisect.bisect_left(rates, timestamp, key=lambda x: x[1])
        if index < len(rates) and rates[index][1] <= timestamp:
            rate = rates[index][0]
        else:
            rate = rates[index-1][0]
        print(currency, timestamp, rate, amount, rate * amount)
        return rate * amount

    def set_price(self, currency, usd_price, timestamp):
        if currency not in self.price:
            self.price[currency] = []
        self.price[currency].append((usd_price, timestamp))

    def apply(self, operation):
        action = operation[0]
        if action == "REQUEST_TRANSFER":
            return self.request_transfer(operation[1], operation[2], operation[3], operation[4], operation[5])
        elif action == "APPROVE_TRANSFER":
            return self.approve_transfer(operation[1])
        elif action == "REJECT_TRANSFER":
            return self.reject_transfer(operation[1])
        return super().apply(operation)


class AddressManagementL4(AddressManagementL3):
    def __init__(self):
        super().__init__()
        self.history = {}

    def _process_transfer(self, transfer_id):
        """
        1. process the transfer directly
        2. add it to history
        history = {
            address: []
        }
        """
        transfer = self.pending_transfer[transfer_id]
        user_id = transfer["user_id"]
        address = self.get_address(user_id, transfer["label"])
        super()._process_transfer(transfer_id)

        self.update_transfer_history(address, transfer["timestamp"])

    def update_transfer_history(self, address, timestamp):
        if address not in self.history:
            self.history[address] = []
        self.history.append(timestamp)


    def generate_transfer_id(self):
        pass

    def batch_transfer(self, user_id, batch_transfers, timestamp):
        pass

    def get_risk_score(self, user_id, label, amount, currency, timestamp):
        """
        1. get address, check timestamp
        2. get amount
        3. get transfer history by check multiple transfers
        4. get transfer history: first-time
        """
        address = self.get_address(user_id, label)
        if not address:
            return 0

        address_timestamp = address["timestamp"]
        score = 0
        if timestamp - address_timestamp < 7 * 24 * 3600:
            score += 30

        # step 2
        usd_amount = self._get_usd_amount(currency, amount, timestamp)
        if usd_amount > 5000:
            score += 20

        # step 3
        transfer_history = self.history[address]
        one_hour_ago = timestamp - 3600
        if len(transfer_history) >= 2:  # multiple transfer
            if transfer_history[-1] >= one_hour_ago and transfer_history[-2] >= one_hour_ago:
                score += 10

        # step 4, first time transfer
        if len(transfer_history) == 0:
            score += 15
        return score

    def verify_2fa(self, transfer_id, code):
        pass
    


def assert_equal(a, b):
    if a != b:
        print(f"Error: {a} != {b}")
        raise

def test_level1():
    manager = AddressManagement()
    print(manager.add_address("a", "l1", "address1", "ETH"))
    assert_equal(manager.add_address("a", "l1", "address1", "ETH"), "label_exists")
    print(manager.add_address("a", "l2", "address2", "BTC"))
    print(manager.add_address("a", "l3", "address3", "SOL"))
    print(manager.delete_address("a", "l3"))

    print(manager.get_addresses("a"))
    print("passed level1 !")

test_level1()


def test_level2():
    manager = AddressManagementL2()
    chars32 = "abcdefgh" * 4
    print(manager.add_address("a", "l1", f"3{chars32}00", "BTC", 0))
    assert_equal(manager.add_address("a", "l1", f"3{chars32}00", "BTC", 0), "label_exists")
    assert_equal(manager.add_address("a", "l2", "address1", "ETH", 0), "invalid_address")
    print(manager.get_addresses("a"))
    assert_equal(manager.get_address_status("a", "l1", 10), "pending")
    assert_equal(manager.get_address_status("a", "l1", 10 + 48 * 3600), "active")
    print("passed level2 !")

test_level2()


def test_level3():
    manager = AddressManagementL3()
    chars32 = "abcdefgh" * 4
    print(manager.add_address("a", "l1", f"3{chars32}00", "BTC", 0))
    assert_equal(manager.add_address("a", "l1", f"3{chars32}00", "BTC", 0), "label_exists")
    assert_equal(manager.add_address("a", "l2", "address1", "ETH", 0), "invalid_address")
    print(manager.set_price("BTC", 3, 0))
    print(manager.set_price("BTC", 4, 9999999))
    print(manager.set_price("BTC", 5, 999999999))
    assert_equal(manager.request_transfer("a", "l1", 333, "BTC", 0), "pending_address_cooling")
    assert_equal(manager.request_transfer("a", "l1", 333, "BTC", 1 + 48 * 3600), "completed")
    assert_equal(manager.request_transfer("a", "l1", 334, "BTC", 2 + 48 * 3600), "pending_approval")
    print(manager.pending_transfer)
    manager.approve_transfer(f"{2 + 48 * 3600}-a")
    print(manager.balance)
    print("passed level3 !")

test_level3()