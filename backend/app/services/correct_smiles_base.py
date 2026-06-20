import re
from typing import List, Tuple, Dict, Optional

VALID_ELEMENTS = {
    'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
    'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
    'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
    'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
    'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
    'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
    'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
    'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
    'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
    'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
    'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
    'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
}

AROMATIC_ELEMENTS = {'b', 'c', 'n', 'o', 's', 'p', 'se', 'as'}

COMMON_SMILES_ERRORS: Dict[str, str] = {
    'cc': 'cC',
    'c1ccccc': 'c1ccccc1',
    'c1ccc2': 'c1ccc2ccccc2c1',
    'c1ccc2c(c1)': 'c1ccc2c(c1)cccc2',
    'CC(=O)Oc1ccccc1': 'CC(=O)Oc1ccccc1C(=O)O',
    'CC(=O)Nc1ccc(O)': 'CC(=O)Nc1ccc(O)cc1',
    'CN(C)C(=N)N=C(N)': 'CN(C)C(=N)N=C(N)N',
    'OCC(O)C1OC(=O)C(O)=C1': 'OCC(O)C1OC(=O)C(O)=C1O',
    'CC(=O)O': 'CC(=O)Oc1ccccc1C(=O)O',
    'cl': 'Cl',
    'br': 'Br',
    'na': 'Na',
    'k': 'K',
    'ca': 'Ca',
    'mg': 'Mg',
    'fe': 'Fe',
    'zn': 'Zn',
    'cu': 'Cu',
}

class CorrectionSuggestion:
    def __init__(self, original: str, corrected: str, confidence: float, reason: str, error_type: str):
        self.original = original
        self.corrected = corrected
        self.confidence = confidence
        self.reason = reason
        self.error_type = error_type

    def to_dict(self) -> Dict:
        return {
            "original": self.original,
            "corrected": self.corrected,
            "confidence": round(self.confidence, 2),
            "reason": self.reason,
            "error_type": self.error_type
        }

class SmileCorrector:
    def __init__(self):
        pass

    def check_brackets(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        stack = []
        errors = []
        for i, ch in enumerate(smiles):
            if ch in '([':
                stack.append((ch, i))
            elif ch == ')':
                if not stack or stack[-1][0] != '(':
                    errors.append(f"位置{i}: 多余的闭括号')'")
                else:
                    stack.pop()
            elif ch == ']':
                if not stack or stack[-1][0] != '[':
                    errors.append(f"位置{i}: 多余的闭括号']'")
                else:
                    stack.pop()

        if stack:
            for ch, pos in stack:
                matching = ')' if ch == '(' else ']'
                errors.append(f"位置{pos}: 缺少匹配的闭括号'{matching}'")

        if errors:
            corrected = self._fix_brackets(smiles, stack)
            return False, corrected, "; ".join(errors)
        return True, None, ""

    def _fix_brackets(self, smiles: str, unclosed: List[Tuple[str, int]]) -> str:
        corrected = smiles
        for ch, pos in reversed(unclosed):
            matching = ')' if ch == '(' else ']'
            corrected += matching
        corrected = corrected.replace('])', '])')
        return corrected

    def check_ring_numbers(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        ring_map: Dict[str, List[int]] = {}
        errors = []
        i = 0
        while i < len(smiles):
            ch = smiles[i]
            if ch == '%' and i + 2 < len(smiles):
                ring_num = smiles[i:i+3]
                ring_map.setdefault(ring_num, []).append(i)
                i += 3
            elif ch.isdigit():
                ring_num = ch
                ring_map.setdefault(ring_num, []).append(i)
                i += 1
            elif ch in '[]':
                i += 1
                while i < len(smiles) and smiles[i] != ']':
                    i += 1
                i += 1
            else:
                i += 1

        unpaired = []
        for num, positions in ring_map.items():
            if len(positions) % 2 != 0:
                unpaired.append(f"环编号{num}出现{len(positions)}次，应为偶数次")

        if unpaired:
            corrected = self._fix_ring_numbers(smiles, ring_map)
            return False, corrected, "; ".join(unpaired)
        return True, None, ""

    def _fix_ring_numbers(self, smiles: str, ring_map: Dict[str, List[int]]) -> str:
        corrected = smiles
        for num, positions in ring_map.items():
            if len(positions) % 2 != 0:
                last_pos = positions[-1]
                insert_pos = len(corrected)
                while insert_pos > last_pos and corrected[insert_pos - 1] in ')]':
                    insert_pos -= 1
                corrected = corrected[:insert_pos] + num + corrected[insert_pos:]
        return corrected

    def check_invalid_characters(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        valid_pattern = r'^[A-Za-z0-9@+\-=#\/\\%().\[\]]+$'
        invalid_chars = []
        for i, ch in enumerate(smiles):
            if not re.match(r'[A-Za-z0-9@+\-=#\/\\%().\[\]]', ch):
                if not ch.isspace():
                    invalid_chars.append(f"位置{i}: '{ch}'")

        if invalid_chars:
            corrected = re.sub(r'[^A-Za-z0-9@+\-=#\/\\%().\[\]]', '', smiles)
            return False, corrected, f"无效字符: {', '.join(invalid_chars)}"
        return True, None, ""

    def check_element_case(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        errors = []
        corrected = list(smiles)
        i = 0

        while i < len(smiles):
            ch = smiles[i]

            if ch == '[':
                i += 1
                while i < len(smiles) and smiles[i] != ']':
                    i += 1
                i += 1
                continue

            if ch.islower() and ch in 'bcnoasp':
                i += 1
                continue

            if ch.islower() and ch not in 'bcnoasp':
                if i + 1 < len(smiles) and smiles[i + 1].islower():
                    element = ch.upper() + smiles[i + 1]
                    if element in VALID_ELEMENTS:
                        errors.append(f"位置{i}: '{ch}{smiles[i+1]}'应为'{element}'")
                        corrected[i] = ch.upper()
                        i += 2
                        continue

            if ch.isupper():
                element = ch
                if i + 1 < len(smiles) and smiles[i + 1].islower():
                    element += smiles[i + 1]
                    if element in VALID_ELEMENTS:
                        i += 2
                        continue
                    elif ch.lower() in AROMATIC_ELEMENTS:
                        errors.append(f"位置{i}: '{ch}'可能为芳香原子，应为'{ch.lower()}'")
                        corrected[i] = ch.lower()
                i += 1
            else:
                i += 1

        if errors:
            return False, ''.join(corrected), "; ".join(errors)
        return True, None, ""

    def check_bond_symbols(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        errors = []
        corrected = list(smiles)
        i = 0

        while i < len(smiles) - 1:
            if smiles[i] in '=#' and smiles[i + 1] in '=#':
                errors.append(f"位置{i}: 连续的键符号'{smiles[i]}{smiles[i+1]}'")
                corrected[i + 1] = ''
                i += 2
            elif smiles[i] == '-' and i == 0:
                errors.append(f"位置{i}: 开头的单键符号'-'可省略")
                corrected[i] = ''
                i += 1
            else:
                i += 1

        if errors:
            return False, ''.join(corrected), "; ".join(errors)
        return True, None, ""

    def check_empty_input(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        if not smiles or not smiles.strip():
            return False, "CC(=O)Oc1ccccc1C(=O)O", "输入为空，示例：阿司匹林 SMILES 为 CC(=O)Oc1ccccc1C(=O)O"
        if len(smiles.strip()) < 2:
            return False, "CC", f"输入过短（仅{len(smiles)}个字符），SMILES 至少需要2个字符"
        return True, None, ""

    def check_common_patterns(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        errors = []
        corrected = smiles

        for wrong, right in COMMON_SMILES_ERRORS.items():
            if wrong in corrected and wrong != right:
                errors.append(f"常见错误模式: '{wrong}' 可能应为 '{right[:20]}...'" if len(right) > 20 else f"常见错误模式: '{wrong}' 应为 '{right}'")
                corrected = corrected.replace(wrong, right)

        if re.search(r'c1ccccc[^1]', corrected):
            match = re.search(r'c1ccccc[^1]', corrected)
            if match:
                pos = match.start()
                errors.append(f"位置{pos}: 苯环可能未闭合，缺少环编号'1'")
                insert_pos = match.end() - 1
                corrected = corrected[:insert_pos] + '1' + corrected[insert_pos:]

        if errors:
            return False, corrected, "; ".join(errors)
        return True, None, ""

    def check_atoms_count(self, smiles: str) -> Tuple[bool, Optional[str], str]:
        atoms = []
        i = 0
        while i < len(smiles):
            ch = smiles[i]
            if ch == '[':
                i += 1
                element = ''
                while i < len(smiles) and smiles[i] != ']' and smiles[i].isalpha():
                    element += smiles[i]
                    i += 1
                if element:
                    atoms.append(element)
                while i < len(smiles) and smiles[i] != ']':
                    i += 1
                i += 1
            elif ch.isupper():
                element = ch
                if i + 1 < len(smiles) and smiles[i + 1].islower():
                    element += smiles[i + 1]
                    i += 1
                atoms.append(element)
                i += 1
            elif ch.islower() and ch in AROMATIC_ELEMENTS:
                atoms.append(ch.upper())
                i += 1
            else:
                i += 1

        if len(atoms) == 0:
            return False, "CC", "未检测到有效原子，请检查输入是否包含元素符号"
        if len(atoms) == 1:
            return False, smiles + 'C', f"仅检测到1个原子({atoms[0]})，SMILES 至少需要2个原子"

        return True, None, ""

    def correct(self, smiles: str) -> Dict:
        original = smiles.strip()
        suggestions: List[CorrectionSuggestion] = []

        checks = [
            ("empty_input", self.check_empty_input, 0.95),
            ("invalid_characters", self.check_invalid_characters, 0.9),
            ("brackets", self.check_brackets, 0.85),
            ("ring_numbers", self.check_ring_numbers, 0.8),
            ("element_case", self.check_element_case, 0.75),
            ("bond_symbols", self.check_bond_symbols, 0.7),
            ("atoms_count", self.check_atoms_count, 0.65),
            ("common_patterns", self.check_common_patterns, 0.6),
        ]

        current_smiles = original
        is_valid = True
        all_errors = []

        for error_type, check_func, base_confidence in checks:
            valid, corrected, error_msg = check_func(current_smiles)
            if not valid:
                is_valid = False
                all_errors.append(error_msg)
                if corrected and corrected != current_smiles:
                    suggestions.append(CorrectionSuggestion(
                        original=original,
                        corrected=corrected,
                        confidence=base_confidence,
                        reason=error_msg,
                        error_type=error_type
                    ))
                    current_smiles = corrected

        if is_valid:
            suggestions.append(CorrectionSuggestion(
                original=original,
                corrected=original,
                confidence=1.0,
                reason="SMILES 格式正确",
                error_type="valid"
            ))

        unique_corrections = {}
        for sug in suggestions:
            if sug.corrected not in unique_corrections or sug.confidence > unique_corrections[sug.corrected].confidence:
                unique_corrections[sug.corrected] = sug

        sorted_suggestions = sorted(
            unique_corrections.values(),
            key=lambda x: x.confidence,
            reverse=True
        )

        best_suggestion = sorted_suggestions[0] if sorted_suggestions else None

        return {
            "original": original,
            "is_valid": is_valid,
            "errors": all_errors,
            "best_correction": best_suggestion.to_dict() if best_suggestion else None,
            "suggestions": [s.to_dict() for s in sorted_suggestions],
            "can_continue": best_suggestion is not None and best_suggestion.corrected != original
        }

def correct_smiles(smiles: str) -> Dict:
    corrector = SmileCorrector()
    return corrector.correct(smiles)
