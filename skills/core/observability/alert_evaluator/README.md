# alert_evaluator Skill

**Purpose**: Evaluate alert conditions against current state and emit alerts when triggered.

**Used by**: Observability Agent (primary), Collaboration Agent (when routing alerts)

---

## Overview

The `alert_evaluator` skill solves a key problem: different domains have different alert conditions (daily loss limits, budget overages, attendance thresholds), but the evaluation logic is the same: check if condition is met, and if so, emit alert with urgency and recipients.

This skill:

1. **Parses alert conditions** from spec (condition_logic field)
2. **Evaluates against current state** (metrics, prices, positions, time)
3. **Determines if triggered** (yes/no)
4. **Returns alert dict** with context (metric value, threshold, when triggered)

**Design principle**: Skill is stateless. The agent manages alert history and deduplication, and passes current state to this skill on each evaluation.

---

## Usage

### Basic Import

```python
from skills.core.observability.alert_evaluator import AlertEvaluator

# Create skill instance
alert_evaluator = AlertEvaluator()
```

### Evaluate a Single Alert

```python
# From observability spec
alert_spec = {
    'name': 'Daily Loss Limit Reached',
    'condition_logic': 'Daily P&L ≤ -$1,000',
    'urgency': 'critical',
    'recipients': ['Trader', 'Risk Manager']
}

# Current state
current_state = {
    'daily_pnl': -1050,
    'time': '14:30:00'
}

# Metric results from metric_calculator
metric_results = [
    {
        'metric_name': 'Daily P&L',
        'value': -1050,
        'baseline': 'Target +$200-$500/day'
    }
]

alert = alert_evaluator.evaluate_condition(alert_spec, current_state, metric_results)
if alert:
    print(f"ALERT: {alert['alert_name']} ({alert['urgency']})")
    print(f"Recipients: {alert['recipients']}")
else:
    print("Condition not triggered")
```

### Evaluate All Alerts from Spec

```python
from skills.core.spec_query import SpecQuery

spec_query = SpecQuery()
observability_spec = spec_query.load_spec('specs/examples/day-trading/observability.md')
alerts_list = observability_spec['sections']  # All alerts from spec

# Get current state
current_state = {
    'daily_pnl': -1050,
    'rolling_win_rate': 48,
    'time': '14:30:00',
    'market_status': 'open'
}

# Evaluate all
triggered_alerts = alert_evaluator.evaluate_all_conditions(
    alerts_list,
    current_state,
    metric_results
)

# Process triggered alerts
for alert in triggered_alerts:
    print(f"Alert: {alert['alert_name']}")
    print(f"Urgency: {alert['urgency']}")
    print(f"Recipients: {alert['recipients']}")
```

---

## Integration with Other Skills

**Observability Agent workflow:**
```
1. metric_calculator.calculate_all_metrics()
2. alert_evaluator.evaluate_all_conditions(metric_results=results, current_state=state)
3. alert_router.batch_route_alerts(triggered_alerts, collaboration_spec)
```

**Collaboration Agent:**
```
"Route this alert to the right people"
  → alert_router.route_alert(alert, collaboration_spec)
```

---
