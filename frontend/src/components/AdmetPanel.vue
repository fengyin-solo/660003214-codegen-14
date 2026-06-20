<template>
  <div class="bg-slate-800 rounded-lg p-4 border border-slate-700">
    <h3 class="text-sm font-bold text-slate-400 mb-3">ADMET 性质预测</h3>
    <div v-if="store.admet" class="space-y-3">
      <div class="grid grid-cols-2 gap-2 text-sm">
        <div class="bg-slate-900 rounded p-2">
          <div class="text-xs text-slate-500">LogP (脂溶性)</div>
          <div class="text-lg font-bold" :class="store.admet.logP > 3 ? 'text-red-400' : 'text-green-400'">{{ store.admet.logP }}</div>
        </div>
        <div class="bg-slate-900 rounded p-2">
          <div class="text-xs text-slate-500">LogS (溶解度)</div>
          <div class="text-lg font-bold text-cyan-400">{{ store.admet.logS }}</div>
        </div>
        <div class="bg-slate-900 rounded p-2">
          <div class="text-xs text-slate-500">蛋白结合率</div>
          <div class="text-lg font-bold text-purple-400">{{ store.admet.proteinBinding }}%</div>
        </div>
        <div class="bg-slate-900 rounded p-2">
          <div class="text-xs text-slate-500">生物利用度</div>
          <div class="text-lg font-bold" :class="store.admet.bioavailability > 50 ? 'text-green-400' : 'text-orange-400'">{{ store.admet.bioavailability }}%</div>
        </div>
      </div>
      <div class="bg-slate-900 rounded p-3 text-sm">
        <div class="flex justify-between mb-1"><span class="text-slate-500">毒性评估</span><span :class="store.admet.toxicity.includes('高') ? 'text-red-400' : store.admet.toxicity.includes('中') ? 'text-orange-400' : 'text-green-400'">{{ store.admet.toxicity }}</span></div>
        <div class="flex justify-between mb-1"><span class="text-slate-500">代谢稳定性</span><span :class="store.admet.metabolicStability === '稳定' ? 'text-green-400' : store.admet.metabolicStability === '中等' ? 'text-orange-400' : 'text-red-400'">{{ store.admet.metabolicStability }}</span></div>
        <div class="flex justify-between"><span class="text-slate-500">Lipinski五规则</span><span :class="store.admet.ruleOfFive ? 'text-green-400' : 'text-red-400'">{{ store.admet.ruleOfFive ? '✓ 通过' : '✗ 违反' }} ({{ store.admet.violations }})</span></div>
      </div>
    </div>
    <div v-else class="text-slate-500 text-sm">选择分子查看ADMET</div>

    <div v-if="store.similarMolecules.length > 0" class="mt-4">
      <h4 class="text-xs font-bold text-slate-500 mb-2">相似分子 (Tanimoto)</h4>
      <div class="space-y-1">
        <div v-for="mol in store.similarMolecules" :key="mol.id" @click="store.selectMolecule(mol)" class="cursor-pointer flex items-center justify-between bg-slate-900 rounded p-2 hover:bg-slate-700 transition">
          <span class="text-sm text-slate-200">{{ mol.name }}</span>
          <span class="text-xs font-bold" :style="{ color: mol.similarity > 60 ? '#22c55e' : mol.similarity > 30 ? '#eab308' : '#94a3b8' }">{{ mol.similarity }}%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useMoleculeStore } from '../store/molecule'
const store = useMoleculeStore()
</script>
