
import unittest
import sys

def run_foundation_tests():
    loader = unittest.TestLoader()
    suite = loader.discover('tests/foundation', pattern='test_*.py')
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_foundation_tests()
    sys.exit(0 if success else 1)
