# SDD Template: Specification-Driven Operations

A framework for executing, monitoring, and optimizing ongoing operations using specification-driven design and AI-assisted intelligence.

---

## 🚀 **Getting Started**

**Are you using this as a template for a new domain?**

→ See [.fork-guide/INSTRUCTIONS.md](.fork-guide/INSTRUCTIONS.md) for AI-assisted fork guidance  
→ Or [.fork-guide/CHECKLIST.md](.fork-guide/CHECKLIST.md) for manual fork steps

**Are you already in a domain-specific fork?**

→ Read your role guide (e.g., `docs/trader.md`)  
→ See [IMPLEMENTATION.md](IMPLEMENTATION.md) for system setup

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
.fork-guide/                # Fork transition guidance (NOT part of domain forks)
├── INSTRUCTIONS.md         # AI-assisted fork guide
├── CHECKLIST.md            # Manual fork checklist
└── templates/              # Scaffolds for domain forks

ARCHITECTURE.md             # Three-layer architecture model (canonical reference)
STRUCTURE.md                # Template structure and user paths (template reference)

docs/
├── implementers.md         # For those building agents (template reference)
├── operators.md            # For those running the system (template reference)
└── spec-authors.md         # For those writing specs (template reference)

reference/                  # Reference material (kept in domain forks)
├── five-features.md        # The five core features explained
└── agent-interfaces.md     # Agent contracts and interfaces

skills/core/                # Reusable infrastructure (kept in domain forks)
├── audit_log/
├── observability/
└── spec_query/

specs/
├── templates/              # Generic templates (reference)
│   ├── STRATEGIC_TEMPLATE.md
│   ├── EXECUTION_TEMPLATE.md
│   ├── OBSERVABILITY_TEMPLATE.md
│   ├── COLLABORATION_TEMPLATE.md
│   └── REVIEW_TEMPLATE.md
└── examples/
    └── day-trading/        # Example: Day trading instantiation
        ├── strategic.md
        ├── execution.md
        ├── observability.md
        ├── collaboration.md
        ├── review.md
        └── artifacts/      # Supporting media (diagrams, data samples)
```

## How to Use This Template

### For a New Domain (Forking)

To adapt this template for your own domain:

1. **Fork this repository** (on GitHub)
2. **Choose your approach**:
   - **AI-Assisted**: Follow [.fork-guide/INSTRUCTIONS.md](.fork-guide/INSTRUCTIONS.md)
   - **Manual**: Follow [.fork-guide/CHECKLIST.md](.fork-guide/CHECKLIST.md)
3. **Result**: A domain-specific fork ready for agent implementation

### For Template Users (Understanding the Model)

If you want to understand how this template works:

- **Five core features**: See [reference/five-features.md](reference/five-features.md)
- **Architecture**: See [ARCHITECTURE.md](ARCHITECTURE.md)
- **Agent design**: See [docs/implementers.md](docs/implementers.md) and [reference/agent-interfaces.md](reference/agent-interfaces.md)
- **Agent interfaces**: See [reference/agent-interfaces.md](reference/agent-interfaces.md)

### For Developers/AI Agents (Building Implementations)

- Specs are written in **structured markdown**, designed to be both human-readable and machine-interpretable
- Agents read specs as context for decision-making; they don't modify specs (specs are versioned in the repository)
- Orchestration layer logs decisions and outcomes; feedback from logs loops back into periodic spec reviews/updates

## Example: Day Trading

The [specs/examples/day-trading/](specs/examples/day-trading/) directory contains a complete instantiation:

- **[strategic.md](specs/examples/day-trading/strategic.md)**: Market structures, entry models, risk rules
- **[execution.md](specs/examples/day-trading/execution.md)**: Trade execution workflows, approval chains, permission windows
- **[observability.md](specs/examples/day-trading/observability.md)**: Data feeds, alerts, performance metrics
- **[collaboration.md](specs/examples/day-trading/collaboration.md)**: Trader, Risk Manager, Analyst roles
- **[review.md](specs/examples/day-trading/review.md)**: Post-trade journaling, daily/weekly/monthly reviews, feedback loops

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

**To fork this template for your domain:**

1. See [.fork-guide/INSTRUCTIONS.md](.fork-guide/INSTRUCTIONS.md) (AI-assisted) or [.fork-guide/CHECKLIST.md](.fork-guide/CHECKLIST.md) (manual)
2. Follow the transition guide to adapt the template for your domain
3. Result: A domain-specific repo ready for agent implementation

**To understand the template architecture:**

1. Read [reference/five-features.md](reference/five-features.md) for the five core features
2. Read [ARCHITECTURE.md](ARCHITECTURE.md) for the three operational layers
3. Read [docs/implementers.md](docs/implementers.md) for agent design guidance
4. Read [reference/agent-interfaces.md](reference/agent-interfaces.md) for implementation contracts

---

For questions about template design and architecture, see [ARCHITECTURE.md](ARCHITECTURE.md) or [docs/implementers.md](docs/implementers.md).
