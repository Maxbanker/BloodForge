"""
BloodForge v6.0 — Final Tuning Pass (6–12 exchange SPSM fights)
"""

import numpy as np
import pandas as pd
from typing import Dict, Optional
from dataclasses import dataclass

from .core.state import FighterState
from .core.operators import BloodForgeOperators
from .core.actions import ActionSystem
from .mods.street_scrap import StreetScrapMod


@dataclass
class FightResult:
    winner: str
    method: str
    round: int
    exchanges: int
    final_state_a: Dict
    final_state_b: Dict
    history_df: pd.DataFrame


class BloodForgeSim:
    def __init__(
        self,
        fighter_a_config: Dict,
        fighter_b_config: Dict,
        spsm_mode: bool = False,
        max_rounds: int = 3,
        exchanges_per_round: int = 100,
        seed: Optional[int] = None
    ):
        if seed is not None:
            np.random.seed(seed)

        self.spsm_mode = spsm_mode
        self.max_rounds = max_rounds
        self.exchanges_per_round = exchanges_per_round

        self.a = FighterState(name=fighter_a_config.get("name", "Fighter A"),
                              **fighter_a_config.get("init_state", {}))
        self.b = FighterState(name=fighter_b_config.get("name", "Fighter B"),
                              **fighter_b_config.get("init_state", {}))

        self.current_regime = "feelout"
        self.history: list = []
        self.exchange_count = 0
        self.current_round = 1

    def _apply_damage(self, attacker: FighterState, defender: FighterState, action):
        base = action.damage_potential * (0.72 + 0.28 * action.commitment) * max(0.35, attacker.veil_cn)

        defender.pain += base * 0.34
        defender.shock += base * 0.29
        defender.neuro += base * 0.21
        defender.bleed += base * 0.11
        defender.structural = max(0.0, defender.structural - base * 0.05)

        hand_delta = base * 0.18 * action.commitment
        if self.spsm_mode:
            StreetScrapMod.update_hand_fracture(attacker, hand_delta)
        else:
            attacker.hand_damage += hand_delta

        attacker.fatigue = min(1.0, attacker.fatigue + 0.007 * action.commitment)

    def _update_regime(self):
        avg_omega = (self.a.omega + self.b.omega) / 2
        if (self.a.panic + self.b.panic) > 1.3 or max(self.a.fatigue, self.b.fatigue) > 0.65:
            self.current_regime = "brawl"
        elif avg_omega < 0.48:
            self.current_regime = "survival"
        elif self.current_regime == "feelout" and self.exchange_count > 28:
            self.current_regime = "pressing"

    def run_fight(self) -> FightResult:
        fight_over = False

        for round_num in range(1, self.max_rounds + 1):
            self.current_round = round_num
            if fight_over:
                break

            for _ in range(self.exchanges_per_round):
                self.exchange_count += 1
                t = self.exchange_count

                feasible_a = ActionSystem.get_feasible_actions(self.a, self.current_regime, self.spsm_mode)
                feasible_b = ActionSystem.get_feasible_actions(self.b, self.current_regime, self.spsm_mode)

                action_a = ActionSystem.select_action(self.a, feasible_a, regime=self.current_regime, spsm_mode=self.spsm_mode)
                action_b = ActionSystem.select_action(self.b, feasible_b, regime=self.current_regime, spsm_mode=self.spsm_mode)

                self._apply_damage(self.a, self.b, action_a)
                self._apply_damage(self.b, self.a, action_b)

                if self.a.pain > 0.38:
                    self.a.hysteresis_thr["break_conf"] += 0.10
                if self.b.pain > 0.38:
                    self.b.hysteresis_thr["break_conf"] += 0.10

                BloodForgeOperators.update_drift(self.a, opp_pressure=0.50, spsm_mode=self.spsm_mode)
                BloodForgeOperators.update_drift(self.b, opp_pressure=0.50, spsm_mode=self.spsm_mode)

                BloodForgeOperators.update_coherence(self.a, spsm_mode=self.spsm_mode)
                BloodForgeOperators.update_coherence(self.b, spsm_mode=self.spsm_mode)

                BloodForgeOperators.check_collapse(self.a, self.spsm_mode)
                BloodForgeOperators.check_collapse(self.b, self.spsm_mode)

                if np.random.rand() < 0.19 or self.current_regime in ["survival", "reset"]:
                    BloodForgeOperators.update_weave(self.a, spsm_mode=self.spsm_mode)
                    BloodForgeOperators.update_weave(self.b, spsm_mode=self.spsm_mode)

                BloodForgeOperators.update_veil(self.a)
                BloodForgeOperators.update_veil(self.b)

                if self.spsm_mode:
                    StreetScrapMod.update_panic_cascade(self.a, discipline=0.36)
                    StreetScrapMod.update_panic_cascade(self.b, discipline=0.30)
                    StreetScrapMod.apply_env_operator(self.a)
                    StreetScrapMod.apply_env_operator(self.b)

                self.a.clip_all()
                self.b.clip_all()
                self._update_regime()

                self.history.append({
                    "exchange": t,
                    "round": round_num,
                    "regime": self.current_regime,
                    "action_a": action_a.name,
                    "action_b": action_b.name,
                    "a_gamma": round(self.a.gamma, 4),
                    "a_omega": round(self.a.omega, 4),
                    "a_veil": round(self.a.veil_cn, 4),
                    "a_panic": round(self.a.panic, 4),
                    "a_collapse": self.a.collapse,
                    "a_mode": self.a.collapse_mode,
                    "b_gamma": round(self.b.gamma, 4),
                    "b_omega": round(self.b.omega, 4),
                    "b_veil": round(self.b.veil_cn, 4),
                    "b_panic": round(self.b.panic, 4),
                    "b_collapse": self.b.collapse,
                    "b_mode": self.b.collapse_mode,
                    "a_fatigue": round(self.a.fatigue, 4),
                    "b_fatigue": round(self.b.fatigue, 4)
                })

                if (self.a.omega < 0.24 and self.a.veil_cn < 0.27) or \
                   (self.b.omega < 0.24 and self.b.veil_cn < 0.27):
                    fight_over = True
                    break

        if self.a.omega < 0.24 and self.b.omega >= 0.24:
            winner, method = self.b.name, "Psychological TKO"
        elif self.b.omega < 0.24 and self.a.omega >= 0.24:
            winner, method = self.a.name, "Psychological TKO"
        else:
            winner = self.a.name if self.a.omega > self.b.omega else self.b.name
            method = "Decision" if not fight_over else "TKO"

        df = pd.DataFrame(self.history)
        csv_name = f"bloodforge_{self.a.name.replace(' ', '_')}_vs_{self.b.name.replace(' ', '_')}.csv"
        df.to_csv(csv_name, index=False)

        return FightResult(
            winner=winner,
            method=method,
            round=self.current_round,
            exchanges=self.exchange_count,
            final_state_a={"gamma": self.a.gamma, "omega": self.a.omega, "veil": self.a.veil_cn, "panic": self.a.panic},
            final_state_b={"gamma": self.b.gamma, "omega": self.b.omega, "veil": self.b.veil_cn, "panic": self.b.panic},
            history_df=df
        )


# Quick test
if __name__ == "__main__":
    bully = {"name": "Prison Yard Bully", "init_state": {"panic": 0.32, "omega": 0.79}}
    inmate = {"name": "Cornered Inmate", "init_state": {"panic": 0.45, "omega": 0.68}}

    sim = BloodForgeSim(bully, inmate, spsm_mode=True, seed=42)
    result = sim.run_fight()

    print(f"Winner: {result.winner} via {result.method} ({result.exchanges} exchanges)")