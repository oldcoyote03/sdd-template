#!/usr/bin/env python3
"""
Spec Validator: Checks that domain specs are complete and well-formed.

Usage:
    python spec-validator.py specs/[domain]/

Validates:
    1. All 5 core specs exist (strategic.md, execution.md, observability.md, collaboration.md, review.md)
    2. Each spec contains required section headers
    3. No required section is empty
"""

import sys
import os
from pathlib import Path

# Define required specs and their required sections
REQUIRED_SPECS = {
    "strategic.md": [
        "objectives",
        "success",
        "decision",
        "constraint",
    ],
    "execution.md": [
        "action",
        "precondition",
        "approval",
        "authorization",
    ],
    "observability.md": [
        "data",
        "metric",
        "alert",
    ],
    "collaboration.md": [
        "role",
        "visibility",
        "approval",
        "communication",
    ],
    "review.md": [
        "cadence",
        "analysis",
        "feedback",
        "loop",
    ],
}

def validate_spec_exists(spec_dir, spec_name):
    """Check if a spec file exists."""
    spec_path = spec_dir / spec_name
    if not spec_path.exists():
        return False, f"Missing: {spec_name}"
    return True, None

def validate_spec_content(spec_path, required_keywords):
    """
    Check if spec file contains required section keywords (case-insensitive).
    
    Args:
        spec_path: Path to spec file
        required_keywords: List of keywords that should appear in the spec
    
    Returns:
        Tuple of (is_valid: bool, error_message: str or None)
    """
    with open(spec_path, 'r') as f:
        content = f.read().lower()
    
    missing = []
    for keyword in required_keywords:
        if keyword.lower() not in content:
            missing.append(keyword)
    
    if missing:
        return False, f"Missing sections in {spec_path.name}: {', '.join(missing)}"
    
    return True, None

def main():
    if len(sys.argv) < 2:
        print("Usage: python spec-validator.py <path-to-domain-specs>")
        print("Example: python spec-validator.py specs/day-trading/")
        sys.exit(1)
    
    spec_dir = Path(sys.argv[1])
    
    if not spec_dir.exists():
        print(f"Error: Directory not found: {spec_dir}")
        sys.exit(1)
    
    print(f"Validating specs in: {spec_dir}")
    print("-" * 60)
    
    errors = []
    warnings = []
    
    # Check each required spec
    for spec_name, keywords in REQUIRED_SPECS.items():
        exists, error = validate_spec_exists(spec_dir, spec_name)
        
        if not exists:
            errors.append(error)
        else:
            spec_path = spec_dir / spec_name
            is_valid, error = validate_spec_content(spec_path, keywords)
            
            if not is_valid:
                errors.append(error)
            else:
                print(f"✓ {spec_name}")
    
    # Check for artifacts folder (optional but recommended)
    artifacts_path = spec_dir / "artifacts"
    if not artifacts_path.exists():
        warnings.append("Optional: Consider adding an artifacts/ folder for diagrams, data samples, etc.")
    else:
        print(f"✓ artifacts/ folder")
    
    print("-" * 60)
    
    if errors:
        print(f"\n❌ Validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  • {error}")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s):")
            for warning in warnings:
                print(f"  • {warning}")
        sys.exit(1)
    else:
        print("\n✅ All specs are valid!")
        if warnings:
            print(f"\n⚠️  {len(warnings)} suggestion(s):")
            for warning in warnings:
                print(f"  • {warning}")
        sys.exit(0)

if __name__ == "__main__":
    main()
