"""Unit tests for alert_evaluator skill."""

import unittest
from alert_evaluator import AlertEvaluator


class TestAlertEvaluator(unittest.TestCase):
    """Test alert_evaluator skill functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.skill = AlertEvaluator()

    def test_evaluate_condition_daily_loss_limit(self):
        """Test evaluating daily loss limit alert."""
        alert_spec = {
            'name': 'Daily Loss Limit Reached',
            'condition_logic': 'Daily P&L ≤ -$1,000',
            'urgency': 'critical',
            'recipients': ['Trader', 'Risk Manager']
        }
        current_state = {
            'daily_pnl': -1050
        }
        metric_results = [
            {
                'metric_name': 'Daily P&L',
                'value': -1050,
                'baseline': 'Target +$200-$500/day'
            }
        ]

        # Should evaluate (implementation needed)
        result = self.skill.evaluate_condition(alert_spec, current_state, metric_results)
        # Placeholder: result should be dict if triggered, None otherwise

    def test_evaluate_condition_missing_name(self):
        """Test error handling for missing alert name."""
        alert_spec = {
            'condition_logic': 'some logic',
            'urgency': 'high'
        }
        current_state = {}

        with self.assertRaises(KeyError):
            self.skill.evaluate_condition(alert_spec, current_state)

    def test_evaluate_all_conditions(self):
        """Test evaluating multiple alert conditions."""
        alerts_list = [
            {
                'name': 'Daily Loss Limit',
                'condition_logic': 'Daily P&L ≤ -$1,000',
                'urgency': 'critical',
                'recipients': ['Trader']
            },
            {
                'name': 'Win Rate Dropping',
                'condition_logic': 'Rolling win rate < 52%',
                'urgency': 'medium',
                'recipients': ['Trader']
            }
        ]
        current_state = {
            'daily_pnl': -500,
            'rolling_win_rate': 55
        }

        results = self.skill.evaluate_all_conditions(alerts_list, current_state, [])

        # Should return list (possibly empty if no conditions triggered)
        self.assertIsInstance(results, list)


if __name__ == '__main__':
    unittest.main()
