import sys
sys.path.insert(0, '/Users/zhuanzmima0000/项目/字节/solo/任务数据/6600032/660003214-codegen-14/backend')

from app.services.correct_smiles_base import correct_smiles

test_cases = [
    ("CC(=O)Oc1ccccc1C(=O)O", "正确的SMILES"),
    ("c1ccccc", "未闭合苯环"),
    ("clc1ccc(cc1)", "大小写错误"),
    ("CC(==O)O", "双键重复"),
    ("", "空输入"),
    ("CC(=O)Oc1ccccc1", "缺少结尾"),
]

print("=" * 80)
print("SMILES 纠错功能测试")
print("=" * 80)

passed = 0
failed = 0

for i, (smiles, description) in enumerate(test_cases, 1):
    print(f"\n{'=' * 80}")
    print(f"测试用例 {i}: {description}")
    print(f"输入: '{smiles}'")
    print("-" * 80)
    
    result = correct_smiles(smiles)
    
    print(f"是否有效: {result['is_valid']}")
    print(f"是否可继续: {result['can_continue']}")
    
    if result['errors']:
        print("检测到的错误:")
        for error in result['errors']:
            print(f"  - {error}")
    
    if result['best_correction']:
        best = result['best_correction']
        print(f"\n最佳修正建议:")
        print(f"  置信度: {best['confidence']:.2f}")
        print(f"  修正后: '{best['corrected']}'")
        print(f"  原因: {best['reason']}")
        print(f"  错误类型: {best['error_type']}")
    
    if len(result['suggestions']) > 1:
        print(f"\n其他修正建议 ({len(result['suggestions']) - 1} 条):")
        for sug in result['suggestions'][1:]:
            print(f"  - '{sug['corrected']}' (置信度: {sug['confidence']:.2f}, 原因: {sug['reason']})")
    
    if description == "正确的SMILES":
        if result['is_valid']:
            print("\n✓ 测试通过: 正确的SMILES被识别为有效")
            passed += 1
        else:
            print("\n✗ 测试失败: 正确的SMILES被误判为无效")
            failed += 1
    else:
        if not result['is_valid'] and result['best_correction']:
            print(f"\n✓ 测试通过: 成功检测到错误并给出修正建议")
            passed += 1
        else:
            print(f"\n✗ 测试失败: 未能正确检测错误或给出修正建议")
            failed += 1

print("\n" + "=" * 80)
print("测试总结")
print("=" * 80)
print(f"总测试用例: {len(test_cases)}")
print(f"通过: {passed}")
print(f"失败: {failed}")
print(f"通过率: {passed / len(test_cases) * 100:.1f}%")
print("=" * 80)
