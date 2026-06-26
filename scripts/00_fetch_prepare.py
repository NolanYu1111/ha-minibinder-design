import os
import pandas as pd
from Bio import PDB
import utils

# Define structural panels
HA_PANELS = {
    # Templates with VH5-9-1 antibodies
    "VH5-9-1_Templates": ["6N5B", "6N5D", "6N5E"],
    # H3N2 panel (historical and recent)
    "H3N2": ["4WE4", "4WE5", "4ZCJ", "8TJ7", "2VIU", "2HMG"],
    # H4N1 panel (structurally similar to H3)
    "H4N1": ["5Y2M", "6V44", "5XL8", "6V47"],
    # Exploratory panels
    "H1N1": ["4JTV", "6Q0C"],
    "H5N1": ["6AOU", "4WE8"]
}

# Directory configuration
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw", "pdbs")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed", "pdbs")
METADATA_FILE = os.path.join(BASE_DIR, "data", "processed", "ha_structures_curated.csv")

def main():
    print("=== Step 00: PDB Curation & Processing Pipeline ===")
    os.makedirs(RAW_DIR, exist_ok=True)
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    metadata_records = []
    
    for panel_name, pdb_ids in HA_PANELS.items():
        print(f"\nProcessing Panel: {panel_name}")
        for pdb_id in pdb_ids:
            # 1. Download PDB
            raw_path = utils.download_pdb(pdb_id, RAW_DIR)
            if not raw_path:
                print(f"Failed to download {pdb_id}")
                continue
                
            # 2. Clean structure (remove water/heteroatoms, keep first model)
            cleaned_filename = f"{pdb_id}_cleaned.pdb"
            cleaned_path = os.path.join(PROCESSED_DIR, cleaned_filename)
            utils.clean_pdb(raw_path, cleaned_path)
            
            # 3. Analyze structure and fetch basic metadata
            parser = PDB.PDBParser(QUIET=True)
            struct = parser.get_structure(pdb_id, cleaned_path)
            model = struct[0]
            
            header = parser.get_header() if hasattr(parser, 'get_header') else {}
            resolution = header.get("resolution", "N/A")
            
            chains = [chain.get_id() for chain in model.get_chains()]
            chain_str = ",".join(chains)
            
            print(f"PDB {pdb_id}: Resolution = {resolution}, Chains = {chain_str}")
            
            for chain in model:
                residues = list(chain.get_residues())
                seq_len = len(residues)
                
                motif_res = []
                for i in range(len(residues) - 1):
                    res1 = residues[i]
                    res2 = residues[i+1]
                    res1_name = res1.get_resname().strip().upper()
                    res2_name = res2.get_resname().strip().upper()
                    
                    if res1_name == "PRO" and res2_name == "TRP":
                        res1_num = res1.get_id()[1]
                        res2_num = res2.get_id()[1]
                        motif_res.append(f"{res1_num}PRO-{res2_num}TRP")
                
                motif_str = ";".join(motif_res) if motif_res else "None"
                
                metadata_records.append({
                    "PDB_ID": pdb_id,
                    "Panel": panel_name,
                    "Chain": chain.get_id(),
                    "Resolution_Angstroms": resolution,
                    "Chains_In_Structure": chain_str,
                    "Residue_Count": seq_len,
                    "Detected_Pro_Trp_Motif": motif_str,
                    "Cleaned_Path": os.path.relpath(cleaned_path, BASE_DIR)
                })

    df = pd.DataFrame(metadata_records)
    df.to_csv(METADATA_FILE, index=False)
    print(f"\nSaved curated metadata to {METADATA_FILE}")

if __name__ == "__main__":
    main()
