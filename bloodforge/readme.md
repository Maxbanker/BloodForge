# BloodForge Cognitive Combat Simulator

**BF-CCSF v6.0 + Street/Prison Scrap Mod (SPSM v1.1)**

An entropy-driven combat simulation framework that models not just physical damage, but the **cognitive and narrative stability** of fighters under extreme pressure.

This is **v0.1** — an early public release focused on delivering a working implementation of the full symbolic specification.

## What Makes BloodForge Different?

Most combat simulators focus on physics, animations, or basic AI.  
**BloodForge** simulates the **mind** breaking down.

It tracks five core symbolic operators:

- **Drift (Γ)** — How far a fighter deviates from their baseline identity
- **Coherence (Ω)** — Internal structural stability of decision-making
- **Collapse (𝒞)** — Probabilistic breakdown with distinct modes (Hesitation, Panic-Aggression, Shutdown)
- **Weave (W)** — Partial, fragile recovery under pressure
- **Cognitive Veil (V^cn)** — Risk gating tied to psychological state

In **Street/Prison Scrap Mod (SPSM)**, fights become short, dirty, and unforgiving — mistakes compound rapidly on concrete with no rules or referee.

## Features

- Full implementation of BF-CCSF v6.0 specification
- Modular action system with utility-based selection and collapse distortion
- Realistic multi-channel damage (pain, shock, neuro, bleed, structural)
- Regime transitions (feelout → pressing → brawl → survival)
- Traceable CSV logs with all symbolic operators
- Interactive Streamlit web demo with live plots
- Visualization module for cognitive timelines

## Quick Start

### 1. Installation

```bash
git clone https://github.com/yourusername/bloodforge.git
cd bloodforge

# Create virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Run the Web Demo

Bash

```
streamlit run src/app.py
```

Open your browser to http://localhost:8501 and start forging fights.

### 3. Run from Command Line

Bash

```
python -m bloodforge.sim
```

## Current Status (v0.1)

This is an early public release. The simulator successfully implements the core symbolic operators and produces traceable outputs.

**Note:** SPSM mode is still being tuned for the ideal "short and ugly" street fight feel. Feedback on fight pacing and brutality is highly welcome and will directly influence future versions.

## Future Plans

- Stronger narrative summaries and collapse mode visualization
- Improved snowball mechanics in SPSM
- Calibration tools and batch testing
- Unity/Godot export support
- Expanded scenario packs

## Supporting the Project

This simulator is a side project built to support larger research into **Symbolic Recursion** and **Collapse-Resilient Intelligence**.

All donations and sponsorships directly fund continued development and open releases.

You can support via:

- GitHub Sponsors
- Patreon
- One-time contributions

Every contribution helps push the next preprint and major version.

## Citation

If you use BloodForge in your work, please cite:

bibtex

```
Lanier-Egu, Steven (2026). BloodForge Cognitive-Narrative Combat Prototype (BF-CNCP): BF-CCSF v6.0. Zenodo.
https://doi.org/10.5281/zenodo.19354466
```

## License

The framework specification is released under CC BY 4.0. The code implementation is open for research and personal use. Commercial licensing available upon request.

------

**Made with entropy, rage, and consequences.**

Feedback, bug reports, and contributions are welcome! Open an issue or pull request on GitHub.