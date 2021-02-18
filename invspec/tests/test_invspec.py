"""
Unit and regression test for the invspec package.
"""

# Import package, test suite, and other packages as needed
import invspec
import pytest
import sys

def test_invspec_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "invspec" in sys.modules
