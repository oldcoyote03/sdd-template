# Core Skills Interface Contracts

**Purpose**: Define the expected interface for core skills so agents know what to expect when using them.

These are the interface contracts that all implementations must follow.

---

## `spec_query` Skill Interface

**Purpose**: Parse and query markdown specifications by criteria.

### Methods

#### `load_spec(spec_path: str) -> Dict[str, Any]`

Load and parse a markdown spec file.

**Parameters:**
- `spec_path` (str): Path to markdown spec file

**Returns:**
```python
{
    'raw': str,                              # Original markdown text
    'sections': List[Dict],                  # Parsed sections
    'metadata': {
        'total_sections': int,
        'title': str                         # Title from first heading
    }
}
```

**Each section in `sections` contains:**
```python
{
    'title': str,                            # Section heading
    'level': int,                            # Markdown level (1-6)
    'content': str,                          # Section body text
    'attributes': Dict[str, Any]             # Auto-extracted attributes
}
```

**Raises:**
- `FileNotFoundError`: Spec file not found
- `ValueError`: Malformed spec

**Caching:** Implementations should cache results.

---

#### `query(spec_path: str, criteria: Dict[str, Any]) -> List[Dict[str, Any]]`

Query a spec for sections matching criteria.

**Parameters:**
- `spec_path` (str): Path to spec file
- `criteria` (dict): Filter criteria (all must match, AND logic)
  - Examples: `{'tier': 1}`, `{'tier': 1, 'condition': 'price_break'}`

**Returns:**
- List of section dicts matching criteria (empty list if no matches)

**Behavior:**
1. First checks extracted attributes (from section titles)
2. Falls back to text content matching if attribute not found
3. Supports multiple criteria (AND logic)

---

#### `query_section(spec_path: str, section_name: str) -> Optional[Dict[str, Any]]`

Query for a specific section by name.

**Parameters:**
- `spec_path` (str): Path to spec file
- `section_name` (str): Section title (case-insensitive matching)

**Returns:**
- Section dict if found, `None` otherwise

---

#### `get_all_sections(spec_path: str) -> List[Dict[str, Any]]`

Get all sections from a spec.

**Returns:**
- List of all section dicts

---

#### `clear_cache() -> None`

Clear the in-memory cache.

**Use when:** Specs change during runtime.

---

#### `reload_spec(spec_path: str) -> Dict[str, Any]`

Force reload a spec, bypassing cache.

**Returns:**
- Newly parsed spec dict

---

## `audit_log` Skill Interface

**Purpose**: Standardized logging for agent decisions.

### Methods

#### `log(entry: Dict[str, Any]) -> str`

Log an agent decision or action.

**Parameters:**
- `entry` (dict): Must contain:
  - `agent` (str): Agent name
  - `action` (str): Action taken
  - `reasoning` (str): Why this decision
  - `inputs` (dict): Input data used
  - `outputs` (dict): Result/outcome
  - `status` (str): Status (success, pending, error, rejected, skipped)
  - `timestamp` (str, optional): ISO format (auto-generated if omitted)
  - `audit_id` (str, optional): Unique ID (auto-generated if omitted)

**Returns:**
- `audit_id` (str): Unique identifier for this entry

**Raises:**
- `ValueError`: If required fields missing

**Side effects:**
- Entry added to in-memory log
- Entry written to disk immediately

---

#### `query(criteria: Dict[str, Any]) -> List[Dict[str, Any]]`

Query log entries by criteria.

**Parameters:**
- `criteria` (dict): Filter criteria
  - `agent` (str): Filter by agent name
  - `action` (str): Filter by action
  - `status` (str): Filter by status
  - `time_from` (str): ISO timestamp (>=)
  - `time_to` (str): ISO timestamp (<=)
  - `audit_id` (str): Find specific entry
  - All criteria must match (AND logic)

**Returns:**
- List of matching log entries

---

#### `query_by_agent(agent_name: str) -> List[Dict[str, Any]]`

Get all entries for a specific agent.

**Parameters:**
- `agent_name` (str): Agent name

**Returns:**
- List of entries where agent == agent_name

---

#### `query_by_action(action: str) -> List[Dict[str, Any]]`

Get all entries for a specific action.

**Parameters:**
- `action` (str): Action name

**Returns:**
- List of entries where action == action

---

#### `query_by_status(status: str) -> List[Dict[str, Any]]`

Get all entries with a specific status.

**Parameters:**
- `status` (str): Status value (success, pending, error, rejected, skipped)

**Returns:**
- List of entries where status == status

---

#### `query_time_range(time_from: str, time_to: str) -> List[Dict[str, Any]]`

Get entries in a time range.

**Parameters:**
- `time_from` (str): ISO format timestamp (inclusive)
- `time_to` (str): ISO format timestamp (inclusive)

**Returns:**
- List of entries where `time_from <= timestamp <= time_to`

---

#### `get_entry(audit_id: str) -> Optional[Dict[str, Any]]`

Get a specific entry by audit_id.

**Parameters:**
- `audit_id` (str): Audit ID

**Returns:**
- Entry dict if found, `None` otherwise

---

#### `summary(agent: Optional[str] = None) -> Dict[str, Any]`

Get summary statistics of logged activity.

**Parameters:**
- `agent` (str, optional): If provided, summarize only for that agent

**Returns:**
```python
{
    'total_entries': int,
    'by_status': {'success': count, 'error': count, ...},
    'by_action': {'execute_trade': count, ...},
    'by_agent': {'execution': count, ...} or None if filtered,
    'time_range': {
        'first': timestamp_str,
        'last': timestamp_str
    }
}
```

---

#### `export_json(output_file: str) -> None`

Export all log entries to JSON file.

**Parameters:**
- `output_file` (str): Path to output file

**Side effects:**
- Writes all entries to JSON file

---

#### `export_csv(output_file: str) -> None`

Export log entries to CSV file.

**Parameters:**
- `output_file` (str): Path to output file

**Side effects:**
- Writes entries to CSV (nested structures JSON-encoded in cells)

---

#### `load_from_file() -> None`

Load existing log entries from disk into memory.

**Use when:** Restarting agent and want to access previous logs.

**Side effects:**
- Populates in-memory log from disk file

---

## Common Assumptions

### For All Skills

1. **No external dependencies**: Core skills use only Python standard library
2. **Stateless operations**: Skill methods are deterministic and reentrant
3. **Error handling**: Raise clear exceptions with meaningful messages
4. **Thread safety**: Not required (agents are single-threaded; if parallel needed, locking is agent's responsibility)

### For `spec_query`

1. **Markdown is read-only**: Skill never modifies spec files
2. **Sections are headings**: Sections are defined by markdown headings (# through ######)
3. **Attribute extraction is automatic**: From section titles using heuristics
4. **Cache is optional**: Implementations may or may not cache

### For `audit_log`

1. **Logs are append-only**: Entries are never deleted or modified (audit trail)
2. **Timestamps are ISO format**: UTC timestamps with Z suffix (e.g., `2026-05-16T09:45:32Z`)
3. **Audit IDs are unique**: Within a log file
4. **JSON Lines format**: One entry per line (if disk-persisted)

---

## Version

**Current version**: 1.0

**Last updated**: May 16, 2026

**Breaking changes**: Any change to method signatures or return types is a breaking change.

---

## See Also

- [spec_query/README.md](spec_query/README.md) — `spec_query` implementation details
- [audit_log/README.md](audit_log/README.md) — `audit_log` implementation details
- [../README.md](../README.md) — Skills overview
