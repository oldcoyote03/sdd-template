"""Unit tests for dashboard_manager skill."""

import unittest
from dashboard_manager import DashboardManager


class TestDashboardManager(unittest.TestCase):
    """Test dashboard_manager skill functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.skill = DashboardManager()

    def test_render_dashboard_access_granted(self):
        """Test rendering dashboard for authorized role."""
        dashboard_spec = {
            'name': 'Live Trading',
            'metrics': ['Daily P&L', 'Open Positions'],
            'refresh_cadence': 'real-time',
            'audience': ['Trader']
        }
        current_metrics = [
            {
                'metric_name': 'Daily P&L',
                'value': 300,
                'baseline': '+$200-$500/day'
            }
        ]

        result = self.skill.render_dashboard(dashboard_spec, current_metrics, 'Trader')

        # Verify structure
        self.assertIsNotNone(result)
        self.assertEqual(result['dashboard_name'], 'Live Trading')
        self.assertIn('timestamp', result)

    def test_render_dashboard_access_denied(self):
        """Test rendering dashboard for unauthorized role."""
        dashboard_spec = {
            'name': 'Live Trading',
            'metrics': ['Daily P&L'],
            'refresh_cadence': 'real-time',
            'audience': ['Trader']
        }
        current_metrics = []

        with self.assertRaises(ValueError):
            self.skill.render_dashboard(dashboard_spec, current_metrics, 'Analyst')

    def test_render_all_dashboards(self):
        """Test rendering multiple dashboards for roles."""
        dashboards_list = [
            {
                'name': 'Live Trading',
                'metrics': ['Daily P&L'],
                'refresh_cadence': 'real-time',
                'audience': ['Trader']
            },
            {
                'name': 'Weekly Review',
                'metrics': ['Weekly P&L', 'Win Rate'],
                'refresh_cadence': 'daily',
                'audience': ['Trader', 'Risk Manager']
            }
        ]
        current_metrics = []

        results = self.skill.render_all_dashboards(dashboards_list, current_metrics, ['Trader'])

        # Should return dict of dashboards
        self.assertIsInstance(results, dict)


if __name__ == '__main__':
    unittest.main()
