# 药物分子 3D 结构可视化与 ADMET 性质预测

SMILES 分子式解析 → Three.js 球棍模型 3D 渲染、ADMET 性质预测面板、相似分子搜索的药物化学工具。

## 技术栈

- 前端：Vue 3 + TypeScript + Vite + Pinia + Tailwind CSS + Three.js
- 后端：Python FastAPI + NumPy + RDKit
- 数据库：SQLite

## 功能

- SMILES 分子式解析与 Three.js 球棍模型 3D 渲染
- 原子/键类型着色（C灰/N蓝/O红/S黄/P橙）
- 分子旋转/缩放/平移交互
- ADMET 性质预测（LogP/溶解度/毒性/蛋白结合率/代谢稳定性）
- 2D 分子结构图 SVG 生成
- 相似分子 Tanimoto 系数搜索
- 药效团特征标注与高亮
- 50+ 常见药物分子 mock 数据

## 启动

```bash
# 前端
cd frontend && npm install && npm run dev

# 后端
cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload
```
