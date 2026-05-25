<template>
  <div class="product-maintenance">
    <PnlSubNav />

    <div class="pm-body">

      <!-- ── 左侧：产品过滤树 ── -->
      <div class="pm-left">
        <div class="pm-left-header">{{ t('pnlAttribution.productFilter') }}</div>
        <div class="pm-search">
          <el-input
            v-model="searchKeyword"
            :placeholder="t('pnlAttribution.searchProducts')"
            :prefix-icon="Search"
            clearable
            size="small"
            @input="onSearch"
          />
        </div>
        <div class="pm-tree-wrap">
          <el-tree
            ref="treeRef"
            :data="treeData"
            node-key="id"
            :default-expanded-keys="defaultExpandedKeys"
            :current-node-key="activeProduct"
            :filter-node-method="filterNode"
            :props="{ label: 'label', children: 'children' }"
            :highlight-current="true"
            @node-click="onNodeClick"
          />
        </div>
      </div>

      <!-- ── 右侧：归因因子配置 ── -->
      <div class="pm-right">

        <!-- 当前产品内容 -->
        <div class="pm-content">
          <div class="pm-product-title">{{ activeLabel }}</div>

          <div class="pm-factor-list">
            <div
              v-for="factor in currentFactors"
              :key="factor.id"
              class="pm-factor-item"
            >
              <el-icon class="drag-handle"><Grid /></el-icon>
              <div class="factor-body">
                <div class="factor-header">
                  <span class="factor-name">{{ factor.name }}</span>
                  <el-tag size="small" class="factor-badge">{{ factor.badge }}</el-tag>
                </div>
                <div class="factor-desc">{{ factor.desc }}</div>
              </div>
            </div>

            <el-empty
              v-if="currentFactors.length === 0"
              :description="t('pnlAttribution.noAttributionFactors')"
              :image-size="60"
            />
          </div>
        </div>

        <!-- 底部按钮 -->
        <div class="pm-footer">
          <el-button type="primary" @click="onConfirm">{{ t('common.confirm') }}</el-button>
          <el-button @click="onCancel">{{ t('common.cancel') }}</el-button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, Grid } from '@element-plus/icons-vue'
import PnlSubNav from '@/components/PnlSubNav.vue'

const { t } = useI18n()
const router = useRouter()

// ── 左侧产品树数据 ─────────────────────────────────────────────────────────
const treeData = computed(() => [
  { id: 'fx_spot',    label: t('pnlAttribution.productFxSpot') },
  { id: 'fx_forward', label: t('pnlAttribution.productFxForward') },
  { id: 'fx_swap',    label: t('pnlAttribution.productFxSwap') },
  { id: 'fx_option',  label: t('pnlAttribution.productFxOption') },
  { id: 'ccy_swap',   label: t('pnlAttribution.productCcs') },
  { id: 'ir_swap',    label: t('pnlAttribution.productIrs') },
])

const defaultExpandedKeys = []

// ── 当前选中节点 ───────────────────────────────────────────────────────────
const activeProduct = ref('fx_spot')
const activeLabel   = computed(() =>
  treeData.value.find(n => n.id === activeProduct.value)?.label ?? ''
)

function onNodeClick(node) {
  // 只响应叶节点（无子节点）
  if (!node.children || node.children.length === 0) {
    activeProduct.value = node.id
  }
}

// ── 归因因子数据（按产品 id 独立定义） ────────────────────────────────────

// 通用前两步（所有产品共用）
const commonPrefix = () => [
  { id: 'f_init',  name: 'Initial State',    badge: 'Initial State',  desc: 'Stores T-1 PL as the attribution baseline. Always selected by default when creating a new scenario.' },
  { id: 'f_model', name: 'Model Assignment', badge: 'Initialization', desc: 'Re-prices T-1 positions using the T-day pricing model to align the pricing environment, ensuring comparability of subsequent factor movements.' },
]

// FX Spot
const fxSpotFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',         badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_spot',  name: 'FX Spot',            badge: 'Market Data',   desc: 'PL change attributed to movements in the FX spot rate between T-1 and T.' },
  { id: 'f_conv',  name: 'Spot PL Conversion', badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',  badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

// FX Forward
const fxForwardFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',         badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_yield', name: 'Yield curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in yield curve market quotes between T-1 and T.' },
  { id: 'f_spot',  name: 'FX Spot',            badge: 'Market Data',   desc: 'PL change attributed to movements in the FX spot rate between T-1 and T.' },
  { id: 'f_basis', name: 'Basis curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in basis curve market quotes between T-1 and T.' },
  { id: 'f_conv',  name: 'Spot PL Conversion', badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',  badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

// FX Swap
const fxSwapFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',         badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_yield', name: 'Yield curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in yield curve market quotes between T-1 and T.' },
  { id: 'f_basis', name: 'Basis curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in basis curve market quotes between T-1 and T.' },
  { id: 'f_spot',  name: 'FX Spot',            badge: 'Market Data',   desc: 'PL change attributed to movements in the FX spot rate between T-1 and T.' },
  { id: 'f_conv',  name: 'Spot PL Conversion', badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',  badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

// FX Option
const fxOptionFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',                badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_spot',  name: 'FX Spot',                   badge: 'Market Data',   desc: 'PL change attributed to movements in the FX spot rate between T-1 and T.' },
  { id: 'f_vol',   name: 'FX volatility / FX smiles', badge: 'Market Data',   desc: 'PL change attributed to movements in FX implied volatility and volatility smile surface between T-1 and T.' },
  { id: 'f_yield', name: 'Yield curves (cc)',          badge: 'Market Data',   desc: 'PL change attributed to movements in yield curve market quotes between T-1 and T.' },
  { id: 'f_basis', name: 'Basis curves (cc)',          badge: 'Market Data',   desc: 'PL change attributed to movements in basis curve market quotes between T-1 and T.' },
  { id: 'f_conv',  name: 'Spot PL Conversion',        badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',          badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

// CCS (Cross-Currency Swap)
const ccySwapFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',         badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_yield', name: 'Yield curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in yield curve market quotes between T-1 and T.' },
  { id: 'f_basis', name: 'Basis curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in basis curve market quotes between T-1 and T.' },
  { id: 'f_spot',  name: 'FX Spot',            badge: 'Market Data',   desc: 'PL change attributed to movements in the FX spot rate between T-1 and T.' },
  { id: 'f_fix',   name: 'Fixings',            badge: 'Historical',    desc: 'Impact on daily P&L from published rate fixings (e.g. LIBOR/SOFR).' },
  { id: 'f_conv',  name: 'Spot PL Conversion', badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',  badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

// IRS (Interest Rate Swap)
const irSwapFactors = () => [
  ...commonPrefix(),
  { id: 'f_time',  name: 'Time Decay',         badge: 'Time Decay',    desc: 'PL change attributed to pure time decay between T-1 and T.' },
  { id: 'f_yield', name: 'Yield curves (cc)',   badge: 'Market Data',   desc: 'PL change attributed to movements in yield curve market quotes between T-1 and T.' },
  { id: 'f_fix',   name: 'Fixings',            badge: 'Historical',    desc: 'Impact on daily P&L from published rate fixings (e.g. LIBOR/SOFR).' },
  { id: 'f_conv',  name: 'Spot PL Conversion', badge: 'Conversion',    desc: 'Converts product P&L into the scenario reporting currency.' },
  { id: 'f_trade', name: 'Market Operations',  badge: 'Trade Activity', desc: 'Covers all trade lifecycle events (new, cancel, amend, rollover, maturity) impacting the day\'s P&L.' },
]

const factorMap = ref({
  fx_spot:    fxSpotFactors(),
  fx_forward: fxForwardFactors(),
  fx_swap:    fxSwapFactors(),
  fx_option:  fxOptionFactors(),
  ccy_swap:   ccySwapFactors(),
  ir_swap:    irSwapFactors(),
})

const currentFactors = computed(() => factorMap.value[activeProduct.value] ?? [])

// ── 搜索 ──────────────────────────────────────────────────────────────────
const searchKeyword = ref('')
const treeRef = ref(null)
function onSearch(val) {
  treeRef.value?.filter(val)
}
function filterNode(value, data) {
  if (!value) return true
  return data.label.includes(value)
}

// ── 底部操作 ──────────────────────────────────────────────────────────────
function onConfirm() {
  ElMessage.success(t('pnlAttribution.saveSuccess'))
}
function onCancel() {
  router.push({ name: 'scenario-query' })
}
</script>

<style lang="scss" scoped>
.product-maintenance {
  display: flex;
  flex-direction: column;
  height: 100%;
}

/* ── 主体左右布局 ── */
.pm-body {
  display: flex;
  flex: 1;
  min-height: 0;
  margin-top: 12px;
  gap: 12px;
}

/* ── 左侧产品树 ── */
.pm-left {
  width: 280px;
  flex-shrink: 0;
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.pm-left-header {
  padding: 14px 16px 10px;
  font-size: 14px;
  font-weight: 600;
  color: var(--git-text-1);
  border-bottom: 1px solid var(--git-border);
}

.pm-search {
  padding: 10px 12px 8px;
}

.pm-tree-wrap {
  flex: 1;
  overflow-y: auto;
  padding: 4px 4px 16px;

  :deep(.el-tree-node__content) {
    height: 32px;
    font-size: 13px;
  }
  :deep(.el-tree-node.is-current > .el-tree-node__content) {
    background: #eaf1ff;
    color: var(--git-primary);
  }
}

/* ── 右侧配置区 ── */
.pm-right {
  flex: 1;
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
}

/* 内容区 */
.pm-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px;
}

.pm-product-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--git-text-1);
  margin-bottom: 16px;
}

/* 因子列表 */
.pm-factor-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pm-factor-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: #f8f9fb;
  border-radius: 6px;
  border: 1px solid #ebeef2;
  transition: box-shadow 0.15s;

  &:hover { box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); }
}

.drag-handle {
  font-size: 16px;
  color: #c0c8d4;
  cursor: grab;
  flex-shrink: 0;
  &:active { cursor: grabbing; }
}

.factor-body {
  flex: 1;
  min-width: 0;
}

.factor-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 4px;
}

.factor-name {
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
}

.factor-badge {
  font-size: 11px;
  background: #e8f0fe;
  color: #4a7ede;
  border-color: #c6d9fb;
  border-radius: 3px;
}

.factor-desc {
  font-size: 12px;
  color: var(--git-text-3);
  line-height: 1.6;
}

/* 底部按钮 */
.pm-footer {
  padding: 14px 24px;
  border-top: 1px solid var(--git-border);
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}
</style>
