# Guide for Agent Implementers

**You are**: An engineer building the agents and infrastructure that interprets specs and executes operations.

**Your goal**: Create agents that read specs, process signals, make decisions, and log outcomes. Reuse skills to avoid duplication.

**Prerequisites**: Spec authors have written specs in [specs/](../specs/) for your domain.

---

## Overview

Your architecture consists of:

1. **Role-specific agents** (Strategy, Execution, Observability, Collaboration, Review)
2. **Core skills** (spec_query, audit_log, and others)
3. **Event-driven orchestration** (agents listen for signals, publish decisions)
4. **Audit trail** (every decision is logged for review and improvement)

---

## Agent Architecture

### Agent Responsibilities

Each agent has a single well-defined job:

| Agent | Reads | Decides | Produces |
|-------|-------|---------|----------|
| **Strategy** | Strategic spec + Review feedback | How to explain strategy; when to suggest improvements | Strategy context for other agents; refinement proposals |
| **Execution** | Execution spec + Strategic spec + Observability signals | Whether to execute; who must approve | Trade execution commands; approval requests; audit logs |
| **Observability** | Observability spec + Live data feeds | What metrics to calculate; what alerts to generate | Live metrics; alert events; dashboard updates |
| **Collaboration** | Collaboration spec + Alerts/requests from other agents | Who needs to see what; enforce approval workflows | Routed notifications; approval tracking |
| **Review** | Review spec + Trade/outcome logs + Strategic spec | What analyses to run; what patterns to report | Analysis reports; feedback recommendations; refinement suggestions |

### Agent Interface Contracts

Each agent must implement this interface:

```python
class Agent:
    def __init__(self, spec_path: str, skills: Dict[str, Skill]):
        """
        Load agent's primary spec and register skills.
        
        Args:
            spec_path: Path to markdown spec for this agent
            skills: Dict of skill_name -> skill_instance
        """
    
    def on_signal(self, signal: Dict) -> None:
        """
        Handle an incoming signal (data, request, event).
        
        Triggered by event bus. Agent decides internally whether to act.
        """
    
    def log_decision(self, decision: Dict) -> None:
        """
        Log decision to audit trail (typically handled by audit_log skill).
        
        decision: {action, reasoning, inputs, outputs, timestamp}
        """
    
    def publish_event(self, event_type: str, event_data: Dict) -> None:
        """
        Publish event to event bus for other agents to consume.
        
        event_type: 'approval_request', 'trade_execution', 'alert', etc.
        """
```

---

## Skills Model

**Skills are reusable modules** that agents invoke. Core skills are in [skills/core/](../skills/core/).

### Core Skills

#### 1. **spec_query** — Parse and Query Markdown Specs

**Purpose**: Load and query markdown specs without rewriting them.

**What it does**:
- Parse markdown spec files into structured data
- Query by criteria (e.g., "Find all Tier 1 rules where condition == 'price_break'")
- Return matching sections in a navigable format

**Agent uses it**:

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills):
        self.spec_skill = skills['core/spec_query']
    
    def on_market_signal(self, signal):
        # Query: "Find rules that match this signal"
        matching_rules = self.spec_skill.query(
            spec_path='execution.md',
            criteria={'condition': signal['type'], 'tier': signal['tier']}
        )
```

**See**: [skills/core/spec_query/](../skills/core/spec_query/) for implementation and examples.

---

#### 2. **audit_log** — Standardized Logging

**Purpose**: Ensure every decision is logged consistently for audit and review.

**What it does**:
- Log decisions with: timestamp, agent name, action, reasoning, inputs, outputs, status
- Query logs by agent, action, or time window
- Export logs for Review Agent

**Agent uses it**:

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills):
        self.audit_skill = skills['core/audit_log']
    
    def execute_trade(self, rule, signal):
        trade_action = {'action': 'execute', 'size': 5000, ...}
        self.event_bus.publish('trade_execution', trade_action)
        
        # Log the decision
        self.audit_skill.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': f'Tier {rule["tier"]} setup detected',
            'inputs': {'signal': signal, 'rule': rule},
            'outputs': {'trade': trade_action},
            'status': 'success',
            'timestamp': now()
        })
```

**See**: [skills/core/audit_log/](../skills/core/audit_log/) for implementation and examples.

---

### Loading Skills

Create an agent factory that loads skills:

```python
from skills.core.spec_query import SpecQuery
from skills.core.audit_log import AuditLog

class AgentFactory:
    @staticmethod
    def create_execution_agent(spec_path, event_bus):
        # Load core skills
        skills = {
            'core/spec_query': SpecQuery(),
            'core/audit_log': AuditLog(log_file='execution_audit.log')
        }
        
        # Create agent with skills
        agent = ExecutionAgent(spec_path, skills, event_bus)
        return agent
```

---

## Event-Driven Orchestration

Agents don't call each other—they publish and subscribe to events.

### Event Flow Example

```
09:45 AM: Market data arrives
  ↓
  Observability Agent receives signal
  ├─ Query observability.md: What alerts should I check?
  ├─ Calculate metrics (volume, price movement, etc.)
  ├─ Condition met: "Tier 1 setup detected"
  └─ Publish event: 'setup_detected' with details
       ↓
       Execution Agent receives 'setup_detected' event
       ├─ Query execution.md: What's the rule for Tier 1?
       ├─ Check: Does signal match conditions?
       ├─ Yes → Need approval? (check collaboration.md)
       └─ Publish event: 'approval_request' to Collaboration Agent
            ↓
            Collaboration Agent receives 'approval_request'
            ├─ Query collaboration.md: Who should approve Tier 1?
            ├─ Send to Trader (10-second window)
            ├─ Wait for response
            └─ Publish event: 'approval_granted' or 'approval_denied'
                 ↓
                 Execution Agent receives 'approval_granted'
                 ├─ Query execution.md again: Execute now?
                 └─ Publish event: 'trade_execution' with order details
```

### Implementing Event Subscriptions

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills, event_bus):
        self.event_bus = event_bus
        
        # Subscribe to signals
        self.event_bus.subscribe('setup_detected', self.on_market_signal)
        self.event_bus.subscribe('approval_granted', self.on_approval)
    
    def on_market_signal(self, signal):
        # Handle signal (query specs, make decision, publish event)
        ...
    
    def on_approval(self, approval_event):
        # Handle approval (execute trade)
        ...
```

---

## Spec Integration Pattern

**Key principle**: Agents query specs *just-in-time*, not at startup. This keeps agents responsive and spec updates take effect immediately.

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills, event_bus):
        self.spec_path = spec_path
        self.spec_skill = skills['core/spec_query']
        self.event_bus = event_bus
    
    def on_market_signal(self, signal):
        # Query execution.md for rules matching this signal
        rules = self.spec_skill.query(
            spec_path=self.spec_path + '/execution.md',
            criteria={
                'condition': signal['type'],
                'tier': signal['confidence_tier']
            }
        )
        
        if not rules:
            self.audit_skill.log({...})
            return
        
        # For each matching rule, decide whether to execute
        for rule in rules:
            if rule.get('approval_required'):
                # Request approval
                self.event_bus.publish('approval_request', {...})
            else:
                # Execute immediately
                self.execute(rule, signal)
```

---

## Logging & Audit Trails

Every decision must be logged. The audit trail enables:
- Review Agent to analyze outcomes
- Operators to understand why something happened
- Debugging when something goes wrong

**Structured log entry** (via audit_log skill):

```python
{
    'timestamp': '2026-05-16T09:45:32Z',
    'agent': 'execution',
    'action': 'execute_trade',
    'reasoning': 'Tier 1 setup: Price break 445.50, volume confirmed',
    'inputs': {
        'signal': {'type': 'price_break', 'level': 445.50, ...},
        'rule': {'tier': 1, 'size': 5000, 'stop': 445.20, ...}
    },
    'outputs': {
        'trade': {'size': 5000, 'entry': 445.55, 'stop': 445.20, 'target': 446.50}
    },
    'status': 'success',
    'audit_id': 'exec_20260516_0945_001'
}
```

Review Agent queries this log to:
- Count trades by tier and outcome
- Calculate win rates
- Identify patterns
- Recommend spec updates

---

## Testing Strategy

### Test Agent Logic (without live data)

```python
def test_execution_agent_tier1_setup():
    agent = ExecutionAgent('specs/examples/day-trading/execution.md', skills, mock_event_bus)
    
    # Simulate market signal
    signal = {
        'type': 'price_break',
        'level': 445.50,
        'volume': 120000000,
        'confidence_tier': 1
    }
    
    # Agent should query execution.md, match Tier 1 rule, request approval
    agent.on_market_signal(signal)
    
    # Verify event published
    assert mock_event_bus.published('approval_request')
    
    # Verify audit log
    assert agent.audit_skill.query({'agent': 'execution'}) contains signal info
```

### Test Skill Integration

```python
def test_spec_query_skill_tier1_filter():
    skill = SpecQuery()
    rules = skill.query(
        spec_path='specs/examples/day-trading/execution.md',
        criteria={'tier': 1}
    )
    
    # Should return only Tier 1 rules
    assert all(r['tier'] == 1 for r in rules)
    assert len(rules) > 0
```

### Test End-to-End Scenario

```python
def test_execution_flow_tier1_setup():
    # Create all agents with mocked event bus
    agents = create_all_agents(mock_event_bus)
    
    # Simulate market signal
    market_signal = {...}
    agents['observability'].on_market_signal(market_signal)
    
    # Verify Observability → Execution → Collaboration flow
    # Verify final trade execution logged
```

---

## Building an Agent

### 1. Define the Agent Class

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills, event_bus):
        self.spec_path = spec_path
        self.spec_skill = skills['core/spec_query']
        self.audit_skill = skills['core/audit_log']
        self.event_bus = event_bus
        
        # Subscribe to signals
        self.event_bus.subscribe('setup_detected', self.on_market_signal)
        self.event_bus.subscribe('approval_granted', self.on_approval)
    
    # ... implement on_market_signal, on_approval, execute, etc.
```

### 2. Load Specs and Query

```python
def on_market_signal(self, signal):
    # Load rules from spec (just-in-time)
    rules = self.spec_skill.query(
        spec_path=self.spec_path + '/execution.md',
        criteria={'condition': signal['type']}
    )
```

### 3. Make Decisions

```python
for rule in rules:
    if self.should_execute(rule, signal):
        if rule.get('approval_required'):
            self.request_approval(rule, signal)
        else:
            self.execute(rule, signal)
```

### 4. Log Decisions

```python
self.audit_skill.log({
    'agent': 'execution',
    'action': 'execute_trade',
    'reasoning': '...',
    'inputs': {'signal': signal, 'rule': rule},
    'outputs': {'trade': action},
    'status': 'success'
})
```

### 5. Publish Events

```python
self.event_bus.publish('trade_execution', {
    'size': rule['size'],
    'stop': rule['stop'],
    'target': rule['target'],
    'timestamp': now()
})
```

---

## See Also

- [ARCHITECTURE.md](../ARCHITECTURE.md) — System design overview
- [reference/agent-interfaces.md](../reference/agent-interfaces.md) — Agent interface contracts
- [STRUCTURE.md](../STRUCTURE.md) — Other audiences
- [skills/core/](../skills/core/) — Core skills (spec_query, audit_log)
- [specs/examples/day-trading/](../specs/examples/day-trading/) — Example domain specs to work from

---

## Getting Started

1. **Read** [ARCHITECTURE.md](../ARCHITECTURE.md) for system overview
2. **Study** [specs/examples/day-trading/](../specs/examples/day-trading/) to understand what your agents will consume
3. **Review** [skills/core/spec_query/](../skills/core/spec_query/) to learn how to parse specs
4. **Review** [skills/core/audit_log/](../skills/core/audit_log/) to learn logging format
5. **Build** your first agent (recommend starting with Observability Agent—simpler decision logic)
6. **Test** your agent against example signals from specs
7. **Integrate** with event bus and other agents
8. **Log** everything for Review Agent to analyze

---

## Questions?

- **How do I query a spec?** See [skills/core/spec_query/README.md](../skills/core/spec_query/README.md)
- **What should I log?** See [skills/core/audit_log/README.md](../skills/core/audit_log/README.md) for schema
- **How do agents talk to each other?** Event bus with published event types and subscribers
- **What if a spec is ambiguous?** Ask spec authors to clarify (specs should be precise)
