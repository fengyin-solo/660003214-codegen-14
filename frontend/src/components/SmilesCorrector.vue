<template>
  <div class="bg-slate-800 rounded-lg p-4 border border-slate-700">
    <div class="flex items-center justify-between mb-3">
      <h3 class="text-sm font-bold text-slate-400">SMILES 纠错助手</h3>
      <span v-if="correctionResult" :class="['text-xs px-2 py-1 rounded', correctionResult.is_valid ? 'bg-green-900 text-green-400' : 'bg-amber-900 text-amber-400']">
        {{ correctionResult.is_valid ? '✓ 格式正确' : '⚠ 检测到问题' }}
      </span>
    </div>

    <div class="space-y-3">
      <div>
        <label class="text-xs text-slate-400 mb-1 block">输入 SMILES</label>
        <div class="flex gap-2">
          <input
            v-model="inputSmiles"
            @input="onInputChange"
            @keyup.enter="checkAndParse"
            placeholder="例如: CC(=O)Oc1ccccc1C(=O)O"
            class="flex-1 bg-slate-900 border border-slate-600 rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-cyan-500 font-mono"
          />
          <button
            @click="checkAndParse"
            class="px-4 py-2 bg-cyan-600 hover:bg-cyan-500 text-white rounded-lg text-sm font-medium transition-colors"
          >
            解析
          </button>
        </div>
      </div>

      <div v-if="isChecking" class="text-center py-2">
        <span class="text-slate-400 text-sm">正在检查...</span>
      </div>

      <div v-if="correctionResult && !correctionResult.is_valid && correctionResult.errors.length > 0" class="bg-amber-900/30 border border-amber-700 rounded-lg p-3">
        <div class="text-xs font-medium text-amber-400 mb-2">检测到以下问题：</div>
        <ul class="space-y-1">
          <li v-for="(error, index) in correctionResult.errors" :key="index" class="text-xs text-amber-300 flex items-start gap-2">
            <span class="text-amber-500">•</span>
            <span>{{ error }}</span>
          </li>
        </ul>
      </div>

      <div v-if="correctionResult && correctionResult.best_correction && correctionResult.can_continue" class="bg-cyan-900/30 border border-cyan-700 rounded-lg p-3">
        <div class="text-xs font-medium text-cyan-400 mb-2">建议修正：</div>
        <div class="space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-400">原输入：</span>
            <span class="text-xs font-mono text-red-400 line-through">{{ correctionResult.original }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-400">建议：</span>
            <span class="text-xs font-mono text-green-400">{{ correctionResult.best_correction.corrected }}</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">置信度：</span>
            <div class="flex-1 bg-slate-700 rounded-full h-2">
              <div
                class="bg-cyan-500 h-2 rounded-full transition-all"
                :style="{ width: correctionResult.best_correction.confidence * 100 + '%' }"
              ></div>
            </div>
            <span class="text-xs text-cyan-400 font-medium">{{ (correctionResult.best_correction.confidence * 100).toFixed(0) }}%</span>
          </div>
          <div class="text-xs text-slate-400">
            原因：{{ correctionResult.best_correction.reason }}
          </div>
        </div>
        <div class="flex gap-2 mt-3">
          <button
            @click="applyCorrection"
            class="flex-1 px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded text-xs font-medium transition-colors"
          >
            应用修正并解析
          </button>
          <button
            @click="copyCorrection"
            class="px-3 py-1.5 bg-slate-600 hover:bg-slate-500 text-white rounded text-xs font-medium transition-colors"
          >
            复制
          </button>
        </div>
      </div>

      <div v-if="correctionResult && correctionResult.suggestions.length > 1" class="mt-3">
        <div class="text-xs font-medium text-slate-400 mb-2">其他建议：</div>
        <div class="space-y-2 max-h-32 overflow-y-auto">
          <div
            v-for="(suggestion, index) in correctionResult.suggestions.slice(1)" :key="index"
            class="bg-slate-900 rounded p-2 cursor-pointer hover:bg-slate-700 transition-colors"
            @click="selectSuggestion(suggestion)"
          >
            <div class="flex items-center justify-between">
              <span class="text-xs font-mono text-slate-300">{{ suggestion.corrected }}</span>
              <span class="text-xs text-slate-500">{{ (suggestion.confidence * 100).toFixed(0) }}%</span>
            </div>
            <div class="text-xs text-slate-500 mt-1">{{ suggestion.reason }}</div>
          </div>
        </div>
      </div>

      <div v-if="parseResult" class="bg-slate-900 border border-slate-700 rounded-lg p-3 mt-3">
        <div class="text-xs font-medium text-green-400 mb-2">解析成功！</div>
        <div class="text-xs text-slate-400">
          原子数: {{ parseResult.atoms.length }} | 键数: {{ parseResult.bonds.length }}
        </div>
        <button
          @click="loadAsMolecule"
          class="mt-2 w-full px-3 py-1.5 bg-green-600 hover:bg-green-500 text-white rounded text-xs font-medium transition-colors"
        >
          加载为当前分子
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useMoleculeStore } from '../store/molecule'
import type { SmilesCorrectionResponse, ParseResult, Atom3D, Bond3D } from '../types'

const store = useMoleculeStore()
const inputSmiles = ref('')
const correctionResult = ref<SmilesCorrectionResponse | null>(null)
const parseResult = ref<ParseResult | null>(null)
const isChecking = ref(false)
let debounceTimer: number | null = null

async function checkSmiles(smiles: string) {
  if (!smiles.trim()) {
    correctionResult.value = null
    parseResult.value = null
    return
  }

  try {
    const response = await fetch(`http://localhost:8000/api/molecules/correct?smiles=${encodeURIComponent(smiles)}`, {
      method: 'POST'
    })
    correctionResult.value = await response.json()
  } catch (error) {
    console.error('检查SMILES失败:', error)
  }
}

async function parseSmiles(smiles: string) {
  try {
    const response = await fetch(`http://localhost:8000/api/molecules/smiles?smiles=${encodeURIComponent(smiles)}`, {
      method: 'POST'
    })
    return await response.json()
  } catch (error) {
    console.error('解析SMILES失败:', error)
    return null
  }
}

function onInputChange() {
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }
  debounceTimer = window.setTimeout(() => {
    checkSmiles(inputSmiles.value)
  }, 500)
}

async function checkAndParse() {
  isChecking.value = true
  parseResult.value = null

  await checkSmiles(inputSmiles.value)

  if (correctionResult.value && correctionResult.value.is_valid) {
    parseResult.value = await parseSmiles(inputSmiles.value)
  }

  isChecking.value = false
}

function applyCorrection() {
  if (correctionResult.value?.best_correction) {
    inputSmiles.value = correctionResult.value.best_correction.corrected
    checkAndParse()
  }
}

function copyCorrection() {
  if (correctionResult.value?.best_correction) {
    navigator.clipboard.writeText(correctionResult.value.best_correction.corrected)
  }
}

function selectSuggestion(suggestion: any) {
  inputSmiles.value = suggestion.corrected
  checkAndParse()
}

function loadAsMolecule() {
  if (parseResult.value) {
    const customMol: any = {
      id: 999,
      name: '自定义分子',
      smiles: inputSmiles.value,
      formula: 'C?H?O?',
      mw: 0,
      logP: 0,
      category: '自定义',
      atoms: parseResult.value.atoms as Atom3D[],
      bonds: parseResult.value.bonds as Bond3D[]
    }
    store.selectMolecule(customMol)
  }
}

watch(inputSmiles, (newVal) => {
  if (!newVal) {
    correctionResult.value = null
    parseResult.value = null
  }
})
</script>
