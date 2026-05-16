# Skills Library

**Purpose**: Reusable modules that agents invoke to avoid duplication and enable sharing across domains.

**Current status**: Core skills only (foundation). Domain-specific skills (observability, market data, etc.) added in future phases.

---

## What Are Skills?

Skills are self-contained, testable modules that agents use. Each skill solves one specific problem:

- **Spec Query Skill**: Parse and query markdown specs
- **Audit Log Skill**: Standardized logging for all agents

**Design principle**: Skills are independent of domain. A skill built for trading can be reused in personal finance or homeschooling.

---

## Directory Structure

```
skills/
├── README.md                           # This file
├── core/
│   ├── interfaces.md                   # Interface contracts
│   ├── spec_query/
│   │   ├── __init__.py
│   │   ├── spec_query.py               # Implementation
│   │   ├── spec_query_test.py          # Tests
│   │   └── README.md                   # Usage guide
│   └── audit_log/
│       ├── __init__.py
│       ├── audit_log.py                # Implementation
│       ├── audit_log_test.py           # Tests
│       └── README.md                   # Usage guide
│
└── (future: domain-specific skills)
    ├── trading/
    │   ├── market_data/
    │   └── risk_calculation/
    └── observability/
        └── alert_router/
```

---

## Core Skills

### Skill: `spec_query`

**Purpose**: Load markdown specs and query them by criteria.

**Problem it solves**: Agents need to read specs efficiently without parsing markdown themselves.

**Used by**: All agents (every agent reads its primary spec).

**Example**:

```python
from skills.core.spec_query import SpecQuery

spec_query = SpecQuery()

# Find all Tier 1 rules in execution.md
tier1_rules = spec_query.query(
    spec_path='specs/trading/execution.md',
    criteria={'tier': 1}
)
```

**See**: [core/spec_query/README.md](core/spec_query/README.md) for full usage guide.

---

### Skill: `audit_log`

**Purpose**: Standardized, queryable logging for agent decisions.

**Problem it solves**: Without consistent logging, it's hard to audit decisions, analyze patterns, or debug.

**Used by**: All agents (every agent should log every decision).

**Example**:

```python
from skills.core.audit_log import AuditLog

audit_log = AuditLog('logs/trading_audit.log')

# Log a trade execution
audit_log.log({
    'agent': 'execution',
    'action': 'execute_trade',
    'reasoning': 'Tier 1 setup detected',
    'inputs': {'signal': signal, 'rule': rule},
    'outputs': {'trade': action},
    'status': 'success'
})

# Query trades from today
today_trades = audit_log.query({
    'agent': 'execution',
    'action': 'execute_trade',
    'time_from': today_start,
    'time_to': today_end
})
```

**See**: [core/audit_log/README.md](core/audit_log/README.md) for full usage guide.

---

## Using Skills in an Agent

### 1. Register Skills at Agent Initialization

```python
from skills.core.spec_query import SpecQuery
from skills.core.audit_log import AuditLog

class ExecutionAgent:
    def __init__(self, spec_path, event_bus):
        # Register skills
        self.spec_skill = SpecQuery()
        self.audit_skill = AuditLog(log_file='logs/execution_audit.log')
        
        self.spec_path = spec_path
        self.event_bus = event_bus
```

### 2. Use Skills in Decision Logic

```python
def on_market_signal(self, signal):
    # Use spec_query to find matching rules
    rules = self.spec_skill.query(
        spec_path=self.spec_path + '/execution.md',
        criteria={'tier': signal['tier']}
    )
    
    for rule in rules:
        # Make decision...
        
        # Use audit_log to record it
        self.audit_skill.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': f'Tier {rule["tier"]} setup',
            'inputs': {'signal': signal, 'rule': rule},
            'outputs': {'trade': action},
            'status': 'success'
        })
```

---

## Interface Contracts

Each skill has a **contract** — a guaranteed interface that all implementations follow.

**See**: [core/interfaces.md](core/interfaces.md) for the full contract definitions.

Key principles:
1. **Consistent method signatures**: Every implementation has the same method names and parameters
2. **Consistent return types**: Queries always return lists, lookups return dicts or None
3. **Consistent error handling**: Failures raise specific exceptions with clear messages
4. **No external dependencies**: Core skills use only Python standard library

---

## Testing Skills

Each skill has unit tests to verify correctness.

### Run Tests

```bash
# Test spec_query
cd skills/core/spec_query
python -m pytest spec_query_test.py -v

# Test audit_log
cd skills/core/audit_log
python -m pytest audit_log_test.py -v

# Test all core skills
cd skills/core
python -m pytest *_test.py -v
```

### Write Tests

When implementing a new skill, include tests that verify:
1. Basic functionality (create, query, retrieve)
2. Error handling (missing required fields, invalid input)
3. Edge cases (empty results, large datasets)
4. Integration (with other skills, with agents)

---

## Future: Domain-Specific Skills

Once core skills are proven, we'll add domain-specific skill libraries:

### Observability Skills

```
skills/observability/
├── alert_router/            # Route alerts by role
├── metric_calculator/       # Calculate metrics from data
└── dashboard_formatter/     # Format data for display
```

**Reasoning**: Observability patterns are very similar across domains. These skills handle routing, calculation, and presentation.

### Trading Skills

```
skills/trading/
├── market_data/             # Fetch quotes, calculate technicals
├── risk_calculation/        # Position sizing, P&L, limits
└── order_execution/         # Format and submit orders
```

**Reasoning**: These are specific to financial markets, but can be shared across different trading strategies.

### Finance Skills

```
skills/finance/
├── portfolio_calculation/   # Rebalancing, allocation drift
├── tax_calculation/         # Tax-loss harvesting, gains
└── reporting/               # Performance reports
```

---

## Contributing a New Skill

To add a new skill:

1. **Identify the problem**: What does this skill solve? What code is it deduplicating?
2. **Design the interface**: What methods should it have? What are inputs/outputs?
3. **Implement**: Write the Python module
4. **Test**: Write unit tests (target >80% coverage)
5. **Document**: Write README with usage examples
6. **Add to registry**: Update [interfaces.md](core/interfaces.md) with contract
7. **Distribute**: Publish to repo or package manager

---

## Skill Lifecycle

### Phase 1: Core Skills (Current)
- `spec_query` — Load and query markdown specs
- `audit_log` — Standardized logging

### Phase 2: Observability (Future)
- Alert routing, metric calculation, dashboard formatting

### Phase 3: Domain-Specific (Future)
- Trading skills (market data, risk, execution)
- Finance skills (portfolio, tax, reporting)
- etc.

---

## Performance & Scalability

### Current Design

- **In-memory caching**: Specs and logs cached in memory for fast access
- **Disk persistence**: Audit logs written to disk (JSON lines format)
- **Linear scan queries**: O(n) lookup; fine for reasonable log sizes

### For Large-Scale Use

Consider:
- Exporting logs to database for complex queries
- Caching specs across multiple agent processes
- Archiving old logs to cold storage

---

## See Also

- [core/interfaces.md](core/interfaces.md) — Interface contracts
- [core/spec_query/README.md](core/spec_query/README.md) — Spec query usage
- [core/audit_log/README.md](core/audit_log/README.md) — Audit log usage
- [../../docs/implementers.md](../../docs/implementers.md) — How agents use skills
- [../../docs/spec-authors.md](../../docs/spec-authors.md) — Specs that skills query
