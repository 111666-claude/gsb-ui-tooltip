"""提示框：多来源字段合成、优先级覆盖、缺省补全与版本缓存失效。"""


class Tooltip:
    """提示框合成台账。"""

    def __init__(self, defaults):
        self.defaults = dict(defaults)
        self.sources = {}
        self.revision = 0
        self.cache = {}
        self.scanned = 0

    def set_source(self, name, priority, fields):
        self.sources[name] = (priority, dict(fields))
        self.revision += 1
        self.cache.clear()

    def build(self, item):
        """合成一个提示框。"""
        if item in self.cache:
            return dict(self.cache[item])
        self.scanned += len(self.sources)
        fields = dict(self.defaults)
        for name in sorted(self.sources, key=lambda n: (self.sources[n][0], n)):
            fields.update(self.sources[name][1])
        self.cache[item] = fields
        return dict(fields)

    def scanned_count(self):
        return self.scanned
