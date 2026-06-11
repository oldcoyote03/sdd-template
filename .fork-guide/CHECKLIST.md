# Fork Transition Checklist (Manual)

Use this if you prefer to fork the template without AI assistance.

## Setup

- [ ] Fork sdd-template on GitHub
- [ ] Clone your fork locally: `git clone https://github.com/[you]/[your-domain-fork].git`
- [ ] Create a setup branch: `git checkout -b setup/domain-fork`

## Identify Your Domain

Before proceeding, answer these questions:

- [ ] **Domain name**: What is this fork for? (e.g., "day trading", "personal finance")
- [ ] **Roles**: Who will use this system? List 2-3 primary roles (e.g., "Trader, Risk Manager, Analyst")
- [ ] **Specs status**: Do you have specs written, or will you use the templates?
- [ ] **Agents**: Will you implement agents in this repo, or build them elsewhere?

## Cleanup: Remove Template Artifacts

These files/folders are guidance for template users only. Delete them to clean up your domain fork:

**Root-level template documentation** (replace with domain-specific docs):
- [ ] Delete `ARCHITECTURE.md` (use `reference/` for architecture questions instead)
- [ ] Delete `STRUCTURE.md` (not applicable to domain fork)
- [ ] Delete `docs/spec-authors.md` (use actual specs, not templates)
- [ ] Delete `docs/implementers.md` (use `IMPLEMENTATION.md` instead)
- [ ] Delete `docs/operators.md` (replace with domain role guides)

**Fork transition guides** (only for template repo):
- [ ] Delete `.fork-guide/` directory (fork transition guide — not needed after forking)

## Specs: Rename and Populate

- [ ] Rename `specs/examples/day-trading/` to `specs/[your-domain]/`
  - Or delete and create `specs/[your-domain]/` with fresh copies from `specs/templates/`

- [ ] Edit each spec in `specs/[your-domain]/`:
  - [ ] `strategic.md` — add your domain's objectives, decision frameworks, constraints
  - [ ] `execution.md` — define your domain's executable actions and approval workflows
  - [ ] `observability.md` — list what you monitor and alert on
  - [ ] `collaboration.md` — define roles and their visibility/approval authority
  - [ ] `review.md` — define your review cadences and feedback mechanisms

## Documentation: Create Domain Role Guides

For each role identified above, create a guide:

- [ ] Create `docs/[role-1-slug].md` (e.g., `docs/trader.md`)
  - Use `.fork-guide/templates/role-guide-template.md` as a starting point
  - Fill in: What is this role? Daily tasks? What do they see in dashboards? What authority do they have?
  - Keep it domain-specific, not prescriptive

- [ ] Create `docs/[role-2-slug].md`
- [ ] Create `docs/[role-3-slug].md`

## Documentation: IMPLEMENTATION Guide

- [ ] Create `IMPLEMENTATION.md`
  - Use `.fork-guide/templates/implementation-template.md` as a starting point
  - Include: How to run agents, what data sources to connect, how to start dashboards, how to run operational cycles
  - Customize for your domain

## Documentation: README

- [ ] Update `README.md`
  - Use `.fork-guide/templates/readme-template.md` as a starting point
  - Replace [Your Domain] with your actual domain name
  - Link to your role guides

## Agents Setup (if applicable)

If you plan to implement agents in this repo:

- [ ] Create `agents/` directory
  - Will eventually contain: strategy_agent.py, execution_agent.py, observability_agent.py, collaboration_agent.py, review_agent.py

- [ ] Create `skills/domain/` directory
  - List the domain-specific skills you'll need (e.g., for trading: market_data_fetcher, order_executor, position_tracker)
  - Create stub .py files for each skill (to be implemented later)

## Validation

- [ ] Run `python .fork-guide/templates/spec-validator.py` (before deleting .fork-guide/)
  - Checks that all 5 specs exist in `specs/[domain]/`
  - Checks that each spec has required sections
  - Reports any missing or incomplete sections

- [ ] Have colleagues review role guides (are they accurate?)

- [ ] Read IMPLEMENTATION.md and verify it's clear

## Final Cleanup & Commit

- [ ] Delete `.fork-guide/` directory (no longer needed)
- [ ] Delete `docs/template-usage/` directory if not already deleted
- [ ] Verify `reference/` still exists (keep this for reference material)
- [ ] Verify `specs/templates/` still exists (optional; keep as reference)
- [ ] Verify `skills/core/` still exists (reusable infrastructure)

- [ ] `git add .`
- [ ] `git commit -m "setup: fork template for [domain]"`
- [ ] `git push origin setup/domain-fork`
- [ ] Create pull request for review
- [ ] Merge to main

## Ready!

Your domain fork is now ready for agent implementation. Next steps:
- [ ] Implementers build agents using `skills/core/` and `skills/domain/`
- [ ] Operators review role guides and dashboards
- [ ] Run first operational cycle against specs
