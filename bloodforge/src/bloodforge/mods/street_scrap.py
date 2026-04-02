"""
Street/Prison Scrap Mod (SPSM v1.1) — Final Aggressive Version
"""

import numpy as np
from ..core.state import FighterState

class StreetScrapMod:
    """Aggressive version for short, ugly, snowballing fights"""

    @staticmethod
    def apply_env_operator(state: FighterState):
        if state.terrain == "concrete":
            state.shock *= 2.2
            state.neuro *= 2.0

        if state.positional in ["grounded", "mounted"]:
            state.panic = min(1.0, state.panic + 0.25)
            state.omega = max(0.0, state.omega - 0.22)
            state.veil_cn = max(0.0, state.veil_cn - 0.24)
            state.concrete_contact = min(4, state.concrete_contact + 1)

    @staticmethod
    def update_hand_fracture(state: FighterState, delta_hand: float):
        concrete_factor = 1 + 1.2 * min(state.concrete_contact, 4)
        state.hand_damage += delta_hand * concrete_factor
        if state.hand_damage > 0.45:
            state.cognition_exec = max(0.0, state.cognition_exec * 0.52)

    @staticmethod
    def update_panic_cascade(state: FighterState, discipline: float = 0.30):
        """Strong early panic trigger"""
        if state.pain > 0.22 or state.shock > 0.22 or state.neuro > 0.20:
            increase = 0.55 * (1 - discipline) * (1 + state.fatigue * 1.1)
            state.panic = min(1.0, state.panic + increase)