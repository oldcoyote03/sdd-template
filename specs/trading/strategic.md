# Day Trading: Strategic Specification

## Objectives & Success Criteria

**Primary Objective**: Generate consistent daily profits through systematic swing/intraday trading of S&P 500 index ETFs (SPY, QQQ) using structure-based entry models.

**Success Metrics**:
- Win rate: ≥ 55%
- Average profit per trade: $200+
- Daily profitability: ≥ 3 profitable days per 5-day week
- Maximum daily loss limit: $1,000

**Constraints**:
- Maximum capital at risk per trade: $5,000
- Trading hours: 9:30 AM - 4:00 PM ET (regular market hours only)
- No overnight positions
- Minimum holding time: 15 minutes
- Maximum holding time: 4 hours

## Decision Frameworks

### Core Trading Principles

1. **Structure Over Prediction**: Trade established market structure (support, resistance, trend), not predictions.
2. **Risk-First**: Define risk on entry, never add to losing positions.
3. **Systematic Entry**: Only enter at high-probability setup points, not on discretionary whims.
4. **Scale with Confirmation**: Increase size only after successful micro-trades at a setup.

### Market Structure Levels (Top to Bottom)

1. **Macro Level**: Is SPY in uptrend, downtrend, or range?
   - Uptrend: HH/HL pattern, closes above 20-day MA
   - Downtrend: LL/LH pattern, closes below 20-day MA
   - Range: Bouncing between resistance/support without breaking

2. **Daily Level**: What's the bias for today?
   - Identified key levels: overnight gaps, previous day high/low, key support/resistance

3. **Intraday Level**: What's the pattern on 5-min, 15-min charts?
   - Point of Interest: Micro-structure pattern (micro support/resistance, break patterns, channel)

### Entry Models (Hierarchy of Setup Quality)

**Tier 1 (Highest Confidence)**:
- Break above micro-resistance after consolidation, with volume confirmation
- Bounce from micro-support in uptrend with clean structure

**Tier 2 (High Confidence)**:
- Breakout from intraday channel with momentum
- Mean reversion to moving average in established trend

**Tier 3 (Moderate Confidence)**:
- Retest of daily level with intraday structure
- Divergence on lower timeframe with macro bias

### Trade Management Rules

- **Risk per Trade**: Never exceed $500 loss per trade
- **Profit Targets**: 
  - Exit 50% at 1:2 risk/reward
  - Exit 25% at 1:4 risk/reward
  - Trail 25% with 5-min stop
- **Stop Loss**: Placed at micro-structure invalidation point (typically 0.2-0.5% below entry)

### Operational Discipline

- **Trade Journal**: Every trade gets logged with entry rationale, setup tier, and outcome
- **Daily Review**: Each day ends with P&L analysis and pattern recognition
- **Weekly Review**: Win rate, entry model effectiveness, missed opportunities
- **No Revenge Trading**: If down $500 in a day, stop trading until next day

## Operational Scope

- **Markets**: SPY (broad market), QQQ (tech-heavy), optional: IWM (small-cap)
- **Timeframes**: Entry decision on 5-15 min structure, macro bias from daily/4-hour
- **Decision Horizon**: Intraday (decisions within 4-hour window)

## Rationale

Day trading requires speed, discipline, and structural clarity. Rather than predict, we trade high-probability setups where structure + market bias + entry pattern align. Risk-first entry management ensures that bad trades are small (limited downside) and good trades are scalable (higher upside). The journal and review process closes the feedback loop—we learn what entry models work and optimize accordingly.
