"""
Unit tests for spec_query skill.

Tests use the trading specs from specs/trading/ as test data.
"""

import unittest
import os
from spec_query import SpecQuery


class TestSpecQuery(unittest.TestCase):
    """Test spec_query skill functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.skill = SpecQuery()
        # Assume we're in skills/core/spec_query/ directory
        # Trading specs are at ../../specs/trading/
        cls.spec_base = os.path.join(
            os.path.dirname(__file__),
            '../../../../specs/trading'
        )

    def test_load_spec_execution(self):
        """Test loading execution.md spec."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        parsed = self.skill.load_spec(spec_path)

        # Verify structure
        self.assertIn('raw', parsed)
        self.assertIn('sections', parsed)
        self.assertIn('metadata', parsed)
        self.assertGreater(len(parsed['sections']), 0)
        self.assertEqual(parsed['metadata']['total_sections'], len(parsed['sections']))

    def test_cache_works(self):
        """Test that specs are cached after first load."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # First load
        parsed1 = self.skill.load_spec(spec_path)
        # Second load (should come from cache)
        parsed2 = self.skill.load_spec(spec_path)

        # Should be identical objects (same memory reference)
        self.assertIs(parsed1, parsed2)

    def test_query_by_tier(self):
        """Test querying execution.md by tier."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # Query for Tier 1 rules
        tier1_rules = self.skill.query(
            spec_path=spec_path,
            criteria={'tier': 1}
        )

        # Should find at least some Tier 1 sections
        self.assertGreater(len(tier1_rules), 0)

        # All returned sections should have tier=1 attribute
        for rule in tier1_rules:
            attrs = rule.get('attributes', {})
            if 'tier' in attrs:
                self.assertEqual(attrs['tier'], 1)

    def test_query_by_condition(self):
        """Test querying by condition type."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # Query for price_break conditions
        rules = self.skill.query(
            spec_path=spec_path,
            criteria={'condition': 'price_break'}
        )

        # Should find price_break sections or content
        # (may be empty if specs don't contain these patterns)
        self.assertIsInstance(rules, list)

    def test_query_section_by_name(self):
        """Test querying a specific section by name."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # Get all sections first
        all_sections = self.skill.get_all_sections(spec_path)
        if len(all_sections) == 0:
            self.skipTest("No sections found in spec")

        # Try to query first section by name
        first_section_title = all_sections[0].get('title')
        if first_section_title:
            found = self.skill.query_section(spec_path, first_section_title)
            self.assertIsNotNone(found)
            self.assertEqual(found.get('title'), first_section_title)

    def test_reload_spec(self):
        """Test reloading a spec (bypass cache)."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # Load first time
        parsed1 = self.skill.load_spec(spec_path)
        # Reload (should bypass cache)
        parsed2 = self.skill.reload_spec(spec_path)

        # Should be different objects (new parse)
        self.assertIsNot(parsed1, parsed2)
        # But same content
        self.assertEqual(parsed1['raw'], parsed2['raw'])

    def test_clear_cache(self):
        """Test clearing cache."""
        spec_path = os.path.join(self.spec_base, 'execution.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        # Load
        self.skill.load_spec(spec_path)
        self.assertGreater(len(self.skill.cache), 0)

        # Clear
        self.skill.clear_cache()
        self.assertEqual(len(self.skill.cache), 0)

    def test_parse_markdown_structure(self):
        """Test markdown parsing structure."""
        spec_path = os.path.join(self.spec_base, 'strategic.md')
        if not os.path.exists(spec_path):
            self.skipTest(f"Spec file not found: {spec_path}")

        parsed = self.skill.load_spec(spec_path)

        # Each section should have expected keys
        for section in parsed['sections']:
            self.assertIn('title', section)
            self.assertIn('level', section)
            self.assertIn('content', section)
            self.assertIn('attributes', section)

            # Level should be 1-6 (markdown header levels)
            self.assertGreaterEqual(section['level'], 1)
            self.assertLessEqual(section['level'], 6)


if __name__ == '__main__':
    unittest.main()
