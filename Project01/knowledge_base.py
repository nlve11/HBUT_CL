"""动物识别知识库：事实名称、中文标签和产生式规则。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rule_id: str
    premises: frozenset[str]
    conclusion: str


FACT_LABELS = {
    "has_hair": "有毛发",
    "gives_milk": "产奶",
    "has_feathers": "有羽毛",
    "cannot_fly": "不会飞",
    "lays_eggs": "会下蛋",
    "eats_meat": "吃肉",
    "pointed_teeth": "有犬齿",
    "has_claws": "有爪",
    "forward_eyes": "眼睛朝前",
    "has_hooves": "有蹄",
    "chews_cud": "反刍",
    "tawny": "黄褐色",
    "dark_spots": "有深色斑点",
    "black_stripes": "有黑色条纹",
    "long_neck": "长脖子",
    "long_legs": "长腿",
    "swims": "会游泳",
    "black_white": "黑白二色",
    "flies_well": "善飞",
    "mammal": "哺乳类",
    "bird": "鸟类",
    "carnivore": "食肉类",
    "ungulate": "有蹄类",
    "leopard": "金钱豹",
    "tiger": "虎",
    "giraffe": "长颈鹿",
    "zebra": "斑马",
    "ostrich": "鸵鸟",
    "penguin": "企鹅",
    "albatross": "信天翁",
}

ANIMALS = frozenset(
    {"leopard", "tiger", "giraffe", "zebra", "ostrich", "penguin", "albatross"}
)


# FILL-01A：补齐 8 条类别推导规则。
CATEGORY_RULES: tuple[Rule, ...] = (
    Rule("R01", frozenset({"has_hair"}), "mammal"),
    Rule("R02", frozenset({"gives_milk"}), "mammal"),
    Rule("R03", frozenset({"has_feathers"}), "bird"),
    Rule("R04", frozenset({"cannot_fly", "lays_eggs"}), "bird"),
    Rule("R05", frozenset({"mammal", "eats_meat"}), "carnivore"),
    Rule("R06", frozenset({"pointed_teeth", "has_claws", "forward_eyes"}), "carnivore"),
    Rule("R07", frozenset({"mammal", "has_hooves"}), "ungulate"),
    Rule("R08", frozenset({"mammal", "chews_cud"}), "ungulate"),
)

# FILL-01B：补齐 7 条具体动物识别规则。
ANIMAL_RULES: tuple[Rule, ...] = (
    Rule("R09", frozenset({"mammal", "carnivore", "tawny", "dark_spots"}), "leopard"),
    Rule("R10", frozenset({"mammal", "carnivore", "tawny", "black_stripes"}), "tiger"),
    Rule("R11", frozenset({"ungulate", "long_neck", "long_legs", "dark_spots"}), "giraffe"),
    Rule("R12", frozenset({"ungulate", "black_stripes"}), "zebra"),
    Rule("R13", frozenset({"bird", "long_neck", "long_legs", "cannot_fly", "black_white"}), "ostrich"),
    Rule("R14", frozenset({"bird", "swims", "cannot_fly", "black_white"}), "penguin"),
    Rule("R15", frozenset({"bird", "flies_well"}), "albatross"),
)

# 连接两组规则，后续推理引擎只依赖统一的 RULES。
RULES = CATEGORY_RULES + ANIMAL_RULES
