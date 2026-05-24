"""Unit tests for metric_calculator skill."""

import unittest
from metric_calculator import MetricCalculator


class TestMetricCalculator(unittest.TestCase):
    """Test metric_calculator skill functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.skill = MetricCalculator()

    def test_calculate_metric_daily_pnl(self):
        """Test calculating Daily P&L metric."""
        metric_spec = {
            'name': 'Daily P&L',
            'calculation': 'sum of all closed trade profits/losses',
            'baseline': 'target is +$200-$500/day; stop if -$1,000'
        }
        raw_data = {
            'closed_trades': [
                {'profit': 250},
                {'profit': -50},
                {'profit': 100}
            ]
        }

        result = self.skill.calculate_metric(metric_spec, raw_data)

        # Verify structure
        self.assertIn('metric_name', result)
        self.assertIn('value', result)
        self.assertIn('baseline', result)
        self.assertIn('timestamp', result)
        self.assertEqual(result['metric_name'], 'Daily P&L')

    def test_calculate_metric_missing_name(self):
        """Test error handling for missing metric name."""
        metric_spec = {
            'calculation': 'sum',
            'baseline': 'target > 0'
        }
        raw_data = {}

        with self.assertRaises(KeyError):
            self.skill.calculate_metric(metric_spec, raw_data)

    def test_calculate_all_metrics(self):
        """Test calculating multiple metrics."""
        metrics_list = [
            {
                'name': 'Daily P&L',
                'calculation': 'sum of trades',
                'baseline': '+$200-$500'
            },
            {
                'name': 'Win Rate',
                'calculation': 'winners / total trades',
                'baseline': '≥ 55%'
            }
        ]
        raw_data = {
            'closed_trades': [
                {'profit': 100, 'winner': True},
                {'profit': -50, 'winner': False}
            ]
        }

        results = self.skill.calculate_all_metrics(metrics_list, raw_data, {})

        # Should return results for all metrics
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['metric_name'], 'Daily P&L')
        self.assertEqual(results[1]['metric_name'], 'Win Rate')


if __name__ == '__main__':
    unittest.main()
