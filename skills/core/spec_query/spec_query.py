"""
spec_query skill: Parse and query markdown specifications.

This skill enables agents to load markdown spec files and query them
by criteria without modifying the source. Specs are parsed into
structured dictionaries that agents can navigate and filter.
"""

import os
import re
from typing import Dict, List, Any, Optional


class SpecQuery:
    """Parse and query markdown specifications by criteria."""

    def __init__(self):
        """Initialize the skill. No external dependencies needed."""
        self.cache = {}  # Cache parsed specs to avoid re-parsing

    def load_spec(self, spec_path: str) -> Dict[str, Any]:
        """
        Load and parse a markdown spec file.

        Args:
            spec_path: Path to markdown spec file (e.g., 'specs/trading/execution.md')

        Returns:
            Dict with keys: 'raw' (markdown text), 'sections' (parsed sections),
            'frontmatter' (YAML-like config if present), 'metadata' (title, etc.)

        Raises:
            FileNotFoundError: If spec file doesn't exist
            ValueError: If spec is malformed (e.g., invalid markdown)
        """
        # Check cache first
        if spec_path in self.cache:
            return self.cache[spec_path]

        # Load file
        if not os.path.exists(spec_path):
            raise FileNotFoundError(f"Spec not found: {spec_path}")

        with open(spec_path, 'r') as f:
            content = f.read()

        # Parse markdown into sections
        parsed = self._parse_markdown(content)

        # Cache it
        self.cache[spec_path] = parsed

        return parsed

    def query(self, spec_path: str, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Query a spec for sections/rules matching criteria.

        Args:
            spec_path: Path to markdown spec file
            criteria: Dict of filter criteria
                Examples:
                  {'tier': 1}  → find all sections with tier=1
                  {'condition': 'price_break'}  → find sections with condition=price_break
                  {'tier': 1, 'approval_required': True}  → multiple criteria (AND)

        Returns:
            List of matching sections (each section is a dict)
            Empty list if no matches

        Example:
            spec_query = SpecQuery()
            rules = spec_query.query(
                spec_path='specs/trading/execution.md',
                criteria={'tier': 1, 'condition': 'price_break'}
            )
            # Returns list of Tier 1 price_break rules
        """
        parsed = self.load_spec(spec_path)
        sections = parsed.get('sections', [])

        # Filter sections by criteria
        matching = []
        for section in sections:
            if self._matches_criteria(section, criteria):
                matching.append(section)

        return matching

    def query_section(self, spec_path: str, section_name: str) -> Optional[Dict[str, Any]]:
        """
        Query for a specific section by name.

        Args:
            spec_path: Path to markdown spec file
            section_name: Name of section (e.g., 'Tier 1', 'Quick Reference')

        Returns:
            Section dict if found, None otherwise
        """
        parsed = self.load_spec(spec_path)
        sections = parsed.get('sections', [])

        for section in sections:
            if section.get('title', '').lower() == section_name.lower():
                return section

        return None

    def get_all_sections(self, spec_path: str) -> List[Dict[str, Any]]:
        """Get all sections from a spec."""
        parsed = self.load_spec(spec_path)
        return parsed.get('sections', [])

    def _parse_markdown(self, content: str) -> Dict[str, Any]:
        """
        Parse markdown content into structured sections.

        Returns dict with:
          - raw: original markdown
          - sections: list of parsed sections
          - metadata: title, headings, etc.
        """
        sections = []
        lines = content.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            # Detect headers
            header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_section is not None:
                    current_section['content'] = '\n'.join(current_content).strip()
                    sections.append(current_section)

                # Start new section
                level = len(header_match.group(1))
                title = header_match.group(2).strip()
                current_section = {
                    'title': title,
                    'level': level,
                    'content': '',
                    'attributes': self._extract_attributes(title)
                }
                current_content = []
            else:
                if current_section is not None:
                    current_content.append(line)

        # Save last section
        if current_section is not None:
            current_section['content'] = '\n'.join(current_content).strip()
            sections.append(current_section)

        return {
            'raw': content,
            'sections': sections,
            'metadata': {
                'total_sections': len(sections),
                'title': sections[0].get('title', '') if sections else ''
            }
        }

    def _extract_attributes(self, title: str) -> Dict[str, Any]:
        """
        Extract key-value attributes from section title.

        Examples:
          'Tier 1' → {'tier': '1'}
          'Tier 1: High Confidence' → {'tier': '1', 'confidence': 'high'}
          'Setup Rules' → {}
        """
        attrs = {}

        # Extract tier
        tier_match = re.search(r'(?:tier|level)\s*(\d+)', title, re.IGNORECASE)
        if tier_match:
            attrs['tier'] = int(tier_match.group(1))

        # Extract confidence level
        if 'high' in title.lower():
            attrs['confidence'] = 'high'
        elif 'medium' in title.lower():
            attrs['confidence'] = 'medium'
        elif 'low' in title.lower():
            attrs['confidence'] = 'low'

        # Extract condition type (if present in title)
        if 'price' in title.lower() and 'break' in title.lower():
            attrs['condition'] = 'price_break'
        elif 'mean' in title.lower() and 'reversion' in title.lower():
            attrs['condition'] = 'mean_reversion'

        return attrs

    def _matches_criteria(self, section: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        """Check if a section matches all criteria."""
        attrs = section.get('attributes', {})

        for key, value in criteria.items():
            # Check if section has this attribute with matching value
            if attrs.get(key) != value:
                # Also check in content (simple text match as fallback)
                content = section.get('content', '').lower()
                if str(value).lower() not in content.lower():
                    return False

        return True

    def clear_cache(self):
        """Clear the spec cache (use if specs change during runtime)."""
        self.cache.clear()

    def reload_spec(self, spec_path: str) -> Dict[str, Any]:
        """Force reload a spec (bypassing cache)."""
        self.cache.pop(spec_path, None)
        return self.load_spec(spec_path)
