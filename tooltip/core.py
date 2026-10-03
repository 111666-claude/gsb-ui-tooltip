"""提示框：多来源字段合成、优先级覆盖、缺省补全与版本缓存失效。"""


class Tooltip:
    """提示框合成台账。"""

    def __init__(self, defaults):
        self.defaults = dict(defaults)
        self.sources = {}
        self.revision = 0
        self.cache = {}
        self.scanned = 0
        self._merged = None
        self._merged_revision = -1

    def set_source(self, name, priority, fields):
        self.sources[name] = (priority, dict(fields))
        self.revision += 1
        self.cache.clear()

    def _merged_fields(self):
        """按版本缓存的铺底合成：缺省铺底，再按 (优先级, 来源名) 升序依次覆盖。"""
        if self._merged_revision != self.revision:
            merged = dict(self.defaults)
            for name in sorted(self.sources, key=lambda n: (self.sources[n][0], n)):
                merged.update(self.sources[name][1])
            self.scanned += len(self.sources)
            self._merged = merged
            self._merged_revision = self.revision
        return self._merged

    def build(self, item):
        """合成一个提示框。"""
        if item in self.cache:
            return dict(self.cache[item])
        fields = dict(self._merged_fields())
        self.cache[item] = dict(fields)
        return dict(fields)

    def scanned_count(self):
        return self.scanned
