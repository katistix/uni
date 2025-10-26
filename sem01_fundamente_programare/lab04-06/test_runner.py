import numar_complex
import storage


def run_all_tests():
    """Run all module tests silently and return True if all pass"""
    try:
        numar_complex.test_module()
        storage.test_module()
        return True
    except (AssertionError, Exception):
        return False