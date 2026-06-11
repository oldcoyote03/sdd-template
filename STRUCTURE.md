# Choose Your Path

This template serves three distinct audiences. Find your role and start there.

---

## 🎯 **Spec Author Path**

**You are**: A domain expert defining the rules and workflows (strategist, trader, educator, manager)

**Your output**: Markdown specifications that guide operations

**Start here**: [docs/spec-authors.md](docs/spec-authors.md)

**What you'll do**:
- Write strategic specs (decision rules and frameworks)
- Define execution workflows (what actions are allowed, when, by whom)
- Specify monitoring (what data to track, what alerts matter)
- Design collaboration (who is involved, what they see, what they approve)
- Create review processes (how to analyze outcomes and improve)

**Reference**: [specs/templates/](specs/templates/) for templates and [specs/examples/day-trading/](specs/examples/day-trading/) for a complete example

**Timeline**: Start with Strategic spec, flow through the other four in sequence

---

## 🔧 **Implementer Path**

**You are**: An engineer building the agents and orchestration that interprets specs

**Your output**: Agent code and supporting infrastructure that reads specs and executes operations

**Start here**: [docs/implementers.md](docs/implementers.md)

**What you'll do**:
- Understand agent responsibilities (what each agent reads, decides, logs)
- Learn the skills model (reusable modules that agents use)
- Build agents using core skills ([skills/core/](skills/core/))
- Integrate with event bus and orchestration layer
- Implement logging and audit trails

**Reference**: [ARCHITECTURE.md](ARCHITECTURE.md) for system design, [skills/core/interfaces.md](skills/core/interfaces.md) for skill contracts

**Dependencies**: Spec authors should have written specs in [specs/](specs/) before you build agents

---

## 👥 **Operator Path**

**You are**: A person using the system day-to-day (trader, manager, analyst, educator)

**Your output**: Decisions and approvals that keep the operation running

**Start here**: [docs/operators.md](docs/operators.md)

**What you'll do**:
- Monitor alerts and live dashboards
- Approve or reject actions when required
- Drill into decisions and reasoning
- Review reports and feedback
- Provide input for strategy refinement

**Reference**: [docs/operators.md](docs/operators.md) for dashboard guide and interaction patterns

**Prerequisites**: Implementers should have built the system and connected it to data feeds

---

## **Frequent Scenarios**

### "I'm starting a new domain (e.g., personal finance)"

1. Read [docs/spec-authors.md](docs/spec-authors.md)
2. Copy [specs/templates/](specs/templates/) to `specs/personal-finance/`
3. Fill in each spec using templates and trading example as reference
4. Call implementers to build agents for your domain

### "I'm implementing agents for an existing domain"

1. Read [docs/implementers.md](docs/implementers.md)
2. Review specs in [specs/](specs/) for your domain
3. Use core skills from [skills/core/](skills/core/)
4. Build agents following interface contracts in [ARCHITECTURE.md](ARCHITECTURE.md)

### "I'm running the system (trading, managing, etc.)"

1. Read [docs/operators.md](docs/operators.md)
2. Open dashboard and familiarize yourself with alerts and controls
3. Start with low-confidence actions (practice approving/rejecting)
4. Escalate to higher-confidence actions as you get comfortable
5. Review daily/weekly reports to understand outcomes

### "I'm all three roles (team of one)"

That's fine! Just read each guide sequentially and treat them as distinct phases of work:
1. First, write specs (Spec Author mode)
2. Then, build agents (Implementer mode)
3. Finally, operate the system (Operator mode)

Each phase provides separation of concerns and makes your work auditable.

---

## **For Questions**

- **About specs**: See [docs/spec-authors.md](docs/spec-authors.md) and [ARCHITECTURE.md](ARCHITECTURE.md)
- **About agents and skills**: See [docs/implementers.md](docs/implementers.md) and [skills/core/interfaces.md](skills/core/interfaces.md)
- **About operating the system**: See [docs/operators.md](docs/operators.md)
- **About the overall model**: See [ARCHITECTURE.md](ARCHITECTURE.md) and [README.md](README.md)
