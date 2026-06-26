HA Broadly Neutralizing Antibody Design
Computational design and evaluation of novel antibodies targeting conserved, occluded epitopes on Influenza Hemagglutinin (HA) trimers.

Project Goal
Design and computationally evaluate novel antibody variable domains that mimic the "hydrophobic sandwich" paratope of the VH5-9-1 antibody lineage. The design targets the conserved Pro221/Trp222 motif (H3 numbering) in H3 HA, with exploratory cross-reactive testing on structural analogs W210 (H1) and F225 (H5).

Directory Structure

HA_bnAb_Project/
│
├── data/
│   ├── raw/         # Original PDBs, FASTA sequences, and glycan files
│   └── processed/   # Curated PDB structures and metadata tables
│
├── models/
│   ├── rfdiffusion/ # Model checkpoints and diffusion script settings
│   └── classifiers/ # Saved Random Forest or CNN model weights
│
├── notebooks/       # Jupyter pipelines for data exploration and visualization
│   ├── data_processing.ipynb
│   ├── model_training.ipynb
│   ├── docking_analysis.ipynb
│   └── scoring_metrics.ipynb
│
├── scripts/         # Production Python execution scripts
│   ├── utils.py             # Geometric and PDB helper functions
│   ├── 00_fetch_prepare.py  # Fetching and cleaning raw structures
│   ├── 10_epitope_sasa.py   # Epitope accessibility and glycan modeling
│   ├── 20_design_rfmpnn.py  # RFdiffusion + ProteinMPNN candidate generation
│   ├── 30_predict_complex.py# Folding predictions via AlphaFold-Multimer/IgFold
│   ├── 40_dock_score.py     # Rosetta/Vina docking scoring run
│   ├── 50_mm_pbsa.py        # Molecular dynamics MM/PBSA simulation
│   └── 60_filters_rank.py   # Multi-metric filtering and ranking
│
├── results/
│   ├── docking/     # PDB files of docked complex poses
│   ├── figures/     # SASA plots, overlays, and heatmaps
│   └── metrics/     # Ranked CSV tables and metrics
│
├── docs/            # Literature notes and publication roadmap
│   ├── literature_notes.md
│   └── publication_roadmap.md
│
├── README.md
└── requirements.txt



Objectives
Curate the HA Structural Panel: Assemble H3N2 and H4N1 representative structures and identify residue numbers for the Pro/Trp epitope.
Epitope Accessibility & Glycan Modeling: Analyze Solvent Accessible Surface Area (SASA) and steric occlusion by nearby glycans.
Paratope Motif-Guided Design: Run RFdiffusion with motif constraints to generate paratope structures mimicking VH5-9-1's hydrophobic sandwich, followed by sequence design using ProteinMPNN.
Structure Prediction & Folding: Use AlphaFold-Multimer or ColabFold to predict designed antibody-HA complex structures.
Docking & Scoring: Dock designs to the HA panel using Rosetta or AutoDock Vina.
Classifier Training: Train a scikit-learn classifier (Random Forest/XGBoost) to rank candidates based on geometric and chemical interface features.
Cross-Strain Breadth Evaluation: Score designed antibodies against diverse H3 strains and check portability to H1 and H5 analogs.
Reference Panels
Hemagglutinin Structures
H3N2 Panel: PDB 4WE4, 4WE5, 4ZCJ, 8TJ7, 2VIU, 2HMG
H4N1 Panel: PDB 5Y2M, 6V44, 5XL8, 6V47
H1N1 Panel (Exploratory): PDB 4JTV, 6Q0C
H5N1 Panel (Exploratory): PDB 6AOU, 4WE8
VH5-9-1 Class Seed Antibodies
6N5B: VH5-9-1 Fab bound to H3 HA (residues Pro217/Trp218, corresponding to H3 Pro221/Trp222)
6N5D: VH5-9-1 Fab bound to H4 HA
6N5E: VH5-9-1 Fab bound to H3 HA (strain A/Aichi/2/1968 H3N2)
Setup

conda create -y -n ha_bnab python=3.10
conda activate ha_bnab
pip install -r requirements.txt

python scripts/00_fetch_prepare.py
