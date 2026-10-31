"""运行动物识别实验，并保存可复核的推理结果。"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from inference_engine import forward_chain
from knowledge_base import FACT_LABELS, RULES
from student_identity import display_identity, load_identity


OUTPUT_PATH = Path(__file__).resolve().parent / "outputs" / "inference_result.json"


def parse_facts(raw: str) -> set[str]:
    # FILL-06：按英文逗号拆分事实，去除空白并拒绝未知事实。
    facts = {item.strip() for item in raw.split(",") if item.strip()}
    unknown = sorted(facts.difference(FACT_LABELS))
    if unknown:
        raise ValueError(f"未知事实：{', '.join(unknown)}")
    if not facts:
        raise ValueError("至少需要提供一个事实")
    return facts


def main() -> None:
    parser = argparse.ArgumentParser(description="产生式规则动物识别")
    parser.add_argument(
        "--facts",
        default="has_hair,eats_meat,tawny,dark_spots",
        help="用英文逗号分隔的事实名称",
    )
    args = parser.parse_args()

    identity = load_identity()
    facts = parse_facts(args.facts)
    result = forward_chain(facts, RULES)

    print("初始事实：", "、".join(FACT_LABELS[item] for item in sorted(facts)))
    print("推理轨迹：")
    for item in result.fired_rules:
        left = " 且 ".join(FACT_LABELS[x] for x in item.premises)
        print(
            f"  第{item.round_no}轮 {item.rule_id}: {left} -> {FACT_LABELS[item.conclusion]}"
        )
    animal_text = "、".join(FACT_LABELS[x] for x in result.animals) or "无法确定"
    print(f"识别结果：{animal_text}")

    # FILL-07：组织包含原始事实、推理轨迹和动物结论的 payload。
    payload = {
        "initial_facts": sorted(result.initial_facts),
        "all_facts": sorted(result.all_facts),
        "fired_rules": [
            {
                "round": item.round_no,
                "rule_id": item.rule_id,
                "premises": list(item.premises),
                "conclusion": item.conclusion,
            }
            for item in result.fired_rules
        ],
        "animals": list(result.animals),
    }
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"结果文件：{OUTPUT_PATH}")
    display_identity(identity, stage="final-inference")


if __name__ == "__main__":
    main()
