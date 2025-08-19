#!/usr/bin/env python3

import subprocess
import sys
import os

def run_tests():
    """Run all tests with coverage"""
    print("🧪 Running LAMFO API Tests...")
    print("=" * 50)
    
    # Install test dependencies
    print("📦 Installing test dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements-test.txt"])
    
    # Run tests
    print("\n🚀 Running tests...")
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "-v", 
        "--cov=.", 
        "--cov-report=term-missing",
        "--cov-report=html",
        "backend/tests/"
    ])
    
    if result.returncode == 0:
        print("\n✅ All tests passed!")
        print("📊 Coverage report generated in htmlcov/index.html")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    run_tests()