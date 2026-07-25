# alert_router Skill

**Purpose**: Route alerts to recipients based on role and urgency (integrates with collaboration spec).

**Used by**: Observability Agent (primary), Collaboration Agent (when managing alert distribution)

---

## Overview

The `alert_router` skill solves a key problem: not all alerts go to all people, and people prefer different notification channels. An emergency (critical alert) goes to email + SMS with a 30-second acknowledgment window. A low-priority alert goes to in-app only.

This skill:

1. **Identifies recipients** from alert spec (which roles should be notified)
2. **Maps to delivery channels** from collaboration spec (email, SMS, in-app, dashboard)
3. **Sets acknowledgment timeout** based on urgency
4. **Returns routed alert** ready for dispatch

**Design principle**: Skill is stateless. The agent manages alert dispatch (actually sending emails, SMSs, etc.) and passes routing information to this skill.

---

## Usage

### Basic Import

```python
from skills.core.observability.alert_router import AlertRouter

# Create skill instance
alert_router = AlertRouter()
```

### Route a Single Alert

```python
# From alert_evaluator skill
alert = {
    'alert_name': 'Daily Loss Limit Reached',
    'triggered': True,
    'urgency': 'critical',
    'recipients': ['Trader', 'Risk Manager']
}

# From collaboration spec
collaboration_spec = {
    'roles': {
        'Trader': {'name': 'Trader', 'escalation': None},
        'Risk Manager': {'name': 'Risk Manager'}
    },
    'communication_channels': {
        'Trader': ['email', 'sms', 'in-app'],
        'Risk Manager': ['email', 'sms']
    }
}

routed = alert_router.route_alert(alert, collaboration_spec)
# Returns:
# {
#     'alert_id': '550e8400-e29b-41d4-a716-446655440000',
#     'alert_name': 'Daily Loss Limit Reached',
#     'urgency': 'critical',
#     'routing': {
#         'Trader': {
#             'delivery_channels': ['email', 'sms', 'in-app'],
#             'routed_at': '2024-05-24T14:32:15Z'
#         },
#         'Risk Manager': {
#             'delivery_channels': ['email', 'sms'],
#             'routed_at': '2024-05-24T14:32:15Z'
#         }
#     },
#     'expected_acknowledgment_time': '2024-05-24T14:32:45Z'  # 30 seconds for critical
# }

# Use routed alert to dispatch notifications
for role, route_info in routed['routing'].items():
    for channel in route_info['delivery_channels']:
        send_notification(channel, alert, role)
```

### Route All Triggered Alerts

```python
# From alert_evaluator
triggered_alerts = [
    {
        'alert_name': 'Daily Loss Limit',
        'urgency': 'critical',
        'recipients': ['Trader', 'Risk Manager']
    },
    {
        'alert_name': 'Setup Alert',
        'urgency': 'high',
        'recipients': ['Trader']
    }
]

routed_alerts = alert_router.batch_route_alerts(triggered_alerts, collaboration_spec)

# Dispatch all
for routed_alert in routed_alerts:
    dispatch_alert(routed_alert)  # Send notifications to all recipients
```

---

## Integration with Other Skills

**Observability Agent workflow:**
```
1. metric_calculator.calculate_all_metrics()
2. alert_evaluator.evaluate_all_conditions()
3. alert_router.batch_route_alerts(triggered_alerts, collaboration_spec)
4. Dispatch notifications based on routed_alerts
```

**Collaboration Agent:**
```
"I have this critical alert. Who needs to know and how?"
  → alert_router.route_alert(alert, collaboration_spec)
  → Dispatch based on routing results
```

---

## Acknowledgment Windows by Urgency

| Urgency | Timeout | Use Case |
|---------|---------|----------|
| **critical** | 30 seconds | Daily loss limit, halt condition |
| **high** | 60 seconds | Setup alert waiting for approval |
| **medium** | 5 minutes | Threshold approaching (not yet hit) |
| **low** | None | Informational (trade closed, etc.) |

---
