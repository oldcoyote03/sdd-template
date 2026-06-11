# Day Trading: Execution Specification

## Executable Actions

### Action: Initiate Trade

**Preconditions**:
- Market hours: 9:30 AM - 4:00 PM ET
- Portfolio cash > $5,000 available
- Setup matches one of the three entry model tiers (see Strategic Spec)
- Macro bias is confirmed (SPY trend identified)

**Execution Method**:
- **Manual Entry** (default): Operator sees setup alert, reviews 5-min/15-min structure, confirms tier, executes market order
- **Automated Entry** (optional, time-gated): If setup is Tier 1 with volume confirmation, Execution Agent may auto-execute with human review window

**Constraints**:
- Maximum position size: $5,000 notional
- Maximum 4 concurrent trades
- Stop loss is mandatory and in-place before entry is confirmed
- Entry must occur within 2 minutes of alert (setup is time-sensitive)

### Action: Exit Trade (Profit Target)

**Preconditions**:
- Trade is at profit target level (1:2, 1:4, or trailing stop)
- Exit order is not blocked by pending news/economic events

**Execution Method**:
- **Automatic Execution**: Exit orders are submitted immediately when price reaches target
- **Manual Override**: Operator can manually close earlier if market conditions change

**Constraints**:
- Partial exits only at predefined levels (50% / 25% / 25% split)
- No averaging down on losing trades

### Action: Exit Trade (Stop Loss)

**Preconditions**:
- Trade has moved against entry beyond stop loss level
- Stop loss is breached by intraday structure invalidation

**Execution Method**:
- **Automatic Execution**: Stop loss is always triggered automatically at market open or when price breaches

**Constraints**:
- No discretionary override of stop loss
- Max loss per trade: $500 (enforced)

### Action: Daily Position Review

**Preconditions**:
- 4:00 PM ET (market close)

**Execution Method**:
- Automatic: System queries all closed trades and collects P&L
- Manual: Operator reviews daily results and journals trades

**Constraints**:
- All positions must be closed by market close (no overnight holds)

## Approval Workflows

### Tier 1 & 2 Setups

**Approval**: None required if setup criteria are clearly met
- Execution Agent validates against Strategic Spec criteria
- Operator receives pre-execution alert with 10-second review window
- Operator can approve or skip

### Tier 3 Setups

**Approval**: Operator must explicitly approve before entry
- Setup alert marked as "Review Required"
- Operator has 30-second decision window
- If no response in 30 seconds, setup is skipped

### Large Sized Entries (> $4,000 notional)

**Approval**: Requires explicit confirmation
- Execution Agent surfaces alert with position sizing
- Operator confirms desired notional size
- Trade executes at confirmed size

## Permission & Authorization

### Time Windows

- **Active Trading Window**: 9:30 AM - 3:30 PM ET (closes 30 min before market close to avoid volatility)
- **Extended Window** (optional): Up to 4:00 PM for closing existing positions only

### Daily Permission Limits

- **Trading Permission Reset**: Each calendar day at market open (9:30 AM ET)
- **Daily Loss Limit**: Once daily loss exceeds $1,000, all trading is halted until next day
- **Max Trade Count**: Maximum 8 trades per day (prevents overtrading)

### Revocation

- Operator can pause trading by setting "TRADING_PAUSED" flag in system
- Pause is immediate; no new entries but existing positions must be closed
- Manual override via direct execution only (no automated entries)

## Error Handling & Rollback

### Execution Failure

**Scenario**: Order rejected or partially filled
- **Recovery**: Retry with market order (tighter fill than limit)
- **Escalation**: If still rejected, alert Operator; do not retry automatically

**Scenario**: System loses connection to data feed
- **Recovery**: Automatic reconnection (3 retries, 1 second apart)
- **Escalation**: If connection lost > 30 seconds, all automated entries are suspended

### Data Quality Issues

**Scenario**: Trade was entered but not journaled
- **Recovery**: Backfill journal entry with execution details + timestamp
- **Audit**: Flag entry as "recovered" so it's visible in audit trail

### Manual Exit Override

**Scenario**: Operator wants to close trade before stop/target
- **Allowed**: Yes, with manual execution
- **Logging**: Marked as "manual override" with operator note required

## Audit Trail

Every execution is logged with:
- Timestamp (to microsecond precision)
- Symbol and size
- Entry price, entry reason (setup tier + macro bias)
- Stop loss and profit targets
- Exit price and exit reason (target / stop loss / manual override)
- Operator ID (if manual)
- System logs for any retries or errors
