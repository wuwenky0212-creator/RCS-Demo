import request from './request'

export function listTaxRules(params) {
  return request.get('/base-data/tax-rules', { params })
}

export function createTaxRule(data) {
  return request.post('/base-data/tax-rules', data)
}

export function updateTaxRule(ruleId, data) {
  return request.put(`/base-data/tax-rules/${ruleId}`, data)
}

export function toggleTaxRule(ruleId) {
  return request.patch(`/base-data/tax-rules/${ruleId}/toggle`)
}

export function deleteTaxRule(ruleId) {
  return request.delete(`/base-data/tax-rules/${ruleId}`)
}
