# ui-tooltip

提示框：多来源字段合成、优先级覆盖、缺省补全与版本缓存失效，只用 Python 标准库。

```
python3 -m tooltip.cli --sample override
python3 -m tooltip.cli --sample stale
python3 -m tooltip.cli --sample scan
python3 -m unittest discover -s tests -v
```

## 口径（README 为准）

- **缺省**：`defaults` 里的字段先铺底，缺省值可以被来源覆盖。
- **优先级**：按来源优先级从低到高依次覆盖，高优先级最终生效；
  优先级相同按来源名升序。
- **缓存失效**：任何来源新增或修改之后，之前合成的结果必须重新算，不许返回旧值。
- **不变量**：同一份来源配置重复合成结果相同；结果包含所有缺省字段。
- **代价**：同一版本内重复合成不许重扫全部来源，`scanned_count`
  不随合成次数线性增长。
- **规模**：1 万个来源、每秒 10 万次合成，单次摊还 O(生效来源数)。

## 输出契约（不改格式）

```
atk=..
scanned=..
```

## 目录

```
tooltip/core.py   合并、优先级与缓存
tooltip/cli.py    命令行入口
tests/            unittest 用例
```
