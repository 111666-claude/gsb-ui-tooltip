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


class PriorityTest(unittest.TestCase):
    def test_high_priority_wins_regardless_of_name(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("z_low", priority=1, fields={"atk": 10})
        tooltip.set_source("a_high", priority=5, fields={"atk": 99})
        self.assertEqual(tooltip.build("sword")["atk"], 99)

    def test_same_priority_applied_by_name_ascending(self):
        tooltip = Tooltip({})
        tooltip.set_source("b_src", priority=1, fields={"atk": 2})
        tooltip.set_source("a_src", priority=1, fields={"atk": 1})
        self.assertEqual(tooltip.build("sword")["atk"], 2)

    def test_low_priority_cannot_override_high(self):
        tooltip = Tooltip({})
        tooltip.set_source("high", priority=9, fields={"atk": 99})
        tooltip.set_source("low", priority=1, fields={"atk": 10, "spd": 3})
        result = tooltip.build("sword")
        self.assertEqual(result["atk"], 99)
        self.assertEqual(result["spd"], 3)


class DefaultsTest(unittest.TestCase):
    def test_defaults_survive_source_merge(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword"), {"armor": 5, "atk": 10})

    def test_source_overrides_default_value(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"armor": 9})
        self.assertEqual(tooltip.build("sword")["armor"], 9)


class CacheInvalidationTest(unittest.TestCase):
    def test_modified_source_invalidates_cached_result(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        tooltip.build("sword")
        tooltip.set_source("gear", priority=1, fields={"atk": 77})
        self.assertEqual(tooltip.build("sword")["atk"], 77)

    def test_new_source_invalidates_cached_result(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        tooltip.build("sword")
        tooltip.set_source("enchant", priority=2, fields={"atk": 42})
        self.assertEqual(tooltip.build("sword")["atk"], 42)

    def test_repeated_builds_are_stable(self):
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        self.assertEqual(tooltip.build("sword"), tooltip.build("sword"))

    def test_returned_result_does_not_poison_cache(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        tooltip.build("sword")["atk"] = 999
        self.assertEqual(tooltip.build("sword")["atk"], 10)


class ScanCostTest(unittest.TestCase):
    def test_scanned_not_linear_in_build_count(self):
        tooltip = Tooltip({})
        for index in range(100):
            tooltip.set_source("s-%d" % index, priority=index, fields={"atk": index})
        tooltip.build("sword")
        scanned_after_first = tooltip.scanned_count()
        self.assertEqual(scanned_after_first, 100)
        for _ in range(50):
            tooltip.build("sword")
        self.assertEqual(tooltip.scanned_count(), scanned_after_first)

    def test_rescan_after_source_change(self):
        tooltip = Tooltip({})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        tooltip.build("sword")
        self.assertEqual(tooltip.scanned_count(), 1)
        tooltip.set_source("gear", priority=1, fields={"atk": 77})
        tooltip.build("sword")
        self.assertEqual(tooltip.scanned_count(), 2)
