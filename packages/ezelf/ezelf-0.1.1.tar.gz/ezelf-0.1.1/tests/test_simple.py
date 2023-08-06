# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package

import unittest

from ezelf.sync.ezpie import ezecho


class TestSimple(unittest.TestCase):
    def test_ezecho(self):
        self.assertEqual(ezecho("string"), "string")
        self.assertEqual(ezecho(1), 1)
        self.assertEqual(ezecho(3.14), 3.14)


if __name__ == "__main__":
    unittest.main()
