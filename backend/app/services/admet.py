import numpy as np

ATOM_COLORS = {"C": "#6b7280", "N": "#3b82f6", "O": "#ef4444", "S": "#eab308", "P": "#f97316", "H": "#e5e7eb", "F": "#22c55e", "Cl": "#16a34a"}
ATOM_RADII = {"C": 0.3, "N": 0.25, "O": 0.22, "S": 0.35, "P": 0.35, "H": 0.15, "F": 0.18, "Cl": 0.3}

def parse_smiles(smiles: str):
    atoms, bonds = [], []
    last_atom = -1
    pending_bond = 1
    i = 0
    while i < len(smiles):
        ch = smiles[i]
        if ch in '()[]':
            i += 1
            continue
        elif ch == '=':
            pending_bond = 2; i += 1; continue
        elif ch == '#':
            pending_bond = 3; i += 1; continue
        elif ch in '-+@':
            i += 1; continue
        elif ch.isupper():
            element = ch
            if i + 1 < len(smiles) and smiles[i + 1].islower():
                element += smiles[i + 1]; i += 1
            idx = len(atoms)
            atoms.append({
                "element": element,
                "x": float((idx % 3 - 1) * 1.5 + np.random.uniform(-0.3, 0.3)),
                "y": float((idx // 3 % 3 - 1) * 1.5 + np.random.uniform(-0.3, 0.3)),
                "z": float((idx // 9 - 1) * 1.5 + np.random.uniform(-0.3, 0.3)),
                "color": ATOM_COLORS.get(element, "#888888"),
                "radius": ATOM_RADII.get(element, 0.25)
            })
            if last_atom >= 0:
                bonds.append({"atom1": last_atom, "atom2": idx, "order": pending_bond})
            last_atom = idx
            pending_bond = 1
        i += 1
    return atoms, bonds

def compute_admet(mw: float, log_p: float, formula: str) -> dict:
    log_s = round(0.5 - 0.01 * (mw - 20) - log_p, 2)
    hbd = formula.count("O")
    hba = formula.count("N") + hbd
    violations = (1 if mw > 500 else 0) + (1 if log_p > 5 else 0) + (1 if hbd > 5 else 0) + (1 if hba > 10 else 0)
    toxicity = "高毒性风险" if log_p > 3 else "中等毒性" if log_p > 1 else "低毒性"
    protein_binding = min(99, max(10, round(log_p * 15 + 30)))
    metabolic_stability = "稳定" if mw < 300 else "中等" if mw < 450 else "不稳定"
    bioavailability = max(0, min(100, round(100 - log_p * 8 - mw * 0.05)))
    return {
        "logP": round(log_p, 2), "logS": log_s, "toxicity": toxicity,
        "proteinBinding": protein_binding, "metabolicStability": metabolic_stability,
        "bioavailability": bioavailability, "ruleOfFive": violations <= 1, "violations": violations
    }
