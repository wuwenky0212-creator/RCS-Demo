<template>
  <el-dialog
    v-model="visible"
    :title="t('tradeDetail.title')"
    width="960px"
    top="4vh"
    :close-on-click-modal="false"
    destroy-on-close
    class="trade-detail-dialog"
  >
    <div class="detail-body">

      <!-- ① 顶部状态双卡片 -->
      <div class="status-row">
        <div class="status-card">
          <div class="status-card-title">{{ t('tradeDetail.currentStatus') }}</div>
          <div class="status-card-body">
            <el-tag type="" class="status-tag">{{ t('tradeDetail.backReview') }}</el-tag>
            <span class="status-desc">{{ t('tradeDetail.inReview') }}</span>
          </div>
        </div>
        <div class="status-card next-card">
          <div class="status-card-title">
            {{ t('tradeDetail.nextStep') }}
            <el-button link type="primary" size="small" class="next-action-btn">{{ t('tradeDetail.sendConfirmMsg') }}</el-button>
          </div>
          <div class="status-card-body next-desc">
            {{ t('tradeDetail.nextStepDesc') }}
          </div>
        </div>
      </div>

      <!-- ② Tab 导航 -->
      <el-tabs v-model="activeTab" class="detail-tabs">
        <el-tab-pane :label="t('tradeDetail.tabInfo')"  name="info" />
        <el-tab-pane :label="t('tradeDetail.tabAccounting')"  name="accounting" />
      </el-tabs>

      <!-- ③ Tab 内容区 -->
      <div class="tab-content">

        <!-- ══ 同业拆借 交易信息 ══ -->
        <template v-if="activeTab === 'info' && !isBond">

          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionTradeInfo') }}</div>
            <div class="ds-grid">
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.currency') }}</div>
                <div class="ds-value">{{ ib.currency }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradeDirection') }}</div>
                <div class="ds-value">{{ directionLabelMap[ib.directionLabel] || ib.directionLabel }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.notional') }}</div>
                <div class="ds-value">{{ fmt(ib.amount1) }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.bizType') }}</div>
                <div class="ds-value text-muted">{{ ib.bizType || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradeDate') }}</div>
                <div class="ds-value">{{ ib.tradeDate }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.valueDate') }}</div>
                <div class="ds-value">{{ ib.valueDate }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.maturityDate') }}</div>
                <div class="ds-value">{{ ib.maturityDate }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tenor') }}</div>
                <div class="ds-value">{{ ib.tenor }}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionTradeAcct') }}</div>
            <div class="ds-grid">
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.account') }}</div>
                <div class="ds-value ds-value--split">
                  <span>{{ ib.account }}</span>
                  <span class="ds-value-right text-muted">{{ isEn ? ib.accountNameEn : ib.accountNameZh }}</span>
                </div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.counterparty') }}</div>
                <div class="ds-value ds-value--split">
                  <span class="link-orange">{{ ib.counterpartyCode }}</span>
                  <span class="ds-value-right text-muted">{{ isEn ? ib.counterpartyEn : ib.counterpartyZh }}</span>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>Interest Methods</div>
            <div class="ds-grid">
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.interestRate') }}</div>
                <div class="ds-value">{{ ib.rate }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.dayCountBasis') }}</div>
                <div class="ds-value">{{ ib.dayCountBasis }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.bizDayConv') }}</div>
                <div class="ds-value">{{ ib.businessDayConvention }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.holidayCal') }}</div>
                <div class="ds-value">
                  <el-tag size="small" type="info">{{ ib.holidayCalendar }}</el-tag>
                </div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionRemarks') }}</div>
            <div class="ds-grid">
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradeNature') }}</div>
                <div class="ds-value">{{ tradeNatureMap[ib.tradeNature] || ib.tradeNature }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.externalNo') }}</div>
                <div class="ds-value ds-value--split">
                  <span>{{ ib.externalNo }}</span>
                  <span class="ds-value-right text-muted">{{ ib.externalSystem }}</span>
                </div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradePurpose') }}</div>
                <div class="ds-value text-muted">{{ ib.purpose || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.remarks') }}</div>
                <div class="ds-value text-muted">{{ ib.remark || '—' }}</div>
              </div>
            </div>
          </div>

          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionExtended') }}</div>
            <div class="ds-grid">
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.myRecvSettle') }}({{ ib.currency }})</div>
                <div class="ds-value text-muted">{{ ib.myRecvSettle || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.cpPaySettle') }}({{ ib.currency }})</div>
                <div class="ds-value text-muted">{{ ib.cpPaySettle || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.myPaySettle') }}({{ ib.currency }})</div>
                <div class="ds-value text-muted">{{ ib.myPaySettle || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.cpRecvSettle') }}({{ ib.currency }})</div>
                <div class="ds-value text-muted">{{ ib.cpRecvSettle || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.clearingMethod') }}</div>
                <div class="ds-value">{{ ib.clearingMethod || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradingMethod') }}</div>
                <div class="ds-value text-muted">{{ ib.tradingMethod || '—' }}</div>
              </div>
              <div class="ds-row">
                <div class="ds-label">{{ t('tradeDetail.tradingVenue') }}</div>
                <div class="ds-value text-muted">{{ ib.tradingVenue || '—' }}</div>
              </div>
            </div>
          </div>

        </template>

        <!-- ══ 现券买卖 交易信息 ══ -->
        <template v-else-if="activeTab === 'info' && isBond">

          <!-- 债券信息 -->
          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionBondInfo') }}</div>
            <div class="ds-grid ds-grid--3col">
              <!-- 债券代码/简称 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.bondCode') }}</div>
                <div class="ds-val-main">{{ bond.bondCode }}</div>
                <div class="ds-val-sub text-muted">{{ bond.bondName }}</div>
              </div>
              <!-- 交易方向 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.direction') }}</div>
                <div class="ds-val-main dir-buy">{{ bondDirectionMap[bond.direction] || bond.direction }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <!-- 券面总额 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.faceValue') }}({{ bond.currency }})</div>
                <div class="ds-val-main">{{ fmt(bond.faceValue) }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <!-- 交易日 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.tradeDate') }}</div>
                <div class="ds-val-main">{{ bond.tradeDate }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <!-- 结算日 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.settlementDate') }}</div>
                <div class="ds-val-main">{{ bond.settlementDate }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <!-- 净价/点差/成本净价 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.cleanPriceLabel') }}</div>
                <div class="ds-val-main">{{ bond.cleanPrice }}</div>
                <div class="ds-val-sub text-muted">{{ bond.cleanSpread }} / {{ bond.cleanCost }}</div>
              </div>
              <!-- 净价金额/成本净价金额 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.cleanAmtLabel') }}</div>
                <div class="ds-val-main">{{ fmt(bond.cleanAmount) }}</div>
                <div class="ds-val-sub text-muted">{{ fmt(bond.cleanCostAmount) }}</div>
              </div>
              <!-- 全价/点差/成本全价 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.dirtyPriceLabel') }}</div>
                <div class="ds-val-main">{{ bond.dirtyPrice }}</div>
                <div class="ds-val-sub text-muted">{{ bond.dirtySpread }} / {{ bond.dirtyCost }}</div>
              </div>
              <!-- 全价金额/成本全价金额 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.dirtyAmtLabel') }}</div>
                <div class="ds-val-main">{{ fmt(bond.dirtyAmount) }}</div>
                <div class="ds-val-sub text-muted">{{ fmt(bond.dirtyCostAmount) }}</div>
              </div>
              <!-- 应计利息/利息总额 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.interestLabel') }}</div>
                <div class="ds-val-main">{{ bond.accruedInterest }}</div>
                <div class="ds-val-sub text-muted">{{ fmt(bond.totalInterest) }}</div>
              </div>
              <!-- 收益率/点差/成本收益率 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.yieldLabel') }}</div>
                <div class="ds-val-main">{{ bond.yield }}</div>
                <div class="ds-val-sub text-muted">{{ bond.yieldSpread }} / {{ bond.yieldCost }}</div>
              </div>
              <!-- 分润金额 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.profitShare') }}</div>
                <div class="ds-val-main">{{ bond.profitShare }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <!-- 交割方式 -->
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.deliveryMethod') }}</div>
                <div class="ds-val-main">{{ bond.deliveryMethod }}</div>
                <div class="ds-val-sub"></div>
              </div>
            </div>
          </div>

          <!-- 交易账户 -->
          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionTradeAcct') }}</div>
            <div class="ds-grid ds-grid--3col">
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.custodian') }}</div>
                <div class="ds-val-main">{{ isEn ? bond.custodianEn : bond.custodianZh }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.account') }}</div>
                <div class="ds-val-main">{{ bond.account }}</div>
                <div class="ds-val-sub text-muted">{{ bond.accountAlias }}</div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.counterparty') }}</div>
                <div class="ds-val-main link-orange">{{ bond.counterpartyCode }}</div>
                <div class="ds-val-sub text-muted">{{ isEn ? bond.counterpartyEn : bond.counterpartyZh }}</div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.backToBackAcct') }}</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub text-muted">—</div>
              </div>
            </div>
          </div>

          <!-- 备注 -->
          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionRemarks') }}</div>
            <div class="ds-grid ds-grid--3col">
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.tradeNature') }}</div>
                <div class="ds-val-main">{{ tradeNatureMap[bond.tradeNature] || bond.tradeNature }}</div>
                <div class="ds-val-sub"></div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.externalNo') }}</div>
                <div class="ds-val-main">{{ bond.externalNo }}</div>
                <div class="ds-val-sub text-muted">{{ bond.externalSystem }}</div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.tradePurpose') }}</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub"></div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.remarks') }}</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub"></div>
              </div>
            </div>
          </div>

          <!-- 拓展字段 -->
          <div class="detail-section">
            <div class="ds-title"><span class="ds-bar"></span>{{ t('tradeDetail.sectionExtended') }}</div>
            <div class="ds-grid ds-grid--3col">
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.myPaySettle') }}(USD)</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub"></div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.cpRecvSettle') }}(USD)</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub"></div>
              </div>
              <div class="ds-row3">
                <div class="ds-label">{{ t('tradeDetail.clearingMethod') }}</div>
                <div class="ds-val-main text-muted">—</div>
                <div class="ds-val-sub"></div>
              </div>
            </div>
          </div>

        </template>

        <!-- 账务预览 Tab — 现券买卖（规则待定，暂留空） -->
        <template v-else-if="activeTab === 'accounting' && isBond">
          <div class="acct-empty">
            <div class="acct-empty-icon">📋</div>
            <div class="acct-empty-title">{{ t('tradeDetail.acctEmpty') }}</div>
            <div class="acct-empty-desc">{{ t('tradeDetail.acctEmptyDesc') }}</div>
          </div>
        </template>

        <!-- 账务预览 Tab — 同业拆借 -->
        <template v-else-if="activeTab === 'accounting'">
          <div class="acct-wrap">

            <div class="acct-table">
              <div class="acct-thead">
                <div class="acct-th acct-col-seq">{{ t('tradeDetail.acctSeq') }}</div>
                <div class="acct-th acct-col-dir">{{ t('tradeDetail.acctDir') }}</div>
                <div class="acct-th acct-col-inst">{{ t('tradeDetail.acctInst') }}</div>
                <div class="acct-th acct-col-ccy">{{ t('tradeDetail.acctCcy') }}</div>
                <div class="acct-th acct-col-gl">{{ t('tradeDetail.acctGL') }}</div>
                <div class="acct-th acct-col-amt">{{ t('tradeDetail.acctAmt') }}</div>
              </div>

              <template v-for="group in accountingGroups" :key="group.date">
                <div class="acct-group-row" @click="acctGroupsExpanded[group.date] = !acctGroupsExpanded[group.date]">
                  <span class="acct-group-arrow" :class="{ collapsed: !group.expanded }">▼</span>
                  <span class="acct-group-date">{{ group.date }}</span>
                  <span class="acct-group-event">{{ group.event }}</span>
                  <span v-if="group.note" class="acct-group-note">{{ group.note }}</span>
                </div>

                <template v-if="group.expanded">
                  <div
                    v-for="entry in group.entries"
                    :key="entry.seq"
                    class="acct-row"
                  >
                    <div class="acct-col-seq acct-cell">{{ entry.seq }}</div>
                    <div class="acct-col-dir acct-cell">
                      <span :class="entry.direction === 'Dr' ? 'dir-dr' : 'dir-cr'">
                        {{ entry.direction === 'Dr' ? t('tradeDetail.drLabel') : t('tradeDetail.crLabel') }}
                      </span>
                    </div>
                    <div class="acct-col-inst acct-cell">{{ entry.institution }}</div>
                    <div class="acct-col-ccy acct-cell">{{ entry.currency }}</div>
                    <div class="acct-col-gl acct-cell">
                      <span class="gl-code">{{ entry.account }}</span>
                      <span class="gl-name">{{ entry.accountName }}</span>
                    </div>
                    <div class="acct-col-amt acct-cell acct-amount">{{ fmtAmt(entry.amount) }}</div>
                  </div>
                </template>
              </template>
            </div>

            <div class="acct-tax-note">
              <span class="tax-note-title">{{ t('tradeDetail.taxRuleTitle') }}</span>
              <span class="tax-note-item">{{ t('tradeDetail.taxNoteItem') }}</span>
              <span class="tax-note-formula">{{ t('tradeDetail.taxNoteFormula') }}</span>
            </div>

          </div>
        </template>

      </div>
    </div>

    <template #footer>
      <el-button @click="visible = false">{{ t('common.close') }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t, locale } = useI18n()
const props = defineProps({ row: { type: Object, default: null } })
const visible = defineModel({ default: false })
const activeTab = ref('info')

const isEn = computed(() => locale.value === 'en-US')

// ─── Computed translation maps ─────────────────────────────────
const directionLabelMap = computed(() => ({
  '借出': t('tradeDetail.dirLendOut'),
  '借入': t('common.dirBorrow'),
  '买入': t('tradeDetail.dirBuy'),
  '卖出': t('common.dirSell'),
}))

const tradeNatureMap = computed(() => ({
  '同业交易': t('tradeDetail.tradeNatureInterbank'),
}))

const bondDirectionMap = computed(() => ({
  '买入': t('tradeDetail.dirBuy'),
  '卖出': t('common.dirSell'),
}))

// 判断是否现券买卖
const isBond = computed(() => props.row?.product === '现券买卖')

// ── 同业拆借 mock 数据 ────────────────────────────────────────
const ib = {
  currency:               'USD',
  directionLabel:         '借出',
  amount1:                1_000_000.00,
  bizType:                '',
  tradeDate:              '2026-05-08',
  valueDate:              '2026-05-11',
  maturityDate:           '2026-08-11',
  tenor:                  92,
  account:                'HFZBIFIMN001',
  accountNameZh:          '美元货币拆借',
  accountNameEn:          'USD Interbank Lending',
  counterpartyCode:       '10275',
  counterpartyZh:         'ZG农业银行股份有限公司',
  counterpartyEn:         'Agricultural Bank of China (ZG)',
  rate:                   '3.12300000',
  dayCountBasis:          'ACT/360',
  businessDayConvention:  'Modified Following',
  holidayCalendar:        'USD',
  tradeNature:            '同业交易',
  externalNo:             '26050800003781',
  externalSystem:         'RCS',
  purpose:                '',
  remark:                 '',
  myRecvSettle:           '',
  cpPaySettle:            '',
  myPaySettle:            '',
  cpRecvSettle:           '',
  clearingMethod:         'DVP',
  tradingMethod:          '',
  tradingVenue:           '',
}

// ── 现券买卖 mock 数据 ────────────────────────────────────────
const bond = {
  bondCode:           'SHYMAL.IB',
  bondName:           'SHYMAL.IB',
  direction:          '买入',
  currency:           'USD',
  faceValue:          1_000_000.00,
  tradeDate:          '2026-05-08',
  settlementDate:     '2026-05-08',
  cleanPrice:         '100.0000',
  cleanSpread:        '0.00',
  cleanCost:          '100.0000',
  cleanAmount:        1_000_000.00,
  cleanCostAmount:    1_000_000.00,
  dirtyPrice:         '100.8667',
  dirtySpread:        '0.00',
  dirtyCost:          '100.8667',
  dirtyAmount:        1_008_666.67,
  dirtyCostAmount:    1_008_667.00,
  accruedInterest:    '0.86666667',
  totalInterest:      8_666.67,
  yield:              '2.00067241',
  yieldSpread:        '0.000000',
  yieldCost:          '2.00067241',
  profitShare:        '0.00000000',
  deliveryMethod:     'DVP',
  custodianZh:        '上海银行',
  custodianEn:        'Bank of Shanghai',
  account:            'shymalCNY01',
  accountAlias:       'shymalCNY01',
  counterpartyCode:   '10275',
  counterpartyZh:     'ZG农业银行股份有限公司',
  counterpartyEn:     'Agricultural Bank of China (ZG)',
  tradeNature:        '同业交易',
  externalNo:         '26050800003498',
  externalSystem:     'RCS',
}

function fmt(val) {
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
function fmtAmt(val) {
  return Number(val).toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

// ── 账务预览分录数据（双语） ──────────────────────────────────
const acctGroupsExpanded = ref({ '2026-05-08': true, '2026-05-11': true, '2026-08-11': true })

const accountingGroups = computed(() => {
  const en = isEn.value
  const groups = [
    {
      date: '2026-05-08',
      eventKey: 'acctEventTradeDate',
      noteKey: '',
      entries: [
        { seq: 1, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '9135800731',
          accountNameZh: '资金拆出 (表外-交割前头寸)',
          accountNameEn: 'Funds Lent Out (Off-B/S Pre-Settlement Position)',
          amount: 1_000_000.00 },
        { seq: 2, direction: 'Cr', institution: '00001', currency: 'USD',
          account: '9135800831',
          accountNameZh: '资金拆出对应科目 (表外)',
          accountNameEn: 'Contra Account – Funds Lent Out (Off-B/S)',
          amount: 1_000_000.00 },
      ],
    },
    {
      date: '2026-05-11',
      eventKey: 'acctEventValueDate',
      noteKey: '',
      entries: [
        { seq: 1, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '9135800831',
          accountNameZh: '资金拆出对应科目 (表外冲正)',
          accountNameEn: 'Contra Account – Funds Lent Out (Off-B/S Reversal)',
          amount: 1_000_000.00 },
        { seq: 2, direction: 'Cr', institution: '00001', currency: 'USD',
          account: '9135800731',
          accountNameZh: '资金拆出 (表外冲正)',
          accountNameEn: 'Funds Lent Out (Off-B/S Reversal)',
          amount: 1_000_000.00 },
        { seq: 3, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '1303808309',
          accountNameZh: '拆出资金-境外同业拆出 (资产增加)',
          accountNameEn: 'Interbank Loans Placed – Offshore (Asset Increase)',
          amount: 1_000_000.00 },
        { seq: 4, direction: 'Cr', institution: '00001', currency: 'USD',
          account: '2524410301',
          accountNameZh: '结算户 (我方出账/头寸减少)',
          accountNameEn: 'Settlement Account (Payment / Position Decrease)',
          amount: 1_000_000.00 },
      ],
    },
    {
      date: '2026-08-11',
      eventKey: 'acctEventMaturity',
      noteKey: 'acctNoteMaturity',
      entries: [
        { seq: 1, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '2524410301',
          accountNameZh: '结算户 (收回全额本金)',
          accountNameEn: 'Settlement Account (Principal Receipt)',
          amount: 1_000_000.00 },
        { seq: 2, direction: 'Cr', institution: '00001', currency: 'USD',
          account: '1303808309',
          accountNameZh: '拆出资金-境外同业拆出 (本金结清)',
          accountNameEn: 'Interbank Loans Placed – Offshore (Principal Cleared)',
          amount: 1_000_000.00 },
        { seq: 3, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '2524410301',
          accountNameZh: '结算户 (扣税后的实际物理净利息)',
          accountNameEn: 'Settlement Account (Net Interest After WHT)',
          amount:     6_384.80 },
        { seq: 4, direction: 'Dr', institution: '00001', currency: 'USD',
          account: '1221000000',
          accountNameZh: '应收/预缴税费-代扣代缴WHT (独立记账资产)',
          accountNameEn: 'WHT Receivable / Prepaid Tax (Standalone Asset)',
          amount:     1_596.20 },
        { seq: 5, direction: 'Cr', institution: '00001', currency: 'USD',
          account: '6011000000',
          accountNameZh: '利息收入-境外同业拆借 (未扣税的毛利息)',
          accountNameEn: 'Interest Income – Offshore Interbank (Gross Before Tax)',
          amount:     7_981.00 },
      ],
    },
  ]
  return groups.map(g => ({
    ...g,
    event:    t(`tradeDetail.${g.eventKey}`),
    note:     g.noteKey ? t(`tradeDetail.${g.noteKey}`) : '',
    expanded: acctGroupsExpanded.value[g.date] ?? true,
    entries:  g.entries.map(e => ({
      ...e,
      accountName: en ? e.accountNameEn : e.accountNameZh,
    })),
  }))
})
</script>

<style lang="scss">
.trade-detail-dialog {
  .el-dialog__body {
    padding: 0;
    max-height: 78vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
  }
  .el-dialog__footer {
    border-top: 1px solid #ebeef5;
    padding: 12px 20px;
  }
}
</style>

<style lang="scss" scoped>
.detail-body {
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
  padding: 0;
}

/* ── 顶部状态双卡片 ── */
.status-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  padding: 12px 16px 10px;
  background: #f8f9fb;
  border-bottom: 1px solid #ebeef5;
  flex-shrink: 0;
}

.status-card {
  background: #ffffff;
  border: 1px solid #e4e8f0;
  border-radius: 6px;
  padding: 12px 16px;

  .status-card-title {
    font-size: 13px;
    font-weight: 600;
    color: #606266;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
  }

  .status-card-body {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 13px;
    color: #909399;
  }

  .status-tag {
    border-color: var(--git-primary);
    color: var(--git-primary);
    background: #ecf5ff;
  }

  .status-desc {
    color: #606266;
    font-size: 13px;
  }

  &.next-card .next-desc {
    display: block;
    font-size: 13px;
    color: #909399;
    line-height: 1.6;
  }

  .next-action-btn {
    font-size: 13px;
    font-weight: 500;
  }
}

/* ── Tab 导航 ── */
.detail-tabs {
  flex-shrink: 0;
  padding: 0 16px;
  border-bottom: 1px solid #ebeef5;

  :deep(.el-tabs__nav-wrap::after) { height: 1px; }
  :deep(.el-tabs__header) { margin: 0; }
  :deep(.el-tabs__item) {
    font-size: 14px;
    padding: 0 16px;
    height: 44px;
    line-height: 44px;
  }
  :deep(.el-tabs__content) { display: none; }
}

/* ── Tab 内容区 ── */
.tab-content {
  flex: 1;
  overflow-y: auto;
  padding: 0 0 12px;
  background: #f4f6fb;
}

/* ── 各 Section ── */
.detail-section {
  background: #ffffff;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  margin: 10px 16px 0;
  overflow: hidden;
}

.ds-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #303133;
  border-bottom: 1px solid #edf0f7;
  background: #fff;

  .ds-bar {
    display: inline-block;
    width: 3px;
    height: 13px;
    background: var(--git-primary);
    border-radius: 2px;
  }
}

/* ── 同业拆借：2列布局 ── */
.ds-grid {
  display: grid;
  grid-template-columns: 1fr;
}

.ds-row {
  display: grid;
  grid-template-columns: 180px 1fr;
  border-bottom: 1px solid #edf0f7;
  min-height: 36px;

  &:last-child { border-bottom: none; }
}

.ds-label {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: 13px;
  color: #606266;
  background: #f8f9fc;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
}

.ds-value {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: 13px;
  color: #303133;
  background: #fff;

  &--split {
    justify-content: space-between;
  }

  .ds-value-right {
    color: #909399;
    font-size: 13px;
  }
}

/* ── 现券买卖：3列布局（标签 | 主值 | 副值） ── */
.ds-grid--3col {
  display: grid;
  grid-template-columns: 1fr;
}

.ds-row3 {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  border-bottom: 1px solid #edf0f7;
  min-height: 36px;

  &:last-child { border-bottom: none; }
}

.ds-val-main {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: 13px;
  color: #303133;
  background: #fff;
  border-right: 1px solid #edf0f7;
}

.ds-val-sub {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: 13px;
  color: #606266;
  background: #fff;
}

.text-muted { color: #909399; }
.link-orange {
  color: #e6a23c;
  cursor: pointer;
  &:hover { text-decoration: underline; }
}
.dir-buy { color: #67c23a; font-weight: 600; }

/* ── 账务预览 占位 ── */
.acct-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 220px;
  gap: 10px;
  color: #909399;

  .acct-empty-icon {
    font-size: 36px;
    opacity: 0.5;
  }
  .acct-empty-title {
    font-size: 14px;
    font-weight: 600;
    color: #606266;
  }
  .acct-empty-desc {
    font-size: 13px;
    color: #909399;
  }
}

/* ── 账务预览 ── */
.acct-wrap {
  padding: 12px 16px 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.acct-table {
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;
  font-size: 13px;
}

.acct-col-seq  { width: 48px;  flex-shrink: 0; }
.acct-col-dir  { width: 90px;  flex-shrink: 0; }
.acct-col-inst { width: 90px;  flex-shrink: 0; }
.acct-col-ccy  { width: 60px;  flex-shrink: 0; }
.acct-col-gl   { flex: 1;      min-width: 0; }
.acct-col-amt  { width: 130px; flex-shrink: 0; text-align: right; }

.acct-thead {
  display: flex;
  background: #f5f7fa;
  border-bottom: 1px solid #e4e8f0;
  .acct-th {
    padding: 8px 10px;
    font-size: 12px;
    font-weight: 600;
    color: #606266;
  }
}

.acct-group-row {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 7px 10px;
  background: #f0f4ff;
  border-bottom: 1px solid #dde4f5;
  cursor: pointer;
  font-size: 13px;
  user-select: none;

  &:hover { background: #e6edff; }

  .acct-group-arrow {
    font-size: 10px;
    color: #909399;
    transition: transform 0.2s;
    display: inline-block;
    width: 14px;
    &.collapsed { transform: rotate(-90deg); }
  }
  .acct-group-date  { font-weight: 600; color: #303133; }
  .acct-group-event { font-weight: 500; color: #303133; margin-left: 4px; }
  .acct-group-en    { color: #909399; font-size: 12px; }
  .acct-group-note  {
    margin-left: auto;
    font-size: 12px;
    color: var(--git-primary);
    font-weight: 500;
    background: #ecf5ff;
    border: 1px solid #b3d8ff;
    border-radius: 3px;
    padding: 1px 8px;
  }
}

.acct-row {
  display: flex;
  align-items: center;
  border-bottom: 1px solid #f0f2f5;
  background: #fff;

  &:last-child { border-bottom: none; }
  &:hover { background: #fafbff; }
}

.acct-cell {
  padding: 7px 10px;
  color: #303133;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.acct-amount {
  font-family: 'Helvetica Neue', monospace;
  font-weight: 500;
  color: #303133;
  white-space: nowrap;
}

.dir-dr { color: #e6a23c; font-weight: 600; }
.dir-cr { color: #409eff; font-weight: 600; }

.gl-code { color: #606266; margin-right: 6px; font-family: monospace; }
.gl-name { color: #303133; }

.acct-tax-note {
  display: flex;
  flex-direction: column;
  gap: 4px;
  background: #fffbf0;
  border: 1px solid #ffe4a0;
  border-radius: 4px;
  padding: 10px 14px;
  font-size: 12px;

  .tax-note-title {
    font-weight: 600;
    color: #b8860b;
    margin-bottom: 2px;
  }
  .tax-note-item  { color: #606266; }
  .tax-note-formula {
    color: #303133;
    b { color: #e6a23c; }
  }
}
</style>
