# Guide for Operators

**You are**: A person using the system day-to-day to make decisions and keep the operation running.

**Your goal**: Monitor alerts, approve actions when needed, understand outcomes, and provide feedback for improvement.

**Prerequisites**: Implementers have built and deployed the system; spec authors have defined the operation.

---

## Overview

Your job is to **act on alerts, make decisions, and stay informed**—not to understand the code or write specs.

The system shows you:
1. **What needs your attention NOW** (alerts requiring action)
2. **What's the current state** (metrics, positions, open items)
3. **What happened** (history, outcomes, reports)

---

## The Dashboard

The dashboard is your main interface. It presents information in layers: **see high-level summaries by default, drill in for details on demand**.

### Layout

```
┌─────────────────────────────────────────────────────────────┐
│  TOP: ALERTS REQUIRING ACTION (highest priority)             │
│  ┌─ [TIER 1 SETUP ALERT]  🔴 "SPY break 445.50"             │
│  │    Market bias: Uptrend | Volume: 120M | Approve? [Y/N]  │
│  │    Expires: 8 seconds                                     │
│  └─ [RISK ALERT]  🟡 "Daily loss at $800 of $1,000"         │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  MIDDLE: LIVE STATUS                                         │
│  ┌─ Market Overview                                          │
│  │  SPY: 445.60 (+0.3%) | Volume: 120M | Bias: Uptrend     │
│  │  Support: 445.00 | Resistance: 446.50                    │
│  │                                                            │
│  ├─ Active Positions                                         │
│  │  1x SPY @ 445.40 | P&L: +$100 | Risk: -$200             │
│  │                                                            │
│  └─ Recent Alerts (past 1 hour)                              │
│     [9:45 AM] Tier 1 setup → Trader approved                 │
│     [9:30 AM] Daily loss limit: $600 of $1,000               │
│                                                              │
├─────────────────────────────────────────────────────────────┤
│  BOTTOM: HISTORY & REPORTS                                   │
│  [View Today's Trades] [View Weekly Report] [View Journal]   │
│  [View System Health] [View Audit Log]                       │
└─────────────────────────────────────────────────────────────┘
```

### What Each Section Shows

**Top Section (Alerts)**
- Setup alerts (action needed from you)
- Risk alerts (market conditions or limits being approached)
- Approval requests (decisions waiting for your input)
- Each alert includes enough context to decide quickly
- Time remaining (for time-bound decisions)

**Middle Section (Live Status)**
- Current market conditions (from Observability Agent)
- Your open positions and P&L
- Risk metrics (how much loss limit remaining?)
- High-level market bias (for context)

**Bottom Section (History)**
- Searchable log of today's trades/actions
- Weekly reports (from Review Agent)
- Detailed journal entries
- System health and audit logs (for troubleshooting)

---

## How to Interact

### Scenario 1: Approve a Trade Setup

Alert appears: *"Tier 1 setup: SPY break 445.50. Approve?"*

**Your decision**:
1. **Check context**: Look at market bias, volume, risk
2. **Decide**: Click "Approve" or "Reject" (or type Y/N)
3. **See outcome**: System executes (or logs rejection)

**If you approve**:
- System executes trade automatically
- Your approval is logged for audit
- Position appears in "Active Positions"
- Execution details show: entry price, stop, target

**If you reject**:
- System logs your decision and reasoning
- No trade executes
- Observability Agent continues monitoring for next setup

### Scenario 2: Monitor an Approaching Risk Limit

Alert appears: *"Daily loss: $800 of $1,000"*

**What you see**:
- Current P&L (already down $800)
- Remaining risk budget ($200)
- Open positions (and their risk)
- Tier breakdown (how many of each type)

**Your decision**:
- **Let it ride**: If you believe next setup will be profitable
- **Stop trading**: Click "Close all positions" to exit and limit further loss
- **Adjust**: Reduce trade size for next setup

**System's behavior**:
- System continues to monitor but alerts if any new setup would breach the limit
- You stay in control (system doesn't auto-exit without your input)

### Scenario 3: Review What Happened

You want to understand today's results.

**Option A: Quick view**
- Click "View Today's Trades"
- See: All trades executed, entry/exit prices, P&L by trade
- Hover over any trade to see setup details (what triggered it?)

**Option B: Detailed review**
- Click "View Weekly Report" (from Review Agent)
- See: Win rates by tier, setup quality analysis, performance trends
- Read: Recommended changes to strategy for next week

**Option C: Deep dive**
- Click "View Audit Log"
- See: Every decision (by agent), with reasoning
- Search by: trade ID, agent name, time range
- Understand: Why did system execute (or not execute) a particular setup?

---

## Approval Workflows

Different tiers require different approvals:

### Tier 1: High Confidence
- **Who**: You (Trader)
- **Time window**: 10 seconds
- **Decision**: Usually quick (conditions are clear)
- **Example**: "Break above resistance with volume confirmed"

### Tier 2: Medium Confidence
- **Who**: You (Trader) + Risk Manager
- **Time window**: 30 seconds
- **Decision**: Both must approve, or it's rejected
- **Example**: "Mean reversion setup, but lower volume"

### Tier 3: Low Confidence
- **Who**: Risk Manager (veto required)
- **Time window**: 60 seconds
- **Decision**: Risk Manager must not reject; you can approve but must wait
- **Example**: "Weak signal, high risk"

**If you don't respond in time**:
- Alert expires
- Setup is not executed
- System continues monitoring
- Reasoning: "Better to miss one trade than make a rushed decision"

---

## Understanding the Reports

### Daily Report

*Generated at end of day (4 PM)*

Contains:
- **Trades**: All executions, P&L, win/loss by tier
- **Performance**: Win rate, average win/loss, profit factor
- **Risk**: Daily max loss, max drawdown, largest losing trade
- **Feedback**: "Tier 1 performing well (70% win rate vs. 65% target). Tier 2 lower confidence, recommend backtest filter tightening."

**Your action**: Read the feedback. If you agree, discuss with strategy team about updating specs.

### Weekly Report

*Generated Friday 4 PM*

Contains:
- **Weekly P&L**: Total profit/loss for the week
- **Tier analysis**: How did each tier perform? Which are consistent?
- **Setup quality**: Which setup types worked best?
- **Risk management**: Did you hit any limits? When?
- **Recommendations**: Suggested changes to strategy for next week

**Your action**: Bring to team meeting. Discuss whether to implement recommended changes.

---

## Dashboard Actions

### Standard Actions

| Action | When | How |
|--------|------|-----|
| **Approve trade** | Setup alert appears | Click "Approve" or type Y |
| **Reject trade** | Setup alert appears | Click "Reject" or type N |
| **Close position** | Want to exit early | Click "Close" on position |
| **Close all** | Daily loss approaching limit | Click "Liquidate all" |
| **View trade details** | Want to understand a trade | Click on trade row |
| **View reason** | Want to know why setup triggered | Hover over or click alert |
| **View audit log** | Want to see all decisions | Click "System → Audit Log" |

### Advanced Actions (if supported)

| Action | When | Notes |
|--------|------|-------|
| **Override approval** | System rejected something you disagree with | Creates audit flag; analyst reviews later |
| **Adjust risk limits** | Want to change daily loss limit | Requires second approval; logged |
| **Manual trade** | Want to execute outside of alerts | Creates special log entry |

---

## Tips for Effective Operation

### 1. **Stay Informed on Alerts**
- Read the full alert, not just the headline
- Understand why setup triggered (check market context)
- Don't approve if something feels off

### 2. **Watch Risk Metrics**
- Glance at "Daily P&L" frequently
- Know your remaining risk budget
- Adjust behavior if approaching limits

### 3. **Review Daily**
- Spend 5 minutes at end of day reading the daily report
- Look for patterns (which tiers perform? which setups work?)
- Note feedback for next week

### 4. **Provide Feedback**
- If you see something wrong with an alert, report it
- If a setup triggered but looked bad, note it in comments
- This feedback loops back to improve specs

### 5. **Trust the System, But Verify**
- The system is designed to help, not replace your judgment
- If alert looks wrong, reject it—Review Agent will see the rejection
- Audit trail is your safety net

---

## Troubleshooting

### Problem: Alert Didn't Appear (Setup I Expected)

**Check**:
1. Is the condition in the specs? (May not meet threshold)
2. Is market bias correct? (Setup may require specific bias)
3. Is it outside trading hours? (Some setups only during market hours)

**What to do**:
- Click "View Observability Dashboard" to see what metrics are being calculated
- Ask strategy team if specs need adjustment

### Problem: I Rejected an Alert but It Executed Anyway

**Possible reasons**:
- Approval required from two people (you rejected, but other person approved)
- System had queued the signal before you rejected

**What to do**:
- Check audit log to see who approved
- If unexpected, report to implementers

### Problem: Dashboard is Slow or Lagging

**What to do**:
- Refresh page (usually fixes)
- Check "System Health" to see if agents are running
- Report to implementers if persistent

### Problem: I Don't Understand a Report

**What to do**:
- Click on data point to see supporting details
- Check "View Audit Log" for decision details
- Ask strategy/analyst team to explain

---

## Key Metrics to Watch

### Daily Metrics

| Metric | What It Means | When to Act |
|--------|---------------|-------------|
| **Daily P&L** | Profit/loss so far today | If approaching daily loss limit, reduce risk |
| **Win Rate (Today)** | % of trades that profit | Informational; watch weekly trend |
| **Open Positions** | Trades still running | Verify stops/targets are correct |
| **Daily Loss Limit Remaining** | Remaining risk budget | Stop trading if <$200 remaining |

### Weekly Metrics

| Metric | What It Means | When to Act |
|--------|---------------|-------------|
| **Weekly P&L** | Total profit/loss this week | Celebrate wins, analyze losses |
| **Win Rate (By Tier)** | Performance of each tier | Tier <60% → recommend backtest adjustment |
| **Setup Quality** | Best & worst performing setups | Feedback to strategy team |
| **Biggest Drawdown** | Largest loss in a single trade | Verify stop-loss is working correctly |

---

## Glossary

- **Setup**: A market condition that matches a trade entry pattern
- **Tier**: Confidence level (Tier 1 high, Tier 3 low)
- **Approval**: Your explicit permission to execute
- **Audit log**: Record of all decisions and approvals
- **Win rate**: % of trades that made money
- **Profit factor**: Total wins / total losses (higher is better)
- **Drawdown**: How much P&L went down from peak

---

## See Also

- [STRUCTURE.md](../STRUCTURE.md) — Other audiences and roles
- [specs/trading/](../specs/trading/) — Trading rules and workflows (context for what you're approving)
- [docs/spec-authors.md](../docs/spec-authors.md) — How specs are written (if you want to understand the rules)

---

## Getting Started

1. **Log into dashboard** with your credentials
2. **Explore**: Click through each section to familiarize yourself
3. **Read**: Check out today's daily report to see what a normal day looks like
4. **Start small**: Approve a few low-risk (Tier 1) alerts to get comfortable
5. **Review**: At day's end, check the audit log and daily report
6. **Ask**: If anything is unclear, ask your team or consult this guide

---

## Support

For issues or questions:
- **Dashboard issues**: Contact technical support
- **Understanding alerts**: Ask your strategy team
- **Understanding reports**: Check audit log details or ask analyst
- **General questions**: Refer to this guide or [docs/spec-authors.md](../docs/spec-authors.md) for context on how the system works
