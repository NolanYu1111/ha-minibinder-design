# HA Broadly Neutralizing Antibody Design

**Computational design and evaluation of novel antibodies targeting conserved, occluded epitopes on Influenza Hemagglutinin (HA) trimers.**

---

## Project Overview

This project computationally designs and evaluates novel antibody variable domains that mimic the hydrophobic sandwich paratope of the **VH5-9-1 antibody lineage**. We target the conserved **Pro221/Trp222 motif** (H3 numbering) in H3 HA, with exploratory cross-reactive validation on structural analogs W210 (H1) and F225 (H5).

### Key Innovation
Rather than random generation, we guide antibody design with motif-constrained RFdiffusion, ensuring paratope structures recapitulate the geometric and chemical features of the broadly neutralizing VH5-9-1 antibody class.

---

## Project Goals

- [x] **Curate the HA Structural Panel** — Assemble representative H3N2 and H4N1 structures; identify target epitope residues
- [x] **Epitope Accessibility & Glycan Modeling** — Quantify SASA and steric occlusion by nearby glycans
- [ ] **Paratope Motif-Guided Design** — RFdiffusion with motif constraints → ProteinMPNN sequence design
- [ ] **Structure Prediction & Folding** — AlphaFold-Multimer or IgFold for complex structures
- [ ] **Docking & Scoring** — Rosetta or AutoDock Vina docking evaluation
- [ ] **Classifier Training** — Random Forest/XGBoost ranking on geometric & chemical features
- [ ] **Cross-Strain Breadth** — Validate against diverse H3 strains and H1/H5 analogs

---

## Directory Structure

```
HA_bnAb_Project/
│
├── data/
│   ├── raw/                 # Original PDBs, FASTA sequences, glycan files
│   └── processed/           # Curated PDB structures & metadata tables
│
├── models/
│   ├── rfdiffusion/         # Model checkpoints & diffusion script settings
│   └── classifiers/         # Saved Random Forest/CNN model weights
│
├── notebooks/               # Jupyter pipelines for exploration & visualization
│   ├── 01_data_processing.ipynb
│   ├── 02_model_training.ipynb
│   ├── 03_docking_analysis.ipynb
│   └── 04_scoring_metrics.ipynb
│
├── scripts/                 # Production Python execution scripts
│   ├── utils.py                     # Geometric & PDB helper functions
│   ├── 00_fetch_prepare.py          # Fetch & clean raw structures
│   ├── 10_epitope_sasa.py           # SASA & glycan accessibility
│   ├── 20_design_rfmpnn.py          # RFdiffusion + ProteinMPNN
│   ├── 30_predict_complex.py        # AlphaFold-Multimer / IgFold
│   ├── 40_dock_score.py             # Rosetta / AutoDock Vina
│   ├── 50_mm_pbsa.py                # Molecular dynamics MM/PBSA
│   └── 60_filters_rank.py           # Multi-metric filtering & ranking
│
├── results/
│   ├── docking/             # PDB files of docked complex poses
│   ├── figures/             # SASA plots, overlays, heatmaps
│   └── metrics/             # Ranked CSV tables & metrics
│
├── docs/
│   ├── literature_notes.md
│   └── publication_roadmap.md
│
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Reference Panels

### Hemagglutinin Structures

**H3N2 Seasonal Influenza**
| PDB ID | Strain | Notes |
|--------|--------|-------|
| 4WE4 | H3N2 | — |
| 4WE5 | H3N2 | — |
| 4ZCJ | H3N2 | — |
| 8TJ7 | H3N2 | Recent structure |
| 2VIU | H3N2 | — |
| 2HMG | H3N2 | — |

**H4N1 Avian Influenza**
| PDB ID | Strain | Notes |
|--------|--------|-------|
| 5Y2M | H4N1 | — |
| 6V44 | H4N1 | — |
| 5XL8 | H4N1 | — |
| 6V47 | H4N1 | — |

**H1N1 & H5N1 (Exploratory Cross-Reactivity)**
| PDB ID | Strain | Target Residue | Notes |
|--------|--------|---|-------|
| 4JTV | H1N1 | W210 | Structural analog |
| 6Q0C | H1N1 | W210 | — |
| 6AOU | H5N1 | F225 | Structural analog |
| 4WE8 | H5N1 | F225 | — |

### VH5-9-1 Class Seed Antibodies

| PDB ID | Antibody | Target | Bound HA | Notes |
|--------|----------|--------|----------|-------|
| **6N5B** | VH5-9-1 Fab | H3 HA | **Pro217/Trp218** | Primary reference; hydrophobic sandwich motif |
| **6N5D** | VH5-9-1 Fab | H4 HA | — | Cross-reactivity validation |
| **6N5E** | VH5-9-1 Fab | H3 HA | A/Aichi/2/1968 | Historical H3N2 strain |

---

## Quick Start

### Installation

```bash
# Create and activate conda environment
conda create -y -n ha_bnab python=3.10
conda activate ha_bnab

# Install dependencies
pip install -r requirements.txt
```

### Run the Pipeline

```bash
# 1. Fetch and prepare HA structures
python scripts/00_fetch_prepare.py

# 2. Calculate epitope accessibility
python scripts/10_epitope_sasa.py

# 3. Design antibody paratopes (RFdiffusion + ProteinMPNN)
python scripts/20_design_rfmpnn.py

# 4. Predict complex structures (AlphaFold-Multimer)
python scripts/30_predict_complex.py

# 5. Dock designs to HA panel
python scripts/40_dock_score.py

# 6. Run molecular dynamics (MM/PBSA)
python scripts/50_mm_pbsa.py

# 7. Filter, rank, and generate reports
python scripts/60_filters_rank.py
```

For interactive exploration, open the Jupyter notebooks:
```bash
jupyter notebook notebooks/
```

---

## Workflow Overview

```
HA Structures (PDB Panel)
        ↓
   SASA Analysis & Glycan Modeling
        ↓
   Motif-Constrained Design
   (RFdiffusion + ProteinMPNN)
        ↓
   Structure Prediction
   (AlphaFold-Multimer / IgFold)
        ↓
   Docking & Scoring
   (Rosetta / Vina)
        ↓
   Molecular Dynamics
   (MM/PBSA Binding Affinity)
        ↓
   ML Classifier Ranking
   (Random Forest / XGBoost)
        ↓
   Cross-Strain Validation
   (H1, H5 Analogs)
        ↓
   Top Candidate Selection & Synthesis
```

---

## Key Technologies

| Component | Tools | Purpose |
|-----------|-------|---------|
| **Structural Modeling** | RosettaDesign, RFdiffusion | Motif-guided paratope generation |
| **Sequence Design** | ProteinMPNN, ESMFold | In-context antibody sequence design |
| **Structure Prediction** | AlphaFold-Multimer, IgFold | Complex structure validation |
| **Docking** | Rosetta, AutoDock Vina | Antibody–HA binding modes |
| **Dynamics** | GROMACS, AMBER | MM/PBSA free energy calculation |
| **ML Ranking** | scikit-learn, XGBoost | Feature-based candidate prioritization |
| **Visualization** | PyMOL, matplotlib | Structure and metric inspection |

---

## Output & Results

All results are organized in the `results/` directory:

- **`results/docking/`** — Lowest-energy docked PDB files for all designs
- **`results/figures/`** — Publication-ready plots:
  - SASA accessibility heatmaps
  - HA structural overlays
  - Interface interaction networks
  - ML feature importance rankings
- **`results/metrics/`** — CSV tables with per-design scores:
  - Interface buried surface area
  - ΔΔG estimates (Rosetta, MM/PBSA)
  - Per-residue interaction frequencies
  - ML classifier confidence scores

---

## Literature & References

See `docs/literature_notes.md` for an annotated bibliography of:
- VH5-9-1 antibody lineage papers
- HA structure and glycosylation biology
- Computational antibody design techniques
- Influenza surveillance & strain diversity

---

## Citation

If you use this project or its designs, please cite:

```
[Your Lab] HA Broadly Neutralizing Antibody Design.
GitHub Repository: [your-github-link]
Year: 2024–2025
```

---

## Contributing

Contributions, bug reports, and suggestions are welcome! Please open an issue or submit a pull request.

---

## License

[Specify your license here, e.g., MIT, GPL-3.0]

---

## Contact

**Project Lead:** [Your Name]  
**Email:** [your-email]  
**Institution:** [Your Institution]

---

*Last updated: June 2026*
