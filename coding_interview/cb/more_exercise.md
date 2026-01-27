# Exercise 8: Portfolio Tracker with P&L
*Core Coinbase functionality - tracking holdings and performance.*

### Level 1: Track Holdings
Build a portfolio tracker.
- **Operations:**
  - `["BUY", "user_id", "asset", "quantity", "price"]`
  - `["SELL", "user_id", "asset", "quantity", "price"]`
  - `["GET_HOLDINGS", "user_id"]` - returns map of asset -> quantity
- **Logic:**
  - Cannot sell more than owned (return `"insufficient_holdings"`)
  - Track total quantity per asset per user
- **Return:** For BUY/SELL, return updated quantity of that asset

### Level 2: Cost Basis Tracking (FIFO)
Calculate cost basis using First-In-First-Out.
- **Logic:**
  - Track each purchase as a separate "lot" with quantity and price
  - When selling, consume oldest lots first
  - **Example:**
    - BUY 10 BTC @ $100
    - BUY 5 BTC @ $150
    - SELL 12 BTC @ $200
    - Cost basis = (10 × $100) + (2 × $150) = $1300
    - Proceeds = 12 × $200 = $2400
    - Realized P&L = $1100
- **New Operations:**
  - `["GET_COST_BASIS", "user_id", "asset"]` - returns average cost of remaining holdings
  - `["GET_REALIZED_PNL", "user_id"]` - returns total realized profit/loss across all sales
- **Data Structure:** Queue of lots per (user, asset)

### Level 3: Unrealized P&L with Live Prices
Add market prices and unrealized gains.
- **New Operations:**
  - `["SET_MARKET_PRICE", "asset", "price", "timestamp"]`
  - `["GET_PORTFOLIO_VALUE", "user_id", "timestamp"]` - current market value of all holdings
  - `["GET_UNREALIZED_PNL", "user_id", "timestamp"]` - difference between market value and cost basis
- **Logic:**
  - Use most recent price at or before the given timestamp
  - **New Metric:** `["GET_TOTAL_PNL", "user_id", "timestamp"]` = realized + unrealized
- **Edge Cases:**
  - If no price exists for an asset, use the last purchase price
  - Handle assets with zero holdings (should not appear in portfolio)

### Level 4: Tax Lot Optimization & Reporting
Add tax optimization strategies and reporting.
- **New Selling Modes:**
  - `["SELL", "user_id", "asset", "quantity", "price", "method"]`
  - Methods: `"FIFO"` (default), `"LIFO"` (Last-In-First-Out), `"HIFO"` (Highest-In-First-Out)
  - HIFO sells highest cost basis first (minimizes taxable gain)
- **New Operations:**
  - `["GET_TAX_LOTS", "user_id", "asset"]` - returns list of all lots with quantity, cost, and purchase date
  - `["GENERATE_TAX_REPORT", "user_id", "start_timestamp", "end_timestamp"]` - returns:
    - Total proceeds from sales in period
    - Total cost basis of sold assets
    - Net realized gain/loss
    - Short-term vs long-term gains (held > 365 days = long-term)
  - `["SIMULATE_SELL", "user_id", "asset", "quantity", "method", "timestamp"]` - preview P&L without executing
- **Logic:**
  - Track purchase timestamp for each lot
  - Long-term gains are taxed differently (just categorize, don't calculate tax)
- **Challenge:** HIFO requires sorting lots by price; maintain both queue (for FIFO) and sorted structure (for HIFO)

---

# Exercise 9: Order Matching Engine v2
*More advanced trading system with order types.*

### Level 1: Limit Order Book
Implement a basic order book.
- **Operations:**
  - `["PLACE_ORDER", "order_id", "side", "price", "quantity"]` - side is "BUY" or "SELL"
  - `["CANCEL_ORDER", "order_id"]`
  - `["GET_ORDER_BOOK"]` - returns current bids and asks
- **Logic:**
  - BUY orders sorted by price descending (highest first)
  - SELL orders sorted by price ascending (lowest first)
  - No matching in Level 1 - just maintain the book
- **Return:** Order book state after each operation

### Level 2: Order Matching
Add matching logic when orders cross.
- **Logic:**
  - A BUY order at price P matches any SELL order at price ≤ P
  - A SELL order at price P matches any BUY order at price ≥ P
  - Execute at the **resting order's price** (the one already in the book)
  - Partial fills: if BUY 10 @ $100 matches SELL 4 @ $99, execute 4 units @ $99, BUY order remains with 6 units
- **Price-Time Priority:**
  - Best price first
  - If same price, earliest order first
- **New Operation:** `["GET_TRADES"]` - returns list of all executed trades with price, quantity, buy_order_id, sell_order_id

### Level 3: Advanced Order Types
Add market orders and stop orders.
- **New Order Types:**
  - `["PLACE_ORDER", "order_id", "side", "MARKET", "quantity"]` - execute immediately at best available price
  - `["PLACE_ORDER", "order_id", "side", "STOP", "trigger_price", "quantity"]` - becomes market order when price reaches trigger
- **Logic:**
  - Market orders sweep the book until filled or book is empty
  - If market order cannot be fully filled, remaining quantity is cancelled (return `"partial_fill:{filled_qty}"`)
  - Stop orders are dormant until triggered
  - `["UPDATE_MARKET_PRICE", "price"]` - triggers stop orders if conditions met
    - SELL stop triggers when market price ≤ trigger price
    - BUY stop triggers when market price ≥ trigger price
- **New Operation:** `["GET_PENDING_STOPS"]` - returns all stop orders not yet triggered

### Level 4: Iceberg Orders & Self-Trade Prevention
Add sophisticated order features.
- **Iceberg Orders:**
  - `["PLACE_ORDER", "order_id", "side", "price", "total_quantity", "visible_quantity"]`
  - Only `visible_quantity` appears in order book
  - When visible portion fills, automatically replenish from hidden quantity
  - Example: Iceberg BUY 100 @ $50 with visible=10: shows 10 units, when matched, refills to 10 until all 100 are used
- **Self-Trade Prevention:**
  - `["PLACE_ORDER", "order_id", "user_id", "side", "price", "quantity"]` - orders now have user_id
  - If a user's BUY would match their own SELL, cancel the incoming order (return `"self_trade_prevented"`)
- **New Operations:**
  - `["GET_USER_ORDERS", "user_id"]` - returns all active orders for a user
  - `["CANCEL_ALL", "user_id"]` - cancels all orders for a user
  - `["GET_ORDER_DETAILS", "order_id"]` - for iceberg orders, returns both visible and total remaining quantity
- **Challenge:** Iceberg replenishment must maintain time priority (each replenishment gets new timestamp for priority)
