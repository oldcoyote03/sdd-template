# Agent Interfaces and Contracts

This document defines the interfaces that agents should implement to coordinate with other agents and the orchestration layer.

---

## Base Agent Interface

All agents should implement this base interface:

```python
class Agent:
    """Base interface for all operational agents."""
    
    def __init__(self, spec_path: str, skills: Dict[str, Skill]):
        """
        Initialize agent with spec and available skills.
        
        Args:
            spec_path: Path to the spec file this agent reads
            skills: Dictionary of skill instances available to this agent
        """
        pass
    
    def read_spec(self) -> Dict:
        """
        Read and parse the agent's spec file.
        
        Returns:
            Parsed spec as dict
            
        Raises:
            SpecNotFound: If spec file doesn't exist
            SpecInvalid: If spec format is invalid
        """
        pass
    
    def handle_event(self, event: Event) -> Result:
        """
        Process an incoming event based on spec.
        
        Args:
            event: Event to handle (data update, alert, approval, etc.)
            
        Returns:
            Result with decision, action, and logs
        """
        pass
    
    def log_decision(self, decision: Dict) -> None:
        """
        Log a decision for audit trail.
        
        Args:
            decision: Dict with decision context, reasoning, action
        """
        pass
```

---

## Specific Agent Interfaces

### Strategy Agent

```python
class StrategyAgent(Agent):
    """
    Maintains and refines strategic direction.
    
    Reads: Strategic spec
    Receives: Review feedback, operational outcomes
    Sends: Strategic guidance to other agents
    """
    
    def explain_strategy(self, context: str) -> str:
        """
        Explain current strategy to other agents or humans.
        
        Args:
            context: Context for explanation (e.g., "entry decision", "market bias")
            
        Returns:
            Explanation of current strategy rule/framework
        """
        pass
    
    def identify_refinement_opportunities(self, feedback: List[Dict]) -> List[Dict]:
        """
        Identify patterns in feedback that suggest spec refinement.
        
        Args:
            feedback: List of feedback items from Review Agent
            
        Returns:
            List of proposed refinements with rationale
        """
        pass
    
    def validate_consistency(self) -> List[str]:
        """
        Check consistency between Strategic spec and other specs.
        
        Returns:
            List of inconsistencies found (empty if consistent)
        """
        pass
```

### Execution Agent

```python
class ExecutionAgent(Agent):
    """
    Decides when and how to execute actions.
    
    Reads: Execution spec, Strategic spec, Collaboration spec
    Receives: Observability alerts, Collaboration approvals
    Sends: Execution requests, approval requests
    """
    
    def evaluate_readiness(self, alert: Event) -> bool:
        """
        Evaluate if action conditions are met per Execution spec.
        
        Args:
            alert: Alert/signal from Observability Agent
            
        Returns:
            True if ready to execute (or request approval)
        """
        pass
    
    def request_approval(self, action: Dict) -> str:
        """
        Request approval from appropriate role.
        
        Args:
            action: Action requiring approval
            
        Returns:
            Approval request ID
        """
        pass
    
    def execute_action(self, action: Dict, approval: Optional[str] = None) -> Result:
        """
        Execute action per Execution spec.
        
        Args:
            action: Action to execute
            approval: Approval ID (if required and obtained)
            
        Returns:
            Execution result with outcome and logs
        """
        pass
```

### Observability Agent

```python
class ObservabilityAgent(Agent):
    """
    Monitors data and generates alerts.
    
    Reads: Observability spec, Strategic spec
    Receives: Live data feeds
    Sends: Alerts to Collaboration Agent, metrics to dashboards
    """
    
    def ingest_data(self, data: Dict) -> None:
        """
        Ingest incoming data from data source.
        
        Args:
            data: Raw data from external feed
        """
        pass
    
    def calculate_metrics(self) -> Dict:
        """
        Calculate all metrics defined in Observability spec.
        
        Returns:
            Dict of metric_name -> value
        """
        pass
    
    def evaluate_alert_conditions(self) -> List[Event]:
        """
        Evaluate all alert conditions from Observability spec.
        
        Returns:
            List of alert events (empty if no conditions met)
        """
        pass
    
    def publish_dashboard(self, role: str) -> Dict:
        """
        Generate dashboard data for a specific role.
        
        Args:
            role: Role for which to generate dashboard
            
        Returns:
            Dashboard data structure
        """
        pass
```

### Collaboration Agent

```python
class CollaborationAgent(Agent):
    """
    Routes information and enforces approval workflows.
    
    Reads: Collaboration spec
    Receives: Alerts from Observability, approval requests from Execution
    Sends: Notifications to roles, approval status to other agents
    """
    
    def determine_visibility(self, item: Dict, role: str) -> bool:
        """
        Determine if role should see a piece of information.
        
        Args:
            item: Information item (alert, metric, etc.)
            role: Role to check visibility for
            
        Returns:
            True if role should see this item
        """
        pass
    
    def route_alert(self, alert: Event) -> str:
        """
        Route alert to appropriate roles per Collaboration spec.
        
        Args:
            alert: Alert to route
            
        Returns:
            Routing ID for tracking
        """
        pass
    
    def request_approval(self, action: Dict, timeout_sec: int) -> str:
        """
        Request approval from appropriate role with timeout.
        
        Args:
            action: Action requiring approval
            timeout_sec: Seconds to wait for approval
            
        Returns:
            Approval request ID
        """
        pass
    
    def handle_approval_response(self, request_id: str, response: str, role: str) -> None:
        """
        Process approval response from role.
        
        Args:
            request_id: Approval request ID
            response: "approve" or "reject"
            role: Role providing approval
        """
        pass
    
    def get_approval_status(self, request_id: str) -> Dict:
        """
        Get status of approval request.
        
        Args:
            request_id: Approval request ID
            
        Returns:
            Dict with status: "pending", "approved", "rejected", "timeout"
        """
        pass
```

### Review Agent

```python
class ReviewAgent(Agent):
    """
    Analyzes outcomes and generates feedback.
    
    Reads: Review spec, Historical specs, Outcome logs
    Receives: End-of-cycle trigger
    Sends: Analysis reports, feedback to Strategy Agent
    """
    
    def trigger_review(self, cadence: str) -> None:
        """
        Trigger review at specified cadence.
        
        Args:
            cadence: "daily", "weekly", "monthly", etc.
        """
        pass
    
    def analyze_outcomes(self, period: str) -> Dict:
        """
        Analyze outcomes for period per Review spec.
        
        Args:
            period: Time period to analyze (e.g., "2024-01-15 to 2024-01-19")
            
        Returns:
            Analysis results (metrics, patterns, insights)
        """
        pass
    
    def generate_feedback(self, analysis: Dict) -> List[Dict]:
        """
        Generate feedback recommendations based on analysis.
        
        Args:
            analysis: Analysis results
            
        Returns:
            List of feedback items with spec references and rationale
        """
        pass
    
    def generate_report(self, analysis: Dict, feedback: List[Dict]) -> str:
        """
        Generate human-readable review report.
        
        Args:
            analysis: Analysis results
            feedback: Feedback recommendations
            
        Returns:
            Report as formatted string or HTML
        """
        pass
```

---

## Skill Interface

All skills should implement:

```python
class Skill:
    """Base interface for reusable operational skills."""
    
    def __init__(self, name: str, config: Dict = None):
        """
        Initialize skill with name and config.
        
        Args:
            name: Unique skill name
            config: Optional configuration dict
        """
        pass
    
    def execute(self, **kwargs) -> Result:
        """
        Execute skill with given parameters.
        
        Args:
            **kwargs: Skill-specific parameters
            
        Returns:
            Result with outcome and logs
        """
        pass
    
    def validate_params(self, **kwargs) -> Tuple[bool, Optional[str]]:
        """
        Validate parameters before execution.
        
        Args:
            **kwargs: Parameters to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
```

### Example Skills

```python
class AuditLogSkill(Skill):
    """Log decisions for audit trail."""
    
    def execute(self, decision: Dict) -> Result:
        """Log a decision with timestamp and context."""
        pass

class SpecQuerySkill(Skill):
    """Query and parse spec files."""
    
    def execute(self, spec_path: str, query: str) -> Result:
        """Query spec for specific content."""
        pass

class AlertEvaluatorSkill(Skill):
    """Evaluate if alert conditions are met."""
    
    def execute(self, condition: Dict, metrics: Dict) -> Result:
        """Evaluate alert condition against current metrics."""
        pass
```

---

## Event Interface

```python
class Event:
    """Event triggering agent action."""
    
    def __init__(self, event_type: str, source: str, data: Dict, timestamp: float):
        """
        Initialize event.
        
        Args:
            event_type: "data_update", "alert", "approval", "scheduled", etc.
            source: Agent or system that generated event
            data: Event-specific data
            timestamp: Unix timestamp of event
        """
        self.event_type = event_type
        self.source = source
        self.data = data
        self.timestamp = timestamp
```

---

## Result Interface

```python
class Result:
    """Result of agent action or skill execution."""
    
    def __init__(self, success: bool, outcome: Dict, logs: List[str], error: Optional[str] = None):
        """
        Initialize result.
        
        Args:
            success: Whether action succeeded
            outcome: Action-specific outcome data
            logs: List of log messages
            error: Error message if not successful
        """
        self.success = success
        self.outcome = outcome
        self.logs = logs
        self.error = error
```

---

## Core Skills (in skills/core/)

### audit_log/

Provides logging capabilities to all agents.

```python
# Usage in any agent
self.audit_log.execute(decision={
    'agent': 'ExecutionAgent',
    'action': 'execute_trade',
    'params': {...},
    'timestamp': time.time()
})
```

### observability/

Provides alert evaluation and dashboarding capabilities.

```python
# Usage in Observability Agent
self.alert_evaluator.execute(
    condition={'type': 'break_above', 'price': 445.50, 'tolerance': 0.01},
    metrics={'current_price': 445.65, 'volume': 2.5M}
)
```

### spec_query/

Provides spec reading and parsing capabilities.

```python
# Usage in any agent
self.spec_query.execute(
    spec_path='specs/[domain]/strategic.md',
    query='tier_1_setup_definition'
)
```

---

## How to Implement a Custom Agent

1. Inherit from `Agent` base class
2. Implement required methods
3. Use skills from `skills/core/` and `skills/domain/`
4. Log all decisions via `AuditLogSkill`
5. Send/receive events to/from other agents
6. Never modify specs (specs are immutable)

Example:

```python
from skills.core.audit_log import AuditLogSkill
from agents import Agent, Event, Result

class MyAgent(Agent):
    def __init__(self, spec_path: str):
        super().__init__(spec_path)
        self.audit_log = AuditLogSkill('audit_log')
    
    def handle_event(self, event: Event) -> Result:
        self.read_spec()
        
        # Process event
        decision = self._make_decision(event)
        
        # Log decision
        self.audit_log.execute(decision=decision)
        
        # Return result
        return Result(
            success=True,
            outcome={'action': 'executed'},
            logs=['Decision logged']
        )
    
    def _make_decision(self, event: Event) -> Dict:
        # Your logic here
        pass
```

---

## References

- For agent responsibilities and design patterns: See [docs/implementers.md](../docs/implementers.md)
- For five features: See [five-features.md](five-features.md)
