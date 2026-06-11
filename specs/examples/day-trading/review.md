# Day Trading: Review & Feedback Specification

## Review Cadences

### Review: Post-Trade Journaling

**Review Type**: Immediate capture of trade metadata and context
**Frequency**: After each trade closes
**Trigger Conditions**: Any trade completion (profit target, stop loss, manual close)
**Review Owner**: Trader (auto-captured by system; manual notes added by trader)

**What Gets Captured**:
- Entry price, exit price, P&L
- Entry setup tier (1, 2, or 3)
- Macro bias at time of entry
- Time in trade
- Setup quality rating (in retrospect: was the setup clear?)
- Outcome (win/loss)
- Operator notes (optional: what was the trade idea?)

### Review: Daily Performance Review

**Review Type**: End-of-day analysis of all trades and P&L
**Frequency**: Daily at market close (4:00 PM ET)
**Trigger Conditions**: Market close
**Review Owner**: Trader + Risk Manager

**What Gets Analyzed**:
- Daily P&L (total and by trade)
- Win rate (today only)
- Entry model effectiveness (which tiers won? which lost?)
- Missed setups (setups that were skipped; would they have been profitable?)
- Risk/reward ratio (actual vs. target)
- Any unusual market conditions or volatility

**Output**: Daily review report (5-10 min summary)

### Review: Weekly Strategy Review

**Review Type**: Comprehensive analysis of entry models and market structures
**Frequency**: Weekly (Friday after close, 5:00 PM ET)
**Trigger Conditions**: End of week
**Review Owner**: Analyst + Trader + Risk Manager (collaborative discussion)

**What Gets Analyzed**:
- Weekly P&L (total and by day)
- Win rate (weekly + rolling 20-trade average)
- Entry model breakdown (Tier 1 vs. 2 vs. 3 performance)
- Market structure accuracy (did our bias predict actual direction?)
- Most effective entry model (by win rate)
- Worst performing entry model (by win rate)
- Capital efficiency (profit per $1,000 deployed)
- Missed opportunities (setups we didn't trade that were profitable)

**Output**: Weekly review report with recommendations

### Review: Monthly Optimization Review

**Review Type**: Deep-dive into profitability, risk management, and strategy viability
**Frequency**: Monthly (last Friday of month)
**Trigger Conditions**: Month end
**Review Owner**: Trader + Analyst + Risk Manager

**What Gets Analyzed**:
- Monthly P&L and net return %
- Cumulative win rate
- Drawdown analysis (largest consecutive losing trades)
- Risk/reward ratio trends
- Any major losses and root cause analysis
- Market environment (was it favorable for our models?)
- Strategy viability (are we still profitable? Why/why not?)
- Recommendations for next month

**Output**: Monthly performance report + strategy adjustment roadmap

## Analysis Frameworks

### Framework: Trade Setup Quality Analysis

**Analysis Name**: Entry Model Effectiveness
**Questions to Answer**:
- Which entry model tiers are winning most? (Tier 1, 2, or 3)
- What's the win rate by setup tier in real trading vs. backtest?
- Are we filtering setups correctly (are we skipping good ones, or entering bad ones)?
- What's the time-in-trade for each tier? Are we holding too long or exiting too early?

**Data Inputs**:
- Trade journal (entry tier, exit reason, P&L)
- Setup alerts (were there skipped setups that would have been profitable?)
- Historical backtest data (for comparison)

**Success Indicators**:
- Tier 1 win rate ≥ 65% (as backtested)
- Tier 2 win rate ≥ 58%
- Tier 3 win rate ≥ 52%
- Real trading performance within 5% of backtest

**Failure Indicators**:
- Tier win rate dropping > 10% below backtest
- Skipped setups that would have been 3:1 winners (suggests we're being too conservative)

### Framework: Market Structure Accuracy

**Analysis Name**: Macro Bias Prediction
**Questions to Answer**:
- Did our SPY trend prediction (uptrend/downtrend/range) correctly predict actual direction?
- How many times did we get the bias wrong? What were the warning signs?
- Are our support/resistance levels being respected?

**Data Inputs**:
- Daily market structure specs (bias assigned each morning)
- Actual SPY price action (did it follow predicted direction?)
- Trade outcomes by bias (were uptrend trades more profitable than downtrend?)

**Success Indicators**:
- Macro bias correct ≥ 70% of the time
- Profitable trades align with bias prediction

**Failure Indicators**:
- Macro bias wrong > 30% of the time
- Trades against bias are consistently losing

### Framework: Risk Management Audit

**Analysis Name**: Risk Parameter Calibration
**Questions to Answer**:
- Are our stop losses sized correctly? (too tight = whipsawed; too loose = max loss too large)
- Are profit targets realistic? (are we hitting 1:2 and 1:4 targets?)
- Is position sizing appropriate for market volatility?
- Are we respecting daily/weekly loss limits?

**Data Inputs**:
- Trade journal (entry, stop, target, exit)
- Actual market volatility (ATR, daily ranges)
- Daily P&L and drawdown

**Success Indicators**:
- Average stop loss hit rate ≤ 15% (most trades don't hit stops)
- Profit targets hit ≥ 70% of trades
- Max daily loss respected (no days exceeding -$1,000)

**Failure Indicators**:
- Stops hit too frequently (> 25% of trades)
- Targets hit < 50% of trades (suggests targets are unrealistic)

## Feedback Mechanisms

### Feedback Loop 1: Entry Model Refinement → Strategic Spec

**Insight Type**: Patterns in winning/losing setups
**Feedback Mechanism**: If Tier 1 win rate drops below 60%, analyst proposes tightening entry model filters or reconsidering the tier classification
**Loop Target**: Strategic Spec (update entry model definitions)
**Implementation Timeline**: 
- Hypothesis formed: end of week review
- Backtesting: 1 week
- Live testing: 2 weeks (with reduced position size)
- Full deployment: if backtest + live testing validate hypothesis

**Example**: 
- Observation: Tier 1 setups at open of day are winning less frequently than late-morning setups
- Hypothesis: Morning volatility makes the setups less reliable
- Action: Propose adding time filter to Tier 1 definition (exclude 9:30-10:00 AM setups)
- Feedback to spec: Update Strategic Spec to add timing constraint

### Feedback Loop 2: Risk Parameter Adjustment → Execution Spec

**Insight Type**: Stops/targets are miscalibrated
**Feedback Mechanism**: If stops are being hit > 25% or targets hit < 50%, adjust stop placement or target levels
**Loop Target**: Execution Spec (update stop/target formulas)
**Implementation Timeline**: Immediate for next trading day (affects all new trades)

**Example**:
- Observation: 18% of trades are being stopped out despite reaching profit target (whipsawed)
- Hypothesis: Stop loss is too tight; should be 0.4% not 0.2% below entry
- Action: Adjust stop formula in Execution Spec
- Feedback to spec: Update stop loss placement rules

### Feedback Loop 3: Market Structure Updates → Observability Spec

**Insight Type**: Support/resistance levels need updating based on new market data
**Feedback Mechanism**: Weekly market structure review; update daily support/resistance levels if broken
**Loop Target**: Observability Spec (update daily level definitions)
**Implementation Timeline**: Daily (as market breaks key levels)

**Example**:
- Observation: SPY repeatedly bounces off new level (e.g., 446.00) instead of old level (445.50)
- Action: Update daily resistance level in Observability Spec
- Feedback: All future entries and bias calls use the new level

## Reporting & Communication

### Report: Daily Trade Summary

**Report Type**: Text summary with key metrics
**Report Audience**: Trader (personal review)
**Report Frequency**: Daily at market close
**Report Format**: Dashboard + email summary
**Contents**:
- Trades entered/exited
- Daily P&L
- Win rate (today)
- Entry model breakdown (which tiers won)
- Any unusual market events

### Report: Weekly Performance Review

**Report Type**: Detailed analysis with recommendations
**Report Audience**: Trader + Analyst + Risk Manager
**Report Frequency**: Weekly (Friday evening)
**Report Format**: Dashboard + email discussion starter
**Contents**:
- Weekly P&L and return %
- Entry model performance (win rate by tier)
- Market structure accuracy
- Capital efficiency
- Recommended optimizations for next week

### Report: Monthly Comprehensive Review

**Report Type**: Strategic assessment and performance trends
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
