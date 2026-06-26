# 8-Week Scientific Publication Roadmap

This roadmap defines a weekly plan to complete the **HA Broadly Neutralizing Antibody (bnAb) Design project**, perform computational experiments, analyze results, and write a complete manuscript suitable for submission to a peer-reviewed scientific journal (e.g., *PLOS Computational Biology*, *Bioinformatics*, or *Antibodies*) in approximately 2 months.

---

## Overall Timeline at a Glance

| Phase | Weeks | Focus | Deliverables |
|-------|-------|-------|--------------|
| **Data & Framework** | 1–2 | Curate HA structures, extract paratope features | Aligned sequences, epitope coordinates, classifier training data |
| **Computational Design** | 3–4 | RFdiffusion, ProteinMPNN, baseline docking | 100+ candidate antibodies with docking scores |
| **Validation & Scoring** | 5–6 | AlphaFold-Multimer, FoldX, cross-strain evaluation | Structure predictions, binding affinity estimates, breadth validation |
| **Manuscript & Writing** | 7–8 | Draft, refine, compile figures, finalize submission | Complete manuscript ready for peer review |

---

## Week-by-Week Breakdown

### **Week 1: Data Curation & Structural Panel**

**Objectives:**
- Download and curate HA structures (H3, H4, H1, H5) from PDB
- Align sequences and identify target epitope residues (Pro221/Trp222 in H3N2)
- Extract VH5-9-1 reference antibody structures (6N5B, 6N5D, 6N5E)
- Quantify SASA and glycan proximity to epitope

**Tasks:**
- [ ] Fetch PDB files: 4WE4, 4WE5, 4ZCJ, 8TJ7, 2VIU, 2HMG (H3N2)
- [ ] Fetch PDB files: 5Y2M, 6V44, 5XL8, 6V47 (H4N1)
- [ ] Extract HA sequences and align (MAFFT or MUSCLE)
- [ ] Identify Pro/Trp residues and calculate SASA values
- [ ] Extract VH5-9-1 Fab structures and quantify paratope geometry

**Deliverables:**
- Curated HA structure dataset (`.pdb` files, `.csv` with metadata)
- Sequence alignment (FASTA, `.aln`)
- SASA and glycan proximity report

**Tools:** PyMOL, DSSP, MAFFT, Biopython

---

### **Week 2: Epitope Feature Extraction & Classifier Preparation**

**Objectives:**
- Extract geometric and chemical features from VH5-9-1 paratope
- Build training dataset for ML classifier
- Compute baseline metrics (buried surface area, contact counts)
- Set up training/validation splits

**Tasks:**
- [ ] Extract CDR sequences, loop conformations, and contact residues from 6N5B
- [ ] Calculate interface geometry (angles, distances, curvature)
- [ ] Compute chemical features (hydrophobicity, charge, SASA)
- [ ] Generate negative controls (random antibodies)
- [ ] Create `.csv` file for classifier training (features × labels)

**Deliverables:**
- Feature extraction pipeline (`scripts/extract_features.py`)
- Training dataset (`.csv` with 50–100 reference designs)
- Baseline metrics report

**Tools:** Rosetta, ProDy, scikit-learn

---

### **Week 3: Baseline Classifier & Test Docking**

**Objectives:**
- Train a Random Forest or XGBoost classifier on extracted features
- Validate on held-out test set
- Run test docking with RosettaDock or Vina on 1–2 HA structures
- Establish scoring baseline

**Tasks:**
- [ ] Train Random Forest classifier (hyperparameter tuning)
- [ ] Cross-validate on 10 HA structures (leave-one-out)
- [ ] Dock VH5-9-1 Fab to H3 HA (4WE4) using Rosetta or Vina
- [ ] Dock 10 random antibodies as negative controls
- [ ] Calculate AUC, precision, recall; plot ROC curve

**Deliverables:**
- Trained classifier model (`.pkl`, XGBoost/RandomForest)
- Test docking PDB files and scores (`.csv`)
- Classifier validation report (ROC, AUC, feature importance)

**Tools:** scikit-learn, XGBoost, Rosetta, AutoDock Vina

---

### **Week 4: Large-Scale RFdiffusion + ProteinMPNN Design**

**Objectives:**
- Run motif-constrained RFdiffusion to generate 100–200 novel paratope scaffolds
- Use ProteinMPNN to design antibody sequences
- Score all designs with the trained classifier
- Select top 50 candidates for folding

**Tasks:**
- [ ] Set up RFdiffusion with VH5-9-1 motif constraints (CDR geometry)
- [ ] Generate 200 paratope backbones (vary length, loop conformation)
- [ ] Run ProteinMPNN for sequence design on all 200 scaffolds
- [ ] Score all 200 designs with trained classifier
- [ ] Rank by classifier score and select top 50 for AlphaFold

**Deliverables:**
- 200 designed antibody sequences (FASTA)
- Classifier scores for all designs (`.csv`)
- Top 50 candidate list with rankings

**Tools:** RFdiffusion, ProteinMPNN, scikit-learn

---

### **Week 5: Structure Prediction & Complex Folding**

**Objectives:**
- Predict 3D structures of top 50 antibodies using AlphaFold2-Multimer or IgFold
- Dock all predictions to full HA trimer panel (H3N2, H4N1)
- Calculate binding energy estimates (Rosetta REU, Vina score)
- Filter for designs with favorable energetics

**Tasks:**
- [ ] Run AlphaFold2-Multimer for 50 antibody–HA complex predictions
- [ ] Validate pAE (predicted aligned error) scores for confidence
- [ ] Dock all 50 designs to 2–3 representative HA structures (4WE4, 5Y2M)
- [ ] Calculate Rosetta energy or Vina docking score per design
- [ ] Filter for ΔG < –8 kcal/mol; retain ~20–30 designs

**Deliverables:**
- AlphaFold2-Multimer PDB files (50 complexes)
- Docking PDB files for all designs (top-scored pose)
- Binding energy report (`.csv`: design ID, HA target, ΔG, confidence)

**Tools:** AlphaFold2-Multimer, ColabFold, Rosetta, Vina, PyRosetta

---

### **Week 6: FoldX & Breadth Validation (Cross-Strain Testing)**

**Objectives:**
- Run FoldX MM/PBSA to refine binding affinity predictions
- Test top designs against diverse H3 strains (4ZCJ, 8TJ7, 2VIU)
- Evaluate cross-reactivity to H1 (W210 analog) and H5 (F225 analog)
- Assess breadth and strain coverage

**Tasks:**
- [ ] Run FoldX AnalyzeComplex on top 25 designs
- [ ] Extract ΔΔG estimates and per-residue contributions
- [ ] Dock top 25 designs to 4–5 H3N2 strains from reference panel
- [ ] Dock top 25 designs to H1N1 (4JTV) and H5N1 (6AOU)
- [ ] Calculate breadth metric (% HA strains with ΔG < –6 kcal/mol)
- [ ] Identify top 5–10 designs with highest breadth

**Deliverables:**
- FoldX energy decomposition (`.csv`: per-residue contributions)
- Cross-strain docking results (`.csv`: design × HA strain × score)
- Breadth ranking and selectivity analysis
- Heatmap: designs vs. strains (ΔG values)

**Tools:** FoldX, Rosetta, matplotlib, seaborn

---

### **Week 7: Manuscript Draft — Introduction, Methods, Results**

**Objectives:**
- Write scientific manuscript (target 8,000–10,000 words)
- Draft Introduction (VH5-9-1 lineage, HA structure, bnAb targets)
- Write detailed Methods (data curation, design pipeline, validation)
- Compile Results section with key figures

**Tasks:**
- [ ] Write Introduction (2 pages): HA biology, bnAb design, project rationale
- [ ] Write Methods section:
  - Data curation & structure preprocessing
  - RFdiffusion & ProteinMPNN protocols
  - Docking & scoring methodology
  - ML classifier training & validation
  - Cross-strain testing procedure
- [ ] Create **Figure 1:** HA structural panel & epitope identification
- [ ] Create **Figure 2:** VH5-9-1 paratope geometry & motif constraints
- [ ] Create **Figure 3:** RFdiffusion pipeline schematic
- [ ] Create **Figure 4:** Docking results (top designs vs. HA)
- [ ] Create **Figure 5:** Breadth heatmap (designs × strains)
- [ ] Write Results section (main findings, statistical summaries)

**Deliverables:**
- Manuscript draft (introduction, methods, results)
- Publication-quality figures (5 main figures + supplement)
- Supplementary tables (full design metrics, sequences)

**Tools:** LaTeX, matplotlib, seaborn, PyMOL (figure rendering)

---

### **Week 8: Manuscript Refinement, Discussion & Submission**

**Objectives:**
- Write Discussion, Conclusions, and Abstract
- Integrate peer feedback and refine figures
- Finalize supplementary materials
- Prepare for journal submission (PLOS Computational Biology recommended)

**Tasks:**
- [ ] Write Discussion (interpretation, mechanistic insights, limitations)
- [ ] Write Conclusions & Future Directions
- [ ] Draft Abstract (250–300 words)
- [ ] Revise Introduction, Methods, Results for clarity
- [ ] Compile supplementary figures (10–15 additional figures)
- [ ] Create supplementary tables (full sequences, metrics)
- [ ] Format references (PubMed format, 80–100 citations)
- [ ] Internal review & copyediting
- [ ] Prepare submission package (`.pdf`, `.docx`, figures, SI)

**Deliverables:**
- Complete manuscript (Introduction, Methods, Results, Discussion, Conclusions)
- Abstract (standalone)
- All figures & supplementary materials
- Submission-ready LaTeX or Word file

---

## Key Milestones & Checkpoints

| Week | Milestone | Status |
|------|-----------|--------|
| **1** | ✓ HA structural panel curated; SASA & epitope features extracted | ⭕ To Do |
| **2** | ✓ Classifier training dataset ready | ⭕ To Do |
| **3** | ✓ Baseline classifier trained & validated; test docking complete | ⭕ To Do |
| **4** | ✓ 200 antibody designs generated & scored | ⭕ To Do |
| **5** | ✓ AlphaFold-Multimer predictions & docking complete | ⭕ To Do |
| **6** | ✓ FoldX refinement & cross-strain validation; Top 5–10 candidates identified | ⭕ To Do |
| **7** | ✓ Manuscript draft (I, M, R, figures) ready for internal review | ⭕ To Do |
| **8** | ✓ **Complete manuscript & supplementary materials ready for submission** | ⭕ To Do |

---

## Target Journals

1. **[PRIMARY] *PLOS Computational Biology*** — Excellent fit for computational antibody design; strong impact; ~4-month review cycle
2. ***Bioinformatics*/** — High-quality computational methods journal
3. ***Antibodies*** — Specialized antibody design & engineering journal (faster review)
4. ***Nature Communications*** / **Science Advances** — If results are exceptionally strong

### Estimated Journal Timeline
- **Week 8:** Submit manuscript
- **Week 12–16:** Peer review & minor revisions
- **Week 16–20:** Final acceptance & publication

---

## Writing & Collaboration Tips

- **Use shared docs:** Google Docs or Overleaf for real-time manuscript editing
- **Version control:** Commit manuscript drafts to Git weekly
- **Figure quality:** Render all structures in PyMOL with consistent coloring/styling
- **Supplementary data:** Organize all sequences, metrics, and PDB files in `results/`
- **External review:** Send draft to 1–2 collaborators by end of Week 7

---

## Resources & References

- [Antibody structure & design overview](https://www.ncbi.nlm.nih.gov/pubmed/)
- [AlphaFold2-Multimer tutorial](https://github.com/deepmind/alphafold)
- [RFdiffusion & ProteinMPNN papers](https://arxiv.org/search/q-bio)
- [PLOS Computational Biology submission guidelines](https://journals.plos.org/ploscompbiol/s/submission-guidelines)

---

## Contact & Support

For questions or roadmap adjustments, contact the project lead.

---

*Last updated: June 2026*  
*Timeline is flexible and may be adjusted based on computational availability and results.*
