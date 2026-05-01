#!/usr/bin/env python3
"""
Quick verification script for hermes-formatter.
Run this before pushing to GitHub to ensure everything works.
"""

import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    print("Testing imports...")
    from hermes_formatter import format, HermesFormatter, auto_format
    from hermes_formatter.adapters import get_adapter
    print("✅ All imports successful")

def test_telegram():
    print("\nTesting Telegram adapter...")
    from hermes_formatter import format
    msg = "✅ **Success!**\nSee https://example.com"
    result = format(msg, platform="telegram")
    assert "Success" in result
    assert "[example.com]" in result or "example.com" in result
    print(f"   Input:  {msg[:60]}")
    print(f"   Output: {result[:80]}")

def test_discord():
    print("\nTesting Discord adapter...")
    from hermes_formatter import format
    msg = "**Bold** and *italic*"
    result = format(msg, platform="discord")
    assert "**Bold**" in result
    print(f"   ✅ Discord formatting OK")

def test_slack():
    print("\nTesting Slack adapter...")
    from hermes_formatter import format
    msg = "Check https://example.com"
    result = format(msg, platform="slack")
    assert "<https://example.com" in result
    print(f"   ✅ Slack link format OK")

def test_email():
    print("\nTesting Email adapter...")
    from hermes_formatter import format
    msg = "**Report**\nData: https://example.com"
    result = format(msg, platform="email")
    assert isinstance(result, dict)
    assert "html" in result
    assert "text" in result
    print(f"   ✅ Email multipart OK (HTML={len(result['html'])} chars, plain={len(result['text'])} chars)")

def test_cli():
    print("\nTesting CLI adapter...")
    from hermes_formatter import format
    msg = "**Warning:** Issue detected"
    result = format(msg, platform="cli")
    assert "Warning" in result
    print(f"   ✅ CLI colors OK (if Rich installed)")

def test_generic():
    print("\nTesting Generic adapter...")
    from hermes_formatter import format
    msg = "**bold** *italic*"
    result = format(msg, platform="generic", strip_markdown=True)
    assert "bold" in result and "italic" in result
    assert "**" not in result
    print(f"   ✅ Strip markdown OK: '{result}'")

def test_auto_format():
    print("\nTesting auto_format...")
    from hermes_formatter import auto_format
    msg = "Hello"
    result = auto_format(msg, context={"platform": "telegram"})
    assert "Hello" in result
    print(f"   ✅ Auto-detect OK")

def run_all():
    print("=" * 60)
    print("HERMES FORMATTER — VERIFICATION SCRIPT")
    print("=" * 60)

    tests = [
        test_imports,
        test_telegram,
        test_discord,
        test_slack,
        test_email,
        test_cli,
        test_generic,
        test_auto_format,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            failed += 1

    print("\n" + "=" * 60)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("=" * 60)

    if failed == 0:
        print("\n✅ All checks passed! Ready to push to GitHub.")
        print("\nNext steps:")
        print("1. Create repo on GitHub: morolab/hermes-formatter")
        print("2. git remote add origin https://github.com/morolab/hermes-formatter.git")
        print("3. git push -u origin main")
    else:
        print("\n⚠️  Some tests failed. Fix before pushing.")
        sys.exit(1)

if __name__ == "__main__":
    run_all()
