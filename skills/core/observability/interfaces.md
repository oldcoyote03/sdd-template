# Observability Skills Interface Contracts

**Purpose**: Define interface contracts for observability skills so agents know what to expect.

---

## `metric_calculator` Skill Interface

**Purpose**: Calculate metrics from raw data and compare against baselines.

### Methods

#### `calculate_metric(metric_spec: Dict, raw_data: Dict, historical_baseline: Optional[Dict]) -> Dict`

Calculate a single metric and compare against baseline.

**Parameters:**
- `metric_spec` (dict): Metric definition from observability spec with keys:
  - `name` (str): Metric name (e.g., "Daily P&L")
  - `calculation` (str): How to calculate (e.g., "sum of closed trades")
  - `baseline` (str or dict): Reference baseline (e.g., "target is +$200-$500/day")
- `raw_data` (dict): Current data needed for calculation
- `historical_baseline` (dict, optional): Previous values for trend analysis

**Returns:**
```python
{
    'metric_name': str,
    'value': (number or string),
    'baseline': (number or string),
    'comparison': 'above' | 'below' | 'within' | 'unknown',
    'trend': 'improving' | 'declining' | 'stable' | None,
    'timestamp': ISO8601 str
}
```

**Raises:**
- `ValueError`: If calculation cannot be performed (missing data)
- `KeyError`: If required fields in metric_spec are missing

---

#### `calculate_all_metrics(metrics_list: List[Dict], raw_data_dict: Dict, historical_baselines: Dict) -> List[Dict]`

Calculate all metrics in a spec against current data.

**Parameters:**
- `metrics_list` (list): List of metric_spec dicts from observability spec
- `raw_data_dict` (dict): All available current data
- `historical_baselines` (dict): Previous metric values for trend analysis

**Returns:**
- List of metric result dicts (as above)

---

## `alert_evaluator` Skill Interface

**Purpose**: Evaluate alert conditions against current state and emit alerts when triggered.

### Methods

#### `evaluate_condition(alert_spec: Dict, current_state: Dict, metric_results: List[Dict]) -> Optional[Dict]`

Check if a single alert condition is triggered.

**Parameters:**
- `alert_spec` (dict): Alert definition from observability spec with keys:
  - `name` (str): Alert name
  - `condition_logic` (str): How to evaluate (e.g., "Daily P&L ≤ -$1,000")
  - `urgency` (str): 'critical' | 'high' | 'medium' | 'low'
  - `recipients` (list): Role names of recipients
- `current_state` (dict): Current operational state (prices, positions, metrics, time)
- `metric_results` (list): Results from metric_calculator skill

**Returns:**
```python
{
    'alert_name': str,
    'triggered': bool,
    'condition_logic': str,
    'urgency': str,
    'recipients': List[str],
    'context': {
        'metric_name': str,
        'current_value': (any),
        'threshold': (any),
        'triggered_at': ISO8601 str
    }
} | None  # None if condition not triggered
```

**Raises:**
- `ValueError`: If condition_logic cannot be parsed

---

#### `evaluate_all_conditions(alerts_list: List[Dict], current_state: Dict, metric_results: List[Dict]) -> List[Dict]`

Evaluate all alert conditions in a spec.

**Parameters:**
- `alerts_list` (list): List of alert_spec dicts from observability spec
- `current_state` (dict): Current operational state
- `metric_results` (list): Calculated metric results

**Returns:**
- List of alert dicts (only for triggered alerts; empty list if none triggered)

---

## `dashboard_manager` Skill Interface

**Purpose**: Assemble dashboard snapshots from metric results, filtered by audience role.

### Methods

#### `render_dashboard(dashboard_spec: Dict, current_metrics: List[Dict], audience_role: str) -> Optional[Dict]`

Render a single dashboard snapshot.

**Parameters:**
- `dashboard_spec` (dict): Dashboard definition from observability spec with keys:
  - `name` (str): Dashboard name
  - `metrics` (list): Names of metrics to include
  - `refresh_cadence` (str): How often updated (e.g., "real-time", "1-minute", "daily")
  - `audience` (str or list): Role(s) that can see this dashboard
- `current_metrics` (list): List of metric result dicts from metric_calculator
- `audience_role` (str): Role of the user requesting dashboard (for visibility filtering)

**Returns:**
```python
{
    'dashboard_name': str,
    'metrics_on_dashboard': List[Dict],  # Subset of current_metrics
    'role_filtered': bool,  # True if some metrics were hidden
    'refresh_cadence': str,
    'next_refresh_time': ISO8601 str,
    'timestamp': ISO8601 str
} | None  # None if role has no access
```

**Raises:**
- `ValueError`: If audience_role not in dashboard audience list

---

#### `render_all_dashboards(dashboards_list: List[Dict], current_metrics: List[Dict], audience_roles: List[str]) -> Dict[str, Dict]`

Render all dashboards for given roles.

**Parameters:**
- `dashboards_list` (list): List of dashboard_spec dicts from observability spec
- `current_metrics` (list): Current calculated metrics
- `audience_roles` (list): Roles of user(s) requesting dashboards

**Returns:**
```python
{
    'dashboard_name': (dashboard snapshot dict),
    ...
}
```

---

## `alert_router` Skill Interface

**Purpose**: Route alerts to recipients based on role and urgency (integrates with collaboration spec).

### Methods

#### `route_alert(alert: Dict, collaboration_spec: Dict) -> Dict`

Determine recipients for an alert and identify delivery channels.

**Parameters:**
- `alert` (dict): Alert dict from alert_evaluator skill
- `collaboration_spec` (dict): Collaboration spec with keys:
  - `roles` (list): Role definitions
  - `communication_channels` (dict): How each role receives notifications (email, SMS, in-app, etc.)

**Returns:**
```python
{
    'alert_id': str,  # Unique ID for tracking
    'alert_name': str,
    'urgency': str,
    'routing': {
        'role_name': {
            'delivery_channels': List[str],  # ['email', 'sms', 'in-app']
            'routed_at': ISO8601 str
        },
        ...
    },
    'expected_acknowledgment_time': ISO8601 str | None  # Based on urgency
}
```

---

#### `batch_route_alerts(alerts_list: List[Dict], collaboration_spec: Dict) -> List[Dict]`

Route multiple alerts.

**Parameters:**
- `alerts_list` (list): List of alert dicts from alert_evaluator
- `collaboration_spec` (dict): Collaboration spec

**Returns:**
- List of routed alert dicts (as above)

---
