<template>
  <div class="search-box" ref="searchBoxRef">
    <input
      type="text"
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @focus="showDropdown = true"
      :placeholder="placeholder"
      class="search-input"
    />

    <div v-if="showDropdown && filteredSymbols.length > 0" class="search-dropdown">
      <div
        v-for="item in filteredSymbols"
        :key="item.symbol"
        class="dropdown-item"
        @click="handleSelect(item.symbol)"
      >
        <span class="symbol-name">{{ formatSymbol(item.symbol) }}</span>
        <span class="symbol-base">{{ item.base || item.symbol.replace('USDT', '') }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  modelValue: { type: String, default: '' },
  symbols: { type: Array, default: () => [] },
  placeholder: { type: String, default: '搜索...' }
})

const emit = defineEmits(['update:modelValue', 'select'])

const showDropdown = ref(false)
const searchBoxRef = ref(null)

const filteredSymbols = computed(() => {
  if (!props.modelValue) return props.symbols.slice(0, 10)
  const query = props.modelValue.toUpperCase()
  return props.symbols
    .filter(s => s.symbol.toUpperCase().includes(query))
    .slice(0, 10)
})

const formatSymbol = (symbol) => {
  return symbol.replace('USDT', '/USDT')
}

const handleSelect = (symbol) => {
  emit('select', symbol)
  showDropdown.value = false
}

const handleClickOutside = (event) => {
  if (searchBoxRef.value && !searchBoxRef.value.contains(event.target)) {
    showDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.search-box {
  position: relative;
  width: 200px;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  background: #21262d;
  border: 1px solid #30363d;
  border-radius: 6px;
  color: #e6edf3;
  font-size: 13px;
  transition: border-color 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: #f0b90b;
}

.search-input::placeholder {
  color: #8b949e;
}

.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: #161b22;
  border: 1px solid #30363d;
  border-radius: 6px;
  margin-top: 4px;
  max-height: 300px;
  overflow-y: auto;
  z-index: 200;
}

.dropdown-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  cursor: pointer;
  transition: background 0.15s;
}

.dropdown-item:hover {
  background: #21262d;
}

.symbol-name {
  color: #e6edf3;
  font-size: 13px;
}

.symbol-base {
  color: #8b949e;
  font-size: 11px;
}
</style>