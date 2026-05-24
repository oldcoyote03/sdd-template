# metric_calculator Skill

**Purpose**: Calculate operational metrics from raw data and compare against baselines.

**Used by**: Observability Agent (primary), Review Agent, Strategy Agent (when analyzing performance)

---

## Overview

The `metric_calculator` skill solves a key problem: every domain needs to compute metrics differently (P&L in trading, savings rate in finance, attendance % in education), but the comparison logic is generic.

This skill:

1. **Computes metrics** from raw data (any formula specified in spec)
2. **Compares against baselines** (target ranges, thresholds)
3. **Detects trends** (improving, declining, stable)
4. **Returns structured results** that other skills can consume

**Design principle**: Skill is stateless. The agent manages state (historical data, caches) and passes it to this skill on each calculation.

---

## Usage

### Basic Import

```python
from skills.core.observability.metric_calculator import MetricCalculator

# Create skill instance
metric_calculator = MetricCalculator()
```

### Calculate a Single Metric

```python
# From observability spec
metric_spec = {
    'name': 'Daily P&L',
    'calculation': 'Sum of all closed trade profits/losses',
    'baseline': 'Target +$200-$500/day; stop if -$1,000'
}

# Current data
raw_data = {
    'closed_trades': [
        {'profit': 250},
        {'profit': -50},
        {'profit': 100}
    ]
}

# Previous values for trend detection
historical_baseline = {
    'last_day_pnl': 350,
    'rolling_avg_pnl': 280
}

result = metric_calculator.calculate_metric(metric_spec, raw_data, historical_baseline)
# Returns:
# {
#     'metric_name': 'Daily P&L',
#     'value': 300,
#     'baseline': 'Target +$200-$500/day',
#     'comparison': 'within',
#     'trend': 'declining',  # 300 < 350 previous day
#     'timestamp': '2024-05-24T14:32:15Z'
# }
```

### Calculate All Metrics from Spec

```python
from skills.core.spec_query import SpecQuery

spec_query = SpecQuery()
observability_spec = spec_query.load_spec('specs/trading/observability.md')
metrics_list = observability_spec['sections']  # All metrics from spec

# Get all current data
raw_data = {
    'closed_trades': [...],
    'current_positions': [...],
    'market_data': {...}
}

# Calculate all
results = metric_calculator.calculate_all_metrics(metrics_list, raw_data, historical_baseline)
# Returns list of metric results
```

---

## Integration with Other Skills

**Observability Agent workflow:**
```
1. metric_calculator.calculate_all_metrics()
2. alert_evaluator.evaluate_all_conditions(metric_results=results)
3. dashboard_manager.render_all_dashboards(current_metrics=results)
```

**Other agents:**
```
Review Agent: "Calculate win rate metric for analysis"
  → metric_calculator.calculate_metric(spec, data)

Strategy Agent: "What's our current performance?"
  → metric_calculator.calculate_metric(spec, data)
```

---
