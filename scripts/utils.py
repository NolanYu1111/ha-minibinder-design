import os
import urllib.request
import numpy as np
from Bio import PDB

def download_pdb(pdb_id, output_dir):
    """
    Downloads a PDB file from RCSB.
    """
    os.makedirs(output_dir, exist_ok=True)
    pdb_id = pdb_id.upper()
    filename = f"{pdb_id}.pdb"
    filepath = os.path.join(output_dir, filename)
    
    if os.path.exists(filepath):
        print(f"PDB {pdb_id} already exists at {filepath}")
        return filepath
        
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    try:
        print(f"Downloading {pdb_id} from RCSB...")
        urllib.request.urlretrieve(url, filepath)
        return filepath
    except Exception as e:
        print(f"Error downloading PDB {pdb_id}: {e}")
        return None

def clean_pdb(input_filepath, output_filepath, keep_chains=None):
    """
    Cleans a PDB file by removing water molecules (HOH), solvent, and keeping
    only specified chains (or all protein chains if keep_chains is None).
    """
    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("struct", input_filepath)
    
    class CleanSelect(PDB.Select):
        def __init__(self, keep_chains):
            self.keep_chains = [c.upper() for c in keep_chains] if keep_chains else None
            
        def accept_model(self, model):
            # Only keep the first model (model 0)
            return model.get_id() == 0
            
        def accept_chain(self, chain):
            if self.keep_chains:
                return chain.get_id().upper() in self.keep_chains
            return True
            
        def accept_residue(self, residue):
            # Remove heteroatoms (water, ligands)
            res_name = residue.get_resname()
            hetfield = residue.get_id()[0]
            if hetfield.strip() != "":
                # Keep N-acetylglucosamine (NAG/NGA) for glycan analysis
                if res_name.strip() in ["NAG", "NGA", "MAN", "BMA", "FUC", "GAL"]:
                    return True
                return False
            return True

    io = PDB.PDBIO()
    io.set_structure(structure)
    os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
    io.save(output_filepath, CleanSelect(keep_chains))
    print(f"Cleaned structure saved to {output_filepath}")
    return output_filepath

def calculate_centroid(residue):
    """
    Calculates the centroid coordinates of the aromatic ring in a residue
    (TYR, PHE, TRP).
    """
    resname = residue.get_resname().strip().upper()
    atoms = []
    if resname == "PHE":
        atoms = ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"]
    elif resname == "TYR":
        atoms = ["CG", "CD1", "CD2", "CE1", "CE2", "CZ"]
    elif resname == "TRP":
        atoms = ["CG", "CD1", "CD2", "NE1", "CE2", "CE3", "CZ2", "CZ3", "CH2"]
    else:
        return np.mean([atom.get_coord() for atom in residue.get_atoms() if atom.get_name().startswith(("C", "N", "O", "S"))], axis=0)

    coords = []
    for atom_name in atoms:
        try:
            coords.append(residue[atom_name].get_coord())
        except KeyError:
            pass
            
    if coords:
        return np.mean(coords, axis=0)
    else:
        return np.mean([atom.get_coord() for atom in residue.get_atoms()], axis=0)

def calculate_min_distance(residue_a, residue_b):
    """
    Calculates the minimum distance (in Angstroms) between any heavy atom of residue_a
    and residue_b.
    """
    min_dist = float("inf")
    for atom_a in residue_a.get_atoms():
        if atom_a.get_name().startswith("H"):
            continue
        for atom_b in residue_b.get_atoms():
            if atom_b.get_name().startswith("H"):
                continue
            dist = atom_a - atom_b
            if dist < min_dist:
                min_dist = dist
    return min_dist
