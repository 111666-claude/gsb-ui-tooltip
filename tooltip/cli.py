"""命令行入口：跑提示框样例。"""

import argparse

from .core import Tooltip


def build_parser():
    parser = argparse.ArgumentParser(prog="ui-tooltip", description="提示框数据合成")
    parser.add_argument("--sample", default="override", help="override / stale / scan")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.sample == "override":
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("z_low", priority=1, fields={"atk": 10})
        tooltip.set_source("a_high", priority=5, fields={"atk": 99})
        print("atk=%d" % tooltip.build("sword")["atk"])
    elif args.sample == "stale":
        tooltip = Tooltip({"armor": 5})
        tooltip.set_source("gear", priority=1, fields={"atk": 10})
        tooltip.build("sword")
        tooltip.set_source("gear", priority=1, fields={"atk": 77})
        print("atk=%d" % tooltip.build("sword")["atk"])
    elif args.sample == "scan":
        tooltip = Tooltip({})
        for index in range(3000):
            tooltip.set_source("s-%d" % index, priority=index, fields={"atk": index})
        for index in range(3000):
            tooltip.build("sword")
        print("scanned=%d" % tooltip.scanned_count())
    else:
        raise SystemExit("需要 --sample override|stale|scan")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
