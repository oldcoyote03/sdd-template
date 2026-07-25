# Execution Specification Template

## Overview

This template defines what actions can be taken, how they are executed, when they can occur, and what approvals are required.

## Structure

### Executable Actions

- **Action Name**: What is being done?
- **Preconditions**: What must be true before this action can run?
- **Execution Method**: How is it done? (manual, automated API call, etc.)
- **Constraints**: Amount limits, timing constraints, frequency limits, etc.

### Approval Workflows

- **Who Approves**: Which roles/people must sign off?
- **Approval Conditions**: When is approval automatic vs. required?
- **Escalation Path**: What happens if the primary approver is unavailable?

### Permission & Authorization

- **Permitted Time Windows**: When can this action be taken? (market hours, specific times, continuous)
- **Permission Duration**: Is permission granted permanently or for a time window?
- **Revocation**: How quickly can permission be revoked?

### Error Handling & Rollback

- **Failure Modes**: What can go wrong?
- **Recovery Procedures**: How do we handle failures?
- **Audit Trail**: What gets logged?

## Usage

Execution Agents will read this spec to determine:
- "Is an execution allowed right now?"
- "Do I need approval before proceeding?"
- "How do I execute this, and what should I log?"

Be specific about the conditions and approval paths.
