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


class PriorityTest(unittest.TestCase):
    def test_higher_priority_wins_regardless_of_name_order(self):
        tooltip = Tooltip({})
        tooltip.set_source("z_low", priority=1, fields={"atk": 10})
        tooltip.set_source("a_high", priority=5, fields={"atk": 99})
        self.assertEqual(tooltip.build("sword")["atk"], 99)

    def test_same_priority_breaks_tie_by_source_name_ascending(self):
        tooltip = Tooltip({})
        tooltip.set_source("b_src", priority=3, fields={"atk": 2})
        tooltip.set_source("a_src", priority=3, fields={"atk": 1})
        self.assertEqual(tooltip.build("sword")["atk"], 2)


class DefaultsTest(unittest.TestCase):
    def test_defaults_are_filled_in_when_no_source_covers_them(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword"), {"armor": 5, "atk": 10})

    def test_source_overrides_default(self):
        tooltip = Tooltip({"atk": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword")["atk"], 10)


class CacheInvalidationTest(unittest.TestCase):
    def test_changed_source_is_recomputed(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword")["atk"], 10)
        tooltip.set_source("gear", priority=1, fields={"atk": 77})
        self.assertEqual(tooltip.build("sword")["atk"], 77)

    def test_new_source_is_recomputed(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword")["atk"], 10)
        tooltip.set_source("buff", priority=5, fields={"atk": 20})
        self.assertEqual(tooltip.build("sword")["atk"], 20)

    def test_repeated_builds_are_identical_and_include_all_defaults(self):
        tooltip = Tooltip({"armor": 5, "hp": 100})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        first = tooltip.build("sword")
        for _ in range(10):
            self.assertEqual(tooltip.build("sword"), first)
        self.assertEqual(set(first), {"armor", "hp", "atk"})


class ScanCostTest(unittest.TestCase):
    def test_repeated_builds_do_not_rescan_all_sources(self):
        tooltip = Tooltip({})
        for index in range(100):
            tooltip.set_source("s-%d" % index, priority=index, fields={"atk": index})
        tooltip.build("sword")
        scanned_after_first = tooltip.scanned_count()
        for _ in range(99):
            tooltip.build("sword")
        self.assertEqual(tooltip.scanned_count(), scanned_after_first)

    def test_scan_sample_scale(self):
        tooltip = Tooltip({})
        for index in range(3000):
            tooltip.set_source("s-%d" % index, priority=index, fields={"atk": index})
        for _ in range(3000):
            tooltip.build("sword")
        self.assertLessEqual(tooltip.scanned_count(), 6000)


if __name__ == "__main__":
    unittest.main()
