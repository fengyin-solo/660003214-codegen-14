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
  order: number // 1=single, 2=double, 3=triple
}

export interface Molecule {
  id: number
  name: string
  smiles: string
  formula: string
  mw: number
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
