from os import getenv
from unittest import TestCase

if getenv("TESTING") != "1":
    raise OSError("Environment variable TESTING is not set")


class ExampleTestCase(TestCase):

    def test_example(self):
        self.assertEqual(1, 1)
