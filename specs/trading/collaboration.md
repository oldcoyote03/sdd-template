# Day Trading: Collaboration Specification

## Roles & Responsibilities

### Role: Trader

**Responsibilities**:
- Execute trades in accordance with Strategic and Execution specs
- Maintain trade journal with entry rationale and post-trade notes
- Manage daily P&L and stop when loss limit is reached
- Respond to alerts and approve/skip setups
- Participate in weekly review and strategy adjustment meetings

**Authority**:
- Decide whether to execute on any approved setup alert
- Manually override automated exits (with logging required)
- Request pause/resume of trading if needed
- Propose changes to entry models or profit targets

**Escalation**:
- If unable to monitor (internet outage, emergency), escalate to Risk Manager
- If uncertain about setup tier classification, consult with Analyst or ask system to escalate to Review

### Role: Risk Manager

**Responsibilities**:
- Monitor portfolio-level risk (max daily loss, max concurrent positions, leverage)
- Alert if daily loss limit is approaching
- Audit trade execution logs for compliance
- Approve any deviations from Execution Spec (e.g., override time window, increase position size)
- Weekly review: capital efficiency, drawdown analysis

**Authority**:
- Pause/resume trading immediately
- Modify position size limits or daily loss limits (with documented reason)
- Require additional analysis before certain trades

**Escalation**:
- If system errors or data feed issues, escalate to Operations
- If compliance issue detected, escalate to Compliance (external)

### Role: Analyst

**Responsibilities**:
- Maintain Strategic Spec (market structures, entry models)
- Backtest new entry models before deployment
- Analyze trade outcomes for pattern recognition
- Calculate performance metrics (win rate, risk/reward)
- Recommend optimizations based on data

**Authority**:
- Propose changes to entry models or market structure definitions
- Request trader to highlight specific trades for deep-dive analysis

**Escalation**:
- If suggesting major strategy change, consult with Trader and Risk Manager

## Information Visibility

### Trader

**Spec Sections Visible**:
- Strategic: Full visibility (needs to understand the why)
- Execution: Full visibility (must follow approval workflows)
- Observability: Full visibility (alerts and live dashboard)
- Collaboration: Own role only
- Review: Full visibility (performance metrics, feedback)

**Data Access**:
- Real-time: Live quotes, open positions, alerts
- Historical: All personal trades (full journal + exit reasons)
- Reporting: Daily P&L, weekly win rate, personal performance dashboard

**Historical Access**: 5 years of trade history (for pattern analysis)

### Risk Manager

**Spec Sections Visible**:
- Strategic: Summary only (risk parameters)
- Execution: Full visibility (approval workflows, limits)
- Observability: Full visibility (alerts, risk metrics)
- Collaboration: Full visibility (needs to know all roles)
- Review: Full visibility (portfolio performance)

**Data Access**:
- Real-time: Portfolio P&L, risk utilization (open positions, leverage)
- Historical: All trades (aggregate + per-trader if applicable)
- Reporting: Risk dashboards, compliance reports

**Historical Access**: Full historical access for audit

### Analyst

**Spec Sections Visible**:
- Strategic: Full visibility (optimizing entry models)
- Execution: Full visibility (understanding trade constraints)
- Observability: Metrics only (not real-time live data during trading hours; batch data post-market)
- Collaboration: Read-only (needs to know roles for communication)
- Review: Full visibility (analyzing outcomes)

**Data Access**:
- Historical: All trades (for analysis) post-execution
- Real-time: NO (keeps analyst independent of trading noise)
- Reporting: Performance dashboards, pattern analysis

**Historical Access**: 5 years for backtesting

## Approval Workflows

### Workflow: Execute Tier 1 Setup

**Approver**: Trader (human-in-the-loop)
**Conditions**: 
- Auto-approval OK if:
  - Volume confirmation present
  - Macro bias confirmed
  - Setup within active trading window
- If auto-execution enabled, Trader gets 10-second review window before execution

**SLA**: Approval decision within 10 seconds (setup is time-sensitive)
**Fallback**: If no response in 10 seconds, setup is skipped

### Workflow: Execute Tier 3 Setup

**Approver**: Trader
**Conditions**: Always requires explicit approval
**SLA**: Trader must approve within 30 seconds or setup is skipped

### Workflow: Pause Trading

**Approver**: Risk Manager (can auto-trigger if daily loss limit hit)
**Conditions**: Auto-triggered when -$1,000 daily loss limit reached; or manual request from Trader/Risk Manager
**SLA**: Pause is immediate

### Workflow: Modify Position Size Limit

**Approver**: Risk Manager
**Conditions**: Requires documented justification and Trader consultation
**SLA**: Decision within 1 hour

### Workflow: Change to Strategic Spec

**Approver**: Trader + Analyst consensus
**Conditions**: Backtesting results required; proposed change documented
**SLA**: Change proposal to implementation: 1 week (allows Trader time to test before live deployment)

## Communication & Notification

### Event: Tier 1 Setup Alert

**Recipients**: Trader
**Channel**: In-app notification + audible alert
**Urgency**: High (5-second response time expected)
**Message**: "SPY Tier 1 setup: Break above 445.50 micro-resistance with volume. Macro bias: Uptrend. Approve? (Y/N)"

### Event: Daily Loss Limit Hit

**Recipients**: Trader + Risk Manager
**Channel**: Email + SMS + in-app
**Urgency**: Critical (immediate action required)
**Message**: "Daily loss limit reached (-$1,000). Trading paused. Review trades and contact if error."

### Event: Trade Closed

**Recipients**: Trader (journal entry created automatically)
**Channel**: Logged in system (visible on dashboard)
**Urgency**: Low (informational)
**Message**: "[14:32] SPY closed +$245. Profit target hit. Setup: Tier 1, Break above resistance."

### Event: Weekly Review Summary

**Recipients**: Trader + Analyst + Risk Manager
**Channel**: Email + shared dashboard
**Urgency**: Medium (review discussion scheduled)
**Frequency**: Friday 5:00 PM ET
**Message**: "Weekly Summary: +$1,203 P&L. Win rate 58%. 7 Tier 1 trades (71% win). Recommend backtest new mean-reversion model."

### Event: Performance Report (Monthly)

**Recipients**: Trader + Risk Manager + Analyst (optional external stakeholders)
**Channel**: Dashboard + report document
**Frequency**: Last Friday of month
**Message**: Detailed performance metrics, risk analysis, strategy effectiveness

## Onboarding & Offboarding

### New Trader Onboarding

1. **Week 1**: Read Strategic Spec, Execution Spec, understand entry models via training
2. **Week 2**: Paper trading (no real money); Analyst reviews setups with new trader
3. **Week 3**: Live trading with $2,000 daily loss limit (reduced from $1,000); Risk Manager monitors closely
4. **Week 4+**: Graduate to full $1,000 daily loss limit if performance is stable (>50% win rate)

**Progressive Permission Unlocking**:
- No Tier 1 auto-execution approval in Week 1-2 (must manually execute)
- Tier 1 auto-execution enabled Week 3+ if performance is good
- Position sizing capped at $3,000 in Week 1-2; $5,000 in Week 3+

### Role Removal (Offboarding)

**Scenario**: Trader leaves operation
1. **Immediately**: Trading permissions revoked; all open positions closed
2. **Within 24 hours**: Trade journal and outcomes archived for compliance
3. **Within 1 week**: Historical data backed up; knowledge transfer to replacement trader (if applicable)

## Conflicts & Escalation

**Scenario**: Trader and Risk Manager disagree on trade approval
- **Resolution**: Analyst reviews the setup independently; decides based on Strategic Spec criteria
- **Escalation**: If still disputed, pause trading until consensus is reached

**Scenario**: System error causes unauthorized trade
- **Resolution**: Trade is immediately reversed (if possible); Trader and Risk Manager investigate root cause
- **Escalation**: Post-incident review to prevent recurrence; audit logged
