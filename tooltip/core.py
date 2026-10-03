"""提示框：多来源字段合成、优先级覆盖、缺省补全与版本缓存失效。

缺陷：按来源名字顺序覆盖而不是优先级、低优先级覆盖高优先级、缓存不随来源变化失效、
缺省字段被覆盖、每次合成都扫描全部来源。
"""


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

    def build(self, item):
        """合成一个提示框。"""
        self.scanned += len(self.sources)
        if item in self.cache:
            return dict(self.cache[item])
        fields = dict(self.defaults)
        for name in sorted(self.sources):
            fields.update(self.sources[name][1])
        self.cache[item] = dict(fields)
        return dict(fields)

    def scanned_count(self):
        return self.scanned
