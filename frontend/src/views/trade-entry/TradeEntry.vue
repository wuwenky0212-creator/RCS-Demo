<template>
  <div class="trade-entry-page" :class="{ 'is-combo': selectedProduct === 'fx-avg-forward' }">

    <!-- ① 左侧产品树 -->
    <div class="product-tree">
      <div class="tree-header">
        <el-icon class="tree-header-icon"><Grid /></el-icon>
        <span>{{ t('te.financialProducts') }}</span>
      </div>
      <div class="tree-search">
        <el-input v-model="searchText" :placeholder="t('te.searchPlaceholder')" clearable size="small">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </div>
      <div class="tree-body">
        <!-- 交易详情 -->
        <div
          class="tree-standalone"
          :class="{ active: selectedProduct === '__detail__' }"
          @click="selectProduct('__detail__')"
        >{{ t('te.tradeDetails') }}</div>

        <!-- 分类树 -->
        <div v-for="group in filteredGroups" :key="group.label" class="tree-group">
          <div class="group-label" @click="toggleGroup(group.label)">
            <el-icon class="group-arrow" :class="{ expanded: groupExpanded[group.label] !== false }">
              <ArrowRight />
            </el-icon>
            <span class="group-icon-dot" :style="{ background: group.color }"></span>
            <span>{{ group.label }}</span>
          </div>
          <template v-if="groupExpanded[group.label] !== false">
            <template v-for="item in group.items" :key="item.key">
              <!-- 带子项的可折叠条目（如外汇期权） -->
              <template v-if="item.children">
                <div class="tree-item tree-item--subgroup" @click="toggleSubGroup(item.key)">
                  <el-icon class="sub-arrow" :class="{ expanded: subExpanded[item.key] }"><ArrowRight /></el-icon>
                  {{ item.label }}
                </div>
                <template v-if="subExpanded[item.key]">
                  <div
                    v-for="child in item.children" :key="child.key"
                    class="tree-item tree-item--child"
                    :class="{ active: selectedProduct === child.key }"
                    @click="selectProduct(child.key)"
                  >{{ child.label }}</div>
                </template>
              </template>
              <!-- 普通叶子条目 -->
              <div
                v-else
                class="tree-item"
                :class="{ active: selectedProduct === item.key }"
                @click="selectProduct(item.key)"
              >{{ item.label }}</div>
            </template>
          </template>
        </div>
      </div>
    </div>

    <!-- ② 中间表单区 -->
    <div class="form-panel">
      <div class="form-header">
        <!-- 外汇平价远期：组合交易专属头部 -->
        <template v-if="selectedProduct === 'fx-avg-forward'">
          <div class="form-tabs">
            <span class="product-label">{{ t('te.fxAvgForward') }}</span>
            <button class="tab-btn active">
              <el-icon style="color:#f0a500"><Lightning /></el-icon>
              {{ t('te.comboTrade') }}
            </button>
            <span class="af-added-tag">{{ t('te.addedCount', { n: avgFwdTrades.length, max: maxAvgFwdTrades }) }}</span>
          </div>
          <div class="form-action-icons">
            <el-tooltip :content="t('te.tooltipBookmark')"><el-icon class="hd-icon"><Star /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipRefresh')"><el-icon class="hd-icon"><RefreshRight /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipCopy')"><el-icon class="hd-icon"><CopyDocument /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipView')"><el-icon class="hd-icon"><View /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipLock')"><el-icon class="hd-icon"><Lock /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipSaveAs')"><el-icon class="hd-icon"><Document /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipHistory')"><el-icon class="hd-icon"><Clock /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipReminder')"><el-icon class="hd-icon"><Bell /></el-icon></el-tooltip>
            <el-button size="small" class="af-import-btn">{{ t('te.batchImport') }}</el-button>
            <el-button size="small" type="primary" class="af-newtrade-btn"
              :disabled="avgFwdTrades.length >= maxAvgFwdTrades"
              @click="addAvgFwdTrade">{{ t('te.newTrade') }}</el-button>
          </div>
        </template>
        <!-- 普通产品头部 -->
        <template v-else>
          <div class="form-tabs">
            <span class="product-label">{{ currentProductLabel }}</span>
            <button class="tab-btn active">
              <el-icon style="color:#f0a500"><Lightning /></el-icon>
              {{ t('te.tradeBook') }}
            </button>
          </div>
          <div class="form-action-icons">
            <el-tooltip :content="t('te.tooltipBookmark')"><el-icon class="hd-icon"><Star /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipRefresh')"><el-icon class="hd-icon"><RefreshRight /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipCopy')"><el-icon class="hd-icon"><CopyDocument /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipView')"><el-icon class="hd-icon"><View /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipLock')"><el-icon class="hd-icon"><Lock /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipSaveAs')"><el-icon class="hd-icon"><Document /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipHistory')"><el-icon class="hd-icon"><Clock /></el-icon></el-tooltip>
            <el-tooltip :content="t('te.tooltipReminder')"><el-icon class="hd-icon"><Bell /></el-icon></el-tooltip>
          </div>
        </template>
      </div>

      <div class="form-body">

        <!-- ══ 外汇远期 表单 ══ -->
        <template v-if="selectedProduct === 'fx-forward'">

          <!-- 交易信息 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeInfo') }}</div>

            <!-- 货币对：单列全宽 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.currencyPair') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="fxFwd.currencyPair" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%">
                  <el-option label="USD/CNY" value="USD/CNY" />
                  <el-option label="EUR/CNY" value="EUR/CNY" />
                  <el-option label="EUR/USD" value="EUR/USD" />
                  <el-option label="GBP/USD" value="GBP/USD" />
                  <el-option label="USD/JPY" value="USD/JPY" />
                </el-select>
              </div>
            </div>

            <!-- 金额：2列 [BUY ⇌ input | SELL ⇌ input] -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.amount') }}({{ fxFwd.currencyPair || '' }}) <span class="req">*</span></div>
              <div class="fs-cols fs-cols--2">
                <div class="fc">
                  <span class="dir-tag dir-buy">BUY</span>
                  <el-icon class="swap-icon"><Sort /></el-icon>
                  <el-input v-model="fxFwd.buyAmount" :placeholder="t('te.inputPlaceholder')" size="small" style="flex:1;min-width:0" />
                </div>
                <div class="fc">
                  <span class="dir-tag dir-sell">SELL</span>
                  <el-icon class="swap-icon"><Sort /></el-icon>
                  <el-input v-model="fxFwd.sellAmount" :placeholder="t('te.inputPlaceholder')" size="small" style="flex:1;min-width:0" />
                </div>
              </div>
            </div>

            <!-- 即期汇率：3列等宽 [即期汇率 | 点差 | 成本汇率(只读)] -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.spotRateLabel') }}</div>
              <div class="fs-cols fs-cols--rate3">
                <div class="fc fc--readonly">
                  <el-input v-model="fxFwd.spotRate" placeholder="0.000000" size="small" style="width:100%" disabled />
                </div>
                <div class="fc fc--readonly">
                  <el-input v-model="fxFwd.spotBP" placeholder="0.00" size="small" style="width:100%" disabled />
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="spotCostRate" placeholder="0.000000" size="small" style="width:100%" disabled />
                </div>
              </div>
            </div>

            <!-- 远期汇率：3列等宽 [远期汇率 | 点差 | 成本远期汇率(只读)] -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.fwdRateLabel') }}</div>
              <div class="fs-cols fs-cols--rate3">
                <div class="fc fc--readonly">
                  <el-input v-model="fxFwd.fwdRate" placeholder="0.000000" size="small" style="width:100%" disabled />
                </div>
                <div class="fc fc--readonly">
                  <el-input v-model="fxFwd.fwdBP" placeholder="0.00" size="small" style="width:100%" disabled />
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="fwdCostRate" placeholder="0.000000" size="small" style="width:100%" disabled />
                </div>
              </div>
            </div>

            <!-- 分润金额：2列 [金额 | 货币] -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.profitSplit') }}</div>
              <div class="fs-cols fs-cols--profit">
                <div class="fc fc--readonly">
                  <el-input v-model="fxFwd.profitSplit" placeholder="0.00" size="small" style="width:100%" disabled />
                </div>
                <div class="fc fc--readonly">
                  <el-select v-model="fxFwd.profitCcy" size="small" style="width:100%" disabled>
                    <el-option v-for="c in CCY_LIST" :key="c" :label="c" :value="c" />
                  </el-select>
                </div>
              </div>
            </div>

            <!-- 交易日：2列 [日期 | 时间] -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeDate') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--2">
                <div class="fc">
                  <el-date-picker v-model="fxFwd.tradeDate" type="date" :placeholder="t('te.selectDate')"
                    value-format="YYYY-MM-DD" size="small" style="width:100%" />
                </div>
                <div class="fc">
                  <el-time-picker v-model="fxFwd.tradeTime" :placeholder="t('te.selectTime')"
                    value-format="HH:mm:ss" size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 即期起息日：单列 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.spotValueDate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-date-picker v-model="fxFwd.spotValueDate" type="date" :placeholder="t('te.selectDate')"
                  value-format="YYYY-MM-DD" size="small" style="width:100%" @change="calcTenorFwd" />
              </div>
            </div>

            <!-- 择期交割日：单列 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.optionalDate') }}</div>
              <div class="fs-value">
                <el-date-picker v-model="fxFwd.optionalDate" type="date" :placeholder="t('te.selectDate')"
                  value-format="YYYY-MM-DD" size="small" style="width:100%" />
              </div>
            </div>

            <!-- 到期日：单列 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.maturityDate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-date-picker v-model="fxFwd.maturityDate" type="date" :placeholder="t('te.selectDate')"
                  value-format="YYYY-MM-DD" size="small" style="width:100%" @change="calcTenorFwd" />
              </div>
            </div>

            <!-- 期限(天)：只读展示 -->
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.tenor') }}</div>
              <div class="fs-value"><span class="plain-val">{{ fxFwd.tenor || 0 }}</span></div>
            </div>
          </div>

          <!-- 交易账户 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeAccount') }}</div>

            <div class="fs-row" v-for="(acct, idx) in accountRows.value" :key="acct.key"
              :class="{ 'fs-row--last': idx === accountRows.value.length - 1 }">
              <div class="fs-label">{{ acct.label }} <span v-if="acct.req" class="req">*</span></div>
              <div class="fs-cols fs-cols--2">
                <div class="fc">
                  <el-input v-model="fxFwd[acct.key]" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                </div>
                <div class="fc fc--autofill">{{ t('te.autoFill') }}</div>
              </div>
            </div>
          </div>

          <!-- 备注 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secRemarks') }}</div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeNature') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="fxFwd.tradeNature" size="small" style="width:100%">
                  <el-option :label="t('te.natureInterbank')" value="interbank" />
                  <el-option :label="t('te.natureProprietary')" value="proprietary" />
                  <el-option :label="t('te.natureAgency')" value="agency" />
                </el-select>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.externalNo') }}</div>
              <div class="fs-cols fs-cols--profit">
                <div class="fc"><el-input v-model="fxFwd.externalNo" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
                <div class="fc">
                  <el-select v-model="fxFwd.externalSystem" size="small" style="width:100%">
                    <el-option label="RCS" value="RCS" />
                    <el-option label="EXT" value="EXT" />
                  </el-select>
                </div>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradePurpose') }}</div>
              <div class="fs-value"><el-input v-model="fxFwd.purpose" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
            </div>
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.remarks') }}</div>
              <div class="fs-value"><el-input v-model="fxFwd.remark" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
            </div>
          </div>

          <!-- 拓展字段 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secExtFields') }}</div>
            <div class="fs-row" v-for="(ext, idx) in extFields.value" :key="ext.key"
              :class="{ 'fs-row--last': idx === extFields.value.length - 1 }">
              <div class="fs-label">{{ ext.label }}</div>
              <div class="fs-value">
                <el-select v-model="fxFwd[ext.key]" placeholder="" size="small" style="width:100%" clearable />
              </div>
            </div>
          </div>

        </template>

        <!-- ══ 外汇平价远期：组合交易 ══ -->
        <template v-else-if="selectedProduct === 'fx-avg-forward'">
          <div class="af-wrap">

            <!-- 横向可滚动多列表格 -->
            <div class="af-scroll-x">
              <div class="af-grid" :style="{ gridTemplateColumns: `110px repeat(${avgFwdTrades.length}, 200px)` }">

                <!-- ── 列头 ── -->
                <div class="af-cell af-cell--head-label">{{ t('te.elementName') }}</div>
                <div v-for="(trade, idx) in avgFwdTrades" :key="'h'+trade.id" class="af-cell af-cell--head-trade">
                  <span class="af-tdot" :style="{ background: afColors[idx % afColors.length] }"></span>
                  <span class="af-ttitle">{{ t('te.tradeN', { n: idx + 1 }) }}</span>
                  <span class="af-cbadge">{{ afCommon.currencyPair ? afCommon.currencyPair.replace('/', '') : '—' }}</span>
                  <div class="af-ticons">
                    <el-tooltip :content="t('te.tooltipLock')"><el-icon><Lock /></el-icon></el-tooltip>
                    <el-tooltip :content="t('te.tooltipCopy')"><el-icon><CopyDocument /></el-icon></el-tooltip>
                    <el-tooltip :content="t('te.tooltipDelete')"><el-icon class="af-del-icon" @click="removeAvgFwdTrade(trade.id)"><Delete /></el-icon></el-tooltip>
                  </div>
                </div>

                <!-- ── 收 / 付（BUY/SELL 固定，货币 chip 点击切换）── -->
                <div class="af-cell af-cell--label af-cell--dir-label">
                  {{ t('te.recvPay') }} <span class="req">*</span>
                </div>
                <div v-for="trade in avgFwdTrades" :key="'dir'+trade.id" class="af-cell af-cell--dir-block">
                  <!-- BUY 行（固定） -->
                  <div class="af-dir-row">
                    <button class="af-dir-tag af-dir-tag--buy">BUY</button>
                    <span class="af-ccy-chip"
                      title="点击切换货币"
                      @click="trade.direction = trade.direction === 'BUY' ? 'SELL' : 'BUY'">
                      {{ trade.direction === 'BUY' ? afCcy1 : afCcy2 }}
                      <el-icon class="af-swap-hint"><Sort /></el-icon>
                    </span>
                    <el-input
                      :model-value="trade.direction === 'BUY' ? trade.buyAmount : trade.sellAmount"
                      @update:model-value="v => { trade.direction === 'BUY' ? (trade.buyAmount = v) : (trade.sellAmount = v); calcAfTradeCosts(trade) }"
                      placeholder="0.00" size="small" class="af-flex-input" />
                  </div>
                  <!-- SELL 行（固定） -->
                  <div class="af-dir-row">
                    <button class="af-dir-tag af-dir-tag--sell">SELL</button>
                    <span class="af-ccy-chip"
                      title="点击切换货币"
                      @click="trade.direction = trade.direction === 'BUY' ? 'SELL' : 'BUY'">
                      {{ trade.direction === 'BUY' ? afCcy2 : afCcy1 }}
                      <el-icon class="af-swap-hint"><Sort /></el-icon>
                    </span>
                    <el-input
                      :model-value="trade.direction === 'BUY' ? trade.sellAmount : trade.buyAmount"
                      @update:model-value="v => { trade.direction === 'BUY' ? (trade.sellAmount = v) : (trade.buyAmount = v); calcAfTradeCosts(trade) }"
                      placeholder="0.00" size="small" class="af-flex-input" />
                  </div>
                </div>

                <!-- ── 即期汇率 ── -->
                <div class="af-cell af-cell--label">{{ t('te.spotRate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'sr'+trade.id" class="af-cell">
                  <el-input v-model="trade.spotRate" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcAfTradeCosts(trade)" />
                </div>

                <!-- ── 升贴水 ── -->
                <div class="af-cell af-cell--label">{{ t('te.premium') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'pm'+trade.id" class="af-cell">
                  <el-input v-model="trade.premium" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcAfTradeCosts(trade)" />
                </div>

                <!-- ── 远期汇率 ── -->
                <div class="af-cell af-cell--label">{{ t('te.fwdRate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'fr'+trade.id" class="af-cell">
                  <el-input v-model="trade.fwdRate" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcAfTradeCosts(trade)" />
                </div>

                <!-- ── 远期点差(BP) ── -->
                <div class="af-cell af-cell--label af-cell--sub">{{ t('te.spreadBP') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'fbp'+trade.id" class="af-cell">
                  <el-input v-model="trade.fwdBP" placeholder="0.00000000" size="small" style="width:100%"
                    :disabled="!afCommon.mirrorAccount" @input="calcAfTradeCosts(trade)" />
                </div>

                <!-- ── 成本远期汇率 ── -->
                <div class="af-cell af-cell--label af-cell--sub">{{ t('te.costFwdRate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'cfr'+trade.id" class="af-cell">
                  <el-input v-model="trade.costFwdRate" :placeholder="t('te.autoFill')" size="small" style="width:100%" />
                </div>

                <!-- ── 分润金额 ── -->
                <div class="af-cell af-cell--label af-cell--sub">{{ t('te.profitSplit') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'ps'+trade.id" class="af-cell af-cell--2col">
                  <el-input v-model="trade.profitSplit" :placeholder="t('te.inputPlaceholder')" size="small" class="af-flex-input"
                    :disabled="!afCommon.mirrorAccount" />
                  <span class="af-profit-ccy">{{ afCcy2 }}</span>
                </div>

                <!-- ── 即期起息日 ── -->
                <div class="af-cell af-cell--label">{{ t('te.spotValueDate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'svd'+trade.id" class="af-cell">
                  <el-date-picker v-model="trade.spotValueDate" type="date" :placeholder="t('te.selectDate')"
                    value-format="YYYY-MM-DD" size="small" style="width:100%" @change="autoTenor(trade)" />
                </div>

                <!-- ── 择期交割日 ── -->
                <div class="af-cell af-cell--label">{{ t('te.optionalDate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'od'+trade.id" class="af-cell">
                  <el-date-picker v-model="trade.optionalDate" type="date" :placeholder="t('te.selectDate')"
                    value-format="YYYY-MM-DD" size="small" style="width:100%" />
                </div>

                <!-- ── 到期日 ── -->
                <div class="af-cell af-cell--label">{{ t('te.maturityDate') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'md'+trade.id" class="af-cell">
                  <el-date-picker v-model="trade.maturityDate" type="date" :placeholder="t('te.selectDate')"
                    value-format="YYYY-MM-DD" size="small" style="width:100%" @change="autoTenor(trade)" />
                </div>

                <!-- ── 期限(天) = 到期日 - 即期起息日（自动计算，也支持手动输入）── -->
                <div class="af-cell af-cell--label af-cell--last">{{ t('te.tenor') }}</div>
                <div v-for="trade in avgFwdTrades" :key="'tnr'+trade.id" class="af-cell af-cell--last">
                  <el-input v-model="trade.tenor" size="small" style="width:100%" :placeholder="t('te.inputPlaceholder')" />
                </div>

              </div><!-- /af-grid -->
            </div><!-- /af-scroll-x -->

            <!-- 公共要素 -->
            <div class="af-common">
              <div class="af-common-hd" @click="afCommonOpen = !afCommonOpen">
                <span>{{ t('te.commonElements') }}</span>
                <el-icon :class="{ 'is-flip': !afCommonOpen }"><ArrowUp /></el-icon>
              </div>
              <div v-show="afCommonOpen" class="af-common-body">
                <div class="af-cm-sections">

                  <!-- ① 交易信息 -->
                  <div class="af-cm-section">
                    <div class="af-cm-section-title">{{ t('te.secTradeInfo') }}</div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.currencyPair')">{{ t('te.currencyPair') }} <span class="req">*</span></div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.currencyPair" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%">
                          <el-option label="USD/CNY" value="USD/CNY" />
                          <el-option label="EUR/CNY" value="EUR/CNY" />
                          <el-option label="EUR/USD" value="EUR/USD" />
                          <el-option label="GBP/USD" value="GBP/USD" />
                          <el-option label="USD/JPY" value="USD/JPY" />
                        </el-select>
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.parSpotRate')">{{ t('te.parSpotRate') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.avgSpotRateInput" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.parPremium')">{{ t('te.parPremium') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.avgPremiumInput" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.parFwdRate')">{{ t('te.parFwdRate') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.avgFwdRateInput" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                    <div class="af-cm-field af-cm-field--last">
                      <div class="af-cm-fl" :title="t('te.tradeDate')">{{ t('te.tradeDate') }} <span class="req">*</span></div>
                      <div class="af-cm-fv" style="gap:6px">
                        <el-date-picker v-model="afCommon.tradeDate" type="date" :placeholder="t('te.selectDate')"
                          value-format="YYYY-MM-DD" size="small" style="flex:1;min-width:0" />
                        <el-time-picker v-model="afCommon.tradeTime" :placeholder="t('te.selectTime')"
                          value-format="HH:mm:ss" size="small" style="width:96px;flex-shrink:0" />
                      </div>
                    </div>
                  </div>

                  <!-- ② 交易账户 -->
                  <div class="af-cm-section">
                    <div class="af-cm-section-title">{{ t('te.secTradeAccount') }}</div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.account')">{{ t('te.account') }} <span class="req">*</span></div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.account" :placeholder="t('te.selectPlaceholder')" size="small" class="af-flex-input" />
                        <el-input :placeholder="t('te.autoFill')" size="small" class="af-flex-input" disabled />
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.counterparty')">{{ t('te.counterparty') }} <span class="req">*</span></div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.counterparty" :placeholder="t('te.selectPlaceholder')" size="small" class="af-flex-input" />
                        <el-input :placeholder="t('te.autoFill')" size="small" class="af-flex-input" disabled />
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.broker')">{{ t('te.broker') }}</div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.broker" :placeholder="t('te.selectPlaceholder')" size="small" class="af-flex-input" />
                        <el-input :placeholder="t('te.autoFill')" size="small" class="af-flex-input" disabled />
                      </div>
                    </div>
                    <div class="af-cm-field af-cm-field--last">
                      <div class="af-cm-fl" :title="t('te.mirrorAccount')">{{ t('te.mirrorAccount') }}</div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.mirrorAccount" :placeholder="t('te.selectPlaceholder')" size="small" class="af-flex-input" />
                        <el-input :placeholder="t('te.autoFill')" size="small" class="af-flex-input" disabled />
                      </div>
                    </div>
                  </div>

                  <!-- ③ 备注信息 -->
                  <div class="af-cm-section">
                    <div class="af-cm-section-title">{{ t('te.secRemarks') }}</div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.tradeNature')">{{ t('te.tradeNature') }} <span class="req">*</span></div>
                      <div class="af-cm-fv">
                        <el-select v-model="afCommon.tradeNature" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%">
                          <el-option :label="t('te.natureInternal')" value="内部交易" />
                          <el-option :label="t('te.natureInterbank')" value="同业交易" />
                          <el-option :label="t('te.natureCustomer')" value="客户交易" />
                        </el-select>
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.externalNo')">{{ t('te.externalNo') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.externalNo" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.tradePurpose')">{{ t('te.tradePurpose') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.purpose" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                    <div class="af-cm-field af-cm-field--last">
                      <div class="af-cm-fl" :title="t('te.remarks')">{{ t('te.remarks') }}</div>
                      <div class="af-cm-fv">
                        <el-input v-model="afCommon.remark" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
                      </div>
                    </div>
                  </div>

                  <!-- ④ 拓展字段 -->
                  <div class="af-cm-section af-cm-section--ext">
                    <div class="af-cm-section-title">{{ t('te.secExtFields') }}</div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.ourSettlePath')">{{ t('te.ourSettlePath') }}</div>
                      <div class="af-cm-fv"><el-select v-model="afCommon.ourSettlePath" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%" /></div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.theirSettlePath')">{{ t('te.theirSettlePath') }}</div>
                      <div class="af-cm-fv"><el-select v-model="afCommon.theirSettlePath" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%" /></div>
                    </div>
                    <div class="af-cm-field">
                      <div class="af-cm-fl" :title="t('te.clearingMethod')">{{ t('te.clearingMethod') }}</div>
                      <div class="af-cm-fv"><el-select v-model="afCommon.clearingMethod" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%" /></div>
                    </div>
                    <div class="af-cm-field af-cm-field--last">
                      <div class="af-cm-fl" :title="t('te.tradeMethod')">{{ t('te.tradeMethod') }}</div>
                      <div class="af-cm-fv"><el-select v-model="afCommon.tradeMethod" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%" /></div>
                    </div>
                  </div>

                </div><!-- /af-cm-sections -->
              </div>
            </div>

          </div><!-- /af-wrap -->
        </template>

        <!-- ══ 现券买卖 表单 ══ -->
        <template v-else-if="selectedProduct === 'bond-buy-sell'">

          <!-- 交易信息 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeInfo') }}</div>

            <!-- 债券代码/简称 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.bondCodeName') }} <span class="req">*</span></div>
              <div class="fs-value" style="gap:6px">
                <el-input v-model="bond.bondCode" :placeholder="t('te.inputPlaceholder')" size="small" style="flex:1;min-width:0" />
                <el-input :model-value="bond.bondName || t('te.autoFill')" disabled size="small" style="width:110px" class="fc--readonly" />
                <el-icon class="row-ic-sm"><Document /></el-icon>
                <el-icon class="row-ic-sm"><EditPen /></el-icon>
              </div>
            </div>

            <!-- 交易方向 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeDirection') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="bond.tradeDirection" size="small" style="width:100%">
                  <el-option :label="t('te.dirBuy')" value="buy" />
                  <el-option :label="t('te.dirSell')" value="sell" />
                </el-select>
              </div>
            </div>

            <!-- 券面总额 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.faceAmount') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-input v-model="bond.faceAmount" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcBondAmounts" />
              </div>
            </div>

            <!-- 交易日 / 结算日 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeDate') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--2">
                <div class="fc">
                  <el-date-picker v-model="bond.tradeDate" type="date" value-format="YYYY-MM-DD" size="small" style="width:100%" />
                </div>
                <div class="fc">
                  <el-time-picker v-model="bond.tradeTime" value-format="HH:mm:ss" size="small" style="width:100%" />
                </div>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.settleDate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-date-picker v-model="bond.settleDate" type="date" value-format="YYYY-MM-DD" size="small" style="width:100%" />
              </div>
            </div>

            <!-- 净价 / BP / 成本净价 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.netPriceLabel') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--rate3">
                <div class="fc">
                  <el-input v-model="bond.netPrice" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcBondAmounts" />
                </div>
                <div class="fc fc--readonly">
                  <span class="rate-bp">{{ bondFmt8(bond.netPriceBP) }} BP</span>
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.costNetPrice || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 净价金额 / 成本净价金额 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.netAmountLabel') }}</div>
              <div class="fs-cols fs-cols--2">
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.netAmount || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.costNetAmount || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 全价 / BP / 成本全价 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.fullPriceLabel') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--rate3">
                <div class="fc">
                  <el-input v-model="bond.fullPrice" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcBondAmounts" />
                </div>
                <div class="fc fc--readonly">
                  <span class="rate-bp">{{ bondFmt8(bond.fullPriceBP) }} BP</span>
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.costFullPrice || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 全价金额 / 成本全价金额 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.fullAmountLabel') }}</div>
              <div class="fs-cols fs-cols--2">
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.fullAmount || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.costFullAmount || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 应计利息 / 利息总额 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.accruedInterestLabel') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--2">
                <div class="fc fc--readonly">
                  <el-input :model-value="bondFmt8(bond.accruedInterest)" disabled size="small" style="width:100%" />
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.interestTotal || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 收益率 / BP / 成本收益率 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.yieldLabel') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--rate3">
                <div class="fc">
                  <el-input v-model="bond.yield_" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" @input="calcBondAmounts" />
                </div>
                <div class="fc fc--readonly">
                  <span class="rate-bp">{{ bondFmt8(bond.yieldBP) }} BP</span>
                </div>
                <div class="fc fc--readonly">
                  <el-input :model-value="bond.costYield || t('te.autoFill')" disabled size="small" style="width:100%" />
                </div>
              </div>
            </div>

            <!-- 分润金额 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.profitSplit') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-input :model-value="bondFmt8(bond.profitSplit)" disabled size="small" style="width:100%" class="fc--readonly" />
              </div>
            </div>

            <!-- 交割方式 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.deliveryMethod') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="bond.deliveryType" size="small" style="width:100%">
                  <el-option label="DVP" value="DVP" />
                  <el-option label="FOP" value="FOP" />
                </el-select>
              </div>
            </div>

            <!-- 托管机构 -->
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.custodian') }}</div>
              <div class="fs-value">
                <el-input v-model="bond.custodian" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
              </div>
            </div>
          </div>

          <!-- 交易账户 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeAccount') }}</div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.account') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--acct">
                <div class="fc"><el-input v-model="bond.account" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
                <div class="fc fc--readonly"><el-input :model-value="bond.accountName || t('te.autoFill')" disabled size="small" style="width:100%" /></div>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.counterparty') }} <span class="req">*</span></div>
              <div class="fs-cols fs-cols--acct">
                <div class="fc"><el-input v-model="bond.counterparty" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
                <div class="fc fc--readonly"><el-input :model-value="bond.counterpartyName || t('te.autoFill')" disabled size="small" style="width:100%" /></div>
              </div>
            </div>
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.mirrorAccount') }}</div>
              <div class="fs-cols fs-cols--acct">
                <div class="fc"><el-input v-model="bond.backToBack" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
                <div class="fc fc--readonly"><el-input :model-value="t('te.autoFill')" disabled size="small" style="width:100%" /></div>
              </div>
            </div>
          </div>

          <!-- 备注 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secRemarks') }}</div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeNature') }}</div>
              <div class="fs-value">
                <el-select v-model="bond.tradeNature" size="small" style="width:100%">
                  <el-option :label="t('te.natureInterbank')" value="interbank" />
                  <el-option :label="t('te.natureProprietary')" value="proprietary" />
                  <el-option :label="t('te.natureAgency')" value="agency" />
                </el-select>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.externalNo') }}</div>
              <div class="fs-cols fs-cols--2">
                <div class="fc"><el-input v-model="bond.externalSerial" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" /></div>
                <div class="fc">
                  <el-select v-model="bond.externalSystem" size="small" style="width:100%">
                    <el-option label="RCS" value="RCS" />
                    <el-option label="EXT" value="EXT" />
                  </el-select>
                </div>
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradePurpose') }}</div>
              <div class="fs-value">
                <el-input v-model="bond.tradePurpose" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" />
              </div>
            </div>
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.remarks') }}</div>
              <div class="fs-value">
                <el-input v-model="bond.memo" type="textarea" :rows="2" :maxlength="200"
                  show-word-limit resize="none" :placeholder="t('te.memoPlaceholder')" size="small" style="width:100%" />
              </div>
            </div>
          </div>

          <!-- 拓展字段 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secExtFields') }}</div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ourPaySettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="bond.ourSettlePath" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" clearable />
              </div>
            </div>
            <div class="fs-row">
              <div class="fs-label">{{ t('te.counterRecvSettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="bond.counterSettlePath" :placeholder="t('te.inputPlaceholder')" size="small" style="width:100%" clearable />
              </div>
            </div>
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.clearingMethod') }}</div>
              <div class="fs-value">
                <el-select v-model="bond.clearingType" :placeholder="t('te.selectPlaceholder')" size="small" style="width:100%" clearable>
                  <el-option label="DVP" value="DVP" />
                  <el-option label="FOP" value="FOP" />
                </el-select>
              </div>
            </div>
          </div>

        </template>

        <!-- ══ 同业拆借 表单 ══ -->
        <template v-else-if="selectedProduct === 'interbank'">

          <!-- ① 交易信息 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeInfo') }}</div>

            <!-- 货币 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibCurrency') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="ib.currency" size="small" style="width:100%">
                  <el-option v-for="c in CCY_LIST" :key="c" :label="c" :value="c" />
                </el-select>
              </div>
            </div>

            <!-- 交易方向 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeDirection') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="ib.direction" size="small" style="width:100%">
                  <el-option :label="t('te.ibDirLoan')"    value="loan" />
                  <el-option :label="t('te.ibDirDeposit')" value="deposit" />
                </el-select>
              </div>
            </div>

            <!-- 计息方式 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibInterestType') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="ib.interestType" size="small" style="width:100%">
                  <el-option :label="t('te.ibInterestTypeStandard')" value="standard" />
                  <el-option :label="t('te.ibInterestTypeDiscount')" value="discount" />
                </el-select>
              </div>
            </div>

            <!-- 期初本金/期末本金：始终同行，贴现模式下期初本金自动反算 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibPrincipal') }} <span class="req">*</span></div>
              <div class="fs-value" style="gap:6px">
                <div style="display:flex; gap:6px; width:100%">
                  <!-- 期初本金：标准模式可编辑，贴现模式自动反算 -->
                  <el-input
                    v-if="ib.interestType === 'standard'"
                    v-model="ib.openPrincipal"
                    size="small" :placeholder="t('te.inputPlaceholder')" style="flex:1"
                  />
                  <el-input
                    v-else
                    v-model="ib.openPrincipal"
                    :placeholder="t('te.inputPlaceholder')"
                    size="small" style="flex:1"
                  />
                  <!-- 期末本金：始终可编辑 -->
                  <el-input v-model="ib.closePrincipal" size="small" :placeholder="t('te.inputPlaceholder')" style="flex:1" />
                </div>
              </div>
            </div>

            <!-- 业务品种 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.extBusinessType') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.businessType" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')">
                  <el-option label="同业拆借" value="iblending" />
                  <el-option label="同业存款" value="ibdeposit" />
                </el-select>
              </div>
            </div>

            <!-- 交易日 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeDate') }} <span class="req">*</span></div>
              <div class="fs-value" style="gap:6px">
                <el-date-picker v-model="ib.tradeDate" type="date" value-format="YYYY-MM-DD"
                  size="small" style="flex:1" :placeholder="t('te.selectDate')" />
                <el-time-picker v-model="ib.tradeTime" format="HH:mm:ss" value-format="HH:mm:ss"
                  size="small" style="width:120px" :placeholder="t('te.selectTime')" />
              </div>
            </div>

            <!-- 起息日 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibValueDate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-date-picker v-model="ib.valueDate" type="date" value-format="YYYY-MM-DD"
                  size="small" style="width:100%" :placeholder="t('te.selectDate')" @change="calcIbTenor" />
              </div>
            </div>

            <!-- 到期日 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.maturityDate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-date-picker v-model="ib.maturityDate" type="date" value-format="YYYY-MM-DD"
                  size="small" style="width:100%" :placeholder="t('te.selectDate')" @change="calcIbTenor" />
              </div>
            </div>

            <!-- 期限(天) -->
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.tenor') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-input :model-value="ib.tenorDays" disabled size="small"
                  style="width:100%" :placeholder="t('te.autoFill')" class="fc--readonly" />
              </div>
            </div>
          </div>

          <!-- ② 交易账户 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secTradeAccount') }}</div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeAccount') }} <span class="req">*</span></div>
              <div class="fs-value" style="gap:6px">
                <el-input v-model="ib.account" size="small" :placeholder="t('te.inputPlaceholder')" style="flex:1" />
                <el-input :model-value="t('te.autoFill')" disabled size="small" style="width:110px" class="fc--readonly" />
              </div>
            </div>

            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.counterparty') }} <span class="req">*</span></div>
              <div class="fs-value" style="gap:6px">
                <el-input v-model="ib.counterparty" size="small" :placeholder="t('te.inputPlaceholder')" style="flex:1" />
                <el-input :model-value="t('te.autoFill')" disabled size="small" style="width:110px" class="fc--readonly" />
              </div>
            </div>
          </div>

          <!-- ③ Interest Methods -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.ibSecInterestMethods') }}</div>

            <!-- 利率 / 贴现率 -->
            <div class="fs-row">
              <div class="fs-label">{{ ib.interestType === 'discount' ? t('te.ibDiscountRate') : t('te.ibInterestRate') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-input v-model="ib.interestRate" size="small" :placeholder="t('te.inputPlaceholder')" style="width:100%" />
              </div>
            </div>

            <!-- 计息基础 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibDayCount') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="ib.dayCount" size="small" style="width:100%">
                  <el-option label="ACT/360" value="ACT/360" />
                  <el-option label="ACT/365" value="ACT/365" />
                  <el-option label="30/360"  value="30/360"  />
                  <el-option label="ACT/ACT" value="ACT/ACT" />
                </el-select>
              </div>
            </div>

            <!-- 支付惯例 -->
            <div class="fs-row">
              <div class="fs-label">{{ t('te.ibPayConvention') }} <span class="req">*</span></div>
              <div class="fs-value">
                <el-select v-model="ib.payConvention" size="small" style="width:100%">
                  <el-option label="Modified Following" value="Modified Following" />
                  <el-option label="Following"          value="Following"          />
                  <el-option label="Preceding"          value="Preceding"          />
                  <el-option label="Unadjusted"         value="Unadjusted"         />
                </el-select>
              </div>
            </div>

            <!-- 节假日 -->
            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.ibHolidayCalendar') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.holidayCalendar" multiple size="small" style="width:100%">
                  <el-option v-for="c in CCY_LIST" :key="c" :label="c" :value="c" />
                </el-select>
              </div>
            </div>
          </div>

          <!-- ④ 备注 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secRemarks') }}</div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeNature') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.tradeNature" size="small" style="width:100%">
                  <el-option :label="t('te.natureInterbank')"   value="interbank" />
                  <el-option :label="t('te.natureProprietary')" value="proprietary" />
                </el-select>
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.externalNo') }}</div>
              <div class="fs-value" style="gap:6px">
                <el-input v-model="ib.externalNo" size="small" :placeholder="t('te.inputPlaceholder')" style="flex:1" />
                <el-select v-model="ib.externalSystem" size="small" style="width:80px">
                  <el-option label="RCS" value="RCS" />
                  <el-option label="Bloomberg" value="Bloomberg" />
                </el-select>
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradePurpose') }}</div>
              <div class="fs-value">
                <el-input v-model="ib.tradePurpose" size="small" :placeholder="t('te.inputPlaceholder')" style="width:100%" />
              </div>
            </div>

            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.remarks') }}</div>
              <div class="fs-value">
                <el-input v-model="ib.memo" size="small" :placeholder="t('te.memoPlaceholder')" style="width:100%" />
              </div>
            </div>
          </div>

          <!-- ⑤ 拓展字段 -->
          <div class="fs-card">
            <div class="fs-title"><span class="fs-bar"></span>{{ t('te.secExtFields') }}</div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.ourRecvSettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.ourRecvSettlePath" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')" />
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.counterPaySettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.counterPaySettlePath" size="small" style="width:100%" clearable />
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.ourPaySettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.ourPaySettlePath" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')" />
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.counterRecvSettlePath') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.counterRecvSettlePath" size="small" style="width:100%" clearable />
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.clearingMethod') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.clearingType" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')">
                  <el-option label="DVP" value="DVP" />
                  <el-option label="FOP" value="FOP" />
                </el-select>
              </div>
            </div>

            <div class="fs-row">
              <div class="fs-label">{{ t('te.tradeMethod') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.tradeMethod" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')" />
              </div>
            </div>

            <div class="fs-row fs-row--last">
              <div class="fs-label">{{ t('te.tradeVenue') }}</div>
              <div class="fs-value">
                <el-select v-model="ib.tradeVenue" size="small" style="width:100%" clearable :placeholder="t('te.inputPlaceholder')" />
              </div>
            </div>
          </div>

        </template>

        <!-- ══ 其他产品占位 ══ -->
        <template v-else>
          <div class="placeholder-tip">
            <el-icon style="font-size:32px;color:#c0c4cc"><Document /></el-icon>
            <span>{{ t('te.selectProductHint') }}</span>
          </div>
        </template>

      </div>

      <!-- 底部按钮 -->
      <div class="form-footer">
        <template v-if="selectedProduct === 'fx-avg-forward'">
          <el-button class="btn-clear" @click="handleAvgFwdClear">
            <el-icon><Delete /></el-icon>{{ t('te.btnClearAll') }}
          </el-button>
          <el-button type="primary" class="btn-submit" @click="handleAvgFwdSubmit">
            {{ t('te.btnSubmitCombo', { n: avgFwdTrades.length }) }}
          </el-button>
        </template>
        <template v-else>
          <el-button class="btn-clear" @click="handleClear">
            <el-icon><Delete /></el-icon>{{ t('te.btnClearAll') }}
          </el-button>
          <el-button type="primary" class="btn-submit" @click="handleSubmit">{{ t('te.btnSubmit') }}</el-button>
        </template>
      </div>
    </div>

    <!-- ③ 右侧分析面板（组合交易时隐藏） -->
    <div class="analysis-panel" v-show="selectedProduct !== 'fx-avg-forward'">

      <!-- 遍历各分析面板 -->
      <div
        v-for="item in analysisItems"
        :key="item.key"
        class="ap-card"
        :class="{ 'ap-card--open': expandedPanels[item.key] }"
      >
        <!-- 面板 Header -->
        <div class="ap-hd" @click="togglePanel(item.key)">
          <span class="ap-hd-left">
            <el-icon class="ap-icon"><component :is="item.icon" /></el-icon>
            <span class="ap-label">{{ item.label }}</span>
            <el-icon class="ap-chevron" :class="{ open: expandedPanels[item.key] }"><ArrowRight /></el-icon>
          </span>
          <el-icon class="ap-refresh" @click.stop="handleRefreshAnalysis(item.key)"><RefreshRight /></el-icon>
        </div>

        <!-- 现金流预览内容：仅在 bond-buy-sell 时有实质内容 -->
        <div v-if="expandedPanels[item.key] && item.key === 'cashflow'" class="ap-body">

          <!-- 工具栏 -->
          <div class="cf-toolbar">
            <el-checkbox v-model="cfShowHistory" size="small">{{ t('te.showHistory') }}</el-checkbox>
            <el-button size="small" type="primary" plain :disabled="cfIsAdding" @click="handleCfAdd">{{ t('te.btnAdd') }}</el-button>
          </div>

          <!-- 现金流表格 -->
          <el-table
            :data="cfAllRows"
            size="small"
            class="cf-table"
            :header-cell-style="{ background: '#f8f9fc', color: '#576080', fontSize: '11px', padding: '6px 0' }"
            :cell-style="{ fontSize: '11px', padding: '4px 0' }"
          >
            <el-table-column :label="t('te.colSeq')" type="index" width="42" align="center" />

            <!-- 支付日期 -->
            <el-table-column :label="t('te.colPayDate')" width="104">
              <template #default="{ row }">
                <el-date-picker v-if="row.isEditing" v-model="cfNewRow.payDate"
                  type="date" value-format="YYYY-MM-DD" size="small" style="width:100%" />
                <span v-else>{{ row.payDate }}</span>
              </template>
            </el-table-column>

            <!-- 支付方向 -->
            <el-table-column :label="t('te.colDirection')" width="76" align="center">
              <template #default="{ row }">
                <el-select v-if="row.isEditing" v-model="cfNewRow.direction" size="small" style="width:62px">
                  <el-option label="Pay" value="Pay" />
                  <el-option label="Rec" value="Rec" />
                </el-select>
                <span v-else class="cf-dir-tag" :class="row.direction === 'Pay' ? 'cf-pay' : 'cf-receive'">
                  {{ row.direction === 'Pay' ? 'Pay' : 'Rec' }}
                </span>
              </template>
            </el-table-column>

            <!-- 本金 -->
            <el-table-column :label="t('te.colPrincipal')" align="right" min-width="88">
              <template #default="{ row }">
                <el-input v-if="row.isEditing" v-model="cfNewRow.principal"
                  size="small" style="width:100%" placeholder="0.00" />
                <span v-else class="cf-num">{{ row.principalFmt }}</span>
              </template>
            </el-table-column>

            <!-- 金额 -->
            <el-table-column :label="t('te.colAmount')" align="right" min-width="90">
              <template #default="{ row }">
                <el-input v-if="row.isEditing" v-model="cfNewRow.amount"
                  size="small" style="width:100%" placeholder="0.00" />
                <span v-else :class="row.amount < 0 ? 'cf-neg' : 'cf-pos'">{{ row.amountFmt }}</span>
              </template>
            </el-table-column>

            <!-- 货币 -->
            <el-table-column :label="t('te.colCurrency')" prop="currency" width="52" align="center" />

            <!-- 开始日期 -->
            <el-table-column :label="t('te.colStartDate')" width="104">
              <template #default="{ row }">
                <el-date-picker v-if="row.isEditing" v-model="cfNewRow.startDate"
                  type="date" value-format="YYYY-MM-DD" size="small" style="width:100%" />
                <span v-else>{{ row.startDate }}</span>
              </template>
            </el-table-column>

            <!-- 结束日期 -->
            <el-table-column :label="t('te.colEndDate')" width="104">
              <template #default="{ row }">
                <el-date-picker v-if="row.isEditing" v-model="cfNewRow.endDate"
                  type="date" value-format="YYYY-MM-DD" size="small" style="width:100%" />
                <span v-else>{{ row.endDate }}</span>
              </template>
            </el-table-column>

            <!-- 天数(D) -->
            <el-table-column :label="t('te.colDays')" width="62" align="center">
              <template #default="{ row }">
                <span class="cf-num">{{ row.days }}</span>
              </template>
            </el-table-column>

            <!-- 类型 -->
            <el-table-column :label="t('te.colType')" width="76" align="center">
              <template #default="{ row }">
                <el-select v-if="row.isEditing" v-model="cfNewRow.type" size="small" style="width:68px">
                  <el-option :label="t('te.cfPrincipal')" value="本金" />
                  <el-option :label="t('te.cfInterest')" value="利息" />
                  <el-option :label="t('te.cfTax')" value="税费" />
                </el-select>
                <span v-else class="cf-type-tag" :class="`cf-type--${row.type}`">{{ cfTypeLabel(row.type) }}</span>
              </template>
            </el-table-column>

            <!-- 状态 -->
            <el-table-column :label="t('te.colStatus')" width="54" align="center">
              <template #default="{ row }">
                <span class="cf-status">{{ cfStatusLabel(row.status) }}</span>
              </template>
            </el-table-column>

            <!-- 我方结算路径 -->
            <el-table-column :label="t('te.colOurSettlePath')" min-width="90">
              <template #default="{ row }">
                <el-select v-if="row.isEditing" v-model="cfNewRow.settlePath" size="small" style="width:100%" clearable :placeholder="t('te.selectPlaceholder')" />
                <span v-else class="cf-path">{{ row.settlePath || '—' }}</span>
              </template>
            </el-table-column>

            <!-- 对方结算路径 -->
            <el-table-column :label="t('te.colTheirSettlePath')" min-width="90">
              <template #default="{ row }">
                <el-select v-if="row.isEditing" v-model="cfNewRow.counterSettlePath" size="small" style="width:100%" clearable :placeholder="t('te.selectPlaceholder')" />
                <span v-else class="cf-path">{{ row.counterSettlePath || '—' }}</span>
              </template>
            </el-table-column>

            <!-- 操作列 -->
            <el-table-column :label="t('te.colActions')" width="122" align="center" fixed="right">
              <template #default="{ row, $index }">
                <template v-if="row.isEditing">
                  <el-button link type="primary" size="small" @click="handleCfSave">{{ t('te.btnSave') }}</el-button>
                  <el-button link size="small" style="color:#909399" @click="handleCfCancel">{{ t('te.btnCancel') }}</el-button>
                </template>
                <template v-else>
                  <el-button link type="danger" size="small" @click="handleCfDelete(row, $index)">{{ t('te.btnDelete') }}</el-button>
                  <el-button link type="primary" size="small">{{ t('te.btnEdit') }}</el-button>
                  <el-button link type="primary" size="small">{{ t('te.btnDetail') }}</el-button>
                </template>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="cf-pagination">
            <span class="cf-total">{{ t('te.totalCount', { n: cfAllRows.length }) }}</span>
            <el-pagination
              small
              layout="prev, pager, next"
              :total="cfAllRows.length"
              :page-size="cfPageSize"
              :current-page="1"
              hide-on-single-page
            />
            <el-select v-model="cfPageSize" size="small" style="width:76px;flex-shrink:0">
              <el-option :label="t('te.perPage20')" :value="20" />
              <el-option :label="t('te.perPage50')" :value="50" />
            </el-select>
            <span class="cf-goto">
              <span>{{ t('te.goTo') }}</span>
              <el-input size="small" style="width:36px" model-value="1" />
              <span>{{ t('te.page') }}</span>
            </span>
          </div>
        </div>

        <!-- 其他面板占位内容 -->
        <div v-else-if="expandedPanels[item.key]" class="ap-body ap-body--empty">
          <span>{{ t('te.noData') }}</span>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { ElMessage } from 'element-plus'
import {
  Grid, Star, RefreshRight, CopyDocument, View, Lock,
  Document, Bell, Lightning, Delete, ArrowRight, Search,
  Clock, Sort, DataAnalysis, Warning, ArrowUp, EditPen
} from '@element-plus/icons-vue'

const { t } = useI18n()

// ─── 左侧产品树 ───────────────────────────────────────────────────────────────
const searchText     = ref('')
const selectedProduct     = ref('fx-forward')
const selectedProductKey  = ref('fx-forward')  // alias kept for computed
const currentProductLabel = ref('FX Forward')

const productGroups = [
  {
    label: 'FX Market',
    color: '#409eff',
    items: [
      { key: 'fx-spot',    label: 'FX Spot' },
      { key: 'fx-forward',     label: 'FX Forward' },
      { key: 'fx-avg-forward', label: 'FX Par Forward' },
      { key: 'fx-swap',        label: 'FX Swap' },
      {
        key: 'fx-option-group', label: 'FX Option',
        children: [
          { key: 'fx-opt-eu', label: 'European Option' },
          { key: 'fx-opt-us', label: 'American Option' },
          { key: 'fx-opt-barrier', label: 'Barrier Option' },
        ]
      },
      { key: 'ndf', label: 'NDF' },
      { key: 'ccs', label: 'Cross-Currency Swap' },
    ]
  },
  {
    label: 'Money Market',
    color: '#b8860b',
    items: [
      { key: 'interbank',        label: 'Interbank Lending' },
      { key: 'mm-deposit',       label: 'MM Deposit' },
      { key: 'outright-repo',    label: 'Outright Repo' },
      { key: 'pledge-repo',      label: 'Pledge Repo' },
      { key: 'bond-lending',     label: 'Bond Lending' },
      { key: 'multi-interbank',  label: 'Multi-Period Lending' },
    ]
  },
  {
    label: 'Bond Market',
    color: '#e6a23c',
    items: [
      { key: 'bond-buy-sell', label: 'Bond Buy/Sell' },
      { key: 'bond-issue',    label: 'Bond Issuance' },
    ]
  },
  {
    label: 'Fees',
    color: '#67c23a',
    items: [
      { key: 'fee-cashflow',  label: 'Single-Leg Cashflow' },
      { key: 'fee-asset-cf',  label: 'Asset Mgmt Cashflow' },
    ]
  },
  {
    label: 'Interest Rate',
    color: '#00bcd4',
    items: [
      { key: 'irs',       label: 'IRS' },
      { key: 'irs-opt',   label: 'IRS Option' },
      { key: 'cap-floor', label: 'Cap/Floor' },
    ]
  },
  {
    label: 'Commodities',
    color: '#e6a23c',
    items: [{ key: 'precious-metal', label: 'Precious Metal Lending' }]
  },
  {
    label: 'Credit',
    color: '#9c27b0',
    items: [{ key: 'cds', label: 'CDS' }]
  },
  {
    label: 'Combo Trade',
    color: '#607d8b',
    items: [{ key: 'combo', label: 'Combo Trade' }]
  },
  {
    label: 'Fund Business',
    color: '#ff7043',
    items: [{ key: 'fund', label: 'Fund Subscription/Redemption' }]
  },
]

const groupExpanded = reactive(
  Object.fromEntries(productGroups.map(g => [g.label, g.label === 'FX Market']))
)
const subExpanded = reactive({})

const filteredGroups = computed(() => {
  const q = searchText.value.trim()
  if (!q) return productGroups
  return productGroups
    .map(g => ({
      ...g,
      items: g.items.filter(i =>
        i.label.includes(q) ||
        (i.children && i.children.some(c => c.label.includes(q)))
      )
    }))
    .filter(g => g.items.length > 0)
})

function toggleGroup(label)   { groupExpanded[label] = !groupExpanded[label] }
function toggleSubGroup(key)  { subExpanded[key] = !subExpanded[key] }
function selectProduct(key) {
  selectedProduct.value = key
  currentProductLabel.value = productGroups.flatMap(g => [
    ...g.items.filter(i => !i.children).map(i => ({ key: i.key, label: i.label })),
    ...g.items.filter(i => i.children).flatMap(i => i.children),
  ]).find(i => i.key === key)?.label ?? key
}

// ─── 当前时间 ────────────────────────────────────────────────────────────────
function p2(n) { return String(n).padStart(2, '0') }
const d0      = new Date()
const today   = `${d0.getFullYear()}-${p2(d0.getMonth()+1)}-${p2(d0.getDate())}`
const nowTime = `${p2(d0.getHours())}:${p2(d0.getMinutes())}:${p2(d0.getSeconds())}`

// ─── 外汇远期表单 ─────────────────────────────────────────────────────────────
function emptyFxFwd() {
  return {
    currencyPair:     '',
    premium:          '0.00000000',
    premiumCost:      '0.00000000',
    buyAmount:        '',
    sellAmount:       '',
    spotRate:         '',
    spotBP:           '0.00000000',
    fwdRate:          '',
    fwdBP:            '0.00000000',
    profitSplit:      '0.00000000',
    profitSplitType:  '',
    tradeDate:        today,
    tradeTime:        nowTime,
    spotValueDate:    '',
    optionalDate:     '',
    maturityDate:     '',
    tenor:            '',
    account:          '',
    counterparty:     '',
    broker:           '',
    mirrorAccount:    '',
    tradeNature:      'interbank',
    externalNo:       '',
    externalSystem:   'RCS',
    purpose:          '',
    remark:           '',
    extField1:        '',
    extField2:        '',
    extField3:        '',
    profitCcy:        'CNY',
  }
}

// ─── 货币列表 ─────────────────────────────────────────────────────────────────
const CCY_LIST = ['CNY', 'USD', 'EUR', 'GBP', 'JPY', 'AUD', 'HKD']

// ─── fxFwd 必须先于 computed / watch 声明 ────────────────────────────────────
const fxFwd = reactive(emptyFxFwd())

// ─── 成本汇率：即期汇率 + 点差（BP 换算：1 BP = 0.0001）─────────────────────
const spotCostRate = computed(() => {
  const r = parseFloat(fxFwd.spotRate)
  const bp = parseFloat(fxFwd.spotBP)
  if (isNaN(r)) return ''
  const cost = r + (isNaN(bp) ? 0 : bp * 0.0001)
  return cost.toFixed(6)
})

const fwdCostRate = computed(() => {
  const r = parseFloat(fxFwd.fwdRate)
  const bp = parseFloat(fxFwd.fwdBP)
  if (isNaN(r)) return ''
  const cost = r + (isNaN(bp) ? 0 : bp * 0.0001)
  return cost.toFixed(6)
})

// 货币对变更时自动同步分润货币（取计价货币：USD/CNY → CNY）
watch(() => fxFwd.currencyPair, (val) => {
  if (val && val.includes('/')) {
    fxFwd.profitCcy = val.split('/')[1]
  }
})

// ─── 交易账户行定义 ───────────────────────────────────────────────────────────
const accountRows = computed(() => [
  { key: 'account',       label: t('te.tradeAccount'),    req: true },
  { key: 'counterparty',  label: t('te.counterparty'),    req: true },
  { key: 'broker',        label: t('te.broker'),          req: false },
  { key: 'mirrorAccount', label: t('te.mirrorAccount'),   req: false },
])

// ─── 拓展字段行定义 ───────────────────────────────────────────────────────────
const extFields = computed(() => [
  { key: 'extField1', label: t('te.extBusinessType') },
  { key: 'extField2', label: t('te.extClientType') },
  { key: 'extField3', label: t('te.extTradeChannel') },
])

function calcTenorFwd() {
  if (fxFwd.spotValueDate && fxFwd.maturityDate) {
    const d1   = new Date(fxFwd.spotValueDate)
    const d2   = new Date(fxFwd.maturityDate)
    const diff = Math.round((d2 - d1) / 86400000)
    fxFwd.tenor = diff >= 0 ? String(diff) : ''
  } else {
    fxFwd.tenor = ''
  }
}

function handleClear() {
  if (selectedProduct.value === 'bond-buy-sell') {
    Object.assign(bond, emptyBond())
    calcBondAmounts()
    cfManualRows.value = []
    cfIsAdding.value   = false
  } else if (selectedProduct.value === 'interbank') {
    Object.assign(ib, emptyIb())
  } else {
    Object.assign(fxFwd, emptyFxFwd())
  }
}
function handleSubmit() { ElMessage.success(t('te.msgSubmitted')) }

// ─── 现券买卖表单 ─────────────────────────────────────────────────────────────
function emptyBond() {
  return {
    // 基本标识
    bondCode: '019009.SH', bondName: '10Y Treasury 09',
    tradeDirection: 'buy',
    faceAmount: '1000000',
    tradeDate: today, tradeTime: nowTime,
    settleDate: today,
    // net price
    netPrice: '100.00000000', netPriceBP: 0,
    netAmount: '', costNetPrice: '', costNetAmount: '',
    // full price
    fullPrice: '100.48222222', fullPriceBP: 0,
    fullAmount: '', costFullPrice: '', costFullAmount: '',
    // interest & yield
    accruedInterest: 0, interestTotal: '',
    yield_: '4.49906602', yieldBP: 0, costYield: '',
    // profit
    profitSplit: 0,
    // delivery
    deliveryType: 'DVP', custodian: 'CCDC',
    // account
    account: 'HOBJFBRZ_I001', accountName: 'Subordinated Bond Fund',
    counterparty: 'COFCO-BEI', counterpartyName: 'COFCO Group Co., Ltd.',
    backToBack: '',
    // 备注
    tradeNature: 'interbank', externalSerial: '', externalSystem: 'RCS',
    tradePurpose: '', memo: '',
    // 拓展
    ourSettlePath: '', counterSettlePath: '', clearingType: '',
  }
}

const bond = reactive(emptyBond())

// ─── 同业拆借 / Money Market ──────────────────────────────────────────────────
function emptyIb() {
  const now = new Date()
  const today = now.toISOString().slice(0, 10)
  const nowTime = now.toTimeString().slice(0, 8)
  return {
    currency:      'USD',
    direction:     'loan',
    interestType:  'standard',
    openPrincipal: '',
    closePrincipal:'',
    businessType:  '',
    tradeDate:     today,
    tradeTime:     nowTime,
    valueDate:     '',
    maturityDate:  '',
    tenorDays:     '',
    interestRate:  '',
    dayCount:      'ACT/360',
    payConvention: 'Modified Following',
    holidayCalendar: ['USD'],
    account:       '',
    counterparty:  '',
    tradeNature:   'interbank',
    externalNo:    '',
    externalSystem:'RCS',
    tradePurpose:  '',
    memo:          '',
    // 拓展字段
    ourRecvSettlePath:     '',
    counterPaySettlePath:  '',
    ourPaySettlePath:      '',
    counterRecvSettlePath: '',
    clearingType:  '',
    tradeMethod:   '',
    tradeVenue:    '',
  }
}

const ib = reactive(emptyIb())

function calcIbTenor() {
  if (ib.valueDate && ib.maturityDate) {
    const d1 = new Date(ib.valueDate)
    const d2 = new Date(ib.maturityDate)
    const diff = Math.round((d2 - d1) / 86400000)
    ib.tenorDays = diff >= 0 ? String(diff) : ''
  } else {
    ib.tenorDays = ''
  }
}

// 贴现模式：期初本金（实付）= 面值 / (1 + 利率 × 天数 / 计息基础)
const ibDiscountBasis = computed(() => {
  if (ib.dayCount === 'ACT/365') return 365
  return 360  // ACT/360 / 30/360 / ACT/ACT 统一用360作简化
})

const ibOpenPrincipalCalc = computed(() => {
  if (ib.interestType !== 'discount') return ''
  const face = parseFloat(String(ib.closePrincipal).replace(/,/g, ''))
  const rate = parseFloat(ib.interestRate) / 100
  const days = parseFloat(ib.tenorDays)
  if (!face || isNaN(rate) || isNaN(days) || days <= 0) return ''
  const result = face / (1 + rate * days / ibDiscountBasis.value)
  return result.toFixed(2)
})

const bondFmt8 = v => Number(v || 0).toFixed(8)

// 格式化为千分位两位小数
function fmtAmt2(v) {
  const n = parseFloat(String(v).replace(/,/g, '')) || 0
  return n.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function calcBondAmounts() {
  const face    = parseFloat(String(bond.faceAmount).replace(/,/g, ''))   || 0
  const net     = parseFloat(bond.netPrice)    || 0
  const full    = parseFloat(bond.fullPrice)   || 0
  const netBP   = parseFloat(bond.netPriceBP)  || 0
  const fullBP  = parseFloat(bond.fullPriceBP) || 0
  const yld     = parseFloat(bond.yield_)      || 0
  const yldBP   = parseFloat(bond.yieldBP)     || 0

  // 净价金额 / 全价金额
  bond.netAmount  = face && net  ? fmtAmt2(face * net  / 100) : ''
  bond.fullAmount = face && full ? fmtAmt2(face * full / 100) : ''

  // 应计利息 = 全价 - 净价（每百面值）
  bond.accruedInterest = full && net ? parseFloat((full - net).toFixed(8)) : 0

  // 利息总额 = 券面总额 × 应计利息 / 100
  bond.interestTotal = face && bond.accruedInterest
    ? fmtAmt2(face * bond.accruedInterest / 100)
    : ''

  // 成本净价 / 成本全价（加点差换算：1 BP = 0.0001）
  bond.costNetPrice  = net  ? parseFloat((net  + netBP  * 0.0001).toFixed(8)).toString() : ''
  bond.costFullPrice = full ? parseFloat((full + fullBP * 0.0001).toFixed(8)).toString() : ''

  // 成本净价金额 / 成本全价金额
  const costNet  = parseFloat(bond.costNetPrice)  || 0
  const costFull = parseFloat(bond.costFullPrice) || 0
  bond.costNetAmount  = face && costNet  ? fmtAmt2(face * costNet  / 100) : ''
  bond.costFullAmount = face && costFull ? fmtAmt2(face * costFull / 100) : ''

  // 成本收益率 = 收益率 + 点差（BP）
  bond.costYield = yld ? parseFloat((yld + yldBP * 0.0001).toFixed(8)).toString() : ''
}

// 初始化时触发一次计算（让 mock 数据的导出字段也有值）
calcBondAmounts()

// ─── 右侧分析面板 ─────────────────────────────────────────────────────────────
const analysisItems = computed(() => [
  { key: 'valuation',   label: t('te.analysisValuation'),    icon: DataAnalysis },
  { key: 'cashflow',    label: t('te.analysisCashflow'),     icon: Sort },
  { key: 'op-risk',     label: t('te.analysisOpRisk'),      icon: EditPen },
  { key: 'credit-risk', label: t('te.analysisCreditRisk'),  icon: Warning },
  { key: 'market-risk', label: t('te.analysisMarketRisk'),  icon: Lock },
])

const expandedPanels = reactive({
  valuation: false, cashflow: false,
  'op-risk': false, 'credit-risk': false, 'market-risk': false,
})

function togglePanel(key) { expandedPanels[key] = !expandedPanels[key] }

function handleRefreshAnalysis(key) { ElMessage.info(t('te.msgRefreshing', { key })) }

// 现金流预览
const cfShowHistory = ref(false)

// 天数计算辅助
function cfDays(start, end) {
  if (!start || !end) return ''
  const diff = Math.round((new Date(end) - new Date(start)) / 86400000)
  return diff >= 0 ? diff : ''
}

const bondCashflows = computed(() => {
  if (selectedProduct.value !== 'bond-buy-sell') return []
  const isBuy  = bond.tradeDirection === 'buy'
  const dir    = isBuy ? 'Pay' : 'Rec'
  const sign   = isBuy ? -1 : 1
  const fmtAmt = v => {
    const n = Number(v) || 0
    return (sign * n).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  }
  const fmtNum = v => Number(v || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })

  const rows       = []
  const settleDate = bond.settleDate || bond.tradeDate || ''
  const tradeDate  = bond.tradeDate  || ''
  const ccy        = 'CNY'
  const faceAmt    = bond.faceAmount || ''

  // 应计利息行
  const interest = parseFloat(bond.interestTotal) || parseFloat(bond.accruedInterest) || 0
  if (interest) {
    rows.push({
      payDate: settleDate, direction: dir,
      principal: faceAmt, principalFmt: fmtNum(faceAmt),
      amount: sign * interest, amountFmt: fmtAmt(interest),
      currency: ccy, startDate: tradeDate, endDate: settleDate,
      days: cfDays(tradeDate, settleDate),
      type: '利息', status: '确定',
      settlePath: bond.ourSettlePath || '', counterSettlePath: bond.counterSettlePath || '',
      isEditing: false, isManual: false,
    })
  }

  // 本金行（全价金额）
  const principal = parseFloat(bond.fullAmount) || 0
  if (principal) {
    rows.push({
      payDate: settleDate, direction: dir,
      principal: faceAmt, principalFmt: fmtNum(faceAmt),
      amount: sign * principal, amountFmt: fmtAmt(principal),
      currency: ccy, startDate: tradeDate, endDate: settleDate,
      days: cfDays(tradeDate, settleDate),
      type: '本金', status: '确定',
      settlePath: bond.ourSettlePath || '', counterSettlePath: bond.counterSettlePath || '',
      isEditing: false, isManual: false,
    })
  }

  // 无数据时给占位行方便 Demo 展示
  if (!rows.length && bond.settleDate) {
    rows.push({
      payDate: settleDate, direction: dir,
      principal: '', principalFmt: '0.00',
      amount: 0, amountFmt: '0.00',
      currency: ccy, startDate: tradeDate, endDate: settleDate,
      days: cfDays(tradeDate, settleDate),
      type: '本金', status: '待确定',
      settlePath: '', counterSettlePath: '',
      isEditing: false, isManual: false,
    })
  }
  return rows
})

// ─── 现金流新增 ────────────────────────────────────────────────────────────────
const cfManualRows = ref([])
const cfIsAdding   = ref(false)
const cfPageSize   = ref(20)
const cfNewRow     = reactive({
  payDate: '', direction: 'Rec', principal: '',
  amount: '', currency: 'CNY', startDate: '', endDate: '',
  type: '本金', status: '确定', settlePath: '', counterSettlePath: '',
})

// 合并自动行 + 手动行（+ 正在编辑的新行）
const cfAllRows = computed(() => {
  const base   = bondCashflows.value
  const manual = cfManualRows.value.map(r => ({ ...r, isEditing: false }))
  const rows   = [...base, ...manual]
  if (cfIsAdding.value) {
    rows.push({
      payDate: cfNewRow.payDate, direction: cfNewRow.direction,
      principal: cfNewRow.principal, principalFmt: cfNewRow.principal,
      amount: parseFloat(String(cfNewRow.amount).replace(/,/g, '')) || 0,
      amountFmt: cfNewRow.amount,
      currency: cfNewRow.currency,
      startDate: cfNewRow.startDate, endDate: cfNewRow.endDate,
      days: cfDays(cfNewRow.startDate, cfNewRow.endDate),
      type: cfNewRow.type, status: cfNewRow.status,
      settlePath: cfNewRow.settlePath, counterSettlePath: cfNewRow.counterSettlePath,
      isEditing: true, isManual: true,
    })
  }
  return rows
})

function handleCfAdd() {
  if (cfIsAdding.value) return
  const fmtNum = v => Number(v || 0).toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  Object.assign(cfNewRow, {
    payDate:           bond.settleDate || today,
    direction:         bond.tradeDirection === 'buy' ? 'Pay' : 'Rec',
    principal:         bond.faceAmount ? fmtNum(bond.faceAmount) : '',
    amount:            bond.fullAmount  ? fmtNum(bond.fullAmount)  : '',
    currency:          'CNY',
    startDate:         bond.tradeDate  || today,
    endDate:           bond.settleDate || today,
    type:              '本金',
    status:            '确定',
    settlePath:        bond.ourSettlePath     || '',
    counterSettlePath: bond.counterSettlePath || '',
  })
  cfIsAdding.value = true
}

function handleCfSave() {
  const fmtNum = v => {
    const n = parseFloat(String(v).replace(/,/g, '')) || 0
    return n.toLocaleString('zh-CN', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
  }
  cfManualRows.value.push({
    payDate:           cfNewRow.payDate,
    direction:         cfNewRow.direction,
    principal:         cfNewRow.principal,
    principalFmt:      fmtNum(cfNewRow.principal),
    amount:            parseFloat(String(cfNewRow.amount).replace(/,/g, '')) || 0,
    amountFmt:         fmtNum(cfNewRow.amount),
    currency:          cfNewRow.currency,
    startDate:         cfNewRow.startDate,
    endDate:           cfNewRow.endDate,
    days:              cfDays(cfNewRow.startDate, cfNewRow.endDate),
    type:              cfNewRow.type,
    status:            cfNewRow.status,
    settlePath:        cfNewRow.settlePath,
    counterSettlePath: cfNewRow.counterSettlePath,
    isManual:          true,
    isEditing:         false,
  })
  cfIsAdding.value = false
}

function handleCfCancel() {
  cfIsAdding.value = false
}

function cfTypeLabel(type) {
  const map = { '本金': t('te.cfPrincipal'), '利息': t('te.cfInterest'), '税费': t('te.cfTax') }
  return map[type] ?? type
}
function cfStatusLabel(status) {
  const map = { '确定': t('te.cfStatusConfirmed'), '待确定': t('te.cfStatusPending') }
  return map[status] ?? status
}

function handleCfDelete(row, idx) {
  if (!row.isManual) return   // 自动生成行不允许删除
  const manualIdx = idx - bondCashflows.value.length
  if (manualIdx >= 0) cfManualRows.value.splice(manualIdx, 1)
}

// ─── 外汇平价远期：组合交易 ──────────────────────────────────────────────────

const maxAvgFwdTrades = 12
const afColors = [
  '#52c41a', '#faad14', '#1890ff', '#f5222d',
  '#722ed1', '#13c2c2', '#eb2f96', '#fa8c16',
  '#a0d911', '#08979c', '#531dab', '#d4380d',
]
let afIdSeq = 3

function emptyAvgFwdTrade(id) {
  return {
    id,
    direction:     'BUY',
    buyAmount:     '0.00',
    sellAmount:    '0.00',
    // 即期汇率
    spotRate:      '', spotBP: '', costSpotRate: '',
    // 升贴水
    premium:       '', premiumBP: '', costPremium: '',
    // 远期汇率
    fwdRate:       '', fwdBP: '', costFwdRate: '',
    // 分润（货币默认 CNY，货币对确定后由 watch 更新）
    profitSplit:   '', profitCcy: 'CNY',
    // 日期
    spotValueDate: '',
    optionalDate:  '',
    maturityDate:  '',
    tenor:         '',
  }
}

const avgFwdTrades = ref([emptyAvgFwdTrade(1), emptyAvgFwdTrade(2)])
const afCommonOpen = ref(true)   // 默认展开
const afCommon = reactive({
  // 公共交易要素
  currencyPair:    '',   // 所有笔共用货币对
  tradeDate:       today,
  tradeTime:       nowTime,
  // 交易账户
  account:         '',
  counterparty:    '',
  broker:          '',
  mirrorAccount:   '',
  // 备注信息
  tradeNature:     '',
  externalNo:      '',
  externalSystem:  'RCS',
  purpose:         '',
  remark:          '',
  // 拓展字段
  ourSettlePath:   '',
  theirSettlePath: '',
  clearingMethod:  '',
  tradeMethod:     '',
  // 平价汇率（自动计算 + 支持手动覆盖）
  avgSpotRateInput: '',
  avgPremiumInput:  '',
  avgFwdRateInput:  '',
})

// 货币对中的计价货币（USD/CNY → CNY）—— 必须在 afCommon 之后声明
function afProfitCcy() {
  const pair = afCommon.currencyPair
  return pair && pair.includes('/') ? pair.split('/')[1] : 'CNY'
}

// 货币1 / 货币2（从货币对拆分，UI 用）
const afCcy1 = computed(() => {
  const pair = afCommon.currencyPair
  return pair && pair.includes('/') ? pair.split('/')[0] : t('te.ccy1')
})
const afCcy2 = computed(() => {
  const pair = afCommon.currencyPair
  return pair && pair.includes('/') ? pair.split('/')[1] : t('te.ccy2')
})

// 成本价计算（1 BP = 0.0001）
function calcAfTradeCosts(t) {
  const fmt8 = v => parseFloat(v).toFixed(8)
  const calc = (base, bp) => {
    const b = parseFloat(base)
    const p = parseFloat(bp) || 0
    return isNaN(b) ? '' : fmt8(b + p * 0.0001)
  }
  t.costSpotRate = calc(t.spotRate, t.spotBP)
  t.costPremium  = calc(t.premium,  t.premiumBP)
  t.costFwdRate  = calc(t.fwdRate,  t.fwdBP)

  // Margin = (对客远期汇率 − 成本远期汇率) × CCY1 名义本金
  // 客户买 CCY1 时银行报高价盈利；客户卖 CCY1 时银行报低价盈利
  const fwd     = parseFloat(t.fwdRate)
  const cost    = parseFloat(t.costFwdRate)
  const notional = parseFloat(t.direction === 'BUY' ? t.buyAmount : t.sellAmount)
  if (!isNaN(fwd) && !isNaN(cost) && !isNaN(notional) && notional > 0) {
    const spreadPerUnit = t.direction === 'BUY' ? (fwd - cost) : (cost - fwd)
    t.profitSplit = (spreadPerUnit * notional).toFixed(2)
  } else {
    t.profitSplit = ''
  }
}

// 货币对变更时自动同步所有笔的分润货币
watch(() => afCommon.currencyPair, () => {
  const ccy = afProfitCcy()
  avgFwdTrades.value.forEach(t => { t.profitCcy = ccy })
})

// ─── 期限(天)：到期日 - 即期起息日（自动计算，也支持手动输入）───────────────────
function autoTenor(t) {
  if (t.spotValueDate && t.maturityDate) {
    const diff = Math.round(
      (new Date(t.maturityDate) - new Date(t.spotValueDate)) / 86400000
    )
    t.tenor = diff >= 0 ? String(diff) : ''
  } else {
    t.tenor = ''
  }
}

// ─── 平价汇率：各笔交易的算术平均 ─────────────────────────────────────────────
function numAvg(arr) {
  const nums = arr.map(v => parseFloat(v)).filter(n => !isNaN(n) && n > 0)
  if (!nums.length) return ''
  return (nums.reduce((a, b) => a + b, 0) / nums.length).toFixed(6)
}
const avgSpotRate = computed(() => numAvg(avgFwdTrades.value.map(t => t.spotRate)))
const avgPremium  = computed(() => numAvg(avgFwdTrades.value.map(t => t.premium)))
const avgFwdRate  = computed(() => numAvg(avgFwdTrades.value.map(t => t.fwdRate)))

// 平价汇率字段自动同步（计算值变化时自动填入，用户也可手动覆盖）
watch(avgSpotRate, (val) => { afCommon.avgSpotRateInput = val })
watch(avgPremium,  (val) => { afCommon.avgPremiumInput  = val })
watch(avgFwdRate,  (val) => { afCommon.avgFwdRateInput  = val })

function addAvgFwdTrade() {
  if (avgFwdTrades.value.length < maxAvgFwdTrades) {
    avgFwdTrades.value.push(emptyAvgFwdTrade(afIdSeq++))
  }
}
function removeAvgFwdTrade(id) {
  if (avgFwdTrades.value.length > 1) {
    avgFwdTrades.value = avgFwdTrades.value.filter(t => t.id !== id)
  } else {
    ElMessage.warning(t('te.msgMinOneTrade'))
  }
}
function handleAvgFwdClear() {
  avgFwdTrades.value.forEach(t => Object.assign(t, emptyAvgFwdTrade(t.id)))
  Object.assign(afCommon, {
    currencyPair: '', tradeDate: today, tradeTime: nowTime,
    account: '', counterparty: '', broker: '', mirrorAccount: '',
    tradeNature: '', externalNo: '', externalSystem: 'RCS', purpose: '', remark: '',
    ourSettlePath: '', theirSettlePath: '',
    clearingMethod: '', tradeMethod: '',
    avgSpotRateInput: '', avgPremiumInput: '', avgFwdRateInput: '',
  })
  ElMessage.success(t('te.msgCleared'))
}
function handleAvgFwdSubmit() {
  ElMessage.success(t('te.msgComboSubmitted', { n: avgFwdTrades.value.length }))
}

const afPassCount = computed(() =>
  avgFwdTrades.value.filter(t =>
    t.currencyPair && (parseFloat(t.buyAmount) > 0 || parseFloat(t.sellAmount) > 0)
  ).length
)
const afPendCount = computed(() => avgFwdTrades.value.length - afPassCount.value)
</script>

<style lang="scss" scoped>
.trade-entry-page {
  flex: 1;
  min-height: 0;
  display: grid;
  grid-template-columns: 4fr 8fr 12fr;
  grid-template-rows: minmax(0, 1fr);
  gap: 8px;
  padding: 12px;
  box-sizing: border-box;
  background: var(--git-bg);
  overflow: hidden;

  /* 组合交易：表单区铺满，analysis-panel 已通过 v-show 移出 grid */
  &.is-combo {
    grid-template-columns: 4fr 20fr;
  }
}

/* ═══════════════════════════════════════
   左侧产品树
════════════════════════════════════════ */
.product-tree {
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-width: 0;
  min-height: 0;

  .tree-header {
    height: 44px;
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 0 14px;
    font-size: 14px;
    font-weight: 600;
    color: var(--git-text-1);
    border-bottom: 1px solid var(--git-border);
    flex-shrink: 0;

    .tree-header-icon { color: #f0a500; font-size: 16px; }
  }

  .tree-search {
    padding: 8px 10px;
    border-bottom: 1px solid var(--git-border);
    flex-shrink: 0;
  }

  .tree-body {
    flex: 1;
    overflow-y: auto;
    padding: 4px 0;
  }

  .tree-standalone {
    padding: 7px 14px;
    font-size: 13px;
    color: var(--git-text-2);
    cursor: pointer;
    border-bottom: 1px solid var(--git-border);
    margin-bottom: 4px;

    &:hover { background: #f5f7fa; color: var(--git-primary); }
    &.active { color: var(--git-primary); background: #e8f0fe; font-weight: 500; }
  }

  .group-label {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 7px 12px;
    font-size: 13px;
    font-weight: 500;
    color: var(--git-text-1);
    cursor: pointer;
    user-select: none;

    &:hover { background: #f5f7fa; }

    .group-arrow {
      font-size: 11px;
      color: var(--git-text-3);
      transition: transform 0.2s;
      flex-shrink: 0;
      &.expanded { transform: rotate(90deg); }
    }

    .group-icon-dot {
      display: inline-block;
      width: 13px; height: 13px;
      border-radius: 3px;
      flex-shrink: 0;
    }
  }

  .tree-item {
    padding: 6px 14px 6px 36px;
    font-size: 13px;
    color: var(--git-text-2);
    cursor: pointer;
    transition: background 0.1s;

    &:hover  { background: #f0f5ff; color: var(--git-primary); }
    &.active { background: #e8f0fe; color: var(--git-primary); font-weight: 500; }

    &--subgroup {
      padding-left: 28px;
      display: flex;
      align-items: center;
      gap: 4px;
      font-weight: 500;
      color: var(--git-text-1);

      .sub-arrow {
        font-size: 11px;
        color: var(--git-text-3);
        transition: transform 0.2s;
        flex-shrink: 0;
        &.expanded { transform: rotate(90deg); }
      }
    }

    &--child { padding-left: 48px; }
  }
}

/* ═══════════════════════════════════════
   中间表单面板
════════════════════════════════════════ */
.form-panel {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  height: 100%;          /* 撑满 grid 行高，使 form-body 的 overflow-y 生效 */
  box-sizing: border-box;
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  overflow: hidden;
}

.form-header {
  height: 44px;
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
  border-bottom: 1px solid var(--git-border);
  background: #fff;
  flex-shrink: 0;

  .form-tabs {
    display: flex;
    align-items: center;
    gap: 12px;
    height: 100%;

    .product-label {
      font-size: 14px;
      font-weight: 600;
      color: var(--git-text-1);
    }

    .tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 4px 12px;
      border: 1px solid var(--git-border);
      border-radius: 4px;
      background: #f5f9ff;
      font-size: 13px;
      color: var(--git-primary);
      cursor: pointer;
      font-weight: 500;

      &.active { border-color: var(--git-primary); background: #eef4ff; }
    }
  }

  .form-action-icons {
    display: flex;
    align-items: center;
    gap: 14px;

    .hd-icon {
      font-size: 16px;
      color: var(--git-text-3);
      cursor: pointer;
      &:hover { color: var(--git-primary); }
    }
  }
}

/* 嵌入子组件（现券买卖）时去掉内边距和背景，让子组件自行布局 */
.form-body--embed {
  padding: 0 !important;
  background: transparent !important;
  overflow: hidden !important;
  gap: 0 !important;
}

.form-body {
  flex: 1;
  min-height: 0;        /* 关键：让 flex 子项不撑破父容器 */
  overflow-y: auto;
  padding: 10px 14px;
  background: #f4f6fb;

  /* 滚动条样式 */
  &::-webkit-scrollbar        { width: 5px; }
  &::-webkit-scrollbar-track  { background: transparent; }
  &::-webkit-scrollbar-thumb  { background: #d0d5dd; border-radius: 3px; }
  &::-webkit-scrollbar-thumb:hover { background: #a0a8b5; }
}

/* section 卡片间距（替代 flex gap） */
.fs-card + .fs-card { margin-top: 8px; }

/* ─── Section card ─── */
.fs-card {
  background: #fff;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.fs-title {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
  border-bottom: 1px solid #eaecf2;

  .fs-bar {
    display: inline-block;
    width: 3px; height: 13px;
    background: var(--git-primary);
    border-radius: 2px;
    flex-shrink: 0;
  }
}

/* ─── 行布局：24格栅，label 占 8 格(33.333%)，value 占 16 格(66.667%) ─── */
.fs-row {
  display: grid;
  grid-template-columns: calc(8 / 24 * 100%) calc(16 / 24 * 100%);
  border-bottom: 1px solid #edf0f7;
  min-height: 38px;

  &--last { border-bottom: none; }
}

.fs-label {
  display: flex;
  align-items: center;
  padding: 5px 12px;
  font-size: 12px;
  color: var(--git-text-2);
  background: #f8f9fc;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
  user-select: none;
  line-height: 1.4;

  .req { color: #f56c6c; margin-left: 2px; }
}

.fs-value {
  display: flex;
  align-items: center;
  padding: 3px 10px;
  background: #fff;
  gap: 6px;
  min-width: 0;

  /* 全局去掉 element 边框，融入表格风格 */
  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important;
    border: none;
    background: transparent;
    padding: 0 2px;
  }
  :deep(.el-date-editor.el-input) {
    width: 100%;
    box-shadow: none !important;
    --el-input-bg-color: transparent;
  }
  :deep(.el-date-editor .el-input__wrapper) {
    box-shadow: none !important;
    background: transparent;
    padding: 0 4px;
  }

  &--split { gap: 8px; }

  &--multi {
    gap: 6px;
    align-items: center;
  }

  &--rate {
    gap: 6px;
  }

  &--buysell {
    gap: 5px;
    align-items: center;
  }
}

/* ─── 多列值区（替代 fs-value 用于多格布局）─── */
.fs-cols {
  display: flex;
  width: 100%;
  min-width: 0;

  /* 双列等宽 */
  &--2 > .fc { flex: 1; min-width: 0; }

  /* 三列汇率行旧版（兼容保留） */
  &--rate {
    > .fc:first-child { flex: 1; min-width: 0; }
    > .fc--num        { width: 72px; flex-shrink: 0; }
    > .fc--unit       { width: 34px; flex-shrink: 0; }
  }

  /* 三列等宽：即期汇率 | 点差 | 成本汇率 */
  &--rate3 > .fc { flex: 1; min-width: 0; }

  /* 双列分润/外部流水 */
  &--profit > .fc { flex: 1; min-width: 0; }

  /* 账户行：主输入 flex:1 + 自动填入 100px */
  &--acct {
    > .fc:first-child { flex: 1; min-width: 0; }
    > .fc:last-child  { width: 100px; flex-shrink: 0; }
  }
}

/* ─── 单个列格 ─── */
.fc {
  display: flex;
  align-items: center;
  padding: 3px 8px;
  background: #fff;
  border-right: 1px solid #edf0f7;
  min-width: 0;
  gap: 4px;

  &:last-child { border-right: none; }

  /* 消除 el 输入框边框，融入表格风格 */
  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important;
    border: none;
    background: transparent;
    padding: 0 2px;
  }
  :deep(.el-date-editor.el-input)       { width: 100%; }
  :deep(.el-date-editor .el-input__wrapper) {
    box-shadow: none !important;
    background: transparent;
    padding: 0 4px;
  }

  /* 数值格 — 右对齐等宽数字 */
  &--num :deep(.el-input__inner) {
    font-variant-numeric: tabular-nums;
    font-size: 12px;
  }

  /* 单位标签格 — 灰底居中 */
  &--unit {
    font-size: 12px;
    color: var(--git-text-3);
    white-space: nowrap;
    justify-content: center;
    background: #f8f9fc;
    cursor: default;
  }

  /* 自动填入格 — 灰底居中 */
  &--autofill {
    font-size: 12px;
    color: var(--git-text-3);
    background: #f5f7fa;
    justify-content: center;
    cursor: default;
    white-space: nowrap;
  }

  /* 置灰只读格 — 系统自动填入 / 不可编辑 */
  &--readonly {
    background: #f5f7fa;

    :deep(.el-input.is-disabled .el-input__wrapper) {
      background: transparent !important;
      box-shadow: none !important;
      cursor: default;
    }
    :deep(.el-input.is-disabled .el-input__inner) {
      color: var(--git-text-2) !important;
      -webkit-text-fill-color: var(--git-text-2) !important;
      cursor: default;
      font-variant-numeric: tabular-nums;
    }
    :deep(.el-select.is-disabled .el-input__wrapper) {
      background: transparent !important;
      box-shadow: none !important;
      cursor: default;
    }
    :deep(.el-select.is-disabled .el-input__inner) {
      color: var(--git-text-2) !important;
      -webkit-text-fill-color: var(--git-text-2) !important;
      cursor: default;
    }
  }
}

/* ─── 数字输入框 ─── */
.input-number {
  width: 130px;
  :deep(.el-input__inner) {
    font-variant-numeric: tabular-nums;
    font-size: 12px;
    text-align: right;
  }
}

.input-rate-main {
  flex: 1;
  min-width: 0;
}

.input-amt {
  flex: 1;
  min-width: 0;
}

/* ─── 单位标签 ─── */
.unit-tag {
  font-size: 12px;
  color: var(--git-text-3);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ─── BUY / SELL 方向标签 ─── */
.dir-tag {
  font-size: 11px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
  flex-shrink: 0;

  &.dir-buy  { color: #36c9a0; background: #e8faf4; }
  &.dir-sell { color: #f56c6c; background: #fff0f0; }
}

.swap-icon {
  font-size: 13px;
  color: var(--git-text-3);
  flex-shrink: 0;
}

/* ─── 期限(天) 纯文本显示 ─── */
.plain-val {
  font-size: 13px;
  color: var(--git-text-1);
  font-variant-numeric: tabular-nums;
}

/* ─── 自动填入只读格 ─── */
.auto-fill-cell {
  :deep(.el-input__inner) {
    color: var(--git-text-3);
    text-align: center;
    font-size: 12px;
  }
  :deep(.el-input__wrapper) {
    background: #f5f7fa !important;
  }
}

/* ─── 占位提示 ─── */
/* BP 文字标签（现券买卖点差列） */
.rate-bp {
  font-size: 11px;
  color: #9aa0b8;
  font-family: 'Helvetica Neue', monospace;
  white-space: nowrap;
  width: 100%;
  text-align: center;
}

/* 小图标按钮（债券代码行） */
.row-ic-sm {
  font-size: 14px;
  color: #bbc;
  cursor: pointer;
  flex-shrink: 0;
  &:hover { color: var(--git-primary); }
}

/* ─── 同业拆借：贴现公式提示 ─── */
.ib-calc-field {
  :deep(.el-input__inner) {
    color: var(--git-primary) !important;
    -webkit-text-fill-color: var(--git-primary) !important;
    font-weight: 600;
  }
  :deep(.el-input__wrapper) { background: #f5f8ff !important; }
}
.ib-calc-hint {
  display: block;
  font-size: 10px;
  color: var(--git-text-3);
  margin-top: 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.placeholder-tip {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  color: var(--git-text-3);
  font-size: 13px;
  min-height: 200px;
}

/* ─── 底部按钮 ─── */
.form-footer {
  height: 52px;
  min-height: 52px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  padding: 0 20px;
  border-top: 1px solid var(--git-border);
  background: #fff;
  flex-shrink: 0;

  .btn-clear {
    display: flex;
    align-items: center;
    gap: 4px;
  }
  .btn-submit { min-width: 72px; }
}

/* ═══════════════════════════════════════
   右侧分析面板
════════════════════════════════════════ */
/* ── 右侧分析面板 ── */
.analysis-panel {
  display: flex;
  flex-direction: column;
  gap: 5px;
  overflow-y: auto;
  min-width: 0;
  min-height: 0;

  &::-webkit-scrollbar       { width: 4px; }
  &::-webkit-scrollbar-thumb { background: #d0d5dd; border-radius: 2px; }
}

/* 每个可折叠卡片 */
.ap-card {
  background: #fff;
  border: 1px solid var(--git-border);
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
}

/* 卡片头部 */
.ap-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px;
  height: 44px;
  cursor: pointer;
  transition: background 0.1s;
  &:hover { background: #f5f9ff; }

  .ap-hd-left {
    display: flex; align-items: center; gap: 7px;
  }
  .ap-icon    { font-size: 15px; color: var(--git-primary); }
  .ap-label   { font-size: 13px; font-weight: 500; color: var(--git-text-1); }
  .ap-chevron {
    font-size: 12px; color: var(--git-text-3);
    transition: transform .2s;
    transform: rotate(0deg);
    &.open { transform: rotate(90deg); }
  }
  .ap-refresh {
    font-size: 14px; color: var(--git-text-3);
    &:hover { color: var(--git-primary); }
  }
}

/* 卡片内容区 */
.ap-body {
  border-top: 1px solid var(--git-border);
  padding: 8px 0 0;
}

.ap-body--empty {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 60px;
  font-size: 12px;
  color: var(--git-text-3);
  padding: 12px 0;
}

/* ── 现金流预览内容 ── */
.cf-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 12px 6px;
  font-size: 12px;
}

.cf-table {
  width: 100%;
  /* 禁止任何单元格折行 */
  :deep(.el-table__cell) {
    white-space: nowrap;
  }
  :deep(.el-table__header-wrapper th) {
    background: #f8f9fc !important;
  }
  :deep(.el-table__row td) {
    border-bottom: 1px solid #f0f2f7;
  }
  /* 内联编辑行的输入控件去掉多余边框 */
  :deep(.el-input__wrapper) {
    box-shadow: none;
    border: 1px solid #dde1ea;
    border-radius: 3px;
    padding: 0 4px;
  }
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none;
    border: 1px solid #dde1ea;
    border-radius: 3px;
  }
  :deep(.el-date-editor.el-input) { width: 100%; }
  :deep(.el-date-editor .el-input__wrapper) {
    box-shadow: none;
    border: 1px solid #dde1ea;
    border-radius: 3px;
    padding: 0 4px;
  }
}

/* 支付方向标签 */
.cf-dir-tag {
  display: inline-block;
  padding: 1px 7px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 500;
}
.cf-pay     { background: #fff1f0; color: #f5222d; }
.cf-receive { background: #f6ffed; color: #52c41a; }

/* 金额颜色 */
.cf-neg { color: #f5222d; font-variant-numeric: tabular-nums; }
.cf-pos { color: #52c41a; font-variant-numeric: tabular-nums; }
.cf-num { font-variant-numeric: tabular-nums; color: var(--git-text-1); }

/* 类型标签 */
.cf-type-tag {
  display: inline-block;
  padding: 1px 6px;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 500;
}
.cf-type--本金 { background: #e8f0fe; color: #1a56d6; }
.cf-type--利息 { background: #fef9e7; color: #b7770d; }
.cf-type--税费 { background: #fce8f3; color: #9c27b0; }

/* 状态 */
.cf-status { font-size: 11px; color: var(--git-text-2); }

/* 结算路径 */
.cf-path {
  font-size: 11px;
  color: var(--git-text-2);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
  display: block;
}

/* 分页栏 */
.cf-pagination {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  padding: 6px 10px 8px;
  border-top: 1px solid #f0f2f7;
  font-size: 11px;
  color: var(--git-text-2);

  .cf-total { flex-shrink: 0; }
  .cf-goto  { display: flex; align-items: center; gap: 4px; flex-shrink: 0; }
  :deep(.el-pagination) { padding: 0; }
  :deep(.el-pagination .el-pager li) { font-size: 11px; min-width: 22px; height: 22px; line-height: 22px; }
  :deep(.el-pagination button) { height: 22px; min-width: 22px; }
  :deep(.el-input__wrapper) { padding: 0 4px; box-shadow: none; border: 1px solid #dde1ea; border-radius: 2px; }
  :deep(.el-input__inner) { height: 20px; font-size: 11px; text-align: center; }
}

/* ═══════════════════════════════════════
   外汇平价远期 — 组合交易（白肤皮）
════════════════════════════════════════ */

/* 头部标签 */
.af-added-tag {
  display: inline-flex;
  align-items: center;
  padding: 2px 9px;
  border-radius: 10px;
  background: #e8f0fe;
  color: var(--git-primary);
  font-size: 12px;
  font-weight: 500;
  margin-left: 4px;
  cursor: default;
  white-space: nowrap;
}
.af-import-btn  { margin-left: 4px; font-size: 12px; }
.af-newtrade-btn { font-size: 12px; }

/* 整体容器：撑满 form-body，内部两段：表格区（弹性）+ 公共要素（固定底部） */
.af-wrap {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 组合交易时 form-body 变为 flex 列，让 af-wrap 的 flex:1 生效 */
.is-combo .form-body {
  overflow: hidden;
  padding: 8px;
  display: flex;
  flex-direction: column;
}

/* 横向滚动容器：flex:1 使其撑满剩余高度，纵向内容撑高则纵向也可滚 */
.af-scroll-x {
  flex: 1;
  min-height: 0;
  overflow: auto;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  background: #fff;

  &::-webkit-scrollbar        { width: 5px; height: 5px; }
  &::-webkit-scrollbar-track  { background: transparent; }
  &::-webkit-scrollbar-thumb  { background: #d0d5dd; border-radius: 3px; }
}

/* CSS Grid 表格 */
.af-grid {
  display: grid;
  min-width: max-content;
}

/* ── 通用单元格 ── */
.af-cell {
  display: flex;
  align-items: center;
  padding: 5px 8px;
  border-bottom: 1px solid #edf0f7;
  border-right: 1px solid #edf0f7;
  min-height: 38px;
  box-sizing: border-box;
  background: #fff;
  min-width: 0;

  &:last-child { border-right: none; }

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important;
    border: none;
    background: transparent;
    padding: 0 2px;
  }
  :deep(.el-date-editor.el-input)            { width: 100%; }
  :deep(.el-date-editor .el-input__wrapper)  { box-shadow: none !important; background: transparent; padding: 0 4px; }
  :deep(.el-time-picker.el-input .el-input__wrapper) { box-shadow: none !important; background: transparent; padding: 0 4px; }
}

/* 字段标签列 */
.af-cell--label {
  background: #f8f9fc;
  font-size: 12px;
  color: var(--git-text-2);
  border-right: 1px solid #e4e8f0;
  white-space: nowrap;
  user-select: none;
  padding: 5px 10px;
  .req { color: #f56c6c; margin-left: 2px; }
}

/* 最后一行 —— 去掉下边框 */
.af-cell--last { border-bottom: none; }

/* 子级标签行（点差/成本价）—— 浅背景区分层级 */
.af-cell--sub {
  background: #f8f9fc;
  font-size: 11px;
  color: var(--git-text-3);
  padding-left: 14px;
}

/* 只读计算格 */
.af-cell--ro {
  background: #f5f7fa;
  :deep(.el-input.is-disabled .el-input__wrapper) {
    background: transparent !important;
    box-shadow: none !important;
  }
  :deep(.el-input.is-disabled .el-input__inner) {
    color: var(--git-text-2) !important;
    -webkit-text-fill-color: var(--git-text-2) !important;
    font-variant-numeric: tabular-nums;
  }
}

/* 列头：标签格 */
.af-cell--head-label {
  background: #f0f2f5;
  font-size: 12px;
  font-weight: 600;
  color: var(--git-text-1);
  border-bottom: 2px solid #dde1ea;
  border-right: 1px solid #e4e8f0;
  padding: 7px 10px;
}

/* 列头：交易列 */
.af-cell--head-trade {
  background: #f0f2f5;
  border-bottom: 2px solid #dde1ea;
  padding: 6px 8px;
  gap: 5px;
}
.af-tdot {
  display: inline-block;
  width: 10px; height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.af-ttitle {
  font-size: 12px;
  font-weight: 600;
  color: var(--git-text-1);
  white-space: nowrap;
}
.af-cbadge {
  font-size: 11px;
  color: var(--git-primary);
  background: #e8f0fe;
  padding: 1px 5px;
  border-radius: 3px;
  white-space: nowrap;
}
.af-ticons {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-left: auto;
  color: var(--git-text-3);
  font-size: 13px;
  .el-icon            { cursor: pointer; &:hover { color: var(--git-primary); } }
  .af-del-icon:hover  { color: #f56c6c !important; }
}

/* 自动填入格 */
.af-cell--auto {
  background: #f8f9fc;
  :deep(.el-input.is-disabled .el-input__wrapper),
  :deep(.el-select.is-disabled .el-input__wrapper) {
    background: transparent !important; box-shadow: none !important;
  }
  :deep(.el-input.is-disabled .el-input__inner),
  :deep(.el-select.is-disabled .el-input__inner) {
    color: var(--git-text-3) !important;
    -webkit-text-fill-color: var(--git-text-3) !important;
  }
}

/* BP 单元格 */
.af-cell--bp { gap: 4px; }
.af-bp {
  font-size: 11px;
  color: var(--git-text-3);
  background: #f0f2f5;
  padding: 1px 4px;
  border-radius: 2px;
  flex-shrink: 0;
  white-space: nowrap;
}

/* ── 收 / 付 两行布局 ── */

/* 标签列：收/付 合并标签，垂直居中 */
.af-cell--dir-label {
  align-items: center;
  font-size: 12px;
  font-weight: 600;
  color: var(--git-text-1);
}

/* 数据格：flex 列，两行 */
.af-cell--dir-block {
  flex-direction: column;
  gap: 0;
  padding: 0;
  overflow: hidden;
}

/* 每行（收 / 付） */
.af-dir-row {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 5px 8px;
  transition: background 0.12s;

  /* 激活行：淡高亮背景 */
  &.is-active {
    background: #f4fbf8;
  }
}

/* 分隔线 */
.af-dir-divider {
  height: 1px;
  background: #edf0f7;
  flex-shrink: 0;
  margin: 0;
}

/* BUY / SELL 方向标签（可点击） */
.af-dir-tag {
  flex-shrink: 0;
  width: 40px;
  padding: 2px 0;
  border-radius: 3px;
  font-size: 11px;
  font-weight: 700;
  text-align: center;
  cursor: pointer;
  border: 1px solid transparent;
  transition: all 0.15s;
  letter-spacing: 0.3px;

  &--buy {
    color: #36c9a0;
    background: #edfaf5;
    border-color: #b7ebd9;
    &.is-on { background: #36c9a0; color: #fff; border-color: #36c9a0; }
  }
  &--sell {
    color: #f56c6c;
    background: #fff0f0;
    border-color: #ffc9c9;
    &.is-on { background: #f56c6c; color: #fff; border-color: #f56c6c; }
  }
}

/* 货币 chip（可点击切换货币对） */
.af-ccy-chip {
  flex-shrink: 0;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  font-size: 11px;
  font-weight: 600;
  padding: 1px 5px;
  border-radius: 3px;
  border: 1px solid #d0d5e0;
  white-space: nowrap;
  min-width: 36px;
  cursor: pointer;
  user-select: none;
  color: var(--git-text-2);
  background: #f4f6fa;
  transition: all 0.15s;

  &:hover {
    background: #e8ecf5;
    border-color: #b0b8cc;
  }
}

/* swap 提示小图标（只在 hover chip 时变明显）*/
.af-swap-hint {
  font-size: 10px;
  opacity: 0.4;
  transition: opacity 0.15s;
  .af-ccy-chip:hover & { opacity: 0.9; }
}

/* 中间 swap 按钮 */
.af-dir-swap {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 16px;
  margin: 0 8px;
  position: relative;
  cursor: pointer;
  color: var(--git-text-3);
  font-size: 12px;
  flex-shrink: 0;

  /* 横线贯穿 */
  &::before {
    content: '';
    position: absolute;
    left: 0; right: 0;
    top: 50%;
    height: 1px;
    background: #edf0f7;
  }
  /* 图标浮在线上 */
  .el-icon {
    position: relative;
    z-index: 1;
    background: #fff;
    padding: 0 3px;
    border-radius: 2px;
    border: 1px solid #e4e8f0;
    transition: all 0.15s;
  }
  &:hover .el-icon {
    color: var(--git-primary);
    border-color: var(--git-primary);
    background: #eef4ff;
  }
}

/* 双列格 (legacy，保留兼容) */
.af-cell--2col  { gap: 4px; }

.af-profit-ccy {
  flex-shrink: 0;
  width: 48px;
  font-size: 11px;
  font-weight: 600;
  color: var(--git-text-2);
  background: #f4f6fa;
  border: 1px solid #d0d5e0;
  border-radius: 3px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.af-flex-input  { flex: 1; min-width: 0; }

/* 公共要素折叠区：flex-shrink:0 确保不被挤压，始终固定在底部 */
.af-common {
  flex-shrink: 0;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  background: #fff;
  overflow: hidden;
  max-height: 280px;
  overflow-y: auto;

  &::-webkit-scrollbar        { width: 5px; }
  &::-webkit-scrollbar-track  { background: transparent; }
  &::-webkit-scrollbar-thumb  { background: #d0d5dd; border-radius: 3px; }
}
.af-common-hd {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 14px;
  font-size: 13px;
  font-weight: 600;
  color: var(--git-text-1);
  cursor: pointer;
  background: #f8f9fc;
  border-bottom: 1px solid #e4e8f0;
  user-select: none;
  &:hover { background: #f0f2f5; }

  .el-icon {
    font-size: 13px;
    color: var(--git-text-3);
    transition: transform 0.2s;
    &.is-flip { transform: rotate(180deg); }
  }
}
.af-common-body { padding: 12px 14px; }

/* 货币对 + 平价汇率摘要行 */
.af-cm-summary {
  display: flex;
  align-items: stretch;
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 12px;
  background: #fff;
}
.af-cm-sum-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #e4e8f0;

  &:last-child { border-right: none; }
  &--ccy { flex: 0 0 160px; }
}
.af-cm-sum-label {
  font-size: 11px;
  color: var(--git-text-2);
  background: #f8f9fc;
  padding: 4px 10px;
  border-bottom: 1px solid #e4e8f0;
  white-space: nowrap;
  user-select: none;
  .req { color: #f56c6c; margin-left: 2px; }
}
.af-cm-sum-value {
  flex: 1;
  display: flex;
  align-items: center;
  padding: 3px 8px;

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important; border: none; background: transparent; padding: 0 2px;
  }

  &--auto {
    background: #f8f9fc;
    :deep(.el-input.is-disabled .el-input__wrapper) {
      background: transparent !important; box-shadow: none !important;
    }
    :deep(.el-input.is-disabled .el-input__inner) {
      color: var(--git-primary) !important;
      -webkit-text-fill-color: var(--git-primary) !important;
      font-weight: 500;
      font-variant-numeric: tabular-nums;
    }
  }
}

/* 四栏等宽容器 */
.af-cm-sections {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
}

/* 单个 section 卡片 */
.af-cm-section {
  border: 1px solid #e4e8f0;
  border-radius: 4px;
  overflow: hidden;

  /* 拓展字段：标签较长，稍宽一些 */
  &--ext .af-cm-fl {
    width: 96px;
    min-width: 96px;
  }
}
.af-cm-section-title {
  padding: 7px 10px 7px 13px;
  font-size: 12px;
  font-weight: 600;
  color: var(--git-text-1);
  background: #f8f9fc;
  border-bottom: 1px solid #e4e8f0;
  border-left: 3px solid var(--git-primary);
}

/* section 内字段行 */
.af-cm-field {
  display: flex;
  align-items: stretch;
  min-height: 34px;
  border-bottom: 1px solid #edf0f7;
  &--last { border-bottom: none; }

  /* 双子列：两个 sub 并排 */
  &--2sub {
    display: grid;
    grid-template-columns: 1fr 1fr;
    .af-cm-sub { border-right: 1px solid #edf0f7; &:last-child { border-right: none; } }
  }
  /* 三子列 */
  &--3sub {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    .af-cm-sub { border-right: 1px solid #edf0f7; &:last-child { border-right: none; } }
  }
}

/* sub：多列布局时每个子格 */
.af-cm-sub {
  display: flex;
  flex-direction: column;
}

/* 字段 label */
.af-cm-fl {
  font-size: 11px;
  color: var(--git-text-2);
  background: #f8f9fc;
  padding: 3px 8px;
  width: 84px;
  flex-shrink: 0;
  border-right: 1px solid #edf0f7;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  user-select: none;
  display: block;
  line-height: 22px;
  cursor: default;
  .req { color: #f56c6c; margin-left: 2px; }
}

/* 字段 value */
.af-cm-fv {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 2px 6px;
  background: #fff;

  /* 自动计算只读值：蓝色高亮 */
  &--auto {
    background: #f5f8ff;
    :deep(.el-input.is-disabled .el-input__wrapper) {
      background: transparent !important; box-shadow: none !important;
    }
    :deep(.el-input.is-disabled .el-input__inner) {
      color: var(--git-primary) !important;
      -webkit-text-fill-color: var(--git-primary) !important;
      font-weight: 600;
      font-variant-numeric: tabular-nums;
    }
  }

  :deep(.el-input__wrapper),
  :deep(.el-select .el-input__wrapper) {
    box-shadow: none !important;
    border: none;
    background: transparent;
    padding: 0 2px;
  }
  :deep(.el-input.is-disabled .el-input__wrapper),
  :deep(.el-select.is-disabled .el-input__wrapper) {
    background: transparent !important;
    box-shadow: none !important;
  }
  :deep(.el-input.is-disabled .el-input__inner),
  :deep(.el-select.is-disabled .el-input__inner) {
    color: var(--git-text-3) !important;
    -webkit-text-fill-color: var(--git-text-3) !important;
  }
}

/* 期限(天) 纯文本 */
.af-tenor-val {
  font-size: 13px;
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--git-text-1);
  padding: 0 4px;
}

/* 底部校验状态 */
.af-validation {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-right: auto;
  font-size: 12px;
  color: var(--git-text-2);
}
.af-v-pass, .af-v-pend {
  display: flex;
  align-items: center;
  gap: 5px;
}
.af-dot {
  display: inline-block;
  width: 8px; height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
  &--green  { background: #52c41a; }
  &--orange { background: #faad14; }
}
</style>
