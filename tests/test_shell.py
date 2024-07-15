from unittest import TestCase

from src.shell import Shell


class TestShell(TestCase):
    def test_create_Shell(self):
        sut = Shell()
        self.assertIsNotNone(sut)