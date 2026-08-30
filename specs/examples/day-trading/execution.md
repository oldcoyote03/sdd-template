# Domain Execution Specification

This draft is intentionally neutral and should be specialized with explicit domain facts or KB input before use in production workflows.

## Executable Actions

### Action: [Primary Action]

**Preconditions**:
- [condition or trigger]
- [required state or prerequisite]
- [approval or readiness check]

**Execution Method**:
- [manual or automated path]
- [fallback or alternate path]

**Constraints**:
- [limiting rule]
- [resource or timing constraint]
- [safety or authorization boundary]

### Action: [Secondary Action]

**Preconditions**:
- [condition]
- [shared prerequisite]

**Execution Method**:
- [how the action is performed]

**Constraints**:
- [rule to maintain control or quality]
- [approval or documentation requirement]

## Approval Workflows

### Approval: [Tier or Trigger]

**Approval**: [who must approve, or none required]
- [condition for approval]
- [SLA or timing expectation]
- [fallback if not approved]

## Permission & Authorization

### Access & Boundaries

- **Active Window**: [time window or operating window]
- **Daily Limits**: [limit, threshold, or escalation rule]
- **Authority**: [who can approve, pause, or override]

## Error Handling & Rollback

### Execution Failure

**Scenario**: [failure mode]
- **Recovery**: [how to recover]
- **Escalation**: [who or what to notify]

### Data Quality or Coordination Issues

**Scenario**: [issue type]
- **Recovery**: [fallback or correction approach]
- **Audit**: [how to record the issue]

## Audit Trail

Every action should be logged with:
- Timestamp
- Responsible actor or system
- Trigger or event
- Result
- Any exception or override
