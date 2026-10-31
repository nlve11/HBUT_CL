"""产生式系统的最小自动检查。"""

from __future__ import annotations

import unittest

from inference_engine import forward_chain
from knowledge_base import RULES


class ForwardChainTests(unittest.TestCase):
    def test_leopard_requires_multi_step_reasoning(self) -> None:
        result = forward_chain({"has_hair", "eats_meat", "tawny", "dark_spots"}, RULES)
        self.assertEqual(result.animals, ("leopard",))
        self.assertIn("mammal", result.all_facts)
        self.assertIn("carnivore", result.all_facts)

    def test_penguin(self) -> None:
        result = forward_chain(
            {"has_feathers", "cannot_fly", "swims", "black_white"}, RULES
        )
        self.assertEqual(result.animals, ("penguin",))

    def test_unknown_description_has_no_animal(self) -> None:
        result = forward_chain({"long_legs"}, RULES)
        self.assertEqual(result.animals, ())

    def test_same_rule_fires_only_once(self) -> None:
        result = forward_chain({"has_hair", "gives_milk"}, RULES)
        ids = [item.rule_id for item in result.fired_rules]
        self.assertEqual(len(ids), len(set(ids)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
