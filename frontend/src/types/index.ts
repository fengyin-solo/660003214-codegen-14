export interface Atom3D {
  element: string
  x: number
  y: number
  z: number
  color: string
  radius: number
}

export interface Bond3D {
  atom1: number
  atom2: number
  order: number
}

export interface Molecule {
  id: number
  name: string
  smiles: string
  formula: string
  mw: number
  logP: number
  category: string
  atoms: Atom3D[]
  bonds: Bond3D[]
}

export interface ADMETProps {
  logP: number
  logS: number
  toxicity: string
  proteinBinding: number
  metabolicStability: string
  bioavailability: number
  ruleOfFive: boolean
  violations: number
}

export interface MoleculeData {
  id: number
  name: string
  smiles: string
  formula: string
  mw: number
  logP: number
  category: string
  atoms: Atom3D[]
  bonds: Bond3D[]
}

export interface CorrectionSuggestion {
  original: string
  corrected: string
  confidence: number
  reason: string
  error_type: string
}

export interface SmilesCorrectionResponse {
  original: string
  is_valid: boolean
  errors: string[]
  best_correction: CorrectionSuggestion | null
  suggestions: CorrectionSuggestion[]
  can_continue: boolean
}

export interface ParseResult {
  atoms: Atom3D[]
  bonds: Bond3D[]
  correction_applied?: boolean
  original_smiles?: string
  corrected_smiles?: string
  errors?: string[]
  confidence?: number
  used_corrected?: boolean
}

export interface ParseWithCorrectionResponse {
  correction: SmilesCorrectionResponse
  parse_result: ParseResult | null
}
