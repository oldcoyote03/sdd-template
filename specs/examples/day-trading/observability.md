# Day Trading: Observability Specification

## Data Sources & Feeds

### Market Data: Real-Time Quotes

**Source**: Live market data API (e.g., Bloomberg, IQFeed, etc.)
- **Symbols**: SPY, QQQ, IWM
- **Data Type**: OHLCV (Open, High, Low, Close, Volume) + bid/ask spread
- **Feed Frequency**: Real-time (tick-level)
- **Update Frequency**: Every trade (millisecond-level for charts; 1-second aggregation)
- **Retention**: 2 years rolling (intraday + daily bars)

### Technical Indicators

**Source**: Calculated from market data
- **Type**: Moving averages (20-day, 50-day, 200-day SMA), support/resistance levels (daily high/low, previous close, pivot points)
- **Update Frequency**: End of each bar (1-min, 5-min, 15-min, daily)
- **Retention**: 2 years

### News & Events

**Source**: Economic calendar API (e.g., Trading Economics, Investing.com)
- **Data Type**: Scheduled announcements, earnings dates, key economic releases
- **Update Frequency**: Daily (checked at market open and 1 hour before close)
- **Retention**: 1 year

### Trade Execution Data

**Source**: Internal trading system
- **Data Type**: Entry price, exit price, timestamp, position size, outcome (profit/loss)
- **Update Frequency**: Real-time (on each execution)
- **Retention**: 5 years

## Metrics & Signals

### Market Bias Signal

**Metric Name**: Daily Trend Confirmation
- **Calculation**: 
  - Uptrend: SPY close > 20-day MA AND HH/HL pattern
  - Downtrend: SPY close < 20-day MA AND LL/LH pattern
  - Range: SPY oscillating between resistance and support
- **Baseline**: Compare to previous 5 days (consistency check)
- **Relevance**: Determines which entry models are valid today; guides risk management

### Intraday Structure Quality

**Metric Name**: Point of Interest (POI) Formation
- **Calculation**: Micro-resistance/support (at least 3 touches) on 5-15 min timeframe + volume confirmation
- **Baseline**: Compare to typical daily POI count (usually 4-6 valid setups per day)
- **Relevance**: Identifies high-probability entry points

### Entry Setup Confidence

**Metric Name**: Setup Tier Classification
- **Calculation**: Check entry model tier (1, 2, or 3) + volume confirmation + structure alignment
- **Baseline**: Historical hit rate by tier
  - Tier 1: 65%+ win rate (backtested)
  - Tier 2: 58%+ win rate
  - Tier 3: 52%+ win rate
- **Relevance**: Determines auto-execution approval, sizing, and profit targets

### Trade Performance

**Metric Name**: Daily P&L
- **Calculation**: Sum of all closed trade profits/losses
- **Baseline**: Target is +$200-$500/day; stop if -$1,000 in a day
- **Relevance**: Portfolio-level performance metric

**Metric Name**: Win Rate (Rolling)
- **Calculation**: (Winning Trades / Total Trades) × 100 over last 20 trades
- **Baseline**: Target ≥ 55%
- **Relevance**: Determines if entry models are performing or need adjustment

**Metric Name**: Risk/Reward Ratio (Per Trade)
- **Calculation**: Average profit per winning trade / Average loss per losing trade
- **Baseline**: Target ≥ 1.5:1
- **Relevance**: Determines if profit targets and stops are calibrated correctly

## Alert Conditions

### Alert: Tier 1 Setup Identified

**Condition Logic**: 
- Intraday structure forms POI (break above micro-res OR bounce from micro-support)
- Volume is above average (>120% of 20-bar average)
- Macro bias is confirmed for this direction
- Market is NOT within 1 hour of close

**Urgency**: HIGH
**Recipients**: Trader (via notification)
**Expected Response**: Review within 5 seconds; approve/skip

### Alert: Tier 2 Setup Identified

**Condition Logic**:
- Breakout from 15-min channel with momentum
- Mean reversion to MA in established trend
- Setup tier validation confirmed

**Urgency**: MEDIUM
**Recipients**: Trader (via notification)
**Expected Response**: Review within 10 seconds; approve/skip

### Alert: Daily Loss Limit Reached

**Condition Logic**: Daily P&L ≤ -$1,000
**Urgency**: CRITICAL
**Recipients**: Trader + Risk Manager (email + SMS)
**Expected Response**: Acknowledge; trading paused until next day

### Alert: Trade Hit Stop Loss

**Condition Logic**: Position closed at stop loss level
**Urgency**: LOW (informational)
**Recipients**: Trader (logged in journal)
**Expected Response**: No action; automatic exit

### Alert: Win Rate Dropping Below Threshold

**Condition Logic**: Rolling 20-trade win rate < 52%
**Urgency**: MEDIUM (daily review trigger)
**Recipients**: Trader (review alert at market close)
**Expected Response**: Analyze failed trades; potential entry model adjustment

### Alert: Market Near Close

**Condition Logic**: 30 minutes until market close (3:30 PM ET)
**Urgency**: MEDIUM
**Recipients**: Trader
**Expected Response**: Close any open positions; prep for next day review

## Dashboards & Visualizations

### Dashboard: Live Trading

**Metrics Included**:
- Current SPY/QQQ price + trend status
- Current daily P&L (updated real-time)
- Open positions (entry price, current price, unrealized P&L, stop/target levels)
- Recent alerts (setups, stops hit, daily limit warnings)
- Setup tier queue (pending approvals)

**Refresh Cadence**: Real-time (1-second updates)
**Audience**: Trader (during trading hours)

### Dashboard: Daily Performance

**Metrics Included**:
- Daily P&L (by symbol, by trade)
- Win rate (today, rolling 20-trade)
- Trade count (completed, pending)
- Risk/reward ratio (today's trades)
- Time in trade (average holding time)

**Refresh Cadence**: End of each trade + daily at 4:00 PM
**Audience**: Trader (post-trade review)

### Dashboard: Weekly Review

**Metrics Included**:
- Weekly P&L (total and by day)
- Win rate (weekly + rolling)
- Best performing entry model (by win rate)
- Worst performing entry model (by win rate)
- Capital efficiency (profit per $1,000 deployed)

**Refresh Cadence**: Weekly (Friday 4:30 PM)
**Audience**: Trader + Risk Manager

## Data Retention & Archival

- **Real-time data**: Stored in memory + disk cache (30-day rolling)
- **Trade journal data**: Stored in database (5-year retention)
- **Market data**: Stored long-term (2-year intraday, 10-year daily)
- **Archived data**: Moved to cold storage after 6 months; accessible for historical analysis
