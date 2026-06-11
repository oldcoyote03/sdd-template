# Five Core Features

This document explains the five core features and how they interconnect.

---

## Overview

Every operational system built with this template consists of five specifications:

1. **Strategic**: What you're trying to accomplish and why
2. **Execution**: What actions you can take, when, and with what approval
3. **Observability**: What you monitor and how you alert
4. **Collaboration**: Who is involved and what visibility/authority they have
5. **Review**: How you analyze outcomes and improve

Each feature has a corresponding agent that interprets that feature's spec and coordinates with other agents.

---

## 1. Strategic Spec

**Purpose**: Define decision rules, frameworks, priorities, and rationale.

**Content**:
- Objectives and success criteria
- Decision frameworks and rules
- Priorities and constraints
- Underlying reasoning/principles

**Example (Trading)**:
```
Objective: 2% monthly return with max 5% monthly drawdown
Decision Rule: Trade only market uptrends (daily close > 20-EMA)
Rule: Tier 1 setups = micro-resistance break + volume confirmation
Rule: Tier 2 setups = trendline bounce + volume
Constraint: Max 4 concurrent positions
Constraint: Daily loss limit: 1% of account
```

**Agent**: Strategy Agent reads and refines this spec

**Output to other agents**:
- Execution Agent: "Use these market structures and entry criteria"
- Observability Agent: "Monitor for these patterns"
- Review Agent: "Evaluate outcomes against these objectives"

---

## 2. Execution Spec

**Purpose**: Define what actions can be taken, how, when, and with what approvals.

**Content**:
- Executable actions (specific, unambiguous)
- Preconditions for each action
- Approval workflows (who must sign off)
- Permission/authorization rules (timing, amounts, frequency limits)
- Error handling and rollback procedures

**Example (Trading)**:
```
Action: Enter tier 1 setup trade
Preconditions:
  - Setup detected by Observability Agent
  - Trader approval obtained (or auto-execute if within limits)
  - Portfolio has cash available
  - Daily loss limit not breached
Execution:
  - Buy [calculated size] at market
  - Set stop loss [1% below entry]
  - Set target [1:2 ratio]
Approval: Trader role (10-sec window for tier 1)
Limits: Max 4 concurrent positions
```

**Agent**: Execution Agent reads and acts on this spec

**Inputs from other agents**:
- Observability Agent: "Setup condition met"
- Collaboration Agent: "Approval received from Trader"
- Strategy Agent: "Market bias is uptrend (use tier 1 criteria)"

**Output**:
- Action is executed (or logged as pending approval)

---

## 3. Observability Spec

**Purpose**: Define what to monitor, what signals matter, and how to alert.

**Content**:
- Data sources and feed specifications
- Metrics and KPIs to calculate
- Alert thresholds and conditions
- Dashboards and visualizations
- Alert routing (who sees what)

**Example (Trading)**:
```
Data Source: Real-time market data (SPY, QQQ, IWM)
Metric: Daily return (P&L / initial capital)
Metric: Win rate (winners / total trades)
Metric: Drawdown (peak-to-trough)

Alert: Tier 1 setup detected (break + volume)
  Condition: Price > [resistance] AND volume > [20-bar avg * 1.2]
  Route to: Collaboration Agent for trader approval
  
Alert: Daily loss limit approaching
  Condition: Daily loss > 0.8% of account
  Route to: Risk Manager
  
Dashboard: Live trading dashboard
  Shows: Current positions, open orders, alerts, daily P&L
  Refresh: Every 10 seconds
```

**Agent**: Observability Agent reads this spec and continuously monitors

**Output**:
- Metrics calculated
- Alerts generated and routed
- Dashboards published

---

## 4. Collaboration Spec

**Purpose**: Define who is involved, what visibility they have, what approval they must give.

**Content**:
- Roles and responsibilities
- Information visibility rules (who sees what data/alerts)
- Approval workflows (who must sign off on what, with what timing)
- Communication channels (email, Slack, webhook, etc.)
- Escalation paths

**Example (Trading)**:
```
Role: Trader
  Visibility: Live dashboards, setup alerts, active positions
  Responsibilities: Approve/reject tier 1 setups
  Approval Authority: Can veto any tier 1 setup (10-sec window)
  Escalation: If unavailable > 5 min, escalate to Risk Manager

Role: Risk Manager
  Visibility: Daily loss limit, drawdown, portfolio risk metrics
  Responsibilities: Monitor risk thresholds, halt trading if needed
  Approval Authority: Can freeze all trading if daily loss limit breached
  
Role: Analyst
  Visibility: End-of-day trades, weekly/monthly reviews
  Responsibilities: Review trades, identify patterns, recommend spec updates
```

**Agent**: Collaboration Agent reads this spec and enforces workflows

**Inputs from other agents**:
- Execution Agent: "Need approval for action X"
- Observability Agent: "Alert to send to role Y"

**Output**:
- Approvals requested and tracked
- Alerts routed to correct roles
- Audit log of who approved what, when

---

## 5. Review Spec

**Purpose**: Define how outcomes are analyzed, lessons learned, and improvements identified.

**Content**:
- Review cadences and triggers (daily, weekly, monthly, etc.)
- Analysis frameworks (what to measure, compare, evaluate)
- Feedback mechanisms (how insights loop back to strategy/execution)
- Optimization priorities
- Report formats

**Example (Trading)**:
```
Cadence: Daily at market close
  Analysis:
    - Win rate by setup type (Tier 1, 2, 3)
    - Average R-multiple per setup
    - Max consecutive losses
    - Daily P&L against daily objective
  Output: Short email with key metrics
  
Cadence: Weekly on Friday 4:00 PM
  Analysis:
    - Win rate trends across week
    - Most profitable setup type
    - Risk metrics (max drawdown, daily loss limit breaches)
    - Market conditions this week (uptrend, range, downtrend)
  Feedback:
    - If Tier 1 underperforming: investigate entry model
    - If max drawdown > 3%: tighten stop losses
    - If consistent setup type winner: increase size on that type
  Output: Detailed report + recommendations to Strategy Agent

Cadence: Monthly
  Analysis:
    - Monthly return vs. objective
    - Largest win, largest loss
    - Best/worst market condition
    - Biggest learnings
  Feedback: Update Strategic spec with new rules/insights
  Output: Full report with spec change recommendations
```

**Agent**: Review Agent reads this spec and triggers reviews at cadences

**Inputs**:
- Outcome data (trades, decisions, metrics)
- Previous specs (for comparison)

**Output**:
- Review reports
- Feedback recommendations to Strategy Agent
- Proposed spec updates with rationale

---

## How They Interconnect

```
Strategic Spec
  ↓ (Decision rules to apply)
  ↓
Execution Spec + Observability Spec
  ↓ (When conditions met, execute if approved)
  ↓
Collaboration Spec
  ↓ (Route approval requests)
  ↓
Execute action → Log outcome
  ↓
Review Spec
  ↓ (At cadence, analyze outcomes)
  ↓
Feedback loops back to Strategic Spec
  ↓ (Learn, adapt, improve)
  ↓
Cycle repeats
```

### Example Flow (Trading)

```
1. Strategic: "Only trade tier 1 setups in uptrends"
2. Observability: Monitoring for "tier 1 setup detected"
3. Alert triggers: "SPY tier 1 setup, uptrend confirmed"
4. Collaboration: Routes alert to Trader for approval
5. Trader approves
6. Execution: Executes trade per spec (size, stops, targets)
7. Outcome logged: Entry price, exit price, P&L
8. Review (daily): "4 tier 1 trades: 3 wins, 1 loss (75% win rate)"
9. Review (weekly): "Tier 1 win rate 75% vs. backtest 68%. Performing well."
10. Strategy: No changes needed (performing as expected)
11. Next week: Cycle repeats with same spec
```

---

## When to Update Each Spec

- **Strategic**: When objectives change, or learnings suggest new rules
- **Execution**: When you want to change how/when actions are taken
- **Observability**: When you want to monitor different things or change alerts
- **Collaboration**: When roles/approval chains change
- **Review**: When you want different analysis or more/less frequent reviews

**Key principle**: Always update specs through a documented process (commit with message). Never change specs in-place during operations.

---

## For Implementation

When building agents:
- Each agent reads one spec (its authoritative spec)
- Agent may also read other specs for context
- Agents coordinate through events (not shared state)
- All decisions logged for audit and review

See `agent-responsibilities.md` for how agents coordinate.
