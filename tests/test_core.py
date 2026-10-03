import unittest

from tooltip.core import Tooltip


class BasicTest(unittest.TestCase):
    def test_defaults_are_returned(self):
        self.assertEqual(Tooltip({"armor": 5}).build("sword"), {"armor": 5})

    def test_source_field_is_merged(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword")["atk"], 10)

    def test_revision_starts_at_zero(self):
        self.assertEqual(Tooltip({}).revision, 0)

    def test_revision_grows(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={})
        self.assertEqual(tooltip.revision, 1)

    def test_scanned_starts_at_zero(self):
        self.assertEqual(Tooltip({}).scanned_count(), 0)


if __name__ == "__main__":
    unittest.main()
