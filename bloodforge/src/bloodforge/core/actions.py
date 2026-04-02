from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import numpy as np
from scipy.special import erf
from .state import FighterState
from .operators import BloodForgeOperators

@dataclass
class Action:
    """Structured action from Appendix F"""
    name: str
    type: str                      # jab, strike, combination, clinch, reset, shell, panic_swing, etc.
    target: str                    # head, body, mixed, legs, ground
    commitment: float              # [0,1] — low for jabs, high for bursts
    duration: str                  # short, medium, long
    risk: float                    # base risk exposure
    damage_potential: float        # expected multi-channel damage scalar
    positional_gain: float         # ring control / angle value
    control_value: float           # tempo / initiative
    style_align: Dict[str, float]  # alignment with fighter archetypes (e.g., pressure, counter)

    def __post_init__(self):
        if not self.style_align:
            self.style_align = {"default": 0.7}

class ActionSystem:
    """Full v6.0 Action Space + Policy + Collapse Distortion"""

    # Core action library (expandable)
    ACTION_LIBRARY: Dict[str, Action] = {
        "jab": Action(
            name="jab", type="strike", target="head", commitment=0.25, duration="short",
            risk=0.15, damage_potential=0.35, positional_gain=0.4, control_value=0.6,
            style_align={"counter": 0.9, "technical": 0.85, "pressure": 0.6}
        ),
        "cross": Action(
            name="cross", type="strike", target="head", commitment=0.55, duration="short",
            risk=0.35, damage_potential=0.65, positional_gain=0.3, control_value=0.5,
            style_align={"pressure": 0.8, "counter": 0.7}
        ),
        "body_hook": Action(
            name="body_hook", type="strike", target="body", commitment=0.6, duration="medium",
            risk=0.45, damage_potential=0.75, positional_gain=0.5, control_value=0.55,
            style_align={"pressure": 0.9}
        ),
        "combo_3": Action(
            name="3-punch combo", type="combination", target="mixed", commitment=0.75, duration="medium",
            risk=0.65, damage_potential=1.1, positional_gain=0.6, control_value=0.7,
            style_align={"pressure": 0.85, "brawler": 0.75}
        ),
        "clinch": Action(
            name="clinch", type="grapple", target="mixed", commitment=0.4, duration="medium",
            risk=0.3, damage_potential=0.4, positional_gain=0.8, control_value=0.65,
            style_align={"default": 0.7}
        ),
        "reset": Action(
            name="reset", type="tactical", target="none", commitment=0.2, duration="short",
            risk=0.1, damage_potential=0.1, positional_gain=0.9, control_value=0.8,
            style_align={"technical": 0.9, "counter": 0.85}
        ),
        "shell": Action(
            name="shell", type="defense", target="none", commitment=0.1, duration="short",
            risk=0.05, damage_potential=0.0, positional_gain=-0.4, control_value=-0.3,
            style_align={"default": 0.6}
        ),
        "panic_swing": Action(
            name="panic_swing", type="desperation", target="head", commitment=0.95, duration="long",
            risk=0.9, damage_potential=0.8, positional_gain=-0.2, control_value=-0.5,
            style_align={"default": 0.3}
        ),
        "blind_rush": Action(
            name="blind_rush", type="desperation", target="mixed", commitment=0.9, duration="long",
            risk=0.85, damage_potential=0.7, positional_gain=0.3, control_value=-0.4,
            style_align={"default": 0.2}
        ),
        "ground_stomp": Action(  # SPSM specific
            name="ground_stomp", type="ground", target="head", commitment=0.8, duration="short",
            risk=0.6, damage_potential=1.4, positional_gain=0.7, control_value=0.4,
            style_align={"default": 0.5}
        )
    }

    @staticmethod
    def get_feasible_actions(state: FighterState, regime: str = "feelout", spsm_mode: bool = False) -> List[Action]:
        """Generate feasible action set (Appendix F.5 constraints)"""
        feasible = []

        for action in ActionSystem.ACTION_LIBRARY.values():
            # Veil gating (high-risk actions need higher veil)
            if action.commitment > 0.7 and state.veil_cn < 0.45:
                continue
            if action.risk > 0.6 and state.veil_cn < 0.35:
                continue

            # Coherence gating
            if state.omega < 0.35 and action.commitment > 0.5:
                continue  # collapse restricts combos

            # Collapse mode distortion
            if state.collapse:
                if state.collapse_mode == "hesitation" and action.commitment > 0.4:
                    continue
                if state.collapse_mode == "shutdown" and action.damage_potential > 0.3:
                    continue

            # SPSM grounded restrictions / bonuses
            if spsm_mode and state.positional in ["grounded", "mounted"]:
                if action.name == "ground_stomp" and state.positional == "mounted":
                    feasible.append(action)
                    continue
                if action.duration == "long" and state.positional == "grounded":
                    continue  # hard to throw long combos on concrete

            feasible.append(action)

        # Regime filtering (Appendix G)
        if regime == "survival":
            feasible = [a for a in feasible if a.control_value < 0.3 or a.name in ["shell", "reset"]]
        elif regime == "brawl":
            feasible = [a for a in feasible if a.commitment > 0.5]

        return feasible

    @staticmethod
    def compute_utility(action: Action, state: FighterState, opp_model: Dict = None,
                        regime: str = "feelout", spsm_mode: bool = False) -> float:
        """Utility function U(a) from Appendix F.6"""
        base_u = (0.4 * action.damage_potential +
                  0.25 * action.positional_gain +
                  0.2 * action.control_value -
                  0.15 * action.risk)

        # Style alignment boost
        align = action.style_align.get("default", 0.7)
        base_u += 0.3 * align

        # Regime fit
        regime_bonus = {"feelout": 0.8 if action.duration == "short" else 0.4,
                        "pressing": 0.9 if action.commitment > 0.5 else 0.5,
                        "brawl": 1.1 if action.commitment > 0.7 else 0.6,
                        "survival": 1.2 if action.name in ["shell", "reset"] else 0.3}
        base_u *= regime_bonus.get(regime, 1.0)

        # Cognitive gates (multiplicative as per spec)
        veil_factor = state.veil_cn
        coherence_factor = max(0.3, state.omega)  # floor to avoid zero
        u = base_u * veil_factor * coherence_factor

        # Collapse distortion
        if state.collapse:
            if state.collapse_mode == "panic-aggression":
                u += 0.4 if action.commitment > 0.7 else -0.3
            elif state.collapse_mode == "hesitation":
                u -= 0.5 if action.commitment > 0.4 else 0.0
            elif state.collapse_mode == "shutdown":
                u *= 0.4

        # SPSM panic / concrete modifiers
        if spsm_mode and state.panic > 0.6:
            u += 0.25 if "panic" in action.name or action.commitment > 0.8 else -0.2

        return u

    @staticmethod
    def select_action(state: FighterState, feasible: List[Action], opp_model: Dict = None,
                      regime: str = "feelout", spsm_mode: bool = False,
                      temperature: float = 0.3) -> Action:
        """Softmax policy selection with noise"""
        if not feasible:
            return ActionSystem.ACTION_LIBRARY["jab"]  # fallback

        utilities = np.array([ActionSystem.compute_utility(a, state, opp_model, regime, spsm_mode)
                              for a in feasible])

        # Add small noise for realism
        utilities += np.random.normal(0, temperature, len(utilities))

        # Softmax
        exp_u = np.exp(utilities / max(0.1, temperature))
        probs = exp_u / np.sum(exp_u)

        chosen_idx = np.random.choice(len(feasible), p=probs)
        return feasible[chosen_idx]