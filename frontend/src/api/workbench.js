import request from './request'

// 交易复核
export function listTransactionReviews(params) {
  return request.get('/workbench/transaction-review', { params })
}

export function batchApproveTransactionReviews(ids) {
  return request.post('/workbench/transaction-review/batch-approve', { ids })
}

export function approveTransactionReview(id) {
  return request.post(`/workbench/transaction-review/${id}/approve`)
}

// 工作台菜单 + 顶部统计 (用于首页 / 边栏数量徽标，可扩展)
export function getWorkbenchMenu() {
  return request.get('/workbench/menu')
}
