import unittest
import sys
import os

if __name__ == "__main__":
    # Ensure the current directory is in sys.path
    sys.path.append(os.getcwd())
    
    loader = unittest.TestLoader()
    start_dir = 'tests'
    # Discover tests in the 'tests' directory, using the current directory as top-level
    suite = loader.discover(start_dir, top_level_dir='.')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    if not result.wasSuccessful():
        sys.exit(1)