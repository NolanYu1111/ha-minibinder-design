# 8-Week Scientific Publication Roadmap

This roadmap defines a weekly plan to complete the HA Broadly Neutralizing Antibody (bnAb) Design project, perform the computational experiments, analyze the results, and write a complete manuscript suitable for submission to a peer-reviewed scientific journal (e.g., *PLOS Computational Biology*, *Bioinformatics*, or *Antibodies*) in approximately 2 months.

---

## Overall Timeline at a Glance

```mermaid
gantt
    title 8-Week Computational Antibody Design & Publication Roadmap
    dateFormat  X
    axisFormat Week %d
    
    section Data & Framework
    Week 1: Curate structural panels & align sequences         :active, 0, 1
    Week 2: Extract paratopes & setup classifier data         :active, 1, 2
    
    section Computational Design
    Week 3: Train baseline classifier & run test docking      : 2, 3
    Week 4: Large-scale RFdiffusion + ProteinMPNN candidate design : 3, 4
    
    section Validation & Scoring
    Week 5: Fold with AlphaFold & dock with Vina/Rosetta     : 4, 5
    Week 6: Run FoldX, check glycan proximity & evaluate breadth : 5, 6
    
    section Manuscript & Writing
    Week 7: Draft Introduction, Methods, and Results          : 6, 7
    Week 8: Refine Discussion, compile figures, and format    : 7, 8
