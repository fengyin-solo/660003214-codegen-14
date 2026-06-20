import sys
sys.path.insert(0, '/Users/zhuanzmima0000/项目/字节/solo/任务数据/6600032/660003214-codegen-14/backend')

from app.services.correct_smiles_base import correct_smiles

test_cases = [
    ("CC(=O)Oc1ccccc1C(=O)O", "正确的阿司匹林SMILES"),
    ("CC(=O)Oc1ccccc1", "缺少结尾的阿司匹林"),
    ("CC(=O)Oc1cccccc1C(=O)O", "苯环多一个碳"),
    ("c1ccccc", "未闭合的苯环"),
    ("CC(=O)Nc1ccc(O)", "缺少结尾的扑热息痛"),
    ("Clc1ccc(N2C(=O)CN=C(c3ccccc3)c3cc(Cl)ccc32)cc1", "正确的地西泮"),
    ("clc1ccc(cc1)", "氯的大小写错误"),
    ("c1ccccc1(", "多余的开括号"),
    ("c1ccccc1)", "多余的闭括号"),
    ("CC(==O)O", "双键符号重复"),
    ("", "空输入"),
    ("C", "单原子输入"),
    ("c1ccc2", "不完整的萘环"),
    ("Cn1c(=O)c2c(ncn2C)n(C)c1=O", "正确的咖啡因"),
    ("CN(C)C(=N)N=C(N)", "缺少结尾的二甲双胍"),
]

print("=" * 80)
print("SMILES 纠错助手测试")
print("=" * 80)

for i, (smiles, description) in enumerate(test_cases, 1):
    print(f"\n测试用例 {i}: {description}")
    print(f"输入: '{smiles}'")
    print("-" * 60)
    
    result = correct_smiles(smiles)
    
    print(f"是否有效: {result['is_valid']}")
    print(f"是否可继续: {result['can_continue']}")
    
    if result['errors']:
        print("错误:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['best_correction']:
        best = result['best_correction']
        print(f"最佳修正:")
        print(f"  置信度: {best['confidence']:.2f}")
        print(f"  修正后: '{best['corrected']}'")
        print(f"  原因: {best['reason']}")
    
    if len(result['suggestions']) > 1:
        print(f"其他建议 ({len(result['suggestions']) - 1} 条):")
        for sug in result['suggestions'][1:]:
            print(f"  - '{sug['corrected']}' (置信度: {sug['confidence']:.2f})")
    
    print("-" * 60)

print("\n" + "=" * 80)
print("测试完成")
print("=" * 80)
