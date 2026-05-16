# Guide for Spec Authors

**You are**: A domain expert defining rules, workflows, and decision frameworks for your operation.

**Your goal**: Write specifications that other people (agents and operators) will read to make decisions.

**Timeline**: You work before implementers build agents, or in parallel with them.

---

## Overview

Your job is to be **explicit and precise** about how your operation should work. You're not writing code—you're writing business rules, workflows, and frameworks in structured markdown.

Specs are the **single source of truth**. Agents read them to decide what to do. Operators read them to understand the system. Implementers read them to know what to build.

---

## The Five Core Specs

Every domain has five specifications. You'll write them in this order:

### 1. **Strategic Spec** — Decision Rules & Frameworks

**Purpose**: Define the strategic direction and decision rules for your operation.

**Contains**:
- Core business rules (e.g., "We only trade mean reversion setups")
- Decision frameworks (e.g., "Market bias: uptrend, downtrend, or choppy")
- Risk limits (e.g., "Max daily loss: $1,000")
- Quality criteria (e.g., "Entry model win rate target: 65%+")
- Strategic priorities (e.g., "Tier 1 setups prioritized over Tier 3")

**Example from trading**: [specs/trading/strategic.md](../specs/trading/strategic.md)

**When to start**: First. Spend time here—this is your foundation.

**Tips**:
- Be specific with numbers (thresholds, percentages, timeframes)
- Define key terms clearly (what is a "setup"? what is "high confidence"?)
- Organize by priority or category
- Keep sections short and navigable (agents will query sections, not read linearly)

**Template**: [specs/templates/STRATEGIC_TEMPLATE.md](../specs/templates/STRATEGIC_TEMPLATE.md)

---

### 2. **Execution Spec** — What Actions Can Be Taken & When

**Purpose**: Define executable actions, their conditions, approval requirements, and constraints.

**Contains**:
- What actions are allowed (e.g., "Execute trades", "Log updates", "Escalate alerts")
- When actions can be taken (e.g., "Only during market hours", "When high-confidence setup detected")
- Who can execute (e.g., "Trader can execute Tier 1; Risk Manager must approve Tier 3")
- Approval workflows (e.g., "10-second approval window for Tier 1")
- Size/stake constraints (e.g., "$5,000 per trade for Tier 1")
- Stop-loss and profit targets
- Fallback procedures (e.g., "If venue A fails, try venue B")

**Example from trading**: [specs/trading/execution.md](../specs/trading/execution.md)

**When to start**: After Strategic. Strategic defines the rules; Execution defines the actions.

**Tips**:
- Organize by action type or tier (e.g., Tier 1, Tier 2, Tier 3 setups)
- Include specific thresholds and timeframes (agents need precision)
- Define approval requirements clearly
- Include error handling (what happens if something goes wrong?)

**Template**: [specs/templates/EXECUTION_TEMPLATE.md](../specs/templates/EXECUTION_TEMPLATE.md)

---

### 3. **Observability Spec** — What to Monitor & How to Alert

**Purpose**: Define data sources, metrics, and alert conditions.

**Contains**:
- Data sources (e.g., "Live market data from feed X", "Internal trade log")
- Metrics to calculate (e.g., "Win rate", "Daily P&L", "Volatility")
- Alert conditions (e.g., "Alert when daily loss > $800")
- Alert recipients (e.g., "Send to Trader", "Send to Risk Manager")
- Dashboard elements (e.g., "Show live P&L", "Show open positions")
- Review cadences (e.g., "Hourly for alerts, daily for summaries")

**Example from trading**: [specs/trading/observability.md](../specs/trading/observability.md)

**When to start**: After Execution. Execution defines what to monitor; Observability defines how.

**Tips**:
- Be specific about data sources (where will agents get this data?)
- Define alert thresholds precisely (no vague language like "too much")
- Specify alert routing (who sees what?)
- Include dashboard/display guidance

**Template**: [specs/templates/OBSERVABILITY_TEMPLATE.md](../specs/templates/OBSERVABILITY_TEMPLATE.md)

---

### 4. **Collaboration Spec** — Roles, Visibility, & Approval Workflows

**Purpose**: Define who is involved, what they can see, and what they must approve.

**Contains**:
- Roles in the system (e.g., "Trader", "Risk Manager", "Analyst")
- Role responsibilities (e.g., "Trader: Execute trades under Tier 1")
- Visibility rules (e.g., "Risk Manager sees all trades, but Analyst only sees Tier 1")
- Approval workflows (e.g., "Tier 2 requires Trader + Risk Manager approval")
- Communication channels (e.g., "Alert via Slack", "Dashboard visibility")
- Escalation paths (e.g., "If Trader unavailable, escalate to Risk Manager")

**Example from trading**: [specs/trading/collaboration.md](../specs/trading/collaboration.md)

**When to start**: After Observability. Once you know what to monitor and execute, define who's involved.

**Tips**:
- Keep role definitions clear and non-overlapping
- Be explicit about who approves what (no ambiguity)
- Include escalation procedures (what if the primary approver isn't available?)
- Define communication channels clearly

**Template**: [specs/templates/COLLABORATION_TEMPLATE.md](../specs/templates/COLLABORATION_TEMPLATE.md)

---

### 5. **Review Spec** — How to Analyze & Improve

**Purpose**: Define how outcomes are analyzed and feedback loops back into strategy refinement.

**Contains**:
- Review cadences (e.g., "Daily at 4 PM", "Weekly on Fridays")
- Analysis frameworks (e.g., "Win rate by tier", "Setup effectiveness")
- Metrics to track (e.g., "Profit factor", "Risk-adjusted returns")
- Feedback mechanisms (e.g., "Recommend Tier 2 filter tightening if <60% win rate")
- Report structure (e.g., "What sections must be in each report")
- Closed-loop mechanism (e.g., "How feedback impacts strategy updates")

**Example from trading**: [specs/trading/review.md](../specs/trading/review.md)

**When to start**: Last. By now you know what to do, who does it, and how to monitor it. This closes the loop.

**Tips**:
- Make feedback actionable (don't just report; recommend changes)
- Link review insights back to Strategic spec (this is where improvement happens)
- Define metrics concretely (not "good performance" but ">65% win rate")
- Include cadence (how often do you review?)

**Template**: [specs/templates/REVIEW_TEMPLATE.md](../specs/templates/REVIEW_TEMPLATE.md)

---

## Writing Tips

### Be Explicit, Not Ambiguous

❌ Bad: "Execute when we have a good setup"  
✅ Good: "Execute when price breaks 445.50 on volume >100M and market bias is uptrend"

### Use Numbers & Specificity

❌ Bad: "Risk is limited"  
✅ Good: "Max daily loss: $1,000. Max trade size: $5,000. Stop loss: 20 pips below entry"

### Organize for Queries

Agents don't read specs linearly—they query them. Structure so that sections can stand alone:

```markdown
## Execution Rules

### Tier 1: High Confidence
- Condition: [specific]
- Size: $5,000
- Approval: Trader (10 sec)

### Tier 2: Medium Confidence
- Condition: [specific]
- Size: $3,000
- Approval: Trader + Risk Manager (30 sec)
```

Agents can query: "Show me Tier 1 rules where condition matches 'breakout'"

### Include Context

Every decision rule should explain *why*:

```markdown
**Market Bias (Uptrend)**
- Definition: SPY above 20-day MA, higher highs, higher lows
- Why: Establishes directional probability; mean reversion setups work better in clear trends
- Decision impact: Prioritize long entries in uptrend
```

### Reference Other Specs

Cross-link strategically (e.g., Execution spec references Strategic spec for context):

```markdown
## Size Constraints
$5,000 per trade (Strategic spec: "Risk limit of $1,000/day means max 4-5 Tier 1 trades")
```

---

## Example Workflow

You're creating specs for a personal finance domain:

1. **Strategic**: Define your financial goals (retirement at age 65, $2M), risk tolerance (conservative), rules (70/30 stocks/bonds)
2. **Execution**: Define what actions you can take (buy, sell, rebalance), when (quarterly), approval (auto, no human needed for small trades)
3. **Observability**: Define what to monitor (portfolio value, allocation drift, market conditions), alerts (when allocation > 5% from target)
4. **Collaboration**: Define roles (you manage, accountant reviews annually), visibility (accountant sees reports, not daily dashboard)
5. **Review**: Define review cadence (quarterly), analysis (are you on track for retirement? adjust allocation?), feedback (if markets drop, adjust strategy?)

---

## Next Steps

1. Choose your domain (trading, personal finance, homeschooling, operations, etc.)
2. Create directory: `specs/[your-domain]/`
3. Copy templates from `specs/templates/` as starting point
4. Fill in each spec in order: Strategic → Execution → Observability → Collaboration → Review
5. Reference `specs/trading/` if you get stuck
6. When done, share with implementers so they can build agents to interpret your specs

---

## For Questions

- **How do I structure a specific spec?** See the template + `specs/trading/` example
- **What level of detail do I need?** Enough that agents can make consistent decisions without guessing
- **Can I change specs later?** Yes—specs evolve. But log changes so agents and operators understand what changed
- **Should I include implementation details?** No—focus on *what* should happen, not *how* to code it. Implementers handle "how".

---

## See Also

- [ARCHITECTURE.md](../ARCHITECTURE.md) — System overview
- [STRUCTURE.md](../STRUCTURE.md) — Other audiences and roles
- [specs/templates/](../specs/templates/) — Templates for all five specs
- [specs/trading/](../specs/trading/) — Complete trading example
