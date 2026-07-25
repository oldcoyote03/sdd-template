"""
Unit tests for audit_log skill.
"""

import unittest
import os
import json
import tempfile
from datetime import datetime, timedelta
from audit_log import AuditLog


class TestAuditLog(unittest.TestCase):
    """Test audit_log skill functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Use temporary file for each test
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.log')
        self.log_file_path = self.temp_file.name
        self.temp_file.close()
        self.audit_log = AuditLog(self.log_file_path)

    def tearDown(self):
        """Clean up test files."""
        if os.path.exists(self.log_file_path):
            os.remove(self.log_file_path)

    def test_log_entry_created(self):
        """Test logging a basic entry."""
        audit_id = self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'Tier 1 setup detected',
            'inputs': {'signal': 'price_break', 'tier': 1},
            'outputs': {'trade_id': '123', 'size': 5000},
            'status': 'success'
        })

        # Should return an audit_id
        self.assertIsNotNone(audit_id)
        self.assertIsInstance(audit_id, str)

        # Entry should be in memory
        self.assertEqual(len(self.audit_log.log_entries), 1)
        entry = self.audit_log.log_entries[0]
        self.assertEqual(entry['agent'], 'execution')
        self.assertEqual(entry['status'], 'success')

    def test_log_auto_timestamp(self):
        """Test that timestamp is auto-generated."""
        audit_id = self.audit_log.log({
            'agent': 'test',
            'action': 'test_action',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        entry = self.audit_log.get_entry(audit_id)
        self.assertIn('timestamp', entry)
        # Should be ISO format with Z suffix
        self.assertTrue(entry['timestamp'].endswith('Z'))

    def test_log_auto_audit_id(self):
        """Test that audit_id is auto-generated."""
        audit_id = self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        self.assertIsNotNone(audit_id)
        entry = self.audit_log.get_entry(audit_id)
        self.assertEqual(entry['audit_id'], audit_id)

    def test_log_missing_required_fields(self):
        """Test that missing required fields raise error."""
        with self.assertRaises(ValueError):
            self.audit_log.log({
                'agent': 'test',
                # Missing other required fields
                'status': 'success'
            })

    def test_query_by_agent(self):
        """Test querying entries by agent."""
        self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'observability',
            'action': 'publish_alert',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        # Query for execution agent
        results = self.audit_log.query_by_agent('execution')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['agent'], 'execution')

    def test_query_by_action(self):
        """Test querying entries by action."""
        self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'execution',
            'action': 'request_approval',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'pending'
        })

        # Query for execute_trade action
        results = self.audit_log.query_by_action('execute_trade')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['action'], 'execute_trade')

    def test_query_by_status(self):
        """Test querying entries by status."""
        self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'rejected'
        })

        # Query for success
        results = self.audit_log.query_by_status('success')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['status'], 'success')

    def test_query_time_range(self):
        """Test querying entries by time range."""
        now = datetime.utcnow()
        past = (now - timedelta(hours=1)).isoformat() + 'Z'
        future = (now + timedelta(hours=1)).isoformat() + 'Z'

        self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        # Query for entries in range (should find our entry)
        results = self.audit_log.query_time_range(past, future)
        self.assertEqual(len(results), 1)

        # Query for entries before our entry (should find none)
        past_past = (now - timedelta(hours=2)).isoformat() + 'Z'
        past_now = (now - timedelta(minutes=1)).isoformat() + 'Z'
        results = self.audit_log.query_time_range(past_past, past_now)
        self.assertEqual(len(results), 0)

    def test_get_entry(self):
        """Test getting a specific entry by audit_id."""
        audit_id = self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        entry = self.audit_log.get_entry(audit_id)
        self.assertIsNotNone(entry)
        self.assertEqual(entry['audit_id'], audit_id)

    def test_summary(self):
        """Test generating a summary of logged activity."""
        self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'execution',
            'action': 'request_approval',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'pending'
        })

        summary = self.audit_log.summary()

        self.assertEqual(summary['total_entries'], 3)
        self.assertEqual(summary['by_status']['success'], 2)
        self.assertEqual(summary['by_status']['pending'], 1)
        self.assertEqual(summary['by_action']['execute_trade'], 2)
        self.assertEqual(summary['by_action']['request_approval'], 1)
        self.assertEqual(summary['by_agent']['execution'], 3)

    def test_summary_filtered_by_agent(self):
        """Test summary filtered by agent."""
        self.audit_log.log({
            'agent': 'execution',
            'action': 'execute_trade',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })
        self.audit_log.log({
            'agent': 'observability',
            'action': 'publish_alert',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        summary = self.audit_log.summary(agent='execution')

        self.assertEqual(summary['total_entries'], 1)
        self.assertEqual(summary['by_action']['execute_trade'], 1)
        self.assertIsNone(summary['by_agent'])  # Not included when filtered

    def test_export_json(self):
        """Test exporting to JSON."""
        self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {'key': 'value'},
            'outputs': {'result': 'ok'},
            'status': 'success'
        })

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json_file = f.name

        try:
            self.audit_log.export_json(json_file)

            with open(json_file, 'r') as f:
                data = json.load(f)

            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['agent'], 'test')
        finally:
            if os.path.exists(json_file):
                os.remove(json_file)

    def test_persists_to_disk(self):
        """Test that entries are persisted to disk."""
        audit_id = self.audit_log.log({
            'agent': 'test',
            'action': 'test',
            'reasoning': 'test',
            'inputs': {},
            'outputs': {},
            'status': 'success'
        })

        # Verify file was written
        self.assertTrue(os.path.exists(self.log_file_path))

        # Verify we can read it back
        with open(self.log_file_path, 'r') as f:
            line = f.readline()
            entry = json.loads(line)
            self.assertEqual(entry['audit_id'], audit_id)


if __name__ == '__main__':
    unittest.main()
