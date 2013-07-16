from __future__ import with_statement
import unittest

import DTL

class FirstTestCase(unittest.TestCase):

    def test_simple(self):
        self.assertEqual(DTL.__version__, DTL.__version__)


if __name__ == "__main__":
    unittest.main()