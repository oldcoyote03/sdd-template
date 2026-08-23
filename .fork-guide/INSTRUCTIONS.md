# Fork Transition Guide (AI-Assisted)

You are assisting a human to convert sdd-template into a domain-specific fork.

## Input from Human

Before executing the transition, collect answers to these questions:

**Q1**: What domain is this fork for?  
*(Example: "day trading", "personal finance", "homeschooling")*

**Q2**: What are the primary roles in this domain?  
*(Example: "Trader, Risk Manager, Analyst" for trading)*

**Q3**: Where are the operational specs?  
- Already written? (paste or provide link)
- Starting from the templates? (which templates apply?)
- Needs to be created from scratch? (provide high-level description)

**Q4**: Will this repo have agent implementations or just specs?
- Both (specs + agent code)
- Specs only (agents built elsewhere)
- Other?

---

## Transition Steps

### Phase 1: Structural Changes

Execute these file system changes:

1. **Delete template-only artifacts**
   - Delete `docs/template-usage/` directory
   - Keep `.fork-guide/` until the transition is complete; its templates and validator are used in later phases
   - Delete `specs/templates/` directory (optional; can keep as reference)

2. **Rename domain specs folder**
   - Rename `specs/examples/day-trading/` to `specs/[your-domain]/`  
   - Or create `specs/[your-domain]/` if starting from scratch

3. **Preserve reusable infrastructure**
   - Keep `reference/` (contains agent interfaces, feature explanations)
   - Keep `skills/core/` (reusable infrastructure: audit_log, observability, spec_query)

---

### Phase 2: Content Creation

For each primary role from Q2, create a role guide:

1. **Create `docs/[role-slug].md`**  
   - Use `.fork-guide/templates/role-guide-template.md` as a template
   - Fill in what the role is, daily responsibilities, dashboard visibility, decision authority
   - Keep it non-prescriptive; let the domain adapt it

2. **Create `IMPLEMENTATION.md`**
   - Use `.fork-guide/templates/implementation-template.md` as a template
   - Document how to run agents, connect to data sources, start dashboards, run operational cycles
   - This is domain-specific; customize for your domain

3. **Create/Update README.md**
   - Use `.fork-guide/templates/readme-template.md` as a template
   - Replace placeholder [Your Domain] with actual domain name
   - Link to role guides
   - Keep it clean and operational

---

### Phase 3: Spec Completion (if needed)

If specs are not yet written (Q3 = "needs to be created"):

1. **Review spec structure**
   - Open `reference/` to understand the five core features (Strategic, Execution, Observability, Collaboration, Review)
   - Each feature has a corresponding spec file

2. **Populate `specs/[domain]/`**
   - Fill in `strategic.md` with domain-specific objectives, decision frameworks, constraints
   - Fill in `execution.md` with domain actions, preconditions, approval workflows
   - Fill in `observability.md` with monitoring targets, metrics, alert thresholds
   - Fill in `collaboration.md` with role definitions, visibility rules, approval paths
   - Fill in `review.md` with review cadences, analysis frameworks, feedback mechanisms

3. **Validate spec completeness**
   - Run `python .fork-guide/templates/spec-validator.py specs/[your-domain]/`
   - It checks that all 5 specs exist and contain required sections
   - Fix any warnings

---

### Phase 4: Agent Setup (if applicable)

If Q4 = "Both (specs + agent code)":

1. **Create `agents/` directory**
   - Will hold domain-specific agent implementations

2. **Create `skills/domain/` directory**
   - List required domain-specific skills (e.g., market_data_fetcher, trade_executor, position_tracker)
   - Create stub Python modules for each skill

---

## What to Output

Provide the human with:

1. **Updated directory structure** (specs, docs, agents directories as needed)
2. **Populated spec files** (drafts or completed, depending on Q3)
3. **Domain role guides** (from role-guide-template.md, customized)
4. **IMPLEMENTATION.md** (customized for domain)
5. **Updated README.md** (domain-specific)
6. **Summary report** explaining:
   - What was created/changed
   - What the human needs to review or customize
   - What the next steps are (agents implementation, etc.)

---

## Example: Day Trading Fork

### Input from Human
- **Q1**: Day trading
- **Q2**: Trader, Risk Manager, Analyst
- **Q3**: Will use templates as starting point; trader will fill in specific strategies
- **Q4**: Both (specs + agents)

### Output from AI
- ✅ Created `specs/day-trading/` with 5 spec files (initial drafts)
- ✅ Created `docs/trader.md`, `docs/risk-manager.md`, `docs/analyst.md` (non-opinionated templates)
- ✅ Generated `IMPLEMENTATION.md` with sections for agent setup, data feeds, dashboards
- ✅ Updated `README.md` with day-trading-specific intro
- ✅ Marked `docs/template-usage/`, `.fork-guide/`, and `specs/templates/` for deletion during final cleanup
- ✅ Created `skills/domain/` stub with skill categories (market_data, order_execution, etc.)

### Next Steps for Human
- [ ] Edit `specs/day-trading/strategic.md` — add real market structures, entry models, risk rules
- [ ] Review role guides — are they accurate for your team?
- [ ] Edit `IMPLEMENTATION.md` — add specific data feed URLs, deployment instructions
- [ ] Create `agents/` with strategy_agent.py, execution_agent.py, etc.
- [ ] Implementers build domain skills using `skills/domain/` stubs

---

## Notes

- **Specs are the source of truth** — update them as the domain evolves
- **Agent implementations** are separate from specs; agents read and interpret specs
- **Skills are reusable** — core skills in `skills/core/` apply across domains; domain skills go in `skills/domain/`
- **Validation is key** — run spec-validator.py before considering specs "done"
