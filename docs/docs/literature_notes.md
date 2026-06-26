# Literature Review and Research Background

This document compiles the biological background, structural rationale, and key references for the computational design of antibodies targeting conserved Influenza Hemagglutinin (HA) epitopes.

---

## 1. The Core Challenge: Antigenic Drift & Variable Epitopes
Most neutralizing antibodies elicited by seasonal influenza infection or vaccination target the globular head domain of Hemagglutinin (HA1).
- **The Problem**: The head domain is highly immunodominant but tolerates extensive mutations, allowing the virus to undergo rapid **antigenic drift** and evade host immunity.
- **The Solution**: Target subdominant but highly conserved "cryptic" or "stem" epitopes that are essential for the viral life cycle (e.g., membrane fusion machinery) and less prone to mutational escape.

---

## 2. Conserved Epitopes of Influenza Hemagglutinin

### The HA Stem Region (Group 1 vs. Group 2 Broad Neutralizers)
- The HA stem is composed mainly of the HA2 subunit and is highly conserved across strains.
- **Precedent bnAbs**: 
  - **CR6261** (Group 1 specific): Binds to the stem groove using only its heavy chain (VH1-69 germline).
  - **FI6v3** (Group 1 & 2 pan-influenza A): Arises from the VH3-30 germline, using both heavy and light chains to bind a conserved stem epitope.
  - **CR9114** (Pan-influenza A & B): Neutralizes both influenza A and B viruses by targeting a highly conserved stem epitope.

### Cryptic/Occluded Head Epitopes
- **Breathing HA**: The HA trimer is not static. It undergoes transient, reversible opening and closing motions ("breathing") that temporarily expose occluded epitopes near the interface between monomer subunits or in the head domain.
- **The Pro221/Trp222 Motif (H3 numbering)**:
  - Located in the H3 head domain. This motif forms a partially occluded hydrophobic pocket.
  - In structural analogs, it is represented by **W210** in H1 and **F225** in H5.
  - The residue Trp222 is highly conserved across historical H3 and H4 strains.
  - **VH5-9-1 Class Antibodies**: Natural human antibodies from the VH5-9-1 germline family utilize a long CDR H3 loop containing aromatic side chains (Tyr, Phe, Trp) that insert into the hydrophobic pocket to form a **"hydrophobic sandwich"** flanking the HA Trp residue. This interaction allows cross-reactive binding across multiple H3 and H4 strains.

---

## 3. Glycan Shielding and Masking

### The Role of Glycans
- Influenza HA is heavily glycosylated with host-derived N-linked glycans. These glycans act as a steric shield, hiding conserved epitopes from immune recognition.
- Over evolutionary time, H3 strains have doubled their number of N-linked glycosylation sites (PNGs) from 7 in 1968 to 14 in modern strains, increasing the density of the glycan shield.

### Glycan Masking as a Tool
- **Antigen Engineering**: Strategically introducing or removing N-linked glycosylation sites (`N-X-S/T` motifs, where `X != P`) can reshape the immune response:
  - **Hyper-glycosylation** can mask immunodominant variable sites, redirecting the immune system's attention toward subdominant conserved sites (like the stem or cryptic head clefts).
  - Successful glycan masking redirects specificity toward preferred VH germline usage (e.g., VH1-69, VH3-30) that can mature into bnAbs.

---

## 4. Key References and Structural Targets

### Structural Data
- **H3 HA Complex with VH5-9-1 (6N5B)**: Standard template showing the hydrophobic sandwich. Specifically, HA residues Pro217 and Trp218 (PDB numbering) are bound by Fab CDR loops. Trp218 is engaged in aromatic stacking with the antibody.
- **H4 HA Complex with VH5-9-1 (6N5D)**: Shows similar conservation of the hydrophobic sandwich.
- **H3 HA (6N5E)**: Structure showing the motif in A/Aichi/2/1968.

### Key Literature
1. **AlphaFold & ColabFold**: *Nature* (2021) & *Nature Methods* (2022). Foundational tools for structure prediction and complex modeling.
2. **RFdiffusion**: *Nature* (2023). Generates paratope backbones conditioned on target motifs (e.g., placing aromatic side chains around Trp222).
3. **ProteinMPNN**: *Science* (2022). Optimizes candidate antibody sequences for stability and binding geometry.
4. **Bajic et al., Cell Host & Microbe (2019)**: *Influenza antigen engineering focuses immune responses to a conserved epitope*. Demonstrates glycan masking to expose occluded epitopes and redirect antibody responses.
5. **Breathing HA Review**: *Breathing Hemagglutinin Reveals Cryptic Epitopes for Universal Influenza Vaccine Design*. Discusses conformational dynamics exposing hidden clefts.
