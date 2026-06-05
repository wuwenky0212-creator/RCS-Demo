import { createRouter, createWebHashHistory } from 'vue-router'

import MainLayout from '@/layouts/MainLayout.vue'
import TradeEntry from '@/views/trade-entry/TradeEntry.vue'
import TransactionReview from '@/views/workbench/TransactionReview.vue'
import TaxRuleConfig from '@/views/base-data/TaxRuleConfig.vue'
import TradeQuery from '@/views/query/TradeQuery.vue'
import Placeholder from '@/views/Placeholder.vue'
import InternalTransferError from '@/views/workbench/InternalTransferError.vue'
import SuspenseAcct from '@/views/workbench/SuspenseAcct.vue'
import OtherReview from '@/views/workbench/OtherReview.vue'
import ScenarioQuery from '@/views/pnl-attribution/ScenarioQuery.vue'
import AttributionReport from '@/views/pnl-attribution/AttributionReport.vue'
import ProductMaintenance from '@/views/pnl-attribution/ProductMaintenance.vue'
import SpotFxPosition  from '@/views/position/SpotFxPosition.vue'
import FxSwapPosition  from '@/views/position/FxSwapPosition.vue'
import TransferRecords from '@/views/position/TransferRecords.vue'

// RCS-Demo 路由：默认进入"后线工作台 - 交易复核"
const routes = [
  {
    path: '/',
    component: MainLayout,
    redirect: '/workbench/transaction-review',
    children: [
      // 顶部导航占位（后续模块）
      { path: 'home', name: 'home', component: Placeholder, meta: { title: '首页' } },
      { path: 'trade-entry', name: 'trade-entry', component: TradeEntry, meta: { title: '交易录入' } },
      { path: 'position', redirect: '/position/spot-fx', meta: { title: '头寸管理' } },
      { path: 'position/spot-fx',        name: 'position-spot-fx',       component: SpotFxPosition,  meta: { title: '即期货币对头寸' } },
      { path: 'position/fx-swap',        name: 'position-fx-swap',        component: FxSwapPosition,  meta: { title: '外汇掉期头寸' } },
      { path: 'position/transfer-records', name: 'position-transfer-records', component: TransferRecords, meta: { title: '转移记录查询' } },
      { path: 'limit', name: 'limit', component: Placeholder, meta: { title: '限额管理' } },
      { path: 'business', name: 'business', component: Placeholder, meta: { title: '业务管理' } },
      { path: 'query', name: 'query', component: Placeholder, meta: { title: '查询管理' } },
      {
        path: 'base-data',
        name: 'base-data',
        redirect: '/base-data/tax-rules',
        meta: { title: '基础数据' }
      },
      {
        path: 'base-data/tax-rules',
        name: 'tax-rules',
        component: TaxRuleConfig,
        meta: { title: '税务规则配置', group: '税务配置' }
      },
      { path: 'statistics', name: 'statistics', component: TradeQuery, meta: { title: '交易查询' } },
      { path: 'rules', name: 'rules', component: Placeholder, meta: { title: '规则管理' } },
      {
        path: 'pnl-attribution',
        redirect: '/pnl-attribution/scenario-query',
        meta: { title: '损益归因' }
      },
      {
        path: 'pnl-attribution/scenario-query',
        name: 'scenario-query',
        component: ScenarioQuery,
        meta: { title: '情景查询' }
      },
      {
        path: 'pnl-attribution/attribution-report',
        name: 'attribution-report',
        component: AttributionReport,
        meta: { title: '归因分析报告' }
      },
      {
        path: 'pnl-attribution/product-maintenance',
        name: 'product-maintenance',
        component: ProductMaintenance,
        meta: { title: '归因因子配置' }
      },

      // 后线工作台
      {
        path: 'workbench',
        redirect: '/workbench/transaction-review',
        meta: { title: '后线工作台' }
      },
      {
        path: 'workbench/transaction-review',
        name: 'transaction-review',
        component: TransactionReview,
        meta: { title: '交易复核', group: '流程审批' }
      },
      // 工作台其它子菜单暂占位
      { path: 'workbench/clearing-review', name: 'clearing-review', component: Placeholder, meta: { title: '清算审批', group: '流程审批' } },
      { path: 'workbench/adjust-review', name: 'adjust-review', component: Placeholder, meta: { title: '调账审核', group: '流程审批' } },
      { path: 'workbench/other-review', name: 'other-review', component: OtherReview, meta: { title: '其他审核', group: '流程审批' } },
      { path: 'workbench/confirm-match', name: 'confirm-match', component: Placeholder, meta: { title: '证实匹配', group: '证实确认' } },
      { path: 'workbench/confirm-detail', name: 'confirm-detail', component: Placeholder, meta: { title: '证实明细', group: '证实确认' } },
      { path: 'workbench/confirm-msg', name: 'confirm-msg', component: Placeholder, meta: { title: '证实报文', group: '证实确认' } },
      { path: 'workbench/netting', name: 'netting', component: Placeholder, meta: { title: '待轧差处理', group: '清算结算' } },
      { path: 'workbench/dispatch', name: 'dispatch', component: Placeholder, meta: { title: '待发报处理', group: '清算结算' } },
      { path: 'workbench/incoming-sort', name: 'incoming-sort', component: Placeholder, meta: { title: '来账分拣', group: '清算结算' } },
      { path: 'workbench/holiday-adjust', name: 'holiday-adjust', component: Placeholder, meta: { title: '支付假日调整', group: '清算结算' } },
      { path: 'workbench/payment-cancel', name: 'payment-cancel', component: Placeholder, meta: { title: '收付撤销', group: '清算结算' } },
      { path: 'workbench/payment-msg', name: 'payment-msg', component: Placeholder, meta: { title: '收付报文', group: '清算结算' } },
      { path: 'workbench/settle-route', name: 'settle-route', component: Placeholder, meta: { title: '结算路径', group: '清算结算' } },
      { path: 'workbench/measure-track', name: 'measure-track', component: Placeholder, meta: { title: '计量跟踪处理', group: '会计核算' } },
      { path: 'workbench/post-error', name: 'post-error', component: Placeholder, meta: { title: '送账异常处理', group: '会计核算' } },
      { path: 'workbench/balance-init', name: 'balance-init', component: Placeholder, meta: { title: '余额初始', group: '会计核算' } },
      { path: 'workbench/manual-assign', name: 'manual-assign', component: Placeholder, meta: { title: '手工指定', group: '会计核算' } },
      { path: 'workbench/threshold-pass', name: 'threshold-pass', component: Placeholder, meta: { title: '阀值放行', group: '会计核算' } },
      { path: 'workbench/custodian-recon', name: 'custodian-recon', component: Placeholder, meta: { title: '托管机构余额核对', group: '每日核对' } },
      { path: 'workbench/cashflow-entry', name: 'cashflow-entry', component: Placeholder, meta: { title: '单边现金流', group: '交易录入' } },
      { path: 'workbench/fix-mgmt', name: 'fix-mgmt', component: Placeholder, meta: { title: '定盘管理', group: '业务管理' } },
      { path: 'workbench/internal-transfer-error', name: 'internal-transfer-error', component: InternalTransferError, meta: { title: '内部账划转异常处理', group: '内部账处理' } },
      { path: 'workbench/suspense-acct', name: 'suspense-acct', component: SuspenseAcct, meta: { title: '挂账与销账处理', group: '内部账处理' } }
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
