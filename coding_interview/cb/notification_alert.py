"""
# Exercise 10: Notification & Alert System
*Tests event-driven architecture and subscription patterns.*

### Level 1: Price Alerts
Implement a price alert system.
- **Operations:**
  - `["CREATE_ALERT", "alert_id", "user_id", "asset", "condition", "target_price"]`
    - condition: `"ABOVE"` or `"BELOW"`
  - `["DELETE_ALERT", "alert_id"]`
  - `["GET_ALERTS", "user_id"]`
- **Logic:**
  - `["UPDATE_PRICE", "asset", "price"]` - check all alerts for this asset
  - If price crosses the threshold, alert triggers (return list of triggered alert_ids)
  - Triggered alerts are automatically deleted
- **Return:** For UPDATE_PRICE, return `"triggered:[alert_ids]"` or `"no_alerts"`

### Level 2: One-Time vs Recurring Alerts
Add alert persistence options.
- **New Format:** `["CREATE_ALERT", "alert_id", "user_id", "asset", "condition", "target_price", "type"]`
  - type: `"ONCE"` (delete after trigger) or `"RECURRING"` (reset after trigger)
- **Logic:**
  - Recurring alerts need cooldown: cannot trigger again within 60 seconds
  - Track last trigger timestamp per alert
  - `["UPDATE_PRICE", "asset", "price", "timestamp"]` - use timestamp for cooldown check
- **New Operation:** `["GET_ALERT_HISTORY", "user_id"]` - returns all past triggers with timestamp

### Level 3: Percentage-Based & Compound Alerts
More complex alert conditions.
- **New Conditions:**
  - `"PERCENT_CHANGE"`: triggers when price moves X% from a reference point
  - `["CREATE_ALERT", "alert_id", "user_id", "asset", "PERCENT_CHANGE", "5", "reference_price"]`
    - Triggers if price moves ±5% from reference
  - `"AND"` compound alert: triggers only when multiple conditions are met
  - `["CREATE_COMPOUND_ALERT", "alert_id", "user_id", [["BTC", "ABOVE", "50000"], ["ETH", "BELOW", "3000"]]]`
- **Logic:**
  - Compound alerts track each sub-condition independently
  - Only trigger when ALL sub-conditions are true simultaneously
  - Once triggered, all sub-conditions reset
- **New Operation:** `["GET_COMPOUND_STATUS", "alert_id"]` - returns which sub-conditions are currently satisfied

### Level 4: Delivery Channels & Rate Limiting
Add notification routing and throttling.
- **New Operations:**
  - `["SET_PREFERENCES", "user_id", "channel", "enabled", "quiet_hours_start", "quiet_hours_end"]`
    - channel: `"EMAIL"`, `"SMS"`, `"PUSH"`
    - quiet_hours: don't send notifications during this window (e.g., 22:00-08:00)
  - `["DELIVER_NOTIFICATION", "user_id", "message", "timestamp"]`
- **Logic:**
  - Respect quiet hours per channel (queue notifications for later)
  - Rate limit: max 10 notifications per hour per user per channel
  - `["GET_QUEUED_NOTIFICATIONS", "user_id"]` - returns notifications waiting for quiet hours to end
  - `["FLUSH_QUEUE", "user_id", "timestamp"]` - deliver all queued notifications if outside quiet hours
- **Priority System:**
  - `["CREATE_ALERT", ..., "priority"]` - priority 1-3
  - Priority 1 (critical): bypass quiet hours
  - Priority 2 (high): bypass rate limit
  - Priority 3 (normal): follow all rules
- **Challenge:** Efficiently check quiet hours across timezones and manage multiple queues per user/channel

10:51 
11:09
11:26
12:24
"""
from typing import *


class PriceAlert:
    """
    idea:
        update price needs to scan alert per asset
        alert per asset

    Attributes:
        alerts = {
            # asset: [alert1, alert2]
            alert_id: alert1
        }
        alert1 = {
            alert_id, user_id, asset, condition, target_price
        }
    """
    def __init__(self):
        self.alerts = {}

    def create_alert(self, alert_id, user_id, asset, condition, target_price):
        #if asset not in self.alerts:
        #    self.alerts[asset] = []
        
        alert = {
            "alert_id": alert_id,
            "user_id": user_id,
            "asset": asset,
            "condition": condition,
            "target_price": target_price,
        }
        self.alerts[alert_id] = alert

    def delete_alert(self, alert_id):
        if alert_id in self.alerts:
            del self.alerts[alert_id]

    def get_alerts(self, user_id):
        result = []
        for key, alert in self.alerts.items():
            if alert["user_id"] == user_id:
                result.append(alert)
        return result

    def update_price(self, asset, price):
        """
        1. go through each alert
        2. check whether asset price would trigger
        Returns:
            `"triggered:[alert_ids]"` or `"no_alerts"`
        """
        triggered_ids = []
        for alert_id, alert in self.alerts.items():
            if alert["asset"] != asset:
                continue
            # same asset
            if alert["condition"] == "ABOVE" and price > alert["target_price"]:
                triggered_ids.append(alert_id)
            if alert["condition"] == "BELOW" and price < alert["target_price"]:
                triggered_ids.append(alert_id)

        if not triggered_ids:
            return "no_alerts"

        # remove triggered alerts
        for triggered_id in triggered_ids:
            self.delete_alert(triggered_id)
        return triggered_ids

    def apply(self, operation):
        action = operation[0]
        if action == "CREATE_ALERT":
            return self.create_alert(operation[1], operation[2], operation[3], operation[4], operation[5])
        elif action == "DELETE_ALERT":
            return self.delete_alert(operation[1])
        elif action == "GET_ALERTS":
            return self.get_alerts(operation[1])
        elif action == "UPDATE_PRICE":
            return self.update_price(operation[1], operation[2])


class PriceAlertL2(PriceAlert):
    """
    store alert history per user_id
    Attributes:
        history = {
            user_id: [alert1, alert2]
        }
    """
    def __init__(self):
        super().__init__()
        self.history = {}

    def create_alert(self, alert_id, user_id, asset, condition, target_price, type):
        alert = {
            "alert_id": alert_id,
            "user_id": user_id,
            "asset": asset,
            "condition": condition,
            "target_price": target_price,
            "type": type,
        }
        self.alerts[alert_id] = alert

    def update_price(self, asset, price, timestamp):
        """
        1. go through each alert within the same asset
        2. check cooldown status
        3. trigger alert
        4. record past triggered with timestamp
        """
        triggered_ids = []
        for alert_id, alert in self.alerts.items():
            if alert["asset"] != asset:
                continue
            if "last_triggered" in alert and timestamp - alert["last_triggered"] < 60:  # skip in cooldown
                continue

            # same asset
            if alert["condition"] == "ABOVE" and price > alert["target_price"]:
                triggered_ids.append(alert_id)
            if alert["condition"] == "BELOW" and price < alert["target_price"]:
                triggered_ids.append(alert_id)

        if not triggered_ids:
            return "no_alerts"

        # remove triggered alerts
        for triggered_id in triggered_ids:
            alert = self.alerts[triggered_id]
            if alert["type"] == "ONCE":
                self.delete_alert(triggered_id)
            else:
                self.alerts[triggered_id]["last_triggered"] = timestamp

            user_id = alert["user_id"]
            if user_id not in self.history:
                self.history[user_id] = []
            self.history[user_id].append(timestamp)

        return triggered_ids

    def get_alert_history(self, user_id):
        return self.history[user_id]

    def apply(self, operation):
        action = operation[0]
        if action == "CREATE_ALERT":
            return self.create_alert(operation[1], operation[2], operation[3], operation[4], operation[5], operation[6])
        elif action == "UPDATE_PRICE":
            return self.update_price(operation[1], operation[2], operation[3])
        elif action == "GET_ALERT_HISTORY":
            return self.get_alert_history(operation[1])
        return super().apply(operation)

"""
### Level 3: Percentage-Based & Compound Alerts
More complex alert conditions.
- **New Conditions:**
  - `"PERCENT_CHANGE"`: triggers when price moves X% from a reference point
  - `["CREATE_ALERT", "alert_id", "user_id", "asset", "PERCENT_CHANGE", "5", "reference_price"]`
    - Triggers if price moves ±5% from reference
  - `"AND"` compound alert: triggers only when multiple conditions are met
  - `["CREATE_COMPOUND_ALERT", "alert_id", "user_id", [["BTC", "ABOVE", "50000"], ["ETH", "BELOW", "3000"]]]`
- **Logic:**
  - Compound alerts track each sub-condition independently
  - Only trigger when ALL sub-conditions are true simultaneously
  - Once triggered, all sub-conditions reset
- **New Operation:** `["GET_COMPOUND_STATUS", "alert_id"]` - returns which sub-conditions are currently satisfied
"""
class PriceAlertL3(PriceAlertL2):
    """
    compound alert has state: one update price may toggle one state
    compound_alert = {
        alert_id, user_id
        compound = [
            subcondition1
            subcondition2
        ]
    }
    subcondition = {
        asset, condition, target_price, state
    }
    """
    def __init__(self):
        super().__init__()
        self.compound_alerts = {}

    def create_alert(self, alert_id, user_id, asset, condition, percent_change, reference_price):
        alert = {
            "alert_id": alert_id,
            "user_id": user_id,
            "asset": asset,
            "condition": condition,
            "percent_change": percent_change,
            "reference_price": reference_price,
        }
        self.alerts[alert_id] = alert

    def create_compound_alert(self, alert_id, user_id, compound_list: List[Tuple[str, str, int]]):
        subconditions = []
        for compound in compound_list:
            asset, condition, target_price = compound
            subconditions.append({
                "asset": asset,
                "condition": condition,
                "target_price": target_price,
            })

        self.compound_alerts[alert_id] = {
            "alert_id": alert_id,
            "user_id": user_id,
            "subconditions": subconditions,
        }

    def get_compound_status(self, alert_id):
        alert = self.compound_alerts[alert_id]
        subconditions = alert["subconditions"]
        result = []
        for subcondition in subconditions:
            if subcondition["state"] == "satisfied":
                result.append(subcondition)
        return subconditions

    def update_price(self, asset, price, timestamp):
        """
        1. handle percent alert, filter out alert with 
        2. handle compound alert
        3. handle other alert
        """
        result = []
        result.extend(self.handle_reference_alert(asset, price, timestamp))
        result.extend(self.handle_compound_alert(asset, price, timestamp))
        result.extend(super().update_price(asset, price, timestamp))

        for alert in result:
            self.trigger_update_delete(alert, timestamp)
        return result

    def update_alert_history(self, user_id, timestamp):
        if user_id not in self.history:
            self.history[user_id] = []
        self.history[user_id].append(timestamp)

    def trigger_update_delete(self, alert, timestamp):
        """
        1. simulate trigger this alert
        2. update alert history for user
        3. delete this alert
        """
        self.update_alert_history(alert["user_id"], timestamp)
        alert_id = alert["alert_id"]
        del self.alerts[alert_id]

    def handle_reference_alert(self, asset, price, timestamp):
        """
        1. filter out reference alert by condition
        2. update alert history
        2. remove alert 
        """
        triggered_alerts = []
        for alert_id, alert in self.alerts.items():
            if alert["asset"] != asset:
                continue
            if alert["condition"] != "PERCENT_CHANGE":
                continue

            percent_change = price / alert["reference_price"] - 1
            if percent_change > alert["percent_change"] or\
                percent_change < -alert["percent_change"]:
                    triggered_alerts.append(alert)
        return triggered_alerts

    def handle_compound_alert(self, asset, price, timestamp):
        """
        1. go through each compound alert
        2. update alert history
        2. remove alert 
        """
        triggered_alerts = []
        for alert in self.compound_alerts.values():
            met_condition = 0
            for subcondition in alert["subconditions"]:
                if asset != subcondition["asset"]:  # not same asset
                    if "state" in subcondition and subcondition["state"] == "met":
                        met_condition += 1
                    continue

                condition = subcondition["condition"]
                if condition == "ABOVE":
                    if price > int(subcondition["target_price"]):
                        met_condition += 1
                        subcondition["state"] = "met"
                    else:
                        subcondition["state"] = "not_met"
                if condition == "BELOW":
                    if price < int(subcondition["target_price"]):
                        met_condition += 1
                        subcondition["state"] = "met"
                    else:
                        subcondition["state"] = "not_met"
            if met_condition == len(alert["subconditions"]):
                triggered_alerts.append(alert)

        return triggered_alerts


def assert_equal(a, b):
    if a != b:
        print(f"Error: {a} != {b}")
        raise

def test_level1():
    system = PriceAlert()
    system.create_alert("a1", "u1", "gold", "ABOVE", 10)
    print(system.get_alerts("u1"))
    assert_equal(system.update_price("gold", 12), ["a1"])
    print("passed level1 !")

test_level1()


def test_level2():
    system = PriceAlertL2()
    system.create_alert("a1", "u1", "gold", "ABOVE", 10, "RECURRING")
    system.create_alert("a2", "u1", "gold", "BELOW", 15, "ONCE")
    print(system.get_alerts("u1"))
    assert_equal(system.update_price("gold", 12, 0), ["a1", "a2"])
    assert_equal(system.update_price("gold", 12, 59), "no_alerts")
    assert_equal(system.update_price("gold", 12, 61), ["a1"])
    print(system.get_alert_history("u1"))
    print("passed level2 !")

test_level2()


def test_level3():
    system = PriceAlertL3()
    system.create_alert("a1", "u1", "BTC", "PERCENT_CHANGE", 10, 10)
    system.create_compound_alert("a2", "u1", [["BTC", "ABOVE", "50000"], ["ETH", "BELOW", "3000"]])
    print(system.get_alerts("u1"))
    assert_equal(system.update_price("BTC", 50001, 0), ["a1"])
    print(system.get_alert_history("u1"))
    assert_equal(system.update_price("ETH", 2000, 59), ["a2"])
    print(system.get_alert_history("u1"))
    print("passed level3 !")

test_level3()