# spec_query Skill

**Purpose**: Parse markdown specs and query them by criteria without modifying the source.

**Used by**: All agents (every agent needs to read its primary spec and often secondary specs for context)

---

## Overview

The `spec_query` skill solves a key problem: markdown specs are easy for humans to read and version control, but hard for code to navigate. This skill:

1. **Parses markdown** into structured sections
2. **Caches results** (don't re-parse on every agent decision)
3. **Queries by criteria** (find sections matching filters without reading linearly)
4. **Extracts attributes** (tier, confidence, condition type, etc.)

**Design principle**: Specs are read-only. Agents query specs to make decisions, but never modify specs. Specs only change through repository commits.

---

## Usage

### Basic Import

```python
from skills.core.spec_query import SpecQuery

# Create skill instance (once per agent)
spec_skill = SpecQuery()
```

### Load a Spec

```python
# Load and parse a markdown spec
parsed = spec_skill.load_spec('specs/examples/day-trading/execution.md')

# Returns:
# {
#     'raw': (markdown text),
#     'sections': (list of parsed sections),
#     'metadata': {'title': ..., 'total_sections': ...}
# }
```

### Query by Criteria

```python
# Find all Tier 1 rules
tier1_rules = spec_skill.query(
    spec_path='specs/examples/day-trading/execution.md',
    criteria={'tier': 1}
)

# Find Tier 1 rules with price_break condition
tier1_breaks = spec_skill.query(
    spec_path='specs/examples/day-trading/execution.md',
    criteria={'tier': 1, 'condition': 'price_break'}
)

# Returns: List of matching sections (each is a dict)
```

### Query by Section Name

```python
# Get a specific section by name
section = spec_skill.query_section(
    spec_path='specs/examples/day-trading/execution.md',
    section_name='Tier 1: High Confidence'
)

# Returns: Section dict or None if not found
```

### Get All Sections

```python
# Load all sections from a spec
all_sections = spec_skill.get_all_sections('specs/examples/day-trading/strategic.md')

# Iterate and process
for section in all_sections:
    print(f"Title: {section['title']}")
    print(f"Level: {section['level']}")
    print(f"Content: {section['content']}")
    print(f"Attributes: {section['attributes']}")
```

---

## Spec Structure (What Gets Parsed)

The skill parses markdown into sections. Each section contains:

```python
{
    'title': 'Tier 1: High Confidence',      # Section heading text
    'level': 2,                              # Markdown level (1-6, ## = level 2)
    'content': '(section body)',             # All text until next heading
    'attributes': {
        'tier': 1,                           # Extracted from title
        'confidence': 'high',                # high, medium, low
        'condition': 'price_break'           # Detected in title
    }
}
```

### How Attributes Are Extracted

The skill automatically extracts these from section titles:

| Pattern | Attribute | Example |
|---------|-----------|---------|
| `Tier 1`, `Tier 2`, etc. | `tier` | "Tier 1: Setup Rules" → `{'tier': 1}` |
| `High`, `Medium`, `Low` | `confidence` | "Tier 1: High Confidence" → `{'confidence': 'high'}` |
| "price break" | `condition` | "Price Break Setup" → `{'condition': 'price_break'}` |
| "mean reversion" | `condition` | "Mean Reversion Rule" → `{'condition': 'mean_reversion'}` |

If your spec titles don't match these patterns, attributes won't be auto-extracted. Either:
1. Adjust spec titles to include these keywords, or
2. Filter by content instead (criteria matching works on content as fallback)

---

## API Reference

### `SpecQuery()`

Create a new skill instance.

```python
spec_skill = SpecQuery()
```

**No dependencies, no configuration needed.**

---

### `load_spec(spec_path: str) -> Dict`

Load and parse a markdown spec file.

**Args:**
- `spec_path` (str): Path to markdown spec file
  - Can be relative (from current working directory) or absolute
  - Example: `'specs/examples/day-trading/execution.md'`

**Returns:**
- Dict with keys: `raw`, `sections`, `metadata`

**Raises:**
- `FileNotFoundError`: If spec file doesn't exist
- `ValueError`: If spec is malformed

**Caching:** Result is cached. Subsequent calls return cached version.

```python
parsed = spec_skill.load_spec('specs/examples/day-trading/execution.md')
```

---

### `query(spec_path: str, criteria: Dict) -> List[Dict]`

Query a spec for sections matching criteria.

**Args:**
- `spec_path` (str): Path to spec file
- `criteria` (dict): Filter criteria
  - Key-value pairs to match
  - All criteria must match (AND logic)
  - Example: `{'tier': 1, 'condition': 'price_break'}`

**Returns:**
- List of matching section dicts (empty list if no matches)

**How matching works:**
1. First checks extracted attributes (fast)
2. Falls back to content text search if attribute not found (slower but flexible)

```python
# Find Tier 1 rules
rules = spec_skill.query(
    spec_path='specs/examples/day-trading/execution.md',
    criteria={'tier': 1}
)

# Find Tier 1 with specific condition
rules = spec_skill.query(
    spec_path='specs/examples/day-trading/execution.md',
    criteria={'tier': 1, 'condition': 'price_break'}
)

# Returns: [section1, section2, ...]
```

---

### `query_section(spec_path: str, section_name: str) -> Optional[Dict]`

Get a specific section by name.

**Args:**
- `spec_path` (str): Path to spec file
- `section_name` (str): Title of section (case-insensitive)

**Returns:**
- Section dict if found, `None` otherwise

```python
section = spec_skill.query_section(
    spec_path='specs/examples/day-trading/execution.md',
    section_name='Tier 1: High Confidence'
)
```

---

### `get_all_sections(spec_path: str) -> List[Dict]`

Get all sections from a spec.

**Returns:** List of all section dicts

```python
all = spec_skill.get_all_sections('specs/examples/day-trading/strategic.md')
for section in all:
    print(section['title'])
```

---

### `clear_cache()`

Clear the in-memory cache.

**Use when:** Specs change during runtime (rare).

```python
spec_skill.clear_cache()
# Next load will re-parse from disk
```

---

### `reload_spec(spec_path: str) -> Dict`

Force reload a spec, bypassing cache.

**Returns:** Newly parsed spec dict

```python
# Bypass cache and re-read from disk
parsed = spec_skill.reload_spec('specs/examples/day-trading/execution.md')
```

---

## Common Patterns

### Pattern 1: Agent Loads Primary Spec on Init

```python
class ExecutionAgent:
    def __init__(self, spec_path, skills):
        self.spec_skill = skills['core/spec_query']
        self.spec_path = spec_path  # e.g., 'specs/examples/day-trading/execution.md'
    
    def on_market_signal(self, signal):
        # Query spec for matching rules
        rules = self.spec_skill.query(
            spec_path=self.spec_path,
            criteria={'tier': signal['tier']}
        )
```

**Benefit:** Spec changes take effect immediately (agents query just-in-time).

---

### Pattern 2: Cross-Spec Queries

```python
class ExecutionAgent:
    def on_market_signal(self, signal):
        # Query execution.md for rules
        exec_rules = self.spec_skill.query(
            spec_path='specs/examples/day-trading/execution.md',
            criteria={'tier': signal['tier']}
        )
        
        # Query collaboration.md for approval requirements
        approval_rules = self.spec_skill.query(
            spec_path='specs/examples/day-trading/collaboration.md',
            criteria={'tier': signal['tier']}
        )
```

---

### Pattern 3: Multi-Criteria Filtering

```python
# Find high-confidence, high-volume setups
rules = spec_skill.query(
    spec_path='specs/examples/day-trading/execution.md',
    criteria={
        'tier': 1,
        'condition': 'price_break',
        'confidence': 'high'
    }
)
```

---

## Limitations & Future Improvements

### Current Limitations

1. **Attribute extraction is basic**: Only recognizes common patterns (tier, confidence, condition). Custom attributes need spec title naming conventions.
2. **No nested queries**: Can't query within subsections, only top-level.
3. **No YAML frontmatter**: Specs are pure markdown; can't store structured metadata in header.

### Future Improvements

- Support YAML frontmatter for rich metadata
- Allow custom attribute extractors (regex patterns)
- Nested section queries
- Spec validation (check for missing required sections)

---

## Testing

Run tests with:

```bash
cd skills/core/spec_query
python -m pytest spec_query_test.py
```

Tests use specs from `specs/examples/day-trading/` as test data.

---

## See Also

- [skills/core/interfaces.md](../interfaces.md) — Skill interface contracts
- [docs/implementers.md](../../../docs/implementers.md) — How agents use skills
- [specs/examples/day-trading/](../../../specs/examples/day-trading/) — Example specs to query against
