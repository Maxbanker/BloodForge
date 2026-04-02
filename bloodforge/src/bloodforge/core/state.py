from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
from scipy.special import erf

@dataclass
class FighterState:
    """Core v6.0 state for one fighter"""
    name: str
    # Physical
    stamina: float = 1.0
    fatigue: float = 0.0
    hand_damage: float = 0.0
    pain: float = 0.0
    shock: float = 0.0
    neuro: float = 0.0
    bleed: float = 0.0
    structural: float = 1.0

    # Cognition
    cognition_per: float = 1.0   # perception
    cognition_dec: float = 1.0   # decision
    cognition_exec: float = 1.0  # execution
    cognition_emo: float = 1.0   # emotional

    # Cognitive-Narrative Stability (v6.0)
    gamma: float = 0.05          # Drift Γ
    omega: float = 0.82          # Coherence Ω
    veil_cn: float = 0.78        # Cognitive Veil V^cn
    collapse: bool = False
    collapse_mode: str = "none"  # hesitation, panic-aggression, shutdown
    weave_potential: float = 0.0
    panic: float = 0.0

    # SPSM extras
    concrete_contact: int = 0
    positional: str = "standing"  # standing, wall_clinch, grounded, mounted
    terrain: str = "concrete"     # concrete, grass, tile

    # Hysteresis / memory
    hysteresis_thr: Dict[str, float] = field(default_factory=lambda: {
        "break_conf": 0.0, "vision_collapse": 0.0, "body_shock": 0.0,
        "hand_distrust": 0.0, "panic_spike": 0.0
    })

    def clip_all(self):
        for attr in ["stamina", "fatigue", "hand_damage", "pain", "shock", "neuro", "bleed",
                     "structural", "cognition_per", "cognition_dec", "cognition_exec",
                     "cognition_emo", "gamma", "omega", "veil_cn", "panic", "weave_potential"]:
            val = getattr(self, attr)
            setattr(self, attr, np.clip(val, 0.0, 1.0))