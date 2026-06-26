import os
import pandas as pd
from Bio import PDB
from Bio.PDB.SASA import ShrakeRupley
import utils

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
METADATA_FILE = os.path.join(BASE_DIR, "data", "processed", "ha_structures_curated.csv")
SASA_SUMMARY_FILE = os.path.join(BASE_DIR, "data", "processed", "epitope_sasa_summary.csv")

def find_nearby_glycans(model, chain_id, target_residue, max_dist=15.0):
    min_dist = float("inf")
    closest_glycan = None
    target_atoms = list(target_residue.get_atoms())
    
    for other_chain in model:
        for residue in other_chain:
            res_name = residue.get_resname().strip().upper()
            if res_name in ["NAG", "NGA", "MAN", "BMA", "FUC", "GAL"]:
                for atom_t in target_atoms:
                    for atom_g in residue.get_atoms():
                        dist = atom_t - atom_g
                        if dist < min_dist:
                            min_dist = dist
                            closest_glycan = f"{other_chain.get_id()}_{residue.get_id()[1]}_{res_name}"
                            
    return min_dist, closest_glycan

def check_glycosylation_sequons(chain, target_res_num, window=10):
    residues = list(chain.get_residues())
    found_sequons = []
    
    for i in range(len(residues) - 2):
        r1 = residues[i]
        r2 = residues[i+1]
        r3 = residues[i+2]
        
        name1 = r1.get_resname().strip().upper()
        name2 = r2.get_resname().strip().upper()
        name3 = r3.get_resname().strip().upper()
        
        if name1 == "ASN" and name2 != "PRO" and name3 in ["SER", "THR"]:
            asn_num = r1.get_id()[1]
            dist = abs(asn_num - target_res_num)
            if dist <= window:
                found_sequons.append(f"ASN{asn_num}_dist_{dist}")
                
    return ";".join(found_sequons) if found_sequons else "None"

def main():
    print("=== Step 10: Epitope Exposure & SASA Pipeline ===")
    
    if not os.path.exists(METADATA_FILE):
        print(f"Curated metadata not found at {METADATA_FILE}. Run 00_fetch_prepare.py first.")
        return
        
    df_meta = pd.read_csv(METADATA_FILE)
    sasa_records = []
    
    parser = PDB.PDBParser(QUIET=True)
    sr = ShrakeRupley()
    
    for idx, row in df_meta.iterrows():
        pdb_id = row["PDB_ID"]
        chain_id = row["Chain"]
        motif = row["Detected_Pro_Trp_Motif"]
        cleaned_rel_path = row["Cleaned_Path"]
        cleaned_path = os.path.join(BASE_DIR, cleaned_rel_path)
        
        if motif == "None" or not os.path.exists(cleaned_path):
            continue
            
        print(f"Calculating SASA for {pdb_id} chain {chain_id}...")
        try:
            struct = parser.get_structure(pdb_id, cleaned_path)
            model = struct[0]
            chain = model[chain_id]
            
            sr.compute(model, level="R")
            
            motifs = motif.split(";")
            for m in motifs:
                parts = m.split("-")
                pro_part = parts[0]
                trp_part = parts[1]
                
                pro_num = int("".join([c for c in pro_part if c.isdigit()]))
                trp_num = int("".join([c for c in trp_part if c.isdigit()]))
                
                pro_res = chain[pro_num]
                trp_res = chain[trp_num]
                
                pro_sasa = pro_res.sasa
                trp_sasa = trp_res.sasa
                
                glycan_dist, closest_glycan = find_nearby_glycans(model, chain_id, trp_res)
                sequons = check_glycosylation_sequons(chain, trp_num)
                
                sasa_records.append({
                    "PDB_ID": pdb_id,
                    "Panel": row["Panel"],
                    "Chain": chain_id,
                    "Pro_Res_Num": pro_num,
                    "Pro_SASA": round(pro_sasa, 2),
                    "Trp_Res_Num": trp_num,
                    "Trp_SASA": round(trp_sasa, 2),
                    "Total_Motif_SASA": round(pro_sasa + trp_sasa, 2),
                    "Min_Glycan_Distance_Angstrom": round(glycan_dist, 2) if glycan_dist != float("inf") else -1.0,
                    "Closest_Glycan_Residue": closest_glycan if closest_glycan else "None",
                    "Nearby_Glycosylation_Sequons": sequons
                })
        except Exception as e:
            print(f"Error analyzing SASA for {pdb_id} chain {chain_id}: {e}")
            
    df_sasa = pd.DataFrame(sasa_records)
    df_sasa.to_csv(SASA_SUMMARY_FILE, index=False)
    print(f"\nSaved SASA metrics to {SASA_SUMMARY_FILE}")

if __name__ == "__main__":
    main()
