# celonis-support-utils

A Python package implementing a customer support ticket routing domain for Celonis — built as a deliberate exercise in object-oriented design, type safety, and production-grade Python project structure.

---

## What this is

This package models the core domain of a support ticket routing system: tickets arrive from Salesforce, get validated, and are routed to the right engineer based on regional restrictions, shift availability, and customer service level.

It is not a toy project. Every design decision was made with a specific reason, and the architecture reflects real constraints from the Celonis support domain.

---

## Design philosophy

The guiding principle throughout this project was **simplicity first**. Every class, enum, and method exists because the application needs it — not because it might be useful later.

Concretely, this meant:

**Trusting system boundaries.** Fields like `service`, `product_area`, and `severity` come from Salesforce already validated. Remodelling them as enums inside this package would add complexity with no benefit. They stay as strings. Only fields that the routing logic itself needs to reason about — `restriction`, `issue_type`, `service_level` — are parsed into enums.

**Composition over inheritance.** No inheritance hierarchies. `Engineer` has-a `Shift`. `Team` has-a list of `Engineers`. `Ticket` is flat. The domain is expressed through relationships, not subclassing.

**Deferring what isn't needed.** `EscalationRouting` is stubbed with `NotImplementedError`. The shift assignment data layer is marked with a `TODO`. These are intentional — building them before the requirement is clear would be premature optimisation dressed as thoroughness.

**Pushing behaviour onto the class that owns the data.** `Shift.is_active()` knows how to determine if it's currently active. `Engineer.is_on_shift()` delegates to it. The router asks questions; it doesn't reach into objects to inspect their internals.

---

## Architecture

```
src/celonis_support_utils/
├── enums.py        # Region, DayOfWeek, ServiceLevel — shared across the domain
├── shift.py        # Shift — owns shift window logic via is_active()
├── customer.py     # Customer — company name and service level
├── ticket.py       # Ticket + IssueType — the core routing unit
├── engineer.py     # Engineer — shift availability via is_on_shift()
├── team.py         # Team — owns a list of engineers, carries region
├── queue.py        # Queue — holds incoming tickets
└── routing.py      # RoutingStrategy (Protocol), StandardRouting, EscalationRouting
```

### Key relationships

- `Ticket` has-a `Customer`, uses `IssueType` (enum) and `Region` (enum)
- `Team` has-a `list[Engineer]`, carries `Region`
- `Engineer` has-a `Shift`
- `Shift` owns `is_active()` — checks current time against window in the shift's timezone
- `RoutingStrategy` is a `Protocol` — any class with a matching `route()` signature satisfies it, enabling new routing strategies to be added without modifying existing code

### Routing logic

`StandardRouting.route(ticket, teams) -> Engineer | None`

1. Filter teams by regional restriction — `GLOBAL` tickets can go to any team; otherwise only the matching region
2. For each eligible team, find engineers currently on shift
3. Return the first available engineer, or `None` if none found

---

## OOP patterns applied

| Pattern | Where | Why |
|---|---|---|
| **Strategy** | `RoutingStrategy` Protocol + `StandardRouting`, `EscalationRouting` | Swap routing behaviour without changing the router |
| **Composition** | `Engineer` has-a `Shift`, `Team` has-a `list[Engineer]` | Models "has-a" relationships without inheritance |
| **Factory method** | `_parse_*` static methods on each class | Centralise and validate construction from raw external data |
| **Protocol** | `RoutingStrategy` | Structural subtyping — implementations don't need to inherit, just match the interface |

---

## Type safety and tooling

- Full type hints throughout — `mypy --strict` passes clean
- `ruff` for linting and formatting
- `pre-commit` hooks run on every commit
- `pytest` test suite covering shift logic, parsers, validation, and routing
- GitHub Actions CI runs on every push: ruff → mypy → pytest

---

## Getting started

```bash
# Install uv if you don't have it
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync --all-extras

# Run tests
uv run pytest

# Type check
uv run mypy src/

# Lint
uv run ruff check .
```

---

## What I'd do differently

- **Shift assignment data layer** — currently stubbed. The next step is a repository interface that fetches which shift an engineer is assigned to for a given day from a database or Google Sheet.
- **`EscalationRouting`** — deliberately left unimplemented. The routing rules for escalation depend on requirements not yet defined.
- **`Queue`** — currently a simple wrapper around a list. A production queue would be backed by a message broker or database with persistence and concurrency handling.

---

## Project context

Built as Month 1 of a 12-month AI/Robotics learning roadmap, focused on writing structured, production-grade Python. The goal was to move from "comfortable with Python" to "writes code like a senior developer" — typed, tested, linted, and CI-backed.