"""
alert_evaluator skill: Evaluate alert conditions against current state.

This skill enables agents to check if alert conditions are met given current
operational state and metric results. Alerts are emitted when conditions trigger.
Skill is stateless; the agent manages alert history.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class AlertEvaluator:
    """Evaluate alert conditions against current state and emit alerts."""

    def __init__(self):
        """Initialize the skill. No external dependencies needed."""
        pass

    def evaluate_condition(
        self,
        alert_spec: Dict[str, Any],
        current_state: Dict[str, Any],
        metric_results: List[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Check if a single alert condition is triggered.

        Args:
            alert_spec: Alert definition with keys:
                - name (str): Alert name
                - condition_logic (str): How to evaluate
                - urgency (str): 'critical' | 'high' | 'medium' | 'low'
                - recipients (list): Role names
            current_state: Current operational state
            metric_results: Results from metric_calculator skill

        Returns:
            Alert dict if triggered, None otherwise

        Raises:
            ValueError: If condition_logic cannot be parsed
        """
        # TODO: Implement condition evaluation logic
        # This is a stub; actual implementation parses condition_logic
        # See specs/trading/observability.md for examples

        alert_name = alert_spec.get('name')
        if not alert_name:
            raise KeyError("alert_spec must have 'name' key")

        condition_logic = alert_spec.get('condition_logic')
        if not condition_logic:
            raise KeyError("alert_spec must have 'condition_logic' key")

        urgency = alert_spec.get('urgency', 'medium')
        recipients = alert_spec.get('recipients', [])

        # Placeholder: return None (not triggered)
        # Real implementation would evaluate condition_logic against current_state + metric_results
        return None

    def evaluate_all_conditions(
        self,
        alerts_list: List[Dict[str, Any]],
        current_state: Dict[str, Any],
        metric_results: List[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Evaluate all alert conditions in a spec.

        Args:
            alerts_list: List of alert_spec dicts
            current_state: Current operational state
            metric_results: Calculated metric results

        Returns:
            List of triggered alert dicts (empty if none triggered)
        """
        if metric_results is None:
            metric_results = []

        triggered_alerts = []
        for alert_spec in alerts_list:
            try:
                alert = self.evaluate_condition(
                    alert_spec,
                    current_state,
                    metric_results
                )
                if alert:
                    triggered_alerts.append(alert)
            except (ValueError, KeyError) as e:
                # Log error but continue with other alerts
                triggered_alerts.append({
                    'alert_name': alert_spec.get('name', 'unknown'),
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                })

        return triggered_alerts
