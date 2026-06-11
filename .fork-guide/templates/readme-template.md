# [Your Domain] Operations

A specification-driven operational system for [your domain], built from the SDD template.

---

## What is This?

This repository runs [your domain] operations using specification-driven design:

- **Specifications** define strategic rules, execution workflows, monitoring targets, collaboration protocols, and feedback loops
- **Agents** interpret specs and make operational decisions
- **Outcomes** are logged and feed back into continuous improvement

The system is organized around five core features:

| Feature | Purpose |
|---------|---------|
| **Strategic** | Decision rules, priorities, and frameworks |
| **Execution** | What actions can be taken, when, by whom, with what approvals |
| **Observability** | What to monitor, alert on, visualize |
| **Collaboration** | Who is involved, what visibility they have, what they must approve |
| **Review** | How outcomes are analyzed and lessons loop back into improvements |

---

## Roles in This System

Choose your role to get started:

- **[Role 1 Name]** → [docs/[role-1].md](docs/[role-1].md) — [1-line description]
- **[Role 2 Name]** → [docs/[role-2].md](docs/[role-2].md) — [1-line description]
- **[Role 3 Name]** → [docs/[role-3].md](docs/[role-3].md) — [1-line description]

---

## Getting Started

### First Time?

1. **Read your role guide** (see Roles section above)
2. **Understand the specs**: Start with `specs/[domain]/strategic.md` (high-level overview)
3. **Review IMPLEMENTATION.md**: See [IMPLEMENTATION.md](IMPLEMENTATION.md) for how the system runs

### For Operators (Day-to-Day Users)

- Monitor alerts and dashboards (described in your role guide)
- Approve or reject actions when required
- Review outcomes at end of day/week (per [Review Spec](specs/[domain]/review.md))

### For Implementers (Building the System)

See [IMPLEMENTATION.md](IMPLEMENTATION.md) for:
- How to build agents
- How to set up data integrations
- How to validate against specs
- How to run operational cycles

### For Spec Authors (Evolving the System)

- Modify specs in `specs/[domain]/` as the domain evolves
- Keep specs versioned (commit to git with clear messages)
- Notify team of significant changes

---

## Key Docs

- **Strategic Spec**: [specs/[domain]/strategic.md](specs/[domain]/strategic.md) — Decision rules and priorities
- **Execution Spec**: [specs/[domain]/execution.md](specs/[domain]/execution.md) — Executable actions and approvals
- **Observability Spec**: [specs/[domain]/observability.md](specs/[domain]/observability.md) — Monitoring and alerts
- **Collaboration Spec**: [specs/[domain]/collaboration.md](specs/[domain]/collaboration.md) — Roles and workflows
- **Review Spec**: [specs/[domain]/review.md](specs/[domain]/review.md) — Analysis and improvement loops

---

## Reference

For more on the template architecture and design patterns:
- See the original template: [https://github.com/[original-repo]](link)
- See `reference/` folder in this repo for agent interfaces and feature explanations

To fork this repository for another domain:
- Visit the original template's `.fork-guide/` folder

---

## Quick Links

- **Dashboards**: [http://localhost:5000](http://localhost:5000) (when running)
- **Audit Logs**: See IMPLEMENTATION.md for audit log access
- **Issues/Feedback**: [Create an issue](https://github.com/[your-repo]/issues)

---

## Questions?

- **"What should I do as [Role]?"** → See [docs/[your-role].md](docs/[your-role].md)
- **"How is the system built?"** → See [IMPLEMENTATION.md](IMPLEMENTATION.md)
- **"Why this rule/workflow?"** → See the relevant spec file
- **"How do I change something?"** → Update the spec, commit, notify team
