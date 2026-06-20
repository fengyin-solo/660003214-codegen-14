import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { MoleculeData, ADMETProps } from '../types'

const ATOM_COLORS: Record<string, string> = {
  C: '#6b7280', N: '#3b82f6', O: '#ef4444', S: '#eab308',
  P: '#f97316', H: '#e5e7eb', F: '#22c55e', Cl: '#16a34a',
  Br: '#7c2d12', I: '#8b5cf6', Na: '#ec4899', K: '#a855f7'
}

const ATOM_RADII: Record<string, number> = {
  C: 0.3, N: 0.25, O: 0.22, S: 0.35, P: 0.35,
  H: 0.15, F: 0.18, Cl: 0.3, Br: 0.35, I: 0.4
}

function parseSMILES(smiles: string): { atoms: any[]; bonds: any[] } {
  const atoms: any[] = []
  const bonds: any[] = []
  const stack: number[] = []
  let lastAtom = -1
  let pendingBond = 1
  let i = 0

  while (i < smiles.length) {
    const ch = smiles[i]
    if (ch === '(') { stack.push(lastAtom) }
    else if (ch === ')') { stack.pop() }
    else if (ch === '[') {
      let el = ''
      i++
      while (i < smiles.length && smiles[i] !== ']') { el += smiles[i]; i++ }
      const element = el.replace(/[^A-Za-z]/g, '').charAt(0).toUpperCase() + el.replace(/[^A-Za-z]/g, '').slice(1).toLowerCase()
      atoms.push({ element, x: (atoms.length % 3 - 1) * 1.5, y: (Math.floor(atoms.length / 3) % 3 - 1) * 1.5, z: (Math.floor(atoms.length / 9) - 1) * 1.5, color: ATOM_COLORS[element] || '#888', radius: ATOM_RADII[element] || 0.25 })
      if (lastAtom >= 0) bonds.push({ atom1: lastAtom, atom2: atoms.length - 1, order: pendingBond })
      lastAtom = atoms.length - 1
      pendingBond = 1
    }
    else if (ch === '=') { pendingBond = 2 }
    else if (ch === '#') { pendingBond = 3 }
    else if (ch === '-') { pendingBond = 1 }
    else if (/[A-Z]/.test(ch)) {
      let element = ch
      if (i + 1 < smiles.length && /[a-z]/.test(smiles[i + 1])) { element += smiles[i + 1]; i++ }
      atoms.push({ element, x: (atoms.length % 3 - 1) * 1.5 + Math.random() * 0.5, y: (Math.floor(atoms.length / 3) % 3 - 1) * 1.5 + Math.random() * 0.5, z: (Math.floor(atoms.length / 9) - 1) * 1.5 + Math.random() * 0.5, color: ATOM_COLORS[element] || '#888', radius: ATOM_RADII[element] || 0.25 })
      if (lastAtom >= 0) bonds.push({ atom1: lastAtom, atom2: atoms.length - 1, order: pendingBond })
      lastAtom = atoms.length - 1
      pendingBond = 1
    }
    i++
  }
  return { atoms, bonds }
}

const MOCK_MOLECULES: Omit<MoleculeData, 'atoms' | 'bonds'>[] = [
  { id: 1, name: '阿司匹林', smiles: 'CC(=O)Oc1ccccc1C(=O)O', formula: 'C9H8O4', mw: 180.16, logP: 1.19, category: '解热镇痛' },
  { id: 2, name: '布洛芬', smiles: 'CC(C)Cc1ccc(cc1)C(C)C(=O)O', formula: 'C13H18O2', mw: 206.28, logP: 3.97, category: '解热镇痛' },
  { id: 3, name: '青霉素G', smiles: 'CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)O', formula: 'C16H18N2O4S', mw: 334.39, logP: 1.83, category: '抗生素' },
  { id: 4, name: '咖啡因', smiles: 'Cn1c(=O)c2c(ncn2C)n(C)c1=O', formula: 'C8H10N4O2', mw: 194.19, logP: -0.07, category: '中枢神经' },
  { id: 5, name: '二甲双胍', smiles: 'CN(C)C(=N)N=C(N)N', formula: 'C4H11N5', mw: 129.16, logP: -1.43, category: '降糖药' },
  { id: 6, name: '阿莫西林', smiles: 'CC1(C)SC2C(NC(=O)Cc3ccccc3)C(=O)N2C1C(=O)NCc4ccc(O)c(O)c4', formula: 'C16H19N3O5S', mw: 365.4, logP: 0.87, category: '抗生素' },
  { id: 7, name: '扑热息痛', smiles: 'CC(=O)Nc1ccc(O)cc1', formula: 'C8H9NO2', mw: 151.16, logP: 0.46, category: '解热镇痛' },
  { id: 8, name: '维生素C', smiles: 'OCC(O)C1OC(=O)C(O)=C1O', formula: 'C6H8O6', mw: 176.12, logP: -2.41, category: '维生素' },
  { id: 9, name: '地西泮', smiles: 'Clc1ccc(N2C(=O)CN=C(c3ccccc3)c3cc(Cl)ccc32)cc1', formula: 'C16H13ClN2O', mw: 284.74, logP: 2.82, category: '中枢神经' },
  { id: 10, name: '奥美拉唑', smiles: 'COc1ccc2[nH]c(nc2c1)S(=O)Cc1ncc(C)c(OC)c1C', formula: 'C17H19N3O3S', mw: 345.41, logP: 1.17, category: '消化系统' },
  { id: 11, name: '阿替洛尔', smiles: 'CC(C)NCC(O)COc1ccc2CCNC(=O)c2c1', formula: 'C14H22N2O3', mw: 266.34, logP: 0.5, category: '心血管' },
  { id: 12, name: '头孢氨苄', smiles: 'CC1=C(C(=O)NC(=O)C1SCC2=C(C(=C(N2)C(=O)O)N)C)c3ccc(O)cc3', formula: 'C16H17N3O4S', mw: 347.39, logP: -0.53, category: '抗生素' },
  { id: 13, name: '辛伐他汀', smiles: 'CCC(C)C1C(=O)C2C(C1(C)C)CCC3=C(C2)C(C4=CC(=CC=C4)F)O3', formula: 'C25H38O5', mw: 418.57, logP: 4.68, category: '降脂药' },
  { id: 14, name: '西咪替丁', smiles: 'NC(=N)NCCSCc1nc(C)c(C)n1', formula: 'C10H16N6S', mw: 252.34, logP: -0.2, category: '消化系统' },
  { id: 15, name: '硝苯地平', smiles: 'COC(=O)C1=C(C)NC(C)=C(C(=O)OC)C1c1ccccc1[N+](=O)[O-]', formula: 'C17H18N2O6', mw: 346.34, logP: 2.2, category: '心血管' },
  { id: 16, name: '美托洛尔', smiles: 'COCC(O)CNC(C)Cc1ccc(OCC)cc1', formula: 'C15H25NO3', mw: 267.36, logP: 1.88, category: '心血管' },
  { id: 17, name: '雷尼替丁', smiles: 'CN(C)/C=N/CCSCc1c[nH]c(=O)n1', formula: 'C13H22N4O3S', mw: 314.4, logP: 0.27, category: '消化系统' },
  { id: 18, name: '氟西汀', smiles: 'CNCCC(Oc1ccc(F)cc1)c1ccccc1', formula: 'C17H18FNO', mw: 271.33, logP: 4.05, category: '中枢神经' },
  { id: 19, name: '吉非罗齐', smiles: 'CC(C)c1ccc(C(=O)OC(CCO)C(C)C)cc1', formula: 'C15H22O3', mw: 250.33, logP: 4.77, category: '降脂药' },
  { id: 20, name: '卡托普利', smiles: 'CCC(C)C(C(=O)O)NC(=O)CCS', formula: 'C9H15NO3S', mw: 217.29, logP: -0.5, category: '心血管' }
]

export function computeADMET(mol: { mw: number; logP: number; formula: string }): ADMETProps {
  const { mw, logP } = mol
  const logS = 0.5 - 0.01 * (mw - 20) - logP
  const hbd = (mol.formula.match(/O/g) || []).length
  const hba = (mol.formula.match(/N/g) || []).length + hbd
  const violations = (mw > 500 ? 1 : 0) + (logP > 5 ? 1 : 0) + (hbd > 5 ? 1 : 0) + (hba > 10 ? 1 : 0)
  const toxicity = logP > 3 ? '高毒性风险' : logP > 1 ? '中等毒性' : '低毒性'
  const proteinBinding = Math.min(99, Math.max(10, Math.round(logP * 15 + 30)))
  const metabolicStability = mw < 300 ? '稳定' : mw < 450 ? '中等' : '不稳定'
  const bioavailability = Math.max(0, Math.min(100, Math.round(100 - logP * 8 - mw * 0.05)))

  return {
    logP: Math.round(logP * 100) / 100,
    logS: Math.round(logS * 100) / 100,
    toxicity,
    proteinBinding,
    metabolicStability,
    bioavailability,
    ruleOfFive: violations <= 1,
    violations
  }
}

export const useMoleculeStore = defineStore('molecule', () => {
  const molecules = ref<MoleculeData[]>([])
  const currentMolecule = ref<MoleculeData | null>(null)
  const admet = ref<ADMETProps | null>(null)
  const searchQuery = ref('')
  const searchResults = ref<MoleculeData[]>([])
  const isLoading = ref(false)

  const filteredMolecules = computed(() => {
    if (!searchQuery.value) return molecules.value
    const q = searchQuery.value.toLowerCase()
    return molecules.value.filter(m => m.name.toLowerCase().includes(q) || m.category.toLowerCase().includes(q) || m.smiles.toLowerCase().includes(q))
  })

  function loadMolecules() {
    molecules.value = MOCK_MOLECULES.map(m => {
      const { atoms, bonds } = parseSMILES(m.smiles)
      return { ...m, atoms, bonds }
    })
    if (molecules.value.length > 0) selectMolecule(molecules.value[0])
  }

  function selectMolecule(mol: MoleculeData) {
    currentMolecule.value = mol
    admet.value = computeADMET({ mw: mol.mw, logP: mol.logP, formula: mol.formula })
  }

  function searchMolecules(query: string) {
    searchQuery.value = query
    searchResults.value = filteredMolecules.value
  }

  function computeTanimoto(smiles1: string, smiles2: string): number {
    const set1 = new Set(smiles1.split(''))
    const set2 = new Set(smiles2.split(''))
    let intersection = 0
    set1.forEach(s => { if (set2.has(s)) intersection++ })
    const union = set1.size + set2.size - intersection
    return union === 0 ? 0 : Math.round((intersection / union) * 1000) / 10
  }

  const similarMolecules = computed(() => {
    if (!currentMolecule.value) return []
    return molecules.value
      .map(m => ({ ...m, similarity: computeTanimoto(currentMolecule.value!.smiles, m.smiles) }))
      .filter(m => m.id !== currentMolecule.value!.id)
      .sort((a, b) => b.similarity - a.similarity)
      .slice(0, 5)
  })

  return {
    molecules, currentMolecule, admet, searchQuery, searchResults, isLoading,
    filteredMolecules, similarMolecules,
    loadMolecules, selectMolecule, searchMolecules
  }
})
