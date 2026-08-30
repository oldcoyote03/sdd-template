# Domain Review & Feedback Specification

This draft is intentionally neutral. Replace placeholder review cadences, metrics, and feedback loops with explicit domain expectations once the KB or human input defines the operating model.

## Review Cadences

### Review: [Immediate or Routine Review]

**Review Type**: [what is reviewed]
**Frequency**: [timing or trigger]
**Trigger Conditions**: [what initiates the review]
**Review Owner**: [role or process owner]

**What Gets Captured**:
- [review item 1]
- [review item 2]
- [review item 3]

### Review: [Periodic Review]

**Review Type**: [type of review]
**Frequency**: [timing]
**Trigger Conditions**: [operational trigger]
**Review Owner**: [role or group]

**What Gets Analyzed**:
- [question or topic]
- [question or topic]
- [question or topic]

## Analysis Frameworks

### Framework: [Analysis Framework]

**Questions to Answer**:
- [question 1]
- [question 2]
- [question 3]

**Data Inputs**:
- [input 1]
- [input 2]
- [input 3]

**Success Indicators**:
- [indicator or threshold]
- [indicator or threshold]

**Failure Indicators**:
- [warning sign]
- [warning sign]

## Feedback Mechanisms

### Feedback Loop: [Loop Name]

**Insight Type**: [type of result or signal]
**Feedback Mechanism**: [how feedback is routed back into operations]
**Loop Target**: [spec or process being updated]
**Implementation Timeline**: [when the feedback is applied]

## Reporting & Communication

### Report: [Report Name]

**Report Type**: [type of report]
**Report Audience**: [who receives it]
**Report Frequency**: [timing]
**Report Format**: [dashboard, email, or document]
**Contents**:
- [key item 1]
- [key item 2]
- [key item 3]
**Report Audience**: Trader + Analyst + Risk Manager + any external stakeholders
**Report Frequency**: Monthly
**Report Format**: PDF report + interactive dashboard
**Contents**:
- Monthly P&L and cumulative return
- Win rate and risk/reward trends
- Drawdown analysis
- Strategy viability assessment
- Optimization roadmap for next month
- Comparison to prior months/quarters

## Optimization Priorities

### Priority 1 (Immediate): Maintain Win Rate ≥ 55%

**Why**: Win rate is the primary success metric; if it drops, profitability suffers
**Effort vs. Impact**: Medium effort (requires entry model analysis) / High impact (directly affects P&L)
**Dependencies**: Requires Analyst time for backtesting

**Action Items**:
- Monitor daily win rate; if < 55% for 3 consecutive days, trigger deep-dive analysis
- Analyze losing trades for patterns (was a setup tier misclassified? Did we miss a setup quality filter?)
- Backtest proposed entry model tightening before live deployment

### Priority 2 (Weekly): Improve Risk/Reward Ratio

**Why**: Higher risk/reward means larger profits on winners, smaller losses on losers
**Effort vs. Impact**: Low effort (adjust stop/target placement) / Medium impact (improves profit per trade)
**Dependencies**: None; can be changed immediately

**Action Items**:
- If risk/reward < 1.5:1, widen profit targets or tighten stops
- If most winners are hitting 1:2 target but not 1:4, extend the trailing stop time window

### Priority 3 (Monthly): Validate Market Structure Definitions

**Why**: Incorrect bias = trading against the trend = lower win rate
**Effort vs. Impact**: Medium effort (requires chart review) / High impact (improves trend prediction)
**Dependencies**: Requires time to review recent market structure

**Action Items**:
- Backtest last month's trades with different structure definitions (e.g., 50-day MA instead of 20-day MA)
- If alternative structure would have predicted trend better, update Strategic Spec definition

### Priority 4 (Quarterly): Backtest New Entry Models

**Why**: Markets evolve; new models may be more profitable
**Effort vs. Impact**: High effort (requires significant analysis) / Potential high impact (new alpha)
**Dependencies**: Analyst time; live testing time before full deployment

**Action Items**:
- Brainstorm new entry models based on recent winning patterns
- Backtest against 2-year historical data
- If backtest promising (> 58% win rate), live test with reduced position size for 2 weeks
- If live test validates, roll out to full trading

## Feedback Review Cycle

**Weekly Rhythm**:
- Daily reviews: Trader captures trade context and reflects
- Weekly review meeting (Friday): Analyst + Trader + Risk Manager discuss patterns and propose optimizations
- Spec updates: Analyst implements agreed-upon changes to Strategic/Execution/Observability specs
- New week: Trader lives with updated specs; monitors effectiveness

**Continuous Improvement**: Each week's feedback informs next week's execution; specs are living documents that evolve as the operation learns.
