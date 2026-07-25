# audit_log Skill

**Purpose**: Standardized, queryable logging for every agent decision.

**Used by**: All agents (every agent should log every decision for audit, review, and analysis)

---

## Overview

The `audit_log` skill ensures consistent logging across all agents. Every decision gets:

1. **Timestamp** — When the decision was made
2. **Audit ID** — Unique identifier for tracking
3. **Agent name** — Which agent made the decision
4. **Action** — What was done (execute, approve, alert, etc.)
5. **Reasoning** — Why the decision was made
6. **Inputs** — Data used to make the decision
7. **Outputs** — Result of the decision
8. **Status** — Success, pending, error, rejected, etc.

**Why it matters**: This audit trail enables:
- **Review Agent** to analyze patterns and outcomes
- **Operators** to understand why something happened
- **Debugging** when things go wrong
- **Compliance** for auditing and governance

---

## Usage

### Basic Import

```python
from skills.core.audit_log import AuditLog

# Create skill instance (typically per agent or per domain)
audit_log = AuditLog(log_file='logs/trading_audit.log')
```

### Log a Decision

```python
audit_id = audit_log.log({
    'agent': 'execution',
    'action': 'execute_trade',
    'reasoning': 'Tier 1 setup: Price break 445.50 with volume confirmed',
    'inputs': {
        'signal': {'type': 'price_break', 'level': 445.50, 'volume': 120_000_000},
        'rule': {'tier': 1, 'size': 5000, 'stop': 445.20}
    },
    'outputs': {
        'trade': {'id': '123', 'entry': 445.55, 'size': 5000, 'stop': 445.20, 'target': 446.50}
    },
    'status': 'success'
})

# Returns unique audit_id for tracking
# Logs are written to disk immediately
```

### Query by Agent

```python
# Get all decisions made by execution agent
entries = audit_log.query_by_agent('execution')

for entry in entries:
    print(f"{entry['timestamp']}: {entry['action']} → {entry['status']}")
```

### Query by Action

```python
# Get all executions
trades = audit_log.query_by_action('execute_trade')

# Get all approvals
approvals = audit_log.query_by_action('request_approval')
```

### Query by Status

```python
# Get all rejections
rejections = audit_log.query_by_status('rejected')

# Get all pending approvals
pending = audit_log.query_by_status('pending')
```

### Query by Time Range

```python
from datetime import datetime, timedelta

# Last hour
now = datetime.utcnow().isoformat() + 'Z'
one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'

recent = audit_log.query_time_range(one_hour_ago, now)
```

### Get Summary

```python
# Summary of all activity
summary = audit_log.summary()
print(f"Total entries: {summary['total_entries']}")
print(f"By status: {summary['by_status']}")
print(f"By action: {summary['by_action']}")
print(f"By agent: {summary['by_agent']}")

# Example output:
# Total entries: 42
# By status: {'success': 38, 'rejected': 2, 'error': 1, 'pending': 1}
# By action: {'execute_trade': 25, 'request_approval': 12, 'publish_alert': 5}
# By agent: {'execution': 27, 'collaboration': 12, 'observability': 3}
```

### Export Logs

```python
# Export to JSON (for analysis)
audit_log.export_json('audit_export.json')

# Export to CSV (for spreadsheet)
audit_log.export_csv('audit_export.csv')
```

---

## Log Entry Schema

Every log entry follows this structure:

```python
{
    'agent': str,                  # Agent name (execution, observability, etc.)
    'action': str,                 # Action taken (execute_trade, publish_alert, etc.)
    'reasoning': str,              # Explanation of why this decision
    'inputs': Dict,                # Data used to make decision
    'outputs': Dict,               # Result/outcome
    'status': str,                 # success, pending, error, rejected, etc.
    'timestamp': str,              # ISO format, auto-generated if not provided
    'audit_id': str                # Unique ID, auto-generated if not provided
}
```

### Required Fields

All of these must be provided:
- `agent` — Name of agent making decision
- `action` — What action was taken
- `reasoning` — Why (explain the logic)
- `inputs` — What data was used
- `outputs` — What resulted
- `status` — Outcome status

### Optional Fields

- `timestamp` — ISO format (defaults to `datetime.utcnow()`)
- `audit_id` — Custom ID (defaults to auto-generated format)

### Status Values

| Status | Meaning |
|--------|---------|
| `success` | Decision executed successfully |
| `pending` | Decision pending (e.g., waiting for approval) |
| `error` | Decision failed with error |
| `rejected` | Decision was rejected (e.g., by operator or validation) |
| `skipped` | Decision was skipped (e.g., conditions not met) |

---

## API Reference

### `AuditLog(log_file: str = 'audit.log')`

Create a new audit log instance.

```python
audit_log = AuditLog('logs/trading_audit.log')
```

**Args:**
- `log_file` (str): Path where logs are written
  - Default: `'audit.log'` in current directory
  - Creates directory if it doesn't exist

---

### `log(entry: Dict) -> str`

Log an agent decision.

**Args:**
- `entry` (dict): Decision dict with required and optional fields (see schema above)

**Returns:**
- `audit_id` (str): Unique identifier for this entry

**Raises:**
- `ValueError`: If required fields are missing

**Example:**

```python
audit_id = audit_log.log({
    'agent': 'execution',
    'action': 'execute_trade',
    'reasoning': 'Tier 1 setup detected with high confidence',
    'inputs': {'signal': {...}, 'rule': {...}},
    'outputs': {'trade': {...}},
    'status': 'success'
})
```

---

### `query(criteria: Dict) -> List[Dict]`

Query log entries by multiple criteria (AND logic).

**Args:**
- `criteria` (dict): Filter criteria
  - `agent` (str): Filter by agent name
  - `action` (str): Filter by action
  - `status` (str): Filter by status
  - `time_from` (str): ISO timestamp (>=)
  - `time_to` (str): ISO timestamp (<=)
  - `audit_id` (str): Find specific entry

**Returns:**
- List of matching entries

**Example:**

```python
# All trade executions
trades = audit_log.query({'agent': 'execution', 'action': 'execute_trade'})

# All rejections in past hour
from datetime import datetime, timedelta
one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'
rejections = audit_log.query({
    'status': 'rejected',
    'time_from': one_hour_ago
})
```

---

### `query_by_agent(agent_name: str) -> List[Dict]`

Get all entries for a specific agent.

```python
execution_logs = audit_log.query_by_agent('execution')
```

---

### `query_by_action(action: str) -> List[Dict]`

Get all entries for a specific action.

```python
trade_executions = audit_log.query_by_action('execute_trade')
```

---

### `query_by_status(status: str) -> List[Dict]`

Get all entries with a specific status.

```python
errors = audit_log.query_by_status('error')
```

---

### `query_time_range(time_from: str, time_to: str) -> List[Dict]`

Get entries in a time range (ISO format timestamps).

```python
from datetime import datetime, timedelta

now = datetime.utcnow().isoformat() + 'Z'
one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat() + 'Z'

recent = audit_log.query_time_range(one_hour_ago, now)
```

---

### `get_entry(audit_id: str) -> Optional[Dict]`

Get a specific entry by audit_id.

```python
entry = audit_log.get_entry('exec_test_20260516114532')
```

**Returns:** Entry dict or `None` if not found

---

### `summary(agent: Optional[str] = None) -> Dict`

Get summary statistics of logged activity.

**Args:**
- `agent` (str, optional): Filter summary to specific agent

**Returns:** Dict with counts by status, action, time range

**Example:**

```python
# Full summary
summary = audit_log.summary()
print(summary['by_status'])  # {'success': 38, 'rejected': 2}

# Execution agent only
exec_summary = audit_log.summary(agent='execution')
```

---

### `export_json(output_file: str) -> None`

Export all log entries to JSON.

```python
audit_log.export_json('audit_export.json')
```

---

### `export_csv(output_file: str) -> None`

Export log entries to CSV.

```python
audit_log.export_csv('audit_export.csv')
```

---

### `load_from_file() -> None`

Load existing log entries from disk (append mode).

**Use when:** Restarting and want to read previous logs into memory.

```python
audit_log = AuditLog('logs/trading_audit.log')
audit_log.load_from_file()  # Load existing entries
```

---

## Common Patterns

### Pattern 1: Agent Logs Every Decision

```python
class ExecutionAgent:
    def __init__(self, skills, event_bus):
        self.audit_skill = skills['core/audit_log']
        self.event_bus = event_bus
    
    def on_market_signal(self, signal):
        try:
            rules = self.query_rules(signal)
            if not rules:
                self.audit_skill.log({
                    'agent': 'execution',
                    'action': 'evaluate_signal',
                    'reasoning': f'No rules match signal type: {signal["type"]}',
                    'inputs': {'signal': signal},
                    'outputs': {},
                    'status': 'skipped'
                })
                return
            
            # Execute...
            self.audit_skill.log({
                'agent': 'execution',
                'action': 'execute_trade',
                'reasoning': f'Tier {rule["tier"]} setup: {signal["description"]}',
                'inputs': {'signal': signal, 'rule': rule},
                'outputs': {'trade': trade_action},
                'status': 'success'
            })
        except Exception as e:
            self.audit_skill.log({
                'agent': 'execution',
                'action': 'execute_trade',
                'reasoning': f'Error during execution: {str(e)}',
                'inputs': {'signal': signal},
                'outputs': {'error': str(e)},
                'status': 'error'
            })
            raise
```

---

### Pattern 2: Review Agent Queries Audit Log

```python
class ReviewAgent:
    def on_daily_review(self):
        audit_log = self.audit_skill
        
        # Get all trades from today
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat() + 'Z'
        today_end = datetime.utcnow().isoformat() + 'Z'
        
        trades = audit_log.query({
            'agent': 'execution',
            'action': 'execute_trade',
            'time_from': today_start,
            'time_to': today_end
        })
        
        # Analyze
        wins = [t for t in trades if 'profit' in t['outputs'].get('trade', {})]
        losses = [t for t in trades if 'loss' in t['outputs'].get('trade', {})]
        
        win_rate = len(wins) / len(trades) if trades else 0
        
        # Report feedback
        self.publish_report({
            'total_trades': len(trades),
            'win_rate': win_rate,
            'feedback': 'Consider tightening entry criteria if win_rate < 0.65'
        })
```

---

### Pattern 3: Operator Reviews Rejected Decisions

```python
class OperatorDashboard:
    def show_today_rejections(self):
        audit_log = self.audit_skill
        
        rejections = audit_log.query({'status': 'rejected'})
        
        for entry in rejections:
            print(f"{entry['timestamp']}: {entry['agent']} rejected {entry['action']}")
            print(f"  Reasoning: {entry['reasoning']}")
            print(f"  Input was: {entry['inputs']}")
            print()
```

---

## Storage Format

Logs are stored as **JSON lines** (one JSON object per line) for easy streaming and querying:

```
{"agent": "execution", "action": "execute_trade", "reasoning": "...", "inputs": {...}, "outputs": {...}, "status": "success", "timestamp": "2026-05-16T09:45:32Z", "audit_id": "exec_test_20260516094532"}
{"agent": "observability", "action": "publish_alert", "reasoning": "...", "inputs": {...}, "outputs": {...}, "status": "success", "timestamp": "2026-05-16T09:45:35Z", "audit_id": "obse_publ_20260516094535"}
...
```

---

## Performance Notes

- **In-memory cache**: Entries stay in memory for fast querying during runtime
- **Disk persistence**: Written to disk immediately (no batching)
- **Large logs**: For very large log files (>10k entries), consider archiving old entries
- **Querying**: Simple O(n) linear scan; consider exporting to database for complex queries

---

## Testing

Run tests with:

```bash
cd skills/core/audit_log
python -m pytest audit_log_test.py
```

---

## See Also

- [skills/core/interfaces.md](../interfaces.md) — Skill interface contracts
- [docs/implementers.md](../../../docs/implementers.md) — How agents use skills
- [skills/core/spec_query/](../spec_query/) — Companion skill for reading specs
