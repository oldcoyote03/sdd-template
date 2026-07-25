"""
dashboard_manager skill: Assemble dashboard snapshots from metrics.

This skill enables agents to render dashboard views from metric results,
filtered by audience role and refresh cadence. Dashboards are snapshots
that provide role-appropriate visibility into operations.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta


class DashboardManager:
    """Assemble dashboard snapshots from metric results."""

    def __init__(self):
        """Initialize the skill. No external dependencies needed."""
        pass

    def render_dashboard(
        self,
        dashboard_spec: Dict[str, Any],
        current_metrics: List[Dict[str, Any]],
        audience_role: str
    ) -> Optional[Dict[str, Any]]:
        """
        Render a single dashboard snapshot.

        Args:
            dashboard_spec: Dashboard definition with keys:
                - name (str): Dashboard name
                - metrics (list): Metric names to include
                - refresh_cadence (str): Update frequency
                - audience (str or list): Role(s) with access
            current_metrics: List of metric result dicts
            audience_role: Role requesting dashboard (for access control)

        Returns:
            Dashboard snapshot dict if role has access, None otherwise

        Raises:
            ValueError: If audience_role not authorized
        """
        # TODO: Implement dashboard rendering logic
        # This is a stub; actual implementation filters metrics by role,
        # applies refresh_cadence, and formats for UI

        dashboard_name = dashboard_spec.get('name')
        if not dashboard_name:
            raise KeyError("dashboard_spec must have 'name' key")

        audience = dashboard_spec.get('audience', [])
        if isinstance(audience, str):
            audience = [audience]

        # Check access control
        if audience_role not in audience:
            raise ValueError(f"Role '{audience_role}' not authorized for dashboard '{dashboard_name}'")

        metric_names = dashboard_spec.get('metrics', [])
        refresh_cadence = dashboard_spec.get('refresh_cadence', 'real-time')

        # Placeholder: return structure
        return {
            'dashboard_name': dashboard_name,
            'metrics_on_dashboard': [],  # TODO: filter current_metrics by metric_names
            'role_filtered': False,  # TODO: check if role limits visibility
            'refresh_cadence': refresh_cadence,
            'next_refresh_time': self._calculate_next_refresh(refresh_cadence),
            'timestamp': datetime.utcnow().isoformat()
        }

    def render_all_dashboards(
        self,
        dashboards_list: List[Dict[str, Any]],
        current_metrics: List[Dict[str, Any]],
        audience_roles: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Render all dashboards for given roles.

        Args:
            dashboards_list: List of dashboard_spec dicts
            current_metrics: Current calculated metrics
            audience_roles: Roles requesting dashboards

        Returns:
            Dict mapping dashboard_name -> dashboard snapshot
        """
        dashboards = {}

        for dashboard_spec in dashboards_list:
            dashboard_name = dashboard_spec.get('name', 'unknown')

            # Try to render for each role; include if any role can access
            for role in audience_roles:
                try:
                    snapshot = self.render_dashboard(dashboard_spec, current_metrics, role)
                    if snapshot:
                        dashboards[dashboard_name] = snapshot
                        break  # Got a valid snapshot for this dashboard
                except ValueError:
                    # Role not authorized; try next role
                    continue

        return dashboards

    @staticmethod
    def _calculate_next_refresh(refresh_cadence: str) -> str:
        """
        Calculate next refresh time based on cadence.

        Args:
            refresh_cadence: Cadence string (e.g., 'real-time', '1-minute', 'daily')

        Returns:
            ISO8601 timestamp of next refresh
        """
        now = datetime.utcnow()

        if refresh_cadence == 'real-time':
            delta = timedelta(seconds=1)
        elif refresh_cadence == '1-minute':
            delta = timedelta(minutes=1)
        elif refresh_cadence == '5-minute':
            delta = timedelta(minutes=5)
        elif refresh_cadence == 'daily':
            # Next day at midnight
            next_midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
            return next_midnight.isoformat()
        else:
            # Default to 1 minute
            delta = timedelta(minutes=1)

        return (now + delta).isoformat()
