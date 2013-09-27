import unittest
from DTL.api import Path, Profile, loggingUtils

LOCALPATH = Path(__file__).parent

@Profile
def main():
    suite = unittest.TestLoader().discover(LOCALPATH.join('unittests'))
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
