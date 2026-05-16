"""
audit_log skill: Standardized logging for agent decisions.

This skill ensures every agent decision is logged consistently with
timestamp, reasoning, inputs, outputs, and status. Logs can be queried
by agent, action, or time window for review and analysis.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class AuditLog:
    """Standardized logging for agent decisions and outcomes."""

    def __init__(self, log_file: str = 'audit.log'):
        """
        Initialize the audit log skill.

        Args:
            log_file: Path where logs are written
                      (default: 'audit.log' in current directory)
        """
        self.log_file = log_file
        self.log_entries = []  # In-memory log (also written to disk)

        # Ensure directory exists
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

    def log(self, entry: Dict[str, Any]) -> str:
        """
        Log an agent decision or action.

        Args:
            entry: Decision/action dict with keys:
                - agent (str): Name of agent making decision
                - action (str): What action was taken
                - reasoning (str): Why this decision was made
                - inputs (dict): Input data used in decision
                - outputs (dict): Output/result of decision
                - status (str): 'success', 'pending', 'error', 'rejected'
                - timestamp (str, optional): ISO timestamp (auto-generated if omitted)
                - audit_id (str, optional): Unique ID (auto-generated if omitted)

        Returns:
            audit_id: Unique identifier for this log entry

        Example:
            audit_log = AuditLog('logs/trading_audit.log')
            audit_id = audit_log.log({
                'agent': 'execution',
                'action': 'execute_trade',
                'reasoning': 'Tier 1 setup: Price break with volume',
                'inputs': {'signal': signal, 'rule': rule},
                'outputs': {'trade': {'size': 5000, 'entry': 445.50}},
                'status': 'success'
            })
        """
        # Ensure required fields
        required = ['agent', 'action', 'reasoning', 'inputs', 'outputs', 'status']
        missing = [f for f in required if f not in entry]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        # Add auto-generated fields if not provided
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.utcnow().isoformat() + 'Z'
        if 'audit_id' not in entry:
            entry['audit_id'] = self._generate_audit_id(entry)

        # Store in memory
        self.log_entries.append(entry)

        # Write to disk (append)
        self._write_entry(entry)

        return entry['audit_id']

    def query(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query the audit log by criteria.

        Args:
            criteria: Filter criteria
                - agent (str): Filter by agent name
                - action (str): Filter by action
                - status (str): Filter by status
                - time_from (str): ISO timestamp (return entries >= this time)
                - time_to (str): ISO timestamp (return entries <= this time)
                - audit_id (str): Find specific entry by ID

        Returns:
            List of matching log entries

        Example:
            # All trades executed by execution agent
            entries = audit_log.query({'agent': 'execution', 'action': 'execute_trade'})

            # All rejections in the past hour
            from datetime import datetime, timedelta
            one_hour_ago = (datetime.utcnow() - timedelta(hours=1)).isoformat()
            entries = audit_log.query({'status': 'rejected', 'time_from': one_hour_ago})

            # Find specific entry
            entry = audit_log.query({'audit_id': 'exec_20260516_0945_001'})
        """
        matching = []

        for entry in self.log_entries:
            if self._matches_criteria(entry, criteria):
                matching.append(entry)

        return matching

    def query_by_agent(self, agent_name: str) -> List[Dict[str, Any]]:
        """Get all log entries for a specific agent."""
        return self.query({'agent': agent_name})

    def query_by_action(self, action: str) -> List[Dict[str, Any]]:
        """Get all log entries for a specific action."""
        return self.query({'action': action})

    def query_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Get all log entries with a specific status."""
        return self.query({'status': status})

    def query_time_range(self, time_from: str, time_to: str) -> List[Dict[str, Any]]:
        """Get log entries in a time range (ISO format timestamps)."""
        return self.query({'time_from': time_from, 'time_to': time_to})

    def get_entry(self, audit_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific log entry by audit_id."""
        results = self.query({'audit_id': audit_id})
        return results[0] if results else None

    def summary(self, agent: Optional[str] = None) -> Dict[str, Any]:
        """
        Get a summary of logged activity.

        Args:
            agent: If provided, summarize only for that agent

        Returns:
            Dict with summary stats (counts by status, action, etc.)
        """
        entries = self.log_entries
        if agent:
            entries = [e for e in entries if e.get('agent') == agent]

        summary = {
            'total_entries': len(entries),
            'by_status': {},
            'by_action': {},
            'by_agent': {} if not agent else None,
            'time_range': {
                'first': entries[0].get('timestamp') if entries else None,
                'last': entries[-1].get('timestamp') if entries else None
            }
        }

        for entry in entries:
            # Count by status
            status = entry.get('status', 'unknown')
            summary['by_status'][status] = summary['by_status'].get(status, 0) + 1

            # Count by action
            action = entry.get('action', 'unknown')
            summary['by_action'][action] = summary['by_action'].get(action, 0) + 1

            # Count by agent (if not filtered)
            if not agent:
                agent_name = entry.get('agent', 'unknown')
                summary['by_agent'][agent_name] = summary['by_agent'].get(agent_name, 0) + 1

        return summary

    def export_json(self, output_file: str) -> None:
        """Export all log entries to a JSON file."""
        with open(output_file, 'w') as f:
            json.dump(self.log_entries, f, indent=2)

    def export_csv(self, output_file: str) -> None:
        """Export log entries to CSV (basic format)."""
        import csv

        if not self.log_entries:
            return

        # Get all unique keys across entries
        all_keys = set()
        for entry in self.log_entries:
            all_keys.update(entry.keys())

        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
            writer.writeheader()
            for entry in self.log_entries:
                # Flatten nested dicts for CSV
                flat_entry = {}
                for key, value in entry.items():
                    if isinstance(value, (dict, list)):
                        flat_entry[key] = json.dumps(value)
                    else:
                        flat_entry[key] = value
                writer.writerow(flat_entry)

    def load_from_file(self) -> None:
        """Load existing log entries from disk (append mode)."""
        if not os.path.exists(self.log_file):
            return

        with open(self.log_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        self.log_entries.append(entry)
                    except json.JSONDecodeError:
                        # Skip malformed lines
                        pass

    def _write_entry(self, entry: Dict[str, Any]) -> None:
        """Write a single entry to disk (JSON lines format)."""
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')

    def _matches_criteria(self, entry: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if an entry matches all criteria."""
        for key, value in criteria.items():
            if key == 'time_from':
                # Compare timestamps (ISO format)
                if entry.get('timestamp', '') < value:
                    return False
            elif key == 'time_to':
                # Compare timestamps (ISO format)
                if entry.get('timestamp', '') > value:
                    return False
            elif key == 'audit_id':
                # Exact match on ID
                if entry.get('audit_id') != value:
                    return False
            else:
                # Exact match on other fields
                if entry.get(key) != value:
                    return False

        return True

    def _generate_audit_id(self, entry: Dict[str, Any]) -> str:
        """Generate a unique audit ID from agent, action, and timestamp."""
        agent = entry.get('agent', 'unknown')[:4]  # First 4 chars of agent
        action = entry.get('action', 'unknown')[:4]  # First 4 chars of action
        timestamp = entry.get('timestamp', datetime.utcnow().isoformat())
        # Extract date and time from ISO format
        dt_str = timestamp.replace('-', '').replace(':', '').split('.')[0]  # YYYYMMDDHHMMSS
        return f"{agent}_{action}_{dt_str}"
