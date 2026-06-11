"""
metric_calculator skill: Calculate metrics from raw data and compare against baselines.

This skill enables agents to compute operational metrics (P&L, win rate, etc.)
from raw data and compare them against target baselines. Metrics are stateless—
the agent manages state (historical data) and passes it to this skill.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


class MetricCalculator:
    """Calculate metrics from raw data and compare against baselines."""

    def __init__(self):
        """Initialize the skill. No external dependencies needed."""
        pass

    def calculate_metric(
        self,
        metric_spec: Dict[str, Any],
        raw_data: Dict[str, Any],
        historical_baseline: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculate a single metric and compare against baseline.

        Args:
            metric_spec: Metric definition with keys:
                - name (str): Metric name
                - calculation (str): How to calculate
                - baseline (str or dict): Reference baseline
            raw_data: Current data needed for calculation
            historical_baseline: Previous values for trend analysis

        Returns:
            Dict with metric_name, value, baseline, comparison, trend, timestamp

        Raises:
            ValueError: If calculation cannot be performed
            KeyError: If required fields missing
        """
        # TODO: Implement metric calculation logic
        # This is a stub; actual implementation varies by metric type
        # See specs/examples/day-trading/observability.md for examples of metric definitions

        metric_name = metric_spec.get('name')
        if not metric_name:
            raise KeyError("metric_spec must have 'name' key")

        baseline = metric_spec.get('baseline')
        if not baseline:
            raise KeyError("metric_spec must have 'baseline' key")

        # Placeholder: return structure
        return {
            'metric_name': metric_name,
            'value': None,  # TODO: calculate from raw_data
            'baseline': baseline,
            'comparison': None,  # TODO: 'above', 'below', 'within'
            'trend': None,  # TODO: from historical_baseline
            'timestamp': datetime.utcnow().isoformat()
        }

    def calculate_all_metrics(
        self,
        metrics_list: List[Dict[str, Any]],
        raw_data_dict: Dict[str, Any],
        historical_baselines: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Calculate all metrics in a spec against current data.

        Args:
            metrics_list: List of metric_spec dicts
            raw_data_dict: All available current data
            historical_baselines: Previous metric values

        Returns:
            List of metric result dicts
        """
        results = []
        for metric_spec in metrics_list:
            try:
                result = self.calculate_metric(
                    metric_spec,
                    raw_data_dict,
                    historical_baselines
                )
                results.append(result)
            except (ValueError, KeyError) as e:
                # Log error but continue with other metrics
                results.append({
                    'metric_name': metric_spec.get('name', 'unknown'),
                    'error': str(e),
                    'timestamp': datetime.utcnow().isoformat()
                })
        return results
