# Operational System Architecture

## Overview

This template defines a framework for executing, monitoring, and optimizing ongoing operations across diverse domains (trading, personal finance, homeschooling, and others). The system combines specification-driven design with AI-assisted decision-making, executable automation, and collaborative oversight.

> **Note**: For audience-specific guidance, see [STRUCTURE.md](STRUCTURE.md). This document is a comprehensive reference; choose your path for a guided introduction.

## Core Principles

1. **Template over Prescription**: The template provides structural primitives that domains instantiate through configuration, not a fixed process.
2. **Repository as Source of Truth**: Specifications are versioned, collaborative, and auditable in a central repository.
3. **Format Agnostic**: Canonical markdown specs can be rendered as visuals, indexed in data stores, or consumed by agents without duplication.
4. **Flexible Topology**: Features can connect in different ways depending on domain timescales, triggers, and feedback needs.
5. **Evolutionary Architecture**: Start simple (repository + text); add specialized stores and visuals as bottlenecks emerge.

## Three Operational Layers

### 1. Specification Layer (Repository)

**Purpose**: Define what should happen in an operation.

**Canonical Form**: Structured markdown files organized by the five core features.

**Supplementary Media**: Referenced artifacts (diagrams, data samples, visual media, audio explanations) that augment markdown understanding.

**Characteristics**:
- Versioned and collaborative through repository
- Human-readable and AI-interpretable
- Format-agnostic (can be rendered visually, indexed, etc. on demand)
- Role-based access and approval workflows

### 2. Intelligence Layer (LLM Agents + Skills)

**Purpose**: Interpret specifications contextually and make decisions.

**Components**:
- **Role-specific agents**: Interpret and act on specs for different features (Strategy, Execution, Observability, Collaboration, Review)
- **Pre-defined skills**: Reusable patterns across domains (e.g., pattern recognition, decision evaluation, analysis, reporting)
- **Agent coordination**: Mechanisms for agents to communicate and sequence their actions

**Characteristics**:
- Reads specs as context for decision-making
- Can invoke external APIs for data and execution
- Logs decisions and outcomes for audit trails
- Feeds results back to specs for iteration

### 3. Orchestration Layer (Code + Workflows)

**Purpose**: Execute the operation and manage information flow.

**Components**:
- **Event triggers**: What causes agents to activate (live data updates, scheduled reviews, user actions, approval requests)
- **Workflow engines**: Sequences and coordinates agent invocations
- **API integration**: Calls to live data feeds, execution systems, and external services
- **Audit logging**: Records all decisions, executions, and outcomes
- **State management**: Tracks the operational state for feedback loops

**Characteristics**:
- Stateless where possible (specs are the state)
- Event-driven rather than continuous polling
- Results feed back to repository for versioning and review

## Five Core Features

The template is organized around five core features, each expressed as a specification and implemented through corresponding agents and execution logic. These features are architectural primitives, not separate systems: they work together to define decisions, actions, monitoring, collaboration, and review.

For the authoritative definitions of each feature, see [reference/five-features.md](reference/five-features.md).

In brief:
- **Strategic**: Defines goals, decision rules, constraints, and priorities.
- **Execution**: Defines what actions are allowed, when they may occur, and what approvals are required.
- **Observability**: Defines what should be monitored, what thresholds matter, and how alerts should be routed.
- **Collaboration**: Defines roles, visibility, approvals, and escalation paths.
- **Review & Feedback**: Defines how outcomes are analyzed and how lessons loop back into the system.

## Optional Augmentation Features

These features enhance domains that need them:

### Live Data Analysis

Continuous or near-real-time analysis of incoming data streams against strategic specs.

### Automated Execution

Execution of defined tasks without human intervention, subject to time windows and permission policies.

---

## Directory Structure

```
specs/
├── templates/          # Generic templates for each feature (domain-agnostic)
│   ├── STRATEGIC_TEMPLATE.md
│   ├── EXECUTION_TEMPLATE.md
│   ├── OBSERVABILITY_TEMPLATE.md
│   ├── COLLABORATION_TEMPLATE.md
│   └── REVIEW_TEMPLATE.md
│
└── [domain]/           # Domain-specific instantiations
    ├── strategic.md
    ├── execution.md
    ├── observability.md
    ├── collaboration.md
    ├── review.md
    └── artifacts/      # Supporting media (diagrams, samples, etc.)
```

## Workflow Example: Day Trading

1. **Strategic Spec** defines market structures, entry models, and decision criteria.
2. **Observability Spec** defines markets to monitor and alert conditions.
3. **Observability Agent** monitors live data; when an alert condition is met, it notifies relevant stakeholders (Collaboration Spec).
4. **Execution Spec** defines whether trades can be executed automatically or require approval.
5. **Execution Agent** evaluates the setup against the spec and either executes or requests approval.
6. **Journaling** captures trade metadata automatically; operator adds free-form notes.
7. **Review Spec** defines review cadence (e.g., weekly) and analysis frameworks.
8. **Review Agent** analyzes trade outcomes, identifies patterns, recommends strategy refinements.
9. **Strategy Spec** is updated with feedback; loop continues.

---

## Design Considerations

### Format Evolution

Specifications start as markdown. As needs emerge:
- Visual representations can be generated on-demand from specs.
- Specialized data stores (e.g., Elasticsearch) can index specs for fast querying.
- Multiple formats can coexist without duplicating the canonical source.

### Audit and Accountability

- Repository history tracks all spec changes (who, when, why).
- Orchestration layer logs all agent decisions and executions.
- Collaboration specs define approval chains for transparency.

### Scalability and Coordination

- Agents operate independently unless specs define dependencies.
- Orchestration layer manages event sequencing and state handoffs.
- Specs are immutable inputs to agents; agents produce logs, not changes to specs.

### Extension Points

- New domains: Copy template structure, instantiate specs for that domain.
- New agents: Define how they interpret specs and what actions they take.
- New data sources: Register in Observability Spec; Observability Agent queries them.
- New media types: Reference in markdown; agents/humans fetch as needed.

