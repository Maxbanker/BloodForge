# BloodForge Cognitive Combat Simulator

**BF-CCSF v6.0 + Street/Prison Scrap Mod (SPSM v1.1)**

An entropy-driven combat simulation framework that models **cognitive and narrative stability** under pressure — not just physical damage.

This is the official open-source implementation of the **BloodForge Cognitive Combat Simulation Framework (BF-CCSF v6.0)**.

**Framework Specification DOI:**  
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19354466.svg)](https://doi.org/10.5281/zenodo.19354466)

### Try the Full Framework Online

You can also interact with the complete framework through the official **BloodForge Simulator Custom GPT**:
→ [BloodForge Simulator on ChatGPT](https://chatgpt.com/g/g-680157be47bc81918ab13df66019d5a4-bloodforge-simulator)

---

This is **v0.1** — an early public release. The core symbolic operators are implemented and functional, but SPSM mode is still being tuned for the ideal "short and ugly" street fight feel.

## What Makes BloodForge Different?

Most combat simulators focus on physics, animations, or basic AI.  
**BloodForge** simulates the **mind breaking down**.

It tracks five core symbolic operators:

- **Drift (Γ)** — How far a fighter deviates from their baseline identity  
- **Coherence (Ω)** — Internal structural stability of decision-making  
- **Collapse (𝒞)** — Probabilistic breakdown with distinct modes (Hesitation, Panic-Aggression, Shutdown)  
- **Weave (W)** — Partial, fragile recovery under pressure  
- **Cognitive Veil (V^cn)** — Risk gating tied to psychological state  

In **Street/Prison Scrap Mod (SPSM)**, fights become short, dirty, and unforgiving — mistakes compound rapidly on concrete with no rules or referee.

## Features

- Full implementation of BF-CCSF v6.0 specification
- Structured action system with utility-based selection and collapse distortion
- Realistic multi-channel damage (pain, shock, neuro, bleed, structural)
- Tempo regime transitions
- Traceable CSV logs with all symbolic operators
- Interactive Streamlit web demo with live plots
- Visualization module for cognitive timelines

## Quick Start

### 1. Installation

```bash
git clone https://github.com/Maxbanker/BloodForge.git
cd BloodForge

# Create virtual environment (recommended)
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Run the Web Demo (Recommended)

Bash

```
streamlit run src/app.py
```

Open your browser to http://localhost:8501.

### 3. Run a Basic Example

Bash

```
python examples/basic_fight.py
```

## Repository Structure

text

```
BloodForge/
├── setup.py
├── requirements.txt
├── LICENSE
├── README.md
├── examples/
│   └── basic_fight.py
└── src/
    ├── bloodforge/
    │   ├── core/
    │   ├── mods/
    │   ├── sim.py
    │   └── visualize.py
    └── app.py
```

## Current Status (v0.1)

This is an early release. The simulator successfully implements the five core operators and produces traceable outputs.

**Note:** SPSM mode tends to produce shorter, more chaotic fights. The exact "snowball" brutality is still being refined based on feedback.

## Future Plans

- Stronger narrative summaries and collapse mode visualization
- Improved snowball mechanics in SPSM
- Calibration tools and batch testing
- Unity/Godot plugin support
- Expanded scenario packs

## Supporting the Project

This simulator is a side project built to support larger research into **Symbolic Recursion** and **Collapse-Resilient Intelligence**.

All donations and sponsorships directly fund continued development and open releases.

You can support via:

- [GitHub Sponsors](https://github.com/sponsors/Maxbanker)
- Patreon
- One-time contributions

Every contribution helps push the next preprint and major version.

## Citation

bibtex

```
Lanier-Egu, Steven (2026). BloodForge Cognitive-Narrative Combat Prototype (BF-CNCP): BF-CCSF v6.0. Zenodo.
https://doi.org/10.5281/zenodo.19354466
```

## License

The code is released under the **MIT License**. The framework specification is licensed under CC BY 4.0.

------

**Made with entropy, rage, and consequences.**

Feedback, bug reports, and contributions are welcome! Open an issue or pull request on GitHub.
