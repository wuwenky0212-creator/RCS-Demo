<template>
  <div class="fxswap-page">

    <!-- ── 筛选栏 ── -->
    <div class="fxs-filter">
      <span class="fxs-filter-label">{{ t('fxSwap.account') }}</span>
      <el-select v-model="filterAccount" size="small" style="width:220px" clearable :placeholder="t('fxSwap.selectPlaceholder')">
        <el-option v-for="b in BOOKS" :key="b.code" :label="`${b.code}（${b.name}）`" :value="b.code" />
      </el-select>
      <el-button type="primary" size="small" @click="handleQuery">{{ t('fxSwap.query') }}</el-button>
      <el-button size="small" @click="handleReset">{{ t('fxSwap.reset') }}</el-button>
    </div>

    <!-- ── 内容区 ── -->
    <div class="fxs-body">
      <div class="fxs-section">
        <div class="fxs-section-hd">
          <span class="fxs-section-title">{{ t('fxSwap.sectionTitle') }}</span>
          <div class="fxs-auto-refresh">
            <el-switch v-model="autoRefresh" size="small" @change="onAutoRefreshChange" />
            <span class="fxs-ar-label">{{ t('fxSwap.autoRefresh') }}</span>
            <el-icon class="fxs-ar-setting"><Setting /></el-icon>
          </div>
        </div>

        <el-table
          :data="tableData"
          size="small"
          border
          row-key="id"
          :tree-props="{ children: 'children', hasChildren: 'hasChildren' }"
          class="fxs-table"
          :header-cell-style="{ background: '#f5f7fa', color: '#606266', fontWeight: '600', fontSize: '12px' }"
        >
          <!-- 标的 -->
          <el-table-column prop="symbol" :label="t('fxSwap.colSymbol')" width="160" fixed="left">
            <template #default="{ row }">
              <span :class="['sym-cell', `sym--${row.level}`]">{{ row.symbol }}</span>
            </template>
          </el-table-column>

          <!-- 货币1 -->
          <el-table-column prop="ccy1" :label="t('fxSwap.colCcy1')" width="64" align="center" fixed="left">
            <template #default="{ row }"><span class="ccy-tag">{{ row.ccy1 }}</span></template>
          </el-table-column>

          <!-- 货币1(金额) -->
          <el-table-column prop="ccy1Amount" :label="t('fxSwap.colCcy1Amount')" width="140" align="right" fixed="left">
            <template #default="{ row }">
              <span :class="numClass(row.ccy1Amount)">{{ fmtNum(row.ccy1Amount) }}</span>
            </template>
          </el-table-column>

          <!-- 货币2 -->
          <el-table-column prop="ccy2" :label="t('fxSwap.colCcy2')" width="64" align="center" fixed="left">
            <template #default="{ row }"><span class="ccy-tag">{{ row.ccy2 }}</span></template>
          </el-table-column>

          <!-- 货币2(金额) -->
          <el-table-column prop="ccy2Amount" :label="t('fxSwap.colCcy2Amount')" width="140" align="right" fixed="left">
            <template #default="{ row }">
              <span :class="numClass(row.ccy2Amount)">{{ fmtNum(row.ccy2Amount) }}</span>
            </template>
          </el-table-column>

          <!-- 市场远期汇率 -->
          <el-table-column prop="mktFwdRate" :label="t('fxSwap.colMktFwdRate')" width="120" align="right">
            <template #default="{ row }">
              <span v-if="row.mktFwdRate != null">{{ row.mktFwdRate.toFixed(6) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 升贴水 -->
          <el-table-column prop="swapPoints" :label="t('fxSwap.colSwapPoints')" width="90" align="right">
            <template #default="{ row }">
              <span v-if="row.swapPoints != null && row.swapPoints !== ''">{{ row.swapPoints }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 盈亏平衡点 -->
          <el-table-column prop="breakeven" :label="t('fxSwap.colBreakeven')" width="110" align="right">
            <template #default="{ row }">
              <span v-if="row.breakeven != null">{{ row.breakeven.toFixed(6) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 等值敞口 -->
          <el-table-column prop="equivExposure" :label="t('fxSwap.colEquivExposure')" width="140" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.equivExposure)">{{ fmtNum(row.equivExposure) }}</span>
            </template>
          </el-table-column>

          <!-- DV01(货币1) -->
          <el-table-column prop="dv01Ccy1" :label="t('fxSwap.colDv01Ccy1')" width="110" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.dv01Ccy1)">{{ fmtNum(row.dv01Ccy1, 2) }}</span>
            </template>
          </el-table-column>

          <!-- DV01(货币2) -->
          <el-table-column prop="dv01Ccy2" :label="t('fxSwap.colDv01Ccy2')" width="110" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.dv01Ccy2)">{{ fmtNum(row.dv01Ccy2, 2) }}</span>
            </template>
          </el-table-column>

          <!-- 总损益(USD) -->
          <el-table-column prop="totalPnl" :label="t('fxSwap.colTotalPnl')" width="130" align="right">
            <template #default="{ row }">
              <span :class="[numClass(row.totalPnl), 'bold']">{{ fmtNum(row.totalPnl) }}</span>
            </template>
          </el-table-column>

          <!-- 贴现损益(USD) -->
          <el-table-column prop="discPnlUsd" :label="t('fxSwap.colDiscPnlUsd')" width="130" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.discPnlUsd)">{{ fmtNum(row.discPnlUsd) }}</span>
            </template>
          </el-table-column>

          <!-- 贴现损益(CNY) -->
          <el-table-column prop="discPnlCny" :label="t('fxSwap.colDiscPnlCny')" width="140" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.discPnlCny)">{{ fmtNum(row.discPnlCny) }}</span>
            </template>
          </el-table-column>

          <!-- 日损益(USD) -->
          <el-table-column prop="dailyPnl" :label="t('fxSwap.colDailyPnl')" width="120" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.dailyPnl)">{{ fmtNum(row.dailyPnl) }}</span>
            </template>
          </el-table-column>

          <!-- 月损益(USD) -->
          <el-table-column prop="monthlyPnl" :label="t('fxSwap.colMonthlyPnl')" width="120" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.monthlyPnl)">{{ fmtNum(row.monthlyPnl) }}</span>
            </template>
          </el-table-column>

          <!-- 年损益(USD) -->
          <el-table-column prop="yearlyPnl" :label="t('fxSwap.colYearlyPnl')" width="120" align="right">
            <template #default="{ row }">
              <span :class="numClass(row.yearlyPnl)">{{ fmtNum(row.yearlyPnl) }}</span>
            </template>
          </el-table-column>

          <!-- DF1 -->
          <el-table-column prop="df1" :label="t('fxSwap.colDf1')" width="100" align="right">
            <template #default="{ row }">
              <span v-if="row.df1 != null" class="dim-val">{{ row.df1.toFixed(8) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- DF2 -->
          <el-table-column prop="df2" :label="t('fxSwap.colDf2')" width="100" align="right">
            <template #default="{ row }">
              <span v-if="row.df2 != null" class="dim-val">{{ row.df2.toFixed(8) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- SpotDF1 -->
          <el-table-column prop="spotDf1" :label="t('fxSwap.colSpotDf1')" width="110" align="right">
            <template #default="{ row }">
              <span v-if="row.spotDf1 != null" class="dim-val">{{ row.spotDf1.toFixed(8) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- SpotDF2 -->
          <el-table-column prop="spotDf2" :label="t('fxSwap.colSpotDf2')" width="110" align="right">
            <template #default="{ row }">
              <span v-if="row.spotDf2 != null" class="dim-val">{{ row.spotDf2.toFixed(8) }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 货币1曲线 -->
          <el-table-column prop="ccy1Curve" :label="t('fxSwap.colCcy1Curve')" width="150" align="center">
            <template #default="{ row }">
              <span v-if="row.ccy1Curve" class="curve-tag">{{ row.ccy1Curve }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 货币2曲线 -->
          <el-table-column prop="ccy2Curve" :label="t('fxSwap.colCcy2Curve')" width="130" align="center">
            <template #default="{ row }">
              <span v-if="row.ccy2Curve" class="curve-tag">{{ row.ccy2Curve }}</span>
              <span v-else class="dim">—</span>
            </template>
          </el-table-column>

          <!-- 操作 -->
          <el-table-column :label="t('fxSwap.colActions')" width="145" align="center" fixed="right">
            <template #default="{ row }">
              <span class="action-cell">
                <span class="action-link" @click="handleDetail(row)">{{ t('fxSwap.actionDetail') }}</span>
                <span class="action-divider">|</span>
                <span class="action-link" @click="handleInternalTransfer(row)">{{ t('fxSwap.actionTransfer') }}</span>
              </span>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <!-- ══ 转移抽屉 ══ -->
    <el-drawer
      v-model="drawerVisible"
      direction="rtl"
      size="560px"
      :close-on-click-modal="false"
      class="swap-transfer-drawer"
      @close="resetForm"
    >
      <template #header>
        <div class="td-header">
          <span class="td-title">{{ t('fxSwap.drawerTitle') }}</span>
          <div class="td-header-tags">
            <el-tag size="small" type="info" effect="plain">{{ t('fxSwap.tagInternal') }}</el-tag>
            <el-tag v-if="currentRow" size="small" effect="plain">{{ currentRow.symbol }}</el-tag>
          </div>
        </div>
      </template>

      <div class="td-body">
        <div class="td-form-panel">
          <div class="td-form-scroll">

            <!-- ① 交易信息 -->
            <div class="td-section">
              <div class="td-section-title"><span class="td-bar"></span>{{ t('fxSwap.sectionTradeInfo') }}</div>
              <div class="td-fields td-fields--wide">

                <!-- 货币对 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldCurrencyPair')">{{ t('fxSwap.fieldCurrencyPair') }} <span class="req">*</span></div>
                  <div class="td-value">
                    <el-select v-model="tf.currencyPair" :placeholder="t('fxSwap.inputPlaceholder')" size="small" style="width:100%">
                      <el-option label="EUR/USD" value="EURUSD" />
                      <el-option label="USD/CNY" value="USDCNY" />
                      <el-option label="EUR/CNY" value="EURCNY" />
                    </el-select>
                  </div>
                </div>

                <!-- 即期汇率 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldSpotRate')">{{ t('fxSwap.fieldSpotRate') }} <span class="req">*</span></div>
                  <div class="td-value">
                    <el-input v-model="tf.spotRate" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="width:100%" />
                  </div>
                </div>

                <!-- 交易期限 ON/TN/SN -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldTenorQuick')">{{ t('fxSwap.fieldTenorQuick') }}</div>
                  <div class="td-value">
                    <div class="tenor-btns">
                      <button v-for="opt in ['ON','TN','SN']" :key="opt"
                        class="tenor-btn" :class="{ active: tf.tenorQuick === opt }"
                        @click="tf.tenorQuick = opt">{{ opt }}</button>
                    </div>
                  </div>
                </div>

                <!-- 交易日期 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldTradeDate')">{{ t('fxSwap.fieldTradeDate') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-date-picker v-model="tf.tradeDate" type="date" value-format="YYYY-MM-DD"
                      size="small" style="flex:1" :placeholder="t('fxSwap.placeholderDate')" />
                    <el-time-picker v-model="tf.tradeTime" format="HH:mm:ss" value-format="HH:mm:ss"
                      size="small" style="width:110px" :placeholder="t('fxSwap.placeholderTime')" />
                  </div>
                </div>

                <!-- 起息日/到期日 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldNearFarDate')">{{ t('fxSwap.fieldNearFarDate') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-date-picker v-model="tf.nearDate" type="date" value-format="YYYY-MM-DD"
                      size="small" style="flex:1" :placeholder="t('fxSwap.placeholderDate')" @change="calcTenorDays" />
                    <el-date-picker v-model="tf.farDate" type="date" value-format="YYYY-MM-DD"
                      size="small" style="flex:1" :placeholder="t('fxSwap.placeholderDate')" @change="calcTenorDays" />
                  </div>
                </div>

                <!-- 期限(天) -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldTenorDays')">{{ t('fxSwap.fieldTenorDays') }}</div>
                  <div class="td-value td-value--auto">
                    <el-input :value="tf.tenorDays" disabled size="small" style="width:100%" />
                  </div>
                </div>

                <!-- 近端远期点/近端汇率 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldNearPtsRate')">{{ t('fxSwap.fieldNearPtsRate') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.nearSwapPts" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" @input="calcNearRate" />
                    <el-input :value="tf.nearRate" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" disabled class="rate-auto" />
                  </div>
                </div>

                <!-- 远端远期点/远端汇率 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldFarPtsRate')">{{ t('fxSwap.fieldFarPtsRate') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.farSwapPts" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" @input="calcFarRate" />
                    <el-input :value="tf.farRate" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" disabled class="rate-auto" />
                  </div>
                </div>

                <!-- 近端金额 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldNearAmount')">{{ t('fxSwap.fieldNearAmount') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.nearAmt1" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" />
                    <el-input v-model="tf.nearAmt2" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" />
                  </div>
                </div>

                <!-- 远端金额 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldFarAmount')">{{ t('fxSwap.fieldFarAmount') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.farAmt1" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" />
                    <el-input v-model="tf.farAmt2" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="flex:1" />
                  </div>
                </div>

                <!-- 代客外部流水号 -->
                <div class="td-row">
                  <div class="td-label td-label--w" :title="t('fxSwap.fieldClientExtNo')">{{ t('fxSwap.fieldClientExtNo') }}</div>
                  <div class="td-value">
                    <el-input v-model="tf.clientExtNo" size="small" :placeholder="t('fxSwap.inputPlaceholder')" style="width:100%" />
                  </div>
                </div>

                <!-- NoRound -->
                <div class="td-row">
                  <div class="td-label td-label--w">NoRound</div>
                  <div class="td-value">
                    <el-checkbox v-model="tf.noRound" size="small" />
                  </div>
                </div>

              </div>
            </div>

            <!-- ② 账户信息 -->
            <div class="td-section">
              <div class="td-section-title"><span class="td-bar"></span>{{ t('fxSwap.sectionAccount') }}</div>
              <div class="td-fields">

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldAccount') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-select v-model="tf.account" :placeholder="t('fxSwap.selectPlaceholder')" size="small" style="flex:1">
                      <el-option v-for="b in BOOKS" :key="b.code" :label="b.code" :value="b.code" />
                    </el-select>
                    <el-input :placeholder="t('fxSwap.placeholderAutoFill')" size="small" style="width:110px" disabled />
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldCounterparty') }} <span class="req">*</span></div>
                  <div class="td-value td-value--split">
                    <el-select v-model="tf.counterparty" :placeholder="t('fxSwap.selectPlaceholder')" size="small" style="flex:1">
                      <el-option v-for="b in BOOKS" :key="b.code" :label="b.code" :value="b.code" />
                    </el-select>
                    <el-input :placeholder="t('fxSwap.placeholderAutoFill')" size="small" style="width:110px" disabled />
                  </div>
                </div>

              </div>
            </div>

            <!-- ③ 备注 -->
            <div class="td-section">
              <div class="td-section-title"><span class="td-bar"></span>{{ t('fxSwap.sectionRemarks') }}</div>
              <div class="td-fields">

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldTradeNature') }}</div>
                  <div class="td-value">
                    <el-select v-model="tf.tradeNature" :placeholder="t('fxSwap.selectPlaceholder')" size="small" style="width:100%">
                      <el-option :label="t('fxSwap.optionInternal')" value="internal" />
                      <el-option :label="t('fxSwap.optionInterbank')" value="interbank" />
                      <el-option :label="t('fxSwap.optionCustomer')" value="customer" />
                    </el-select>
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldExternalNo') }}</div>
                  <div class="td-value td-value--split">
                    <el-input v-model="tf.externalNo" :placeholder="t('fxSwap.inputPlaceholder')" size="small" style="flex:1" />
                    <el-select v-model="tf.externalSystem" size="small" style="width:80px">
                      <el-option label="RCS" value="RCS" />
                      <el-option label="SWIFT" value="SWIFT" />
                    </el-select>
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldPurpose') }}</div>
                  <div class="td-value">
                    <el-input v-model="tf.purpose" :placeholder="t('fxSwap.inputPlaceholder')" size="small" style="width:100%" />
                  </div>
                </div>

                <div class="td-row">
                  <div class="td-label">{{ t('fxSwap.fieldRemark') }}</div>
                  <div class="td-value">
                    <el-input v-model="tf.remark" type="textarea" :rows="2"
                      :placeholder="t('fxSwap.inputPlaceholder')" size="small" style="width:100%" />
                  </div>
                </div>

              </div>
            </div>

          </div><!-- /td-form-scroll -->

          <!-- 底部按钮 -->
          <div class="td-footer">
            <el-button size="small" @click="resetForm">
              <el-icon><Delete /></el-icon>{{ t('fxSwap.btnClearAll') }}
            </el-button>
            <el-button type="primary" size="small" @click="handleSubmit">{{ t('fxSwap.btnSubmit') }}</el-button>
          </div>
        </div>
      </div>
    </el-drawer>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import { Setting, Delete } from '@element-plus/icons-vue'
import { PORTFOLIOS } from '@/data/bookStructure.js'

const { t } = useI18n()

// ── 筛选 ─────────────────────────────────────────────────────────────────────
const BOOKS = PORTFOLIOS.slice(0, 8)
const filterAccount = ref('')
const autoRefresh   = ref(false)
let   refreshTimer  = null

function handleQuery()  { ElMessage.success(t('fxSwap.querySuccess')) }
function handleReset()  { filterAccount.value = '' }
function onAutoRefreshChange(val) {
  clearInterval(refreshTimer)
  if (val) refreshTimer = setInterval(() => {}, 30000)
}

// ── 转移抽屉 ──────────────────────────────────────────────────────────────────
const drawerVisible = ref(false)
const currentRow    = ref(null)

const tf = reactive({
  currencyPair:  '',
  spotRate:      '',
  tenorQuick:    '',
  tradeDate:     new Date().toISOString().slice(0, 10),
  tradeTime:     '',
  nearDate:      '',
  farDate:       '',
  tenorDays:     0,
  nearSwapPts:   '',
  nearRate:      '',
  farSwapPts:    '',
  farRate:       '',
  nearAmt1:      '',
  nearAmt2:      '',
  farAmt1:       '',
  farAmt2:       '',
  nearSpread:    '',
  farSpread:     '',
  nearMargin:    '',
  farMargin:     '',
  clientExtNo:   '',
  noRound:       false,
  account:       '',
  counterparty:  '',
  tradeNature:   'internal',
  externalNo:    '',
  externalSystem:'RCS',
  purpose:       '',
  remark:        '',
})

function calcNearRate() {
  const spot = parseFloat(tf.spotRate), pts = parseFloat(tf.nearSwapPts)
  tf.nearRate = (!isNaN(spot) && !isNaN(pts)) ? (spot + pts * 0.0001).toFixed(6) : ''
}
function calcFarRate() {
  const spot = parseFloat(tf.spotRate), pts = parseFloat(tf.farSwapPts)
  tf.farRate = (!isNaN(spot) && !isNaN(pts)) ? (spot + pts * 0.0001).toFixed(6) : ''
}
function calcTenorDays() {
  if (tf.nearDate && tf.farDate) {
    const diff = Math.round((new Date(tf.farDate) - new Date(tf.nearDate)) / 86400000)
    tf.tenorDays = diff >= 0 ? diff : 0
  }
}

function handleDetail(row) {
  ElMessage.info(`${t('fxSwap.actionDetail')}: ${row.symbol}`)
}

function handleInternalTransfer(row) {
  currentRow.value     = row
  resetForm()
  tf.currencyPair      = row.symbol || ''
  tf.spotRate          = row.mktFwdRate != null ? row.mktFwdRate.toFixed(6) : ''
  tf.tradeDate         = new Date().toISOString().slice(0, 10)
  drawerVisible.value  = true
}

function resetForm() {
  Object.assign(tf, {
    currencyPair: '', spotRate: '', tenorQuick: '',
    tradeDate: new Date().toISOString().slice(0, 10), tradeTime: '',
    nearDate: '', farDate: '', tenorDays: 0,
    nearSwapPts: '', nearRate: '', farSwapPts: '', farRate: '',
    nearAmt1: '', nearAmt2: '', farAmt1: '', farAmt2: '',
    nearSpread: '', farSpread: '', nearMargin: '', farMargin: '',
    clientExtNo: '', noRound: false,
    account: '', counterparty: '',
    tradeNature: 'internal', externalNo: '', externalSystem: 'RCS',
    purpose: '', remark: '',
  })
}

function handleSubmit() {
  if (!tf.account || !tf.counterparty) {
    ElMessage.warning(t('fxSwap.transferTargetRequired'))
    return
  }
  ElMessage.success(t('fxSwap.transferSuccess'))
  drawerVisible.value = false
}

// ── 格式化工具 ─────────────────────────────────────────────────────────────
function fmtNum(v, dp = 2) {
  if (v == null || v === '') return '—'
  return Number(v).toLocaleString('en', { minimumFractionDigits: dp, maximumFractionDigits: dp })
}
function numClass(v) {
  return { 'num-neg': v != null && v < 0, 'num-pos': false }
}

// ── Mock 数据（基于截图）─────────────────────────────────────────────────
const tableData = ref([
  {
    id: 'eurusd', symbol: 'EURUSD', level: 'pair',
    ccy1: 'EUR', ccy1Amount: -715386.07,
    ccy2: 'USD', ccy2Amount: -579787.47,
    mktFwdRate: 1.1711, swapPoints: null, breakeven: 0.364931,
    equivExposure: -13419437.30, dv01Ccy1: 644.19, dv01Ccy2: -742.02,
    totalPnl: -11752.75, discPnlUsd: -11752.75, discPnlCny: -2353027.30,
    dailyPnl: -142.75, monthlyPnl: -11752.75, yearlyPnl: -11752.75,
    df1: null, df2: null, spotDf1: null, spotDf2: null,
    ccy1Curve: null, ccy2Curve: null,
    children: [
      {
        id: 'balance', symbol: 'Balance', level: 'deal',
        ccy1: 'EUR', ccy1Amount: 6000000,
        ccy2: 'USD', ccy2Amount: -7026596.64,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.171099,
        equivExposure: 0, dv01Ccy1: 0, dv01Ccy2: 0,
        totalPnl: -183.79, discPnlUsd: -183.79, discPnlCny: -9207.22,
        dailyPnl: -142.75, monthlyPnl: -183.79, yearlyPnl: -183.79,
        df1: 1, df2: 1, spotDf1: 1, spotDf2: 1,
        ccy1Curve: null, ccy2Curve: null,
      },
      {
        id: 'tom', symbol: 'TOM[20260605]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: 13000000,
        ccy2: 'USD', ccy2Amount: -14749243,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.134557,
        equivExposure: 0, dv01Ccy1: 0, dv01Ccy2: -0.29,
        totalPnl: 534945.94, discPnlUsd: 534945.94, discPnlCny: 3766607.88,
        dailyPnl: 0, monthlyPnl: 534945.94, yearlyPnl: 534945.94,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: 'tom_1', symbol: '20260605', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 13000000, ccy2: 'USD', ccy2Amount: -14749243,
            mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.134557,
            equivExposure: 0, dv01Ccy1: 0, dv01Ccy2: -0.29,
            totalPnl: 534945.94, discPnlUsd: 534945.94, discPnlCny: 3766607.88,
            dailyPnl: 0, monthlyPnl: 534945.94, yearlyPnl: 534945.94,
            df1: 0.99997901, df2: 0.99979244, spotDf1: 0.99997901, spotDf2: 0.99979244,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: 'spot', symbol: 'SPOT[20260608]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: 2000000, ccy2: 'USD', ccy2Amount: -2342200,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.1711,
        equivExposure: 0, dv01Ccy1: 0, dv01Ccy2: 0,
        totalPnl: 0, discPnlUsd: 0, discPnlCny: 0,
        dailyPnl: 0, monthlyPnl: 0, yearlyPnl: 0,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: 'spot_1', symbol: '20260608', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 2000000, ccy2: 'USD', ccy2Amount: -2342200,
            mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.1711,
            equivExposure: 0, dv01Ccy1: 0, dv01Ccy2: 0,
            totalPnl: 0, discPnlUsd: 0, discPnlCny: 0,
            dailyPnl: 0, monthlyPnl: 0, yearlyPnl: 0,
            df1: 0.99977150, df2: 0.99958496, spotDf1: 0.99977150, spotDf2: 0.99958496,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '1d', symbol: '1D[20260609]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: -11995356.80, ccy2: 'USD', ccy2Amount: 11997372,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.000168,
        equivExposure: -133281.74, dv01Ccy1: 6.57, dv01Ccy2: -6.01,
        totalPnl: -1026324.03, discPnlUsd: -1026324.03, discPnlCny: -7226450.11,
        dailyPnl: 0, monthlyPnl: -1026324.03, yearlyPnl: -1026324.03,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '1d_1', symbol: '20260609', level: 'deal',
            ccy1: 'EUR', ccy1Amount: -11995356.80, ccy2: 'USD', ccy2Amount: 11997372,
            mktFwdRate: 1.171324, swapPoints: 2.24, breakeven: 1.000168,
            equivExposure: -133281.74, dv01Ccy1: 6.57, dv01Ccy2: -6.01,
            totalPnl: -1026324.03, discPnlUsd: -1026324.03, discPnlCny: -7226450.11,
            dailyPnl: 0, monthlyPnl: -1026324.03, yearlyPnl: -1026324.03,
            df1: 0.99981546, df2: 0.99937732, spotDf1: 0.99997901, spotDf2: 0.99979244,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '2w', symbol: '2W[20260622]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: 3000000, ccy2: 'USD', ccy2Amount: -3302103,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.100701,
        equivExposure: 216666.67, dv01Ccy1: -10.68, dv01Ccy2: 11.63,
        totalPnl: 91270.27, discPnlUsd: 91270.27, discPnlCny: 1501448.14,
        dailyPnl: 0, monthlyPnl: 91270.27, yearlyPnl: 91270.27,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '2w_1', symbol: '20260618', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 3000000, ccy2: 'USD', ccy2Amount: -3302103,
            mktFwdRate: 1.171801, swapPoints: 7.01, breakeven: 1.100701,
            equivExposure: 216666.67, dv01Ccy1: -10.68, dv01Ccy2: 11.63,
            totalPnl: 91270.27, discPnlUsd: 91270.27, discPnlCny: 1501448.14,
            dailyPnl: 0, monthlyPnl: 91270.27, yearlyPnl: 91270.27,
            df1: 0.99929547, df2: 0.99843317, spotDf1: 0.99997901, spotDf2: 0.99979244,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '3w', symbol: '3W[20260629]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: 20000, ccy2: 'USD', ccy2Amount: -20200,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.010000,
        equivExposure: 100, dv01Ccy1: 0, dv01Ccy2: 0,
        totalPnl: 161.89, discPnlUsd: 161.89, discPnlCny: 1139.91,
        dailyPnl: 0, monthlyPnl: 161.89, yearlyPnl: 161.89,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '3w_1', symbol: '20260623', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 20000, ccy2: 'USD', ccy2Amount: -20200,
            mktFwdRate: 1.172106, swapPoints: 10.06, breakeven: 1.010000,
            equivExposure: 100, dv01Ccy1: 0, dv01Ccy2: 0,
            totalPnl: 161.89, discPnlUsd: 161.89, discPnlCny: 1139.91,
            dailyPnl: 0, monthlyPnl: 161.89, yearlyPnl: 161.89,
            df1: 0.99904364, df2: 0.99788898, spotDf1: 0.99997901, spotDf2: 0.99979244,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '1m', symbol: '1M[20260708]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: -4999000, ccy2: 'USD', ccy2Amount: 5862707.34,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.172776,
        equivExposure: -610988.89, dv01Ccy1: 30.09, dv01Ccy2: -35.24,
        totalPnl: 1712.27, discPnlUsd: 1712.27, discPnlCny: 12056.25,
        dailyPnl: 0, monthlyPnl: 1712.27, yearlyPnl: 1712.27,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '1m_1', symbol: '20260630', level: 'deal',
            ccy1: 'EUR', ccy1Amount: -4999000, ccy2: 'USD', ccy2Amount: 5862707.34,
            mktFwdRate: 1.172464, swapPoints: 13.64, breakeven: 1.172776,
            equivExposure: -610988.89, dv01Ccy1: 30.09, dv01Ccy2: -35.24,
            totalPnl: 1712.27, discPnlUsd: 1712.27, discPnlCny: 12056.25,
            dailyPnl: 0, monthlyPnl: 1712.27, yearlyPnl: 1712.27,
            df1: 0.99861454, df2: 0.99729342, spotDf1: 0.99977150, spotDf2: 0.99958496,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '2m', symbol: '2M[20260810]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: 176000, ccy2: 'USD', ccy2Amount: -206735.58,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.174634,
        equivExposure: 50844.44, dv01Ccy1: -2.50, dv01Ccy2: 2.93,
        totalPnl: -79.17, discPnlUsd: -79.17, discPnlCny: -557.45,
        dailyPnl: 0, monthlyPnl: -79.17, yearlyPnl: -79.17,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '2m_1', symbol: '20260730', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 176000, ccy2: 'USD', ccy2Amount: -206735.58,
            mktFwdRate: 1.174115, swapPoints: 30.14, breakeven: 1.174634,
            equivExposure: 50844.44, dv01Ccy1: -2.50, dv01Ccy2: 2.93,
            totalPnl: -79.17, discPnlUsd: -79.17, discPnlCny: -557.45,
            dailyPnl: 0, monthlyPnl: -79.17, yearlyPnl: -79.17,
            df1: 0.99704950, df2: 0.99424729, spotDf1: 0.99977150, spotDf2: 0.99958496,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '3m', symbol: '3M[20260908]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: -50000, ccy2: 'USD', ccy2Amount: 58759.25,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.175185,
        equivExposure: 79444.44, dv01Ccy1: -3.90, dv01Ccy2: 4.56,
        totalPnl: 9.85, discPnlUsd: 9.85, discPnlCny: 87.27,
        dailyPnl: 0, monthlyPnl: 9.85, yearlyPnl: 9.85,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '3m_1', symbol: '20260813', level: 'deal',
            ccy1: 'EUR', ccy1Amount: -50000, ccy2: 'USD', ccy2Amount: 58759.25,
            mktFwdRate: 1.174849, swapPoints: 37.49, breakeven: 1.175185,
            equivExposure: -18333.33, dv01Ccy1: 0.90, dv01Ccy2: -1.05,
            totalPnl: 12.82, discPnlUsd: 12.82, discPnlCny: 90.24,
            dailyPnl: 0, monthlyPnl: 12.82, yearlyPnl: 12.82,
            df1: 0.99626357, df2: 0.99283339, spotDf1: 0.99977150, spotDf2: 0.99958496,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
          {
            id: '3m_2', symbol: '20260901', level: 'deal',
            ccy1: 'EUR', ccy1Amount: 0, ccy2: 'USD', ccy2Amount: 0,
            mktFwdRate: 1.175908, swapPoints: 48.08, breakeven: 0,
            equivExposure: 97777.78, dv01Ccy1: -4.80, dv01Ccy2: 5.62,
            totalPnl: -0.42, discPnlUsd: -0.42, discPnlCny: -2.97,
            dailyPnl: 0, monthlyPnl: -0.42, yearlyPnl: -0.42,
            df1: 0.99509144, df2: 0.99083964, spotDf1: 0.99979244, spotDf2: 0.99979244,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
      {
        id: '5m', symbol: '5M[20261109]', level: 'tenor',
        ccy1: 'EUR', ccy1Amount: -6000000, ccy2: 'USD', ccy2Amount: 7076448,
        mktFwdRate: 1.1711, swapPoints: 0, breakeven: 1.179408,
        equivExposure: -4900000, dv01Ccy1: 239.67, dv01Ccy2: -280.71,
        totalPnl: 2218.24, discPnlUsd: 2218.24, discPnlCny: 15618.84,
        dailyPnl: 0, monthlyPnl: 2218.24, yearlyPnl: 2218.24,
        df1: null, df2: null, spotDf1: null, spotDf2: null, ccy1Curve: null, ccy2Curve: null,
        children: [
          {
            id: '5m_1', symbol: '20261020', level: 'deal',
            ccy1: 'EUR', ccy1Amount: -6000000, ccy2: 'USD', ccy2Amount: 7076448,
            mktFwdRate: 1.179533, swapPoints: 82.33, breakeven: 1.179408,
            equivExposure: -4900000, dv01Ccy1: 239.67, dv01Ccy2: -280.71,
            totalPnl: 2218.24, discPnlUsd: 2218.24, discPnlCny: 15618.84,
            dailyPnl: 0, monthlyPnl: 2218.24, yearlyPnl: 2218.24,
            df1: 0.99214830, df2: 0.98472156, spotDf1: 0.99977150, spotDf2: 0.99958496,
            ccy1Curve: 'EUR_FX_OFFSHORE', ccy2Curve: 'USD_SOFR',
          },
        ],
      },
    ],
  },
])
</script>

<style lang="scss" scoped>
.fxswap-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

/* ── 筛选栏 ── */
.fxs-filter {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-bottom: 1px solid var(--git-border);
  flex-shrink: 0;
}
.fxs-filter-label { font-size: 13px; color: var(--git-text-2); white-space: nowrap; }

/* ── 内容区 ── */
.fxs-body { flex: 1; overflow: auto; padding: 16px 20px; }
.fxs-section { margin-bottom: 24px; }

.fxs-section-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 10px;
}
.fxs-section-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--git-text-1);
  position: relative;
  padding-left: 10px;
  &::before {
    content: '';
    position: absolute;
    left: 0; top: 2px; bottom: 2px;
    width: 3px;
    background: var(--git-primary);
    border-radius: 2px;
  }
}
.fxs-auto-refresh { display: flex; align-items: center; gap: 6px; }
.fxs-ar-label { font-size: 12px; color: var(--git-text-2); }
.fxs-ar-setting {
  font-size: 14px;
  color: var(--git-text-3);
  cursor: pointer;
  &:hover { color: var(--git-primary); }
}

/* ── 表格 ── */
.fxs-table {
  width: 100%;
}

/* 行层级样式 */
.sym-cell { font-size: 12px; }
.sym--pair    { font-weight: 700; color: var(--git-text-1); }
.sym--tenor   { font-weight: 600; color: var(--git-primary); }
.sym--deal    { color: var(--git-text-2); }
.sym--balance { font-style: italic; color: var(--git-text-3); }

/* 货币标签 */
.ccy-tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--git-text-2);
}

/* 数值颜色 */
.num-neg { color: #c0392b; }
.bold    { font-weight: 600; }

/* 折算因子（小字） */
.dim-val {
  font-size: 11px;
  color: var(--git-text-3);
  font-variant-numeric: tabular-nums;
}
.dim { color: var(--git-text-3); }

/* 曲线标签 */
.curve-tag {
  font-size: 11px;
  background: #f0f4ff;
  color: var(--git-primary);
  border: 1px solid #d0ddff;
  border-radius: 3px;
  padding: 1px 5px;
  white-space: nowrap;
}

/* ── 操作列 ── */
.action-cell {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}
.action-link {
  font-size: 12px;
  color: var(--git-primary);
  cursor: pointer;
  &:hover { opacity: 0.75; }
}
.action-divider {
  font-size: 12px;
  color: var(--git-border);
  user-select: none;
}

/* ── 转移抽屉 ── */
:deep(.swap-transfer-drawer) {
  .el-drawer__header { padding: 16px 20px 12px; border-bottom: 1px solid var(--git-border); margin-bottom: 0; }
  .el-drawer__body   { padding: 0; display: flex; flex-direction: column; overflow: hidden; }
}
.td-header { display: flex; align-items: center; gap: 10px; }
.td-title  { font-size: 15px; font-weight: 600; color: var(--git-text-1); }
.td-header-tags { display: flex; gap: 6px; }

.td-body { flex: 1; display: flex; min-height: 0; overflow: hidden; }
.td-form-panel { flex: 1; display: flex; flex-direction: column; min-width: 0; }
.td-form-scroll { flex: 1; overflow-y: auto; padding: 16px 20px; }

.td-section { margin-bottom: 20px; }
.td-section-title {
  display: flex; align-items: center; gap: 6px;
  font-size: 13px; font-weight: 600; color: var(--git-text-1);
  margin-bottom: 8px; padding-left: 2px;
}
.td-bar {
  display: inline-block; width: 3px; height: 13px;
  background: var(--git-primary); border-radius: 2px; flex-shrink: 0;
}

.td-fields { border: 1px solid #e4e8f0; border-radius: 4px; overflow: hidden; }
.td-row {
  display: flex; align-items: stretch; min-height: 36px;
  border-bottom: 1px solid #edf0f7;
  &:last-child { border-bottom: none; }
}
.td-label {
  width: 100px; flex-shrink: 0; display: flex; align-items: center;
  padding: 0 10px; font-size: 12px; color: var(--git-text-2);
  background: #f8f9fc; border-right: 1px solid #edf0f7; white-space: nowrap;
  .req { color: #f56c6c; margin-left: 2px; }
}
.td-value {
  flex: 1; display: flex; align-items: center; padding: 3px 8px; background: #fff;
  &--auto {
    background: #f5f8ff;
    :deep(.el-input.is-disabled .el-input__wrapper) { background: transparent !important; box-shadow: none !important; }
    :deep(.el-input.is-disabled .el-input__inner) {
      color: var(--git-primary) !important; -webkit-text-fill-color: var(--git-primary) !important; font-weight: 600;
    }
  }
  &--split { gap: 6px; }
  :deep(.el-input__wrapper), :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important; border: 1px solid #dcdfe6; border-radius: 4px;
    background: #fff; padding: 0 8px; transition: border-color 0.2s;
    &:hover { border-color: var(--git-primary); }
  }
  :deep(.el-textarea__inner) { box-shadow: none !important; border: 1px solid #dcdfe6; border-radius: 4px; resize: none; }
  :deep(.el-date-editor .el-input__wrapper) { padding: 0 8px; }
}

.td-row--tall { min-height: 44px; }
.td-value--buysell { padding: 0; gap: 0; align-items: stretch; }
.bs-half { flex: 1; display: flex; align-items: center; padding: 4px 8px; gap: 6px; min-width: 0; }
.bs-sep { width: 1px; background: #edf0f7; align-self: stretch; }
.bs-tag { font-size: 11px; font-weight: 700; white-space: nowrap; letter-spacing: 0.5px;
  &--buy  { color: var(--git-primary); }
  &--sell { color: #f56c6c; }
}
.bs-arrow { color: var(--git-text-3); font-size: 13px; flex-shrink: 0; }
.bs-input { flex: 1; min-width: 0; }

/* 掉期专用：宽标签，超长截断 + hover tooltip */
.td-label--w {
  width: 136px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  display: block;
  line-height: 36px;
  cursor: default;
}
/* 基础标签也加截断 */
.td-label {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  cursor: default;
}

/* ON/TN/SN 按钮组 */
.tenor-btns { display: flex; gap: 6px; }
.tenor-btn {
  padding: 2px 14px; font-size: 12px;
  border: 1px solid var(--git-border); border-radius: 4px;
  background: #fff; color: var(--git-text-2); cursor: pointer; transition: all 0.15s;
  &:hover { border-color: var(--git-primary); color: var(--git-primary); }
  &.active { background: var(--git-primary); color: #fff; border-color: var(--git-primary); }
}

/* 自动计算汇率（蓝色只读） */
.rate-auto {
  :deep(.el-input__inner) { color: var(--git-primary) !important; -webkit-text-fill-color: var(--git-primary) !important; font-weight: 600; }
  :deep(.el-input__wrapper) { background: #f5f8ff !important; }
}

.td-footer {
  flex-shrink: 0; padding: 12px 20px; border-top: 1px solid var(--git-border);
  display: flex; justify-content: flex-end; gap: 10px; background: #fff;
}
</style>
