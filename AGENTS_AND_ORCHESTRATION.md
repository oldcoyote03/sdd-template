# Agent & Orchestration Guide

This document provides guidance for developers building the Intelligence and Orchestration layers that will consume and act on the specifications.

## Role-Based Agents

Each core feature has a corresponding agent that interprets and acts on that feature's specification:

### Strategy Agent

**Purpose**: Maintain, refine, and explain strategic direction.

**Inputs**:
- Strategic spec (market structures, entry models, risk rules)
- Review feedback from previous review cycles

**Responsibilities**:
- Explain the current strategy to other agents and humans
- Identify patterns in feedback that suggest strategy refinement
- Propose updates to Strategic spec based on analysis results
- Maintain consistency between Strategic spec and other specs

**Example Interactions**:
- *From Review Agent*: "Tier 1 win rate dropped to 48%. Recommend investigating entry model."
- *To Execution Agent*: "Current market bias is uptrend; prioritize long entries."
- *To Observability Agent*: "Focus monitoring on these market structures."

### Execution Agent

**Purpose**: Decide when and how to execute actions in accordance with specs.

**Inputs**:
- Execution spec (what actions are allowed, when, with what approvals)
- Strategic spec (context for decisions)
- Collaboration spec (who needs to approve)
- Observability signals (when setup conditions are met)

**Responsibilities**:
- Evaluate if conditions are met for execution
- Request approvals when required
- Execute actions (or log if waiting for approval)
- Log execution details for audit trail

**Example Interactions**:
- *From Observability Agent*: "Tier 1 setup detected: SPY breaking above 445.50. Market bias: uptrend. Volume confirmed."
- *To Collaboration Agent*: "Setup alert; Trader approval needed within 10 seconds."
- *To Orchestration*: "Execute trade: 1x SPY at market, size $5,000. Stop: 445.20. Target: 446.50."

### Observability Agent

**Purpose**: Monitor data and generate alerts based on specifications.

**Inputs**:
- Observability spec (data sources, metrics, alert conditions)
- Live data feeds (market data, operational metrics, events)

**Responsibilities**:
- Ingest and process data from specified sources
- Calculate metrics
- Evaluate alert conditions continuously
- Route alerts to appropriate recipients
- Maintain dashboards and visualizations

**Example Interactions**:
- *Continuously ingests*: Live market data (SPY quotes, volume, etc.)
- *Every minute*: Recalculate setup quality signals, market bias
- *When condition met*: "Daily loss limit approaching ($800 of $1,000). Alert: Risk Manager."
- *Every 10 seconds*: Publish live dashboard (current P&L, open positions, recent alerts)

### Collaboration Agent

**Purpose**: Route information and enforce approval workflows.

**Inputs**:
- Collaboration spec (roles, visibility, approval workflows, communication channels)
- Requests from other agents (alerts to send, approvals to request)

**Responsibilities**:
- Determine who needs to see each piece of information (based on role visibility rules)
- Enforce approval workflows (wait for approval, escalate if timeout)
- Route notifications to appropriate channels
- Maintain audit log of who approved what, when

**Example Interactions**:
- *From Execution Agent*: "Need approval for Tier 3 setup. Trader role required."
- *To Trader*: "Tier 3 setup alert: Mean reversion to 20-day MA. Approve? (Y/N) [Expires in 30 sec]"
- *From Trader*: "Approved"
- *To Execution Agent*: "Approval granted from Trader at 14:32:15. Proceed."

### Review Agent

**Purpose**: Analyze outcomes and feed insights back into strategy refinement.

**Inputs**:
- Review spec (review cadences, analysis frameworks, feedback mechanisms)
- Trade/outcome data (journal entries, logs, performance metrics)
- Previous strategy specs (for comparison)

**Responsibilities**:
- Trigger reviews at specified cadences
- Perform specified analyses (win rate, setup effectiveness, risk calibration)
- Identify patterns and insights
- Recommend feedback (what specs should change)
- Generate reports

**Example Interactions**:
- *Every Friday 4:00 PM*: "Weekly review triggered."
- *Analyzes*: "Tier 1 setups: 10 trades, 7 winners (70% win rate). Tier 2: 5 trades, 3 winners (60%). Tier 3: 2 trades, 1 winner (50%)."
- *Reports*: "Tier 1 performing well (vs. 65% backtest). Recommend backtest Tier 2 filter tightening."
- *Logs*: "Feedback to Strategy Agent: Consider tightening Tier 2 entry model."

## Orchestration Patterns

### Event-Driven Execution

The system should be **event-driven**, not continuously polling:

**Event Sources**:
1. Market data updates (new price, volume, etc.) → trigger Observability Agent
2. Alert conditions met → trigger Collaboration Agent → trigger Execution Agent
3. Approval received → trigger Execution Agent
4. Scheduled triggers (daily close, weekly review) → trigger Review Agent
5. User actions (manual trade, override) → trigger Execution Agent with logging

**Flow Example**:
```
9:45 AM: Market data received (SPY 445.60)
  ↓ Observability Agent calculates indicators
  ↓ Condition met: Break above 445.50 resistance with volume
  ↓ Generate alert event
  ↓ Collaboration Agent routes to Trader
  ↓ Send notification: "Tier 1 setup detected"
  ↓ Wait for Trader approval (10-second window)
  ↓ Trader responds: "Approve"
  ↓ Execution Agent proceeds
  ↓ Execute trade: 1x SPY at market
  ↓ Observability Agent logs trade data
  ↓ Orchestration layer logs: "Trade executed at 9:45:32 AM"
```

### Approval Workflow Pattern

```
Execution Agent detects valid setup
  ↓
IF approval required (Execution spec)
  ↓
  Collaboration Agent identifies approver (role)
  ↓
  Route approval request to approver
  ↓
  Wait for approval OR timeout
  ↓
  IF approved → Execution Agent proceeds
  IF timeout → Skip this setup (log as skipped)
ELSE → Execution Agent proceeds immediately
```

### Feedback Loop Pattern

```
END OF REVIEW CYCLE:
  ↓
Review Agent analyzes outcomes
  ↓
Generate insights (patterns, thresholds exceeded, recommendations)
  ↓
IF feedback applies to Strategic spec
  ↓
  Propose spec update (with backtest validation if needed)
  ↓
  Log proposed change and rationale
  ↓
NEXT CYCLE:
  ↓
Strategy Agent reads updated spec
  ↓
Execution uses new spec rules
```

## Integration Points

### Data Ingestion

Observability Agent must connect to:
- **Market data APIs** (quotes, volumes, bars)
- **Internal logs** (trade execution logs, operational metrics)
- **External data** (economic calendar, news, sentiment)

**Pattern**: Agents should subscribe to data feeds; data updates trigger agent logic rather than agents polling.

### Execution APIs

Execution Agent must call:
- **Order submission APIs** (brokers, trading platforms)
- **Order status APIs** (check if filled, pending, etc.)
- **Portfolio APIs** (get current positions, cash available)

**Pattern**: Execution Agent logs every API call and response for audit trail.

### Logging & Persistence

Orchestration layer must log:
- **Decision logs**: What agents decided and why
- **Action logs**: What actions were executed, when, by whom
- **Outcome logs**: Results of actions (filled orders, P&L, etc.)
- **Audit trail**: Who approved what, when, what changed

**Storage**: 
- Real-time: In-memory for fast access
- Persistent: Repository (versioned) or database (queryable)
- Archive: Cold storage after retention period

### Spec Access

All agents read specs from:
- **Repository** (authoritative source)
- **Cache** (local copy for fast access, invalidated when spec updates)

**Pattern**: Specs are immutable inputs to agents; agents don't modify specs. Only review cycle → human decision → repo commit updates specs.

## Example: Building an Entry Execution Orchestration

Here's a concrete walkthrough of how agents coordinate:

### Setup: Day Trading, Tier 1 Entry

**Specs in repository**:
- Strategic: "Tier 1 setup = break above micro-resistance + volume confirmation"
- Execution: "Tier 1 entries auto-execute after Trader review (10-sec window)"
- Observability: "Monitor SPY 5-min and 15-min structure; alert on POI breaks with volume"
- Collaboration: "Trader role has veto on any setup"

### Orchestration Flow

```
9:00 AM: Orchestration subscribes to market data for SPY

9:45 AM: Tick arrives: SPY = 445.65
  ↓
  Observability Agent triggered:
    - Pulls Strategic spec (what's a Tier 1 setup?)
    - Compares 445.65 to micro-resistance level 445.50
    - Checks volume (recent vol 2.3M vs 20-bar avg 2.1M = 109% -> not enough)
    - No alert yet (volume confirmation missing)

9:46 AM: Tick arrives: SPY = 445.68, Volume spike to 5.2M
  ↓
  Observability Agent triggered:
    - Checks break again (445.68 > 445.50 ✓)
    - Checks volume (5.2M vs 20-bar avg 2.1M = 247% ✓)
    - Checks macro bias (SPY in uptrend per daily spec ✓)
    - CONDITION MET: Generate alert event
    
  ↓ Alert routed to Collaboration Agent:
    - Pulls Collaboration spec (Tier 1 setups: who approves?)
    - Routes to Trader role
    - Creates notification: 
      "SPY Tier 1 setup: Break 445.50 with volume. 
       Macro: Uptrend. Approve? Y/N [expires 9:46:10]"
    - Sends via email, SMS, in-app
    
  ↓ Trader sees alert, approves: "Y"
    - Collaboration Agent logs: "Trader approved at 9:46:05"
    - Execution Agent triggered with approval status
    
  ↓ Execution Agent:
    - Pulls Execution spec (what's the entry process?)
    - Validates: portfolio cash > $5,000? ✓
    - Validates: not exceeding 4 concurrent positions? ✓
    - Validates: time window 9:30-15:30? ✓
    - Validates: stop loss calculated? (445.50 - 0.2% = 445.40) ✓
    - Validates: targets set? (1:2 = 445.80, 1:4 = 446.00) ✓
    - READY TO EXECUTE
    
  ↓ Execution calls broker API:
    - Submit market order: BUY 112 shares SPY at market
      (position size: $5,000 ÷ 445.68 ≈ 112 shares)
    - Sets stop loss order: SELL 112 shares at 445.40 (stop)
    - Sets profit target orders: 
      SELL 56 shares at 445.80 (1:2 target)
      SELL 28 shares at 446.00 (1:4 target)
      SELL 28 shares TRAILING STOP (5-min trail)
    
  ↓ Broker confirms fills:
    - Entry filled: 112 shares @ 445.67
    - Stop order pending
    - Target orders pending
    
  ↓ Orchestration logs trade execution:
    - Entry: 112 SPY @ 445.67 at 9:46:06
    - Setup: Tier 1, break above resistance
    - Macro: Uptrend
    - Stop: 445.40, Target 1:2 = 445.80
    - Logging includes: price, size, stop, targets, timestamp, Trader approval

9:47 AM: Tick arrives: SPY = 445.90
  ↓
  Observability Agent:
    - Recognizes open trade at 445.67
    - Monitors 1:2 target level (445.80)
    - Profit at +$16/share
    
10:00 AM: Tick arrives: SPY = 445.82
  ↓
  Observability Agent:
    - Detects: price crossed 1:2 target (445.80)
    - Triggers partial exit order: SELL 56 shares @ market
    - Broker fills: 56 shares @ 445.82 (realizes +$17/share for partial)
    - Trade now: 56 shares remaining with trailing stop
    
  ↓ Orchestration logs:
    - Partial exit: 56 shares @ 445.82 at 10:00:15
    - Exit reason: 1:2 profit target
    - P&L: +$17 realized
    
10:15 AM: Tick arrives: SPY = 446.50
  ↓
  Observability Agent:
    - Detects: price moved to +$83/share on remaining position
    - Still holding 56 shares with trailing stop
    
14:32 PM: Tick arrives: SPY = 445.60 (pullback)
  ↓
  Observability Agent:
    - Detects: price 5-min bars starting to reverse
    - Triggers trailing stop exit (trail breached)
    - SELL 28 shares @ 445.61
    
  ↓ Orchestration logs:
    - Partial exit: 28 shares @ 445.61
    - Exit reason: 1:4 profit target (previously hit)
    - Remaining: 28 shares (trailing stop)
    
16:00 PM: Market close
  ↓
  Orchestration finalizes trade:
    - Exit all remaining: 28 shares @ 445.55 (market close)
    - Journaling agent creates trade entry:
      "Entry: 445.67 | Exit: 445.66 avg | Size: 112 | P&L: +$107 total"
    
  ↓ Review Agent triggered at market close:
    - Logs this trade as: Tier 1 ✓, Win ✓, Setup quality: Good ✓
    - Adds to daily stats
```

This walkthrough shows:
- How specs guide each agent's decisions
- How agents coordinate through events
- How audit trail captures everything
- How results feed back to reviews

## Tips for Implementation

1. **Keep agents stateless**: Specs are the state; agents should be idempotent
2. **Log everything**: Every decision point, every external call, every outcome
3. **Test with paper trading first**: Before real money, validate agents on historical/simulated data
4. **Make specs version-controlled**: Every update to a spec gets a commit with rationale
5. **Design for observability**: You need to understand why agents made decisions
6. **Escalate intelligently**: When agents are uncertain, escalate to human with full context
7. **Close feedback loops**: Review agents analyze outcomes; learnings update specs; cycle continues

