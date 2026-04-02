import numpy as np
from scipy.special import erf
from .state import FighterState

class BloodForgeOperators:
    """v6.0 Cognitive-Narrative Operators + SPSM v1.1 overrides"""

    # Default params from Appendix B (tunable)
    ALPHA = {"pain": 0.08, "shock": 0.06, "fatigue": 0.05, "panic": 0.07, "opp_pressure": 0.04,
             "discipline": 0.06, "tactical": 0.05}
    BETA = {"gamma": 0.10, "panic": 0.09, "shock": 0.08, "break_conf": 0.12,
            "vision": 0.07, "pressure": 0.06, "corner": 0.10, "weave": 0.11}
    GAMMA_WEAVE = {"dec": 0.22, "emo": 0.20, "adapt": 0.18, "recover": 0.18,
                   "corner_calm": 0.12, "corner_iq": 0.10}
    LAMBDA = {"omega": 0.22, "gamma": 0.18, "veil": 0.15}
    DELTA = {"gamma": 0.65, "panic": 0.55}

    THETA = {"omega": 0.50, "gamma": 0.45, "emo": 0.55, "panic": 0.58, "dec": 0.52,
             "stop_omega": 0.20, "stop_exec": 0.30, "stop_veil": 0.22}

    SIGMA = {"omega": 0.06, "gamma": 0.07, "panic": 0.06}  # for ERF

    @staticmethod
    def erf_prob(x: float, theta: float, sigma: float) -> float:
        """Smooth ERF-based probability"""
        return 0.5 * (1 + erf((x - theta) / sigma))

    @staticmethod
    def update_drift(state: FighterState, opp_pressure: float = 0.0, discipline: float = 0.5,
                     tactical: float = 0.5, spsm_mode: bool = False):
        """Drift Γ update (SPSM amplifies)"""
        delta = (BloodForgeOperators.ALPHA["pain"] * state.pain +
                 BloodForgeOperators.ALPHA["shock"] * state.shock +
                 BloodForgeOperators.ALPHA["fatigue"] * state.fatigue +
                 BloodForgeOperators.ALPHA["panic"] * state.panic +
                 BloodForgeOperators.ALPHA["opp_pressure"] * opp_pressure -
                 BloodForgeOperators.ALPHA["discipline"] * discipline -
                 BloodForgeOperators.ALPHA["tactical"] * tactical)

        if spsm_mode:
            delta *= 1.4
            if state.positional in ["grounded", "mounted"]:
                delta += 0.08
        state.gamma = np.clip(state.gamma + delta, 0.0, 1.0)

    @staticmethod
    def update_coherence(state: FighterState, corner_effect: float = 0.0, spsm_mode: bool = False):
        """Coherence Ω update"""
        decay = (BloodForgeOperators.BETA["gamma"] * state.gamma +
                 BloodForgeOperators.BETA["panic"] * state.panic +
                 BloodForgeOperators.BETA["shock"] * state.shock +
                 BloodForgeOperators.BETA["break_conf"] * state.hysteresis_thr["break_conf"] +
                 BloodForgeOperators.BETA["vision"] * state.hysteresis_thr["vision_collapse"] +
                 BloodForgeOperators.BETA["pressure"] * state.hysteresis_thr.get("opp_pressure", 0.0))

        if spsm_mode:
            decay *= 1.3
            if state.positional in ["grounded", "mounted"]:
                decay += 0.15

        state.omega = np.clip(state.omega - decay + BloodForgeOperators.BETA["corner"] * corner_effect +
                              BloodForgeOperators.BETA["weave"] * state.weave_potential, 0.0, 1.0)

    @staticmethod
    def check_collapse(state: FighterState, spsm_mode: bool = False) -> bool:
        """ERF-based probabilistic collapse"""
        p_omega = BloodForgeOperators.erf_prob(BloodForgeOperators.THETA["omega"] - state.omega,
                                               BloodForgeOperators.THETA["omega"], BloodForgeOperators.SIGMA["omega"])
        p_gamma = BloodForgeOperators.erf_prob(state.gamma - BloodForgeOperators.THETA["gamma"],
                                               BloodForgeOperators.THETA["gamma"], BloodForgeOperators.SIGMA["gamma"]) * \
                  BloodForgeOperators.erf_prob(BloodForgeOperators.THETA["emo"] - state.cognition_emo,
                                               BloodForgeOperators.THETA["emo"], 0.05)
        p_panic = BloodForgeOperators.erf_prob(state.panic - BloodForgeOperators.THETA["panic"],
                                               BloodForgeOperators.THETA["panic"], BloodForgeOperators.SIGMA["panic"]) * \
                  BloodForgeOperators.erf_prob(BloodForgeOperators.THETA["dec"] - state.cognition_dec,
                                               BloodForgeOperators.THETA["dec"], 0.05)

        p_collapse = 1 - (1 - p_omega) * (1 - p_gamma) * (1 - p_panic)
        if spsm_mode:
            p_collapse = min(1.0, p_collapse * 1.2)  # earlier collapse

        state.collapse = np.random.rand() < p_collapse
        if state.collapse:
            # Assign mode (simplified)
            if state.panic > 0.6 and state.gamma > 0.5:
                state.collapse_mode = "panic-aggression"
            elif state.omega < 0.35 and state.veil_cn < 0.4:
                state.collapse_mode = "shutdown"
            else:
                state.collapse_mode = "hesitation"
        return state.collapse

    @staticmethod
    def update_weave(state: FighterState, corner_calm: float = 0.0, corner_iq: float = 0.0,
                     spsm_mode: bool = False):
        """Weave W"""
        w = (BloodForgeOperators.GAMMA_WEAVE["dec"] * state.cognition_dec +
             BloodForgeOperators.GAMMA_WEAVE["emo"] * state.cognition_emo +
             BloodForgeOperators.GAMMA_WEAVE["adapt"] * 0.7 +  # placeholder trait
             BloodForgeOperators.GAMMA_WEAVE["recover"] * 0.7 +
             BloodForgeOperators.GAMMA_WEAVE["corner_calm"] * corner_calm +
             BloodForgeOperators.GAMMA_WEAVE["corner_iq"] * corner_iq)

        overwhelm = 0.6 * (state.shock + state.pain) + 0.4 * 0.5  # placeholder
        w_eff = w * (1 - state.panic) * (1 - overwhelm)
        if spsm_mode:
            w_eff *= 0.5  # suppressed recovery

        state.weave_potential = w_eff
        # Apply in sim loop
        state.omega += BloodForgeOperators.LAMBDA["omega"] * w_eff
        state.gamma -= BloodForgeOperators.LAMBDA["gamma"] * w_eff
        state.veil_cn += BloodForgeOperators.LAMBDA["veil"] * w_eff

    @staticmethod
    def update_veil(state: FighterState):
        """Cognitive Veil V^cn"""
        state.veil_cn = np.clip(state.veil_cn * (1 - BloodForgeOperators.DELTA["gamma"] * state.gamma) *
                                state.omega * (1 - BloodForgeOperators.DELTA["panic"] * state.panic), 0.0, 1.0)