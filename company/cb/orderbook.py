class OrderQueue:
    """
    OrderQueue is a convenient data structure to quickly find highest bid

    Idea:
    1. hashmap to store each order, which can be referred by order_id
    2. use a queue to store the order_id

    Data Structure:
    queue = []
    what_is_better: determine how to compare this order is attractive for "the other" side
    """
    def __init__(self, what_is_better):
        self.what_is_better = what_is_better
        self.queue = []
        self.storage = {}

    def in_order(self, x, y):
        """
        Args:
            x,y is the whole order for comparison

        Return:
            >: x>y
            =: x=y
            <: x<y
        """
        if x["price"] == y["price"] and x["order_id"] == y["order_id"]:
            return "="

        if self.what_is_better == "lower":
            if x["price"] < y["price"]:
                return "<"
            if x["price"] == y["price"] and x["order_id"] < y["order_id"]:
                return "<"
            return ">"
        else:  # higher is better
            if x["price"] > y["price"]:
                return ">"
            if x["price"] == y["price"] and x["order_id"] < y["order_id"]:
                return ">"
            return "<"

    def find_best_order(self):
        if not self.queue:
            return None
        return self.storage[self.queue[0]]

    def insert(self, operation):
        order_id = operation["order_id"]
        self.storage[order_id] = operation
        if not self.queue:
            self.queue.append(order_id)
            return

        position = self.find_position(operation)
        # print(operation, position, self.queue)
        self.queue.insert(position, order_id)

    def remove(self, order_id):
        """
        Cancel one order:
        1. binary search to find that order, remove from queue
        2. remove from hashmap
        """
        position = self.find_position(self.storage[order_id], exact_match=True)
        print(f"find {order_id} with position: {position}")
        if position == -1:  # not found
            print("error: removing non-exist item")
            return False
        else:
            self.queue.pop(position)
        del self.storage[order_id]


    def find_position(self, operation, exact_match=False):
        """
        find the right position for given operation.
        return -1 for not found
        """
        left = 0
        right = len(self.queue)
        while left < right:
            mid = (left + right) // 2
            # print(left, mid, right, self.queue, self.storage)
            # print(left, mid, right, operation)
            result = self.in_order(operation, self.storage[self.queue[mid]])
            if result == "=":
                return mid
            elif result == "<":
                right = mid
            else:
                left = mid + 1

        if exact_match:
            if self.storage[self.queue[left]] == operation:
                return left
            else:
                return -1
        else:
            return left


class OrderBook:
    def __init__(self):
        """
        storage = {
            "id_1": {
                "side": "Buy"
            }
        }
        sell = {}
        buy = {}
        """
        self.storage = {}
        self.sell_orders = OrderQueue(what_is_better="lower")
        self.buy_orders = OrderQueue(what_is_better="higher")

    def buy(self, buy_order):
        pass

    def sell(self, sell_order, is_market_order=False):
        """
        1. find the best buy order
        2. match it with current sell_order
        """
        best_buy_order = self.buy_orders.find_best_order()
        if not best_buy_order:  # no buy order found
            return sell_order["order_id"]

        while best_buy_order and sell_order["quantity"] > 0:
            if sell_order["price"] <= best_buy_order["price"]:  # price match 
                self.trade(best_buy_order, sell_order)
                if best_buy_order["quantity"] == 0 and sell_order["quantity"] > 0:
                    best_buy_order = self.buy_orders.find_best_order()
                continue

            if is_market_order:  # always trade regardless of price
                self.trade(best_buy_order, sell_order)
                if best_buy_order["quantity"] == 0 and sell_order["quantity"] > 0:
                    best_buy_order = self.buy_orders.find_best_order()
                continue

        if sell_order["quantity"] == 0:  # fully traded
            return "trade_executed"
        return sell_order["order_id"]


    def trade(self, buy_order, sell_order):
        """
        force trade on this buy and sell order.
        It would clean up if order quantity falls to 0
        """
        min_quantity = min(buy_order["quantity"], sell_order["quantity"])
        buy_order["quantity"] -= min_quantity
        sell_order["quantity"] -= min_quantity

        if buy_order["quantity"] == 0:
            self.buy_orders.remove(buy_order["order_id"])
        if sell_order["quantity"] == 0:
            self.sell_orders.remove(sell_order["order_id"])

    def clean_operation(self, operation) -> dict:
        action, order_id, side, price, quantity = operation
        return {
            "action": action,
            "order_id": order_id,
            "side": side,
            "price": float(price),
            "quantity": int(quantity),
        }

    def cancel_order(self, operation):
        if operation["side"] == "Sell":
            print("cancelling sell order")
            self.sell_orders.remove(operation["order_id"])
        else:
            print("cancelling buy order")
            self.buy_orders.remove(operation["order_id"])

    def manageOrders(self, operation):
        """
        Args:
            operation: ["ADD_ORDER", "id_1", "Buy", "100.0", "5"]
            (Action, OrderID, Side, Price, Quantity).
        """
        cleaned_operation = self.clean_operation(operation)
        action = cleaned_operation["action"]
        if action == "ADD_ORDER":
            order_id = cleaned_operation["order_id"]

            # execute action later
            if cleaned_operation["side"] == "Sell":
                self.sell_orders.insert(cleaned_operation)
                return self.sell(cleaned_operation)
            elif cleaned_operation["side"] == "Buy":
                self.buy_orders.insert(cleaned_operation)
                return self.buy(cleaned_operation)
            return order_id
        elif action == "CANCEL_ORDER":
            self.cancel_order(operation)


def test():
    buy_queue = OrderQueue(what_is_better="higher")
    buy_queue.insert({
        "order_id": "o3",
        "price": 3,
    })
    buy_queue.insert({
        "order_id": "o1",
        "price": 1,
    })
    buy_queue.insert({
        "order_id": "o5",
        "price": 5,
    })
    buy_queue.insert({
        "order_id": "o6",
        "price": 6,
    })
    buy_queue.insert({
        "order_id": "o4",
        "price": 4,
    })
    buy_queue.insert({
        "order_id": "o32",
        "price": 3,
    })
    print(buy_queue.queue)


test()

ob = OrderBook()
print(ob.manageOrders(["ADD_ORDER", "id_1", "Buy", "100.0", "1"]))
print(ob.manageOrders(["ADD_ORDER", "id_b2", "Buy", "100.0", "2"]))
print(ob.manageOrders(["ADD_ORDER", "id_2", "Sell", "100.0", "4"]))
print(ob.manageOrders(["ADD_ORDER", "id_3", "Sell", "100.0", "9"]))
print(ob.buy_orders.queue, ob.sell_orders.queue)
print(ob.buy_orders.storage, ob.sell_orders.storage)

