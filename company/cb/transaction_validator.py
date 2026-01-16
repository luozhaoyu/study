"""
# Exercise 3: Transaction Validator
*This tests your ability to handle state transitions and fraud detection.*

### Level 1: Basic Transaction Processing
Implement a function that processes bank transactions.
- **Input:** List of operations: `["DEPOSIT", "account_id", "amount"]` or `["WITHDRAW", "account_id", "amount"]`
- **Logic:** 
  - Start all accounts at balance 0
  - DEPOSIT adds to balance
  - WITHDRAW subtracts (cannot go negative - return `"insufficient_funds"`)
- **Return:** Current balance after operation, or error message

### Level 2: Transaction Limits
Add daily spending limits and transaction history.
- **New Input:** `["SET_LIMIT", "account_id", "daily_limit"]`
- **Logic:**
  - Track total withdrawals per day per account
  - If a withdrawal would exceed the daily limit, return `"limit_exceeded"`
  - Transactions include timestamps: `["WITHDRAW", "account_id", "amount", "timestamp"]`
  - Day boundaries reset at midnight (use timestamp to determine which day)
- **Return:** Balance or appropriate error message

### Level 3: Fraud Detection - Velocity Checks
Detect suspicious patterns.
- **Rules:**
  - If more than 3 withdrawals occur within a 60-second window, flag as `"suspicious_activity"` and block the transaction
  - If total withdrawal amount exceeds 2x the daily limit within any 1-hour window, flag as `"potential_fraud"`
- **New Operation:** `["GET_STATUS", "account_id"]` returns `"active"`, `"flagged"`, or `"blocked"`
- **Logic:** Once an account is flagged, all transactions require manual approval (return `"awaiting_approval"`)

### Level 4: Multi-Currency and Exchange Rates
Support multiple currencies with real-time conversion.
- **New Format:** `["DEPOSIT", "account_id", "amount", "currency", "timestamp"]`
- **New Operation:** `["SET_RATE", "from_currency", "to_currency", "rate", "timestamp"]`
- **Logic:**
  - Each account has a base currency (set on first transaction)
  - All limits are calculated in the base currency
  - When transacting in a different currency, use the most recent exchange rate at that timestamp
  - Handle rate updates: `SET_RATE USD EUR 0.85 1000` means at timestamp 1000, 1 USD = 0.85 EUR
- **Challenge:** Efficiently look up exchange rates by timestamp (binary search or sorted structure)
"""
import bisect
from uu import Error


def convert_to_operation(raw_input):
    if len(raw_input) < 3:
        print(f"input may be invalid: {raw_input}")
        return None

    operation = {
        "action": raw_input[0],
        "account_id": raw_input[1],
        "amount": float(raw_input[2]),
    }

    if len(raw_input) >= 4:
        operation["timestamp"] = int(raw_input[3]) # timestamp as int
    return operation


class Account:
    """
    1. accounting
    2. Support daily transaction limit
    Attributes:
        history: [withdraw1, withdraw2, withdraw3]
    """
    def __init__(self, balance=0):
        self.balance = balance
        self.daily_limit = 0
        self.history = []
        self.status = "active"
        self.base_currency = None

    def set_limit(self, daily_limit):
        self.daily_limit = daily_limit
        return self.daily_limit

    def check_daily_limit(self, operation):
        """Check daily limit by counting total withdraws
        """
        end_timestamp = operation["timestamp"]
        total_daily_withdraw = operation["amount"]
        i = len(self.history) - 1
        while i >= 0 and end_timestamp - self.history[i]["timestamp"] < 3600 * 24:  # still within 1 day
            total_daily_withdraw += self.history[i]["amount"]
            if total_daily_withdraw > self.daily_limit:
                return "limit_exceeded"
            i -= 1
        return "good"

    def check_velocity(self, operation):
        result = self.check_1min_withdraw(operation)
        if result == "suspicious_activity":
            return result

        self.check_1hour_withdraw(operation)

    def check_1min_withdraw(self, operation):
        if len(self.history) <= 1:
            return "good"

        end_timestamp = operation["timestamp"]
        i = len(self.history) - 2
        if end_timestamp - self.history[i]["timestamp"] <= 60:  # within 60s window
            self.status = "blocked"
            return "suspicious_activity"
        return "good"

    def check_1hour_withdraw(self, operation):
        """Check daily limit by counting total withdraws
        """
        end_timestamp = operation["timestamp"]
        total_withdraw = operation["amount"]
        i = len(self.history) - 1
        while i >= 0 and end_timestamp - self.history[i]["timestamp"] < 3600:  # within 1 hour
            total_withdraw += self.history[i]["amount"]
            if total_withdraw > 2 * self.daily_limit:
                self.status = "flagged"
                return "potential_fraud"
            i -= 1
        return "good"

    def withdraw(self, operation):
        """
        1. check balance has enough
        2. check new withdraw limit
        2.1 detect fraud
        2.5 check manual approval requirement
        3. add to history
        4. withdraw
        """
        amount = operation["amount"]
        if self.balance < amount:
            return "insufficient_funds"

        result = self.check_daily_limit(operation)
        if result == "limit_exceeded":
            return result

        result = self.check_velocity(operation)
        if result == "suspicious_activity":  # block the transaction
            return result

        if self.need_manual_approval():
            return "awaiting_approval"

        self.history.append(operation)

        self.balance -= amount
        return self.balance

    def deposit(self, raw_input, rate_map):
        """
        check manual approval requirement
        Args:
            rate_map: external map stores currency rate
        """
        amount = None
        currency = None
        timestamp = None
        if len(raw_input) == 3:
            _, _, amount = raw_input
        if len(raw_input) == 4:
            _, _, amount, timestamp = raw_input
            timestamp = int(timestamp)
        else:
            _, _, amount, currency, timestamp = raw_input
            timestamp = int(timestamp)
        amount = float(amount)

        if self.need_manual_approval():
            return "awaiting_approval"

        if not self.base_currency:
            self.base_currency = currency

        amount = self.currency_exchange(rate_map, currency, self.base_currency, amount, timestamp)
        self.balance += amount
        return self.balance

    def currency_exchange(self, rate_map, from_currency, to_currency, amount, timestamp):
        if from_currency == to_currency:
            return amount

        conversion_pair = (from_currency, to_currency)
        if not conversion_pair in rate_map:
            raise Error(f"no rate for converting from {from_currency} to {to_currency}")

        rate_history = rate_map[conversion_pair]
        recent_rate_index = bisect.bisect_right(rate_history, timestamp, key=lambda x: x[1])
        recent_rate = rate_history[recent_rate_index-1][0]
        return amount * recent_rate

    def need_manual_approval(self):
        return self.status == "flagged" or self.status == "blocked"


class Bank:
    """
    Attributes:
        account: {
            "id_1": Account("id_1"),
            "id_2": 20,
        }
        rate_map : {
            "USD-EUR": [(rate, timestamp), (0.85, 1000), (0.9, 1005)]
        }
    """
    def __init__(self):
        self.account = {}
        self.rate_map = {}

    def process(self, raw_input):
        """
        operation = {
            "action": "DEPOSIT",
            "account_id": 123,
            "amount": 10,
        }
        """
        action = raw_input[0]
        account_id = raw_input[1]
        if not account_id in self.account:
            self.account[account_id] = Account()
        account = self.account[account_id]

        if action == "DEPOSIT":
            return account.deposit(raw_input, self.rate_map)
        elif action == "WITHDRAW":
            operation = convert_to_operation(raw_input)
            return account.withdraw(operation)
        elif action == "SET_LIMIT":
            return account.set_limit(float(raw_input[2]))
        elif action == "SET_RATE":
            return self.set_rate(raw_input)
        return "Unknown operation"

    def set_rate(self, raw_input):
        _, from_currency, to_currency, rate, timestamp = raw_input
        rate = float(rate)
        timestamp = int(timestamp)

        rate_pair = (from_currency, to_currency)
        value = (rate, timestamp)
        if not rate_pair in self.rate_map:
            self.rate_map[rate_pair] = []
        bisect.insort(self.rate_map[rate_pair], value, key=lambda x: x[1])

        reverse_pair = (to_currency, from_currency)
        reverse_value = (1 / rate, timestamp)
        if not reverse_pair in self.rate_map:
            self.rate_map[reverse_pair] = []
        bisect.insort(self.rate_map[reverse_pair], reverse_value, key=lambda x: x[1])

    def set_limit(self, daily_limit):
        account_id = operation["account_id"]
        if not account_id in self.account:
            self.account[account_id] = Account()
        return self.account[account_id].set_limit(daily_limit)

    def deposit(self, operation):
        account_id = operation["account_id"]
        if not account_id in self.account:
            self.account[account_id] = Account()
        return self.account[account_id].deposit(operation)

    def withdraw(self, operation):
        account_id = operation["account_id"]
        if not account_id in self.account:
            return "insufficient_funds"

        return self.account[account_id].withdraw(operation)


def assertEqual(a, b):
    if a != b:
        print(f"{a} != {b}")
        raise Error("not equal")

def test():
    bank = Bank()
    # level 1
    assert "insufficient_funds" == bank.process(["WITHDRAW", "jo", 1])
    assert 1 == bank.process(["DEPOSIT", "jo", 1, 0])
    assert 3 == bank.process(["DEPOSIT", "jo", 2, 0])
    assert 0 == bank.process(["WITHDRAW", "jo", 3, 0])
    assert "insufficient_funds" == bank.process(["WITHDRAW", "jo", 3, 0])

    # level 2
    assert 10 == bank.process(["SET_LIMIT", "j2", 10])
    assert 100 == bank.process(["DEPOSIT", "j2", 100, 0])
    assert 95 == bank.process(["WITHDRAW", "j2", 5, 999])
    assert 90 == bank.process(["WITHDRAW", "j2", 5, 1000])
    assert "limit_exceeded" == bank.process(["WITHDRAW", "j2", 5, 1001])

    # level 3
    assert 10 == bank.process(["SET_LIMIT", "j3", 10])
    assert 100 == bank.process(["DEPOSIT", "j3", 100, 0])
    assert 99 == bank.process(["WITHDRAW", "j3", 1, 999])
    assert 98 == bank.process(["WITHDRAW", "j3", 1, 1000])
    assert "suspicious_activity" == bank.process(["WITHDRAW", "j3", 1, 1001])
    assert "awaiting_approval" == bank.process(["WITHDRAW", "j3", 1, 99999])
    assert "awaiting_approval" == bank.process(["DEPOSIT", "j3", 1, 99999])

    assert 10 == bank.process(["SET_LIMIT", "j4", 10])
    assert 100 == bank.process(["DEPOSIT", "j4", 100, 0])
    assert 95 == bank.process(["WITHDRAW", "j4", 5, 0])
    assert 90 == bank.process(["WITHDRAW", "j4", 5, 10000])
    assert "limit_exceeded" == bank.process(["WITHDRAW", "j4", 1, 10001])

    # level 4
    bank.process(["SET_RATE", "USD", "EUR", 0.85, 10])
    bank.process(["SET_RATE", "USD", "EUR", 0.9, 15])
    bank.process(["SET_RATE", "USD", "EUR", 0.75, 5])
    assertEqual(bank.process(["DEPOSIT", "j5", 100, "USD", 0]), 100)
    print(bank.process(["DEPOSIT", "j5", 100, "EUR", 6]))
    print(bank.process(["DEPOSIT", "j5", 100, "EUR", 11]))
    print(bank.rate_map)

    print("passed test")

test()