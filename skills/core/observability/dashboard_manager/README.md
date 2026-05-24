# dashboard_manager Skill

**Purpose**: Assemble dashboard snapshots from metric results, filtered by audience role and refresh cadence.

**Used by**: Observability Agent (primary), UI/API layer (when serving dashboards to operators)

---

## Overview

The `dashboard_manager` skill solves a key problem: different roles see different dashboards with different metrics and refresh rates. A Trader needs real-time live trading dashboard; a Risk Manager needs a weekly review dashboard. This skill assembles the right view for the right role.

This skill:

1. **Filters metrics** by role (visibility control)
2. **Selects relevant metrics** for the dashboard
3. **Calculates next refresh time** based on cadence
4. **Returns dashboard snapshot** ready for UI rendering

**Design principle**: Skill is stateless. The agent passes metrics and role information; the skill returns a snapshot.

---

## Usage

### Basic Import

```python
from skills.core.observability.dashboard_manager import DashboardManager

# Create skill instance
dashboard_manager = DashboardManager()
```

### Render a Single Dashboard

```python
# From observability spec
dashboard_spec = {
    'name': 'Live Trading',
    'metrics': ['Daily P&L', 'Open Positions', 'Recent Alerts'],
    'refresh_cadence': 'real-time',
    'audience': ['Trader']  # Who can see this dashboard
}

# Current metrics from metric_calculator
current_metrics = [
    {
        'metric_name': 'Daily P&L',
        'value': 300,
        'baseline': '+$200-$500/day'
    },
    {
        'metric_name': 'Open Positions',
        'value': 2,
        'baseline': None
    }
]

# Render for Trader role
snapshot = dashboard_manager.render_dashboard(
    dashboard_spec,
    current_metrics,
    audience_role='Trader'
)

# Returns:
# {
#     'dashboard_name': 'Live Trading',
#     'metrics_on_dashboard': [...],  # Filtered to requested metrics
#     'refresh_cadence': 'real-time',
#     'next_refresh_time': '2024-05-24T14:32:16Z',
#     'timestamp': '2024-05-24T14:32:15Z'
# }

# Access denied for different role
try:
    snapshot = dashboard_manager.render_dashboard(
        dashboard_spec,
        current_metrics,
        audience_role='Analyst'  # Not in audience list
    )
except ValueError:
    print("Analyst not authorized to view Live Trading dashboard")
```

### Render All Dashboards for User

```python
from skills.core.spec_query import SpecQuery

spec_query = SpecQuery()
observability_spec = spec_query.load_spec('specs/trading/observability.md')
dashboards_list = observability_spec['sections']  # All dashboards from spec

# Current metrics
current_metrics = [...]

# Render all dashboards that this user's roles can access
user_roles = ['Trader']
dashboards = dashboard_manager.render_all_dashboards(
    dashboards_list,
    current_metrics,
    user_roles
)

# Returns dict:
# {
#     'Live Trading': {...},
#     'Daily Performance': {...},
#     ...
# }
```

---

## Integration with Other Skills

**Observability Agent workflow:**
```
1. metric_calculator.calculate_all_metrics()
2. alert_evaluator.evaluate_all_conditions()
3. dashboard_manager.render_all_dashboards(audience_roles=[user_roles])
   → Return to UI for rendering
```

**UI/API Layer:**
```
User requests dashboards
  → Identify user's roles
  → Call dashboard_manager.render_all_dashboards(user_roles)
  → Render returned snapshots to user
```

---
