"""可追踪的前向推理引擎。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from knowledge_base import ANIMALS, Rule


@dataclass(frozen=True)
class FiredRule:
    round_no: int
    rule_id: str
    premises: tuple[str, ...]
    conclusion: str


@dataclass(frozen=True)
class InferenceResult:
    initial_facts: frozenset[str]
    all_facts: frozenset[str]
    fired_rules: tuple[FiredRule, ...]
    animals: tuple[str, ...]


def forward_chain(
    initial_facts: Iterable[str], rules: Iterable[Rule]
) -> InferenceResult:
    """反复匹配规则，直到一轮中没有产生新事实。"""

    initial = frozenset(initial_facts)
    known = set(initial)
    trace: list[FiredRule] = []
    fired_ids: set[str] = set()
    round_no = 0

    while True:
        round_no += 1
        changed = False
        for rule in rules:
            # FILL-02：判断规则是否尚未触发、前提是否全部满足。
            can_fire = (
                rule.rule_id not in fired_ids
                and rule.premises.issubset(known)
            )
            if not can_fire:
                continue

            # FILL-03：记录已触发规则，并仅在结论为新事实时更新 known。
            fired_ids.add(rule.rule_id)
            if rule.conclusion in known:
                continue

            known.add(rule.conclusion)
            changed = True
            trace.append(
                FiredRule(
                    round_no,
                    rule.rule_id,
                    tuple(sorted(rule.premises)),
                    rule.conclusion,
                )
            )

        # FILL-04：当本轮没有新增事实时结束推理。
        if not changed:
            break

    # FILL-05：从已知事实中筛出动物结论并稳定排序。
    animals = tuple(sorted(known.intersection(ANIMALS)))
    return InferenceResult(initial, frozenset(known), tuple(trace), animals)
