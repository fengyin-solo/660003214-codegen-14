from pydantic import BaseModel
from typing import List, Optional

class Atom3D(BaseModel):
    element: str
    x: float
    y: float
    z: float
    color: str = "#888888"
    radius: float = 0.25

class Bond3D(BaseModel):
    atom1: int
    atom2: int
    order: int = 1

class MoleculeBase(BaseModel):
    name: str
    smiles: str
    formula: str
    mw: float
    logP: float
    category: str

class MoleculeData(MoleculeBase):
    id: int
    atoms: List[Atom3D] = []
    bonds: List[Bond3D] = []

class ADMETResult(BaseModel):
    logP: float
    logS: float
    toxicity: str
    proteinBinding: float
    metabolicStability: str
    bioavailability: float
    ruleOfFive: bool
    violations: int

class CorrectionSuggestion(BaseModel):
    original: str
    corrected: str
    confidence: float
    reason: str
    error_type: str

class SmilesCorrectionResponse(BaseModel):
    original: str
    is_valid: bool
    errors: List[str]
    best_correction: Optional[CorrectionSuggestion] = None
    suggestions: List[CorrectionSuggestion] = []
    can_continue: bool
