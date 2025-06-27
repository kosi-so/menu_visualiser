#!/usr/bin/env python3
"""
Test runner script for menu_visualiser OCR tests.
"""
import sys
import subprocess
import os


def run_tests():
    """Run the test suite."""
    print("Running OCR tests...")
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run pytest
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", "tests/", "-v"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with return code: {result.returncode}")
            sys.exit(result.returncode)
            
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)


def run_specific_test(test_file):
    """Run a specific test file."""
    print(f"Running test file: {test_file}")
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", test_file, "-v"
        ], capture_output=False, text=True)
        
        if result.returncode == 0:
            print("\n✅ Test passed!")
        else:
            print(f"\n❌ Test failed with return code: {result.returncode}")
            sys.exit(result.returncode)
            
    except Exception as e:
        print(f"Error running test: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        run_specific_test(test_file)
    else:
        # Run all tests
        run_tests() 