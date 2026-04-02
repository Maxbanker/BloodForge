"""
BloodForge v6.0 — Cognitive Combat Simulator
Polished Demo
"""

import streamlit as st
import pandas as pd

from bloodforge.sim import BloodForgeSim

st.set_page_config(page_title="BloodForge v6.0", page_icon="🩸", layout="wide")

st.title("🩸 BloodForge")
st.subheader("Cognitive Combat Simulation Framework (BF-CCSF v6.0)")
st.caption("Entropy-driven • Cognitive-Narrative Stability • Traceable Collapse")

with st.sidebar:
    st.header("Configure Fight")

    spsm_mode = st.checkbox("Enable Street/Prison Scrap Mod (SPSM v1.1)", value=True,
                            help="No rules. Concrete. Brutal snowballing.")

    col1, col2 = st.columns(2)
    with col1:
        a_name = st.text_input("Fighter A", "Prison Yard Bully", key="a_name")
        a_panic = st.slider("Initial Panic (A)", 0.0, 1.0, 0.35, 0.05)
        a_omega = st.slider("Initial Coherence Ω (A)", 0.4, 1.0, 0.78, 0.02)

    with col2:
        b_name = st.text_input("Fighter B", "Cornered Inmate", key="b_name")
        b_panic = st.slider("Initial Panic (B)", 0.0, 1.0, 0.45, 0.05)
        b_omega = st.slider("Initial Coherence Ω (B)", 0.4, 1.0, 0.68, 0.02)

    seed = st.number_input("Random Seed", value=42, step=1)

    run_button = st.button("🔥 Forge the Fight", type="primary", use_container_width=True)

if run_button:
    with st.spinner("Forging the fight..."):
        fighter_a = {"name": a_name, "init_state": {"panic": a_panic, "omega": a_omega}}
        fighter_b = {"name": b_name, "init_state": {"panic": b_panic, "omega": b_omega}}

        sim = BloodForgeSim(fighter_a, fighter_b, spsm_mode=spsm_mode, seed=seed)
        result = sim.run_fight()

    st.success(f"**Winner: {result.winner}** via {result.method} ({result.exchanges} exchanges)")

    tab1, tab2, tab3 = st.tabs(["📈 Timeline", "📊 Raw Data", "📝 Summary"])

    with tab1:
        st.subheader("Cognitive Operators Over Time")
        st.caption("Γ = Drift · Ω = Coherence · V^cn = Cognitive Veil")
        plot_cols = ["a_gamma", "b_gamma", "a_omega", "b_omega", "a_veil", "b_veil", "a_panic", "b_panic"]
        st.line_chart(result.history_df[plot_cols])

    with tab2:
        st.subheader("Full Exchange Log")
        st.dataframe(result.history_df, use_container_width=True)

        csv = result.history_df.to_csv(index=False).encode()
        st.download_button("Download CSV", csv, f"bloodforge_{a_name}_vs_{b_name}.csv", "text/csv")

    with tab3:
        st.subheader("Fight Summary")
        st.info(f"""
        **{result.winner}** won by **{result.method}**

        Final states:
        - {a_name}: Ω = {result.final_state_a.get('omega', 0):.3f}, Γ = {result.final_state_a.get('gamma', 0):.3f}, Veil = {result.final_state_a.get('veil', 0):.3f}
        - {b_name}: Ω = {result.final_state_b.get('omega', 0):.3f}, Γ = {result.final_state_b.get('gamma', 0):.3f}, Veil = {result.final_state_b.get('veil', 0):.3f}
        """)

else:
    st.info("Configure fighters in the sidebar and click **Forge the Fight** to begin.")

    st.markdown("""
    ### Why BloodForge stands out
    - Models **Drift (Γ)** — deviation from identity under pressure
    - Tracks **Coherence (Ω)** — structural stability of decision-making
    - Probabilistic **Collapse (𝒞)** with distinct modes
    - Partial recovery via **Weave (W)**
    - Risk gating via **Cognitive Veil (V^cn)**

    **SPSM mode** turns fights into short, dirty, unforgiving scraps.
    """)

st.caption("BloodForge BF-CCSF v6.0 • Steven Lanier-Egu")