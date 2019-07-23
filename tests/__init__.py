import os


def load_tests(loader, standard_tests, pattern):
    # top level directory cached on loader instance
    curr_dir = os.path.dirname(__file__)
    package_tests = loader.discover(start_dir=curr_dir, pattern=pattern if pattern else '*_test.py')
    standard_tests.addTests(package_tests)
    return standard_tests
