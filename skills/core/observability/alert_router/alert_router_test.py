"""Unit tests for alert_router skill."""

import unittest
from alert_router import AlertRouter


class TestAlertRouter(unittest.TestCase):
    """Test alert_router skill functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.skill = AlertRouter()

    def test_route_alert_critical(self):
        """Test routing a critical alert."""
        alert = {
            'alert_name': 'Daily Loss Limit Reached',
            'triggered': True,
            'urgency': 'critical',
            'recipients': ['Trader', 'Risk Manager']
        }
        collaboration_spec = {
            'roles': {
                'Trader': {'name': 'Trader'},
                'Risk Manager': {'name': 'Risk Manager'}
            },
            'communication_channels': {
                'Trader': ['email', 'sms', 'in-app'],
                'Risk Manager': ['email', 'sms']
            }
        }

        result = self.skill.route_alert(alert, collaboration_spec)

        # Verify structure
        self.assertIn('alert_id', result)
        self.assertIn('routing', result)
        self.assertEqual(result['alert_name'], 'Daily Loss Limit Reached')
        self.assertEqual(result['urgency'], 'critical')
        self.assertIsNotNone(result['expected_acknowledgment_time'])

    def test_route_alert_low_urgency(self):
        """Test routing a low-urgency alert."""
        alert = {
            'alert_name': 'Trade Hit Stop Loss',
            'triggered': True,
            'urgency': 'low',
            'recipients': ['Trader']
        }
        collaboration_spec = {
            'roles': {'Trader': {}},
            'communication_channels': {}
        }

        result = self.skill.route_alert(alert, collaboration_spec)

        # Low urgency alerts should have no acknowledgment timeout
        self.assertIsNone(result['expected_acknowledgment_time'])

    def test_batch_route_alerts(self):
        """Test routing multiple alerts."""
        alerts_list = [
            {
                'alert_name': 'Daily Loss Limit',
                'triggered': True,
                'urgency': 'critical',
                'recipients': ['Trader']
            },
            {
                'alert_name': 'Setup Alert',
                'triggered': True,
                'urgency': 'high',
                'recipients': ['Trader']
            }
        ]
        collaboration_spec = {
            'roles': {'Trader': {}},
            'communication_channels': {}
        }

        results = self.skill.batch_route_alerts(alerts_list, collaboration_spec)

        # Should return routed alerts for all inputs
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['alert_name'], 'Daily Loss Limit')
        self.assertEqual(results[1]['alert_name'], 'Setup Alert')


if __name__ == '__main__':
    unittest.main()
