#!/usr/bin/env python3
"""Test all API keys at once"""

import sys
import subprocess

def run_test(script_name, service_name):
    """Run a test script and return result"""
    print(f"\n{'='*60}")
    print(f"Testing {service_name}...")
    print('='*60)
    
    try:
        result = subprocess.run(
            ["python", f"scripts/{script_name}"],
            capture_output=False,
            text=True
        )
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run {script_name}: {e}")
        return False


def main():
    """Run all tests"""
    print("\n🧪 Testing All API Keys\n")
    
    tests = [
        ("test_anthropic.py", "Anthropic"),
        ("test_github.py", "GitHub"),
        ("test_netlify.py", "Netlify"),
        ("test_firebase.py", "Firebase"),
    ]
    
    results = {}
    
    for script, service in tests:
        results[service] = run_test(script, service)
    
    # Summary
    print(f"\n{'='*60}")
    print("SUMMARY")
    print('='*60)
    
    for service, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{service:20s} {status}")
    
    # Overall result
    all_passed = all(results.values())
    
    print(f"\n{'='*60}")
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your API keys are configured correctly.")
    else:
        print("⚠️  SOME TESTS FAILED")
        print("Please check the failed services above.")
    print('='*60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
