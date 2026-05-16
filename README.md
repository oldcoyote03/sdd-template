# Operational System Template

A framework for executing, monitoring, and optimizing ongoing operations using specification-driven design and AI-assisted intelligence.

---

## 👋 **First Time Here?**

**Choose your role** to get started:
- **Writing specs?** → [Spec Author Path](STRUCTURE.md#-spec-author-path)
- **Building agents?** → [Implementer Path](STRUCTURE.md#-implementer-path)  
- **Operating the system?** → [Operator Path](STRUCTURE.md#-operator-path)

See [STRUCTURE.md](STRUCTURE.md) for full guidance.

---

## What Is This?

This template helps you run ongoing operations—whether trading, personal finance, homeschooling, or other domains—by structuring them around five core features:

1. **Strategic**: Decision rules and frameworks
2. **Execution**: What actions can be taken, how, and with what approvals
3. **Observability**: What data to monitor and how to alert
4. **Collaboration**: Who is involved, what they see, and what approval they give
5. **Review & Feedback**: How outcomes are analyzed and lessons loop back into improvement

## Architecture

Three operational layers work together:

- **Specification Layer** (Markdown in Repository): Define what should happen
- **Intelligence Layer** (LLM Agents): Interpret specs contextually and make decisions
- **Orchestration Layer** (Code + Workflows): Execute the operation, manage data flow, and log outcomes

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed explanation.

## Directory Structure

```
specs/
├── templates/           # Generic templates (domain-agnostic)
│   ├── STRATEGIC_TEMPLATE.md
│   ├── EXECUTION_TEMPLATE.md
│   ├── OBSERVABILITY_TEMPLATE.md
│   ├── COLLABORATION_TEMPLATE.md
│   └── REVIEW_TEMPLATE.md
│
└── trading/             # Example: Day trading instantiation
    ├── strategic.md
    ├── execution.md
    ├── observability.md
    ├── collaboration.md
    ├── review.md
    └── artifacts/       # Supporting media (diagrams, data samples, etc.)
```

## How to Use This Template

### For a New Domain

1. **Copy the template structure**: `specs/[your-domain]/` directory
2. **Fill in each spec**:
   - Start with [STRATEGIC_TEMPLATE.md](specs/templates/STRATEGIC_TEMPLATE.md) → fill in your strategy
   - Then [EXECUTION_TEMPLATE.md](specs/templates/EXECUTION_TEMPLATE.md) → fill in your executable actions
   - Then [OBSERVABILITY_TEMPLATE.md](specs/templates/OBSERVABILITY_TEMPLATE.md) → define what to monitor
   - Then [COLLABORATION_TEMPLATE.md](specs/templates/COLLABORATION_TEMPLATE.md) → define roles and approvals
   - Finally [REVIEW_TEMPLATE.md](specs/templates/REVIEW_TEMPLATE.md) → define feedback loops

3. **Add supporting artifacts**: Place diagrams, data samples, or other media in `[your-domain]/artifacts/`

4. **Reference the example**: Look at [specs/trading/](specs/trading/) for a concrete instantiation; use it as inspiration but customize for your domain

### For Developers/AI Agents

- Specs are written in **structured markdown**, designed to be both human-readable and machine-interpretable
- Agents read specs as context for decision-making; they don't modify specs (specs are versioned in the repository)
- Orchestration layer logs decisions and outcomes; feedback from logs loops back into periodic spec reviews/updates

## Example: Day Trading

The [specs/trading/](specs/trading/) directory contains a complete instantiation:

- **[strategic.md](specs/trading/strategic.md)**: Market structures, entry models, risk rules
- **[execution.md](specs/trading/execution.md)**: Trade execution workflows, approval chains, permission windows
- **[observability.md](specs/trading/observability.md)**: Data feeds, alerts, performance metrics
- **[collaboration.md](specs/trading/collaboration.md)**: Trader, Risk Manager, Analyst roles
- **[review.md](specs/trading/review.md)**: Post-trade journaling, daily/weekly/monthly reviews, feedback loops

This example demonstrates how the template handles:
- Real-time data monitoring and alerts
- Automated execution with human oversight
- Approval workflows and permission boundaries
- Multi-role collaboration
- Feedback loops that improve strategy over time

## Key Principles

- **Format Agnostic**: Markdown specs can be rendered as visuals, indexed in data stores, or consumed by agents without duplicating the source
- **Repository as Source of Truth**: All specs are versioned, collaborative, and auditable
- **Flexible Topology**: Features can connect differently depending on domain timescales and operational needs
- **Evolutionary Architecture**: Start simple (repo + text); add specialized stores or visual layers as needs emerge
- **Closed Feedback Loops**: Review mechanisms ensure that operational outcomes inform strategy refinement

## Next Steps

1. Choose a domain (trading, personal finance, homeschooling, other)
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand the model
3. Copy the spec structure and fill in your domain-specific specs
4. Reference [specs/trading/](specs/trading/) for an example if needed
5. Build orchestration logic (agents, workflows) that reads your specs and executes your operation

---

For questions or to extend the template, see [ARCHITECTURE.md](ARCHITECTURE.md) for design guidance.
