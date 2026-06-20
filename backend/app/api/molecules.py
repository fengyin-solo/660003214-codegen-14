from fastapi import APIRouter, HTTPException
from app.services.admet import parse_smiles, compute_admet

router = APIRouter()

MOLECULES = [
    {"id": 1, "name": "阿司匹林", "smiles": "CC(=O)Oc1ccccc1C(=O)O", "formula": "C9H8O4", "mw": 180.16, "logP": 1.19, "category": "解热镇痛"},
    {"id": 2, "name": "布洛芬", "smiles": "CC(C)Cc1ccc(cc1)C(C)C(=O)O", "formula": "C13H18O2", "mw": 206.28, "logP": 3.97, "category": "解热镇痛"},
    {"id": 3, "name": "青霉素G", "smiles": "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O", "formula": "C16H18N2O4S", "mw": 334.39, "logP": 1.83, "category": "抗生素"},
    {"id": 4, "name": "咖啡因", "smiles": "Cn1c(=O)c2c(ncn2C)n(C)c1=O", "formula": "C8H10N4O2", "mw": 194.19, "logP": -0.07, "category": "中枢神经"},
    {"id": 5, "name": "二甲双胍", "smiles": "CN(C)C(=N)N=C(N)N", "formula": "C4H11N5", "mw": 129.16, "logP": -1.43, "category": "降糖药"},
    {"id": 6, "name": "阿莫西林", "smiles": "CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)NCc4ccc(O)c(O)c4", "formula": "C16H19N3O5S", "mw": 365.4, "logP": 0.87, "category": "抗生素"},
    {"id": 7, "name": "扑热息痛", "smiles": "CC(=O)Nc1ccc(O)cc1", "formula": "C8H9NO2", "mw": 151.16, "logP": 0.46, "category": "解热镇痛"},
    {"id": 8, "name": "维生素C", "smiles": "OCC(O)C1OC(=O)C(O)=C1O", "formula": "C6H8O6", "mw": 176.12, "logP": -2.41, "category": "维生素"},
    {"id": 9, "name": "地西泮", "smiles": "Clc1ccc(N2C(=O)CN=C(c3ccccc3)c3cc(Cl)ccc32)cc1", "formula": "C16H13ClN2O", "mw": 284.74, "logP": 2.82, "category": "中枢神经"},
    {"id": 10, "name": "奥美拉唑", "smiles": "COc1ccc2[nH]c(nc2c1)S(=O)Cc1ncc(C)c(OC)c1C", "formula": "C17H19N3O3S", "mw": 345.41, "logP": 1.17, "category": "消化系统"},
    {"id": 11, "name": "阿替洛尔", "smiles": "CC(C)NCC(O)COc1ccc2CCNC(=O)c2c1", "formula": "C14H22N2O3", "mw": 266.34, "logP": 0.5, "category": "心血管"},
    {"id": 12, "name": "头孢氨苄", "smiles": "CC1=C(C(=O)NC(=O)C1SCC2=C(C(=C(N2)C(=O)O)N)C)c3ccc(O)cc3", "formula": "C16H17N3O4S", "mw": 347.39, "logP": -0.53, "category": "抗生素"},
    {"id": 13, "name": "辛伐他汀", "smiles": "CCC(C)C1C(=O)C2C(C1(C)C)CCC3=C(C2)C(C4=CC(=CC=C4)F)O3", "formula": "C25H38O5", "mw": 418.57, "logP": 4.68, "category": "降脂药"},
    {"id": 14, "name": "西咪替丁", "smiles": "NC(=N)NCCSCc1nc(C)c(C)n1", "formula": "C10H16N6S", "mw": 252.34, "logP": -0.2, "category": "消化系统"},
    {"id": 15, "name": "硝苯地平", "smiles": "COC(=O)C1=C(C)NC(C)=C(C(=O)OC)C1c1ccccc1[N+](=O)[O-]", "formula": "C17H18N2O6", "mw": 346.34, "logP": 2.2, "category": "心血管"},
    {"id": 16, "name": "美托洛尔", "smiles": "COCC(O)CNC(C)Cc1ccc(OCC)cc1", "formula": "C15H25NO3", "mw": 267.36, "logP": 1.88, "category": "心血管"},
    {"id": 17, "name": "雷尼替丁", "smiles": "CN(C)/C=N/CCSCc1c[nH]c(=O)n1", "formula": "C13H22N4O3S", "mw": 314.4, "logP": 0.27, "category": "消化系统"},
    {"id": 18, "name": "氟西汀", "smiles": "CNCCC(Oc1ccc(F)cc1)c1ccccc1", "formula": "C17H18FNO", "mw": 271.33, "logP": 4.05, "category": "中枢神经"},
    {"id": 19, "name": "吉非罗齐", "smiles": "CC(C)c1ccc(C(=O)OC(CCO)C(C)C)cc1", "formula": "C15H22O3", "mw": 250.33, "logP": 4.77, "category": "降脂药"},
    {"id": 20, "name": "卡托普利", "smiles": "CCC(C)C(C(=O)O)NC(=O)CCS", "formula": "C9H15NO3S", "mw": 217.29, "logP": -0.5, "category": "心血管"}
]

@router.get("/")
def list_molecules():
    return MOLECULES

@router.get("/{mol_id}")
def get_molecule(mol_id: int):
    mol = next((m for m in MOLECULES if m["id"] == mol_id), None)
    if not mol:
        raise HTTPException(status_code=404, detail="Molecule not found")
    atoms, bonds = parse_smiles(mol["smiles"])
    return {**mol, "atoms": atoms, "bonds": bonds}

@router.get("/{mol_id}/admet")
def get_admet(mol_id: int):
    mol = next((m for m in MOLECULES if m["id"] == mol_id), None)
    if not mol:
        raise HTTPException(status_code=404, detail="Molecule not found")
    return compute_admet(mol["mw"], mol["logP"], mol["formula"])

@router.post("/smiles")
def parse_smiles_endpoint(smiles: str):
    atoms, bonds = parse_smiles(smiles)
    return {"atoms": atoms, "bonds": bonds}
