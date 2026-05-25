/**
 * 簿记架构数据
 * Entity → Business Unit → Book → Portfolio
 *
 * 机构实体：OBID（雅加达分行）
 */

export const ENTITY = {
  code:    'OBID',
  name:    'OBID（雅加达分行）',
  nameEn:  'OBID (Jakarta Branch)',
}

// ─── 业务单元 ─────────────────────────────────────────────────────────────────
export const BUSINESS_UNITS = [
  { code: 'OBID_T', name: '交易业务', nameEn: 'Trading'          },
  { code: 'OBID_I', name: '投资业务', nameEn: 'Investment'       },
  { code: 'OBID_L', name: '司库业务', nameEn: 'Treasury'         },
]

// ─── Book（业务组 / 交易台） ───────────────────────────────────────────────────
export const BOOKS = [
  { code: 'OBIDTFXD',  name: '代客外汇组',       nameEn: 'Client FX Desk',          businessUnit: 'OBID_T', accountType: '交易账户', accountTypeEn: 'Trading Account'  },
  { code: 'OBIDIFIR',  name: '投资业务',           nameEn: 'Investment',               businessUnit: 'OBID_I', accountType: '银行账户', accountTypeEn: 'Banking Account'  },
  { code: 'OBIDL_MML', name: '货币市场流动性组',   nameEn: 'Money Market Liquidity',   businessUnit: 'OBID_L', accountType: '银行账户', accountTypeEn: 'Banking Account'  },
]

// 账户性质翻译映射
export const ACCOUNT_TYPE_EN = {
  '交易账户': 'Trading Account',
  '银行账户': 'Banking Account',
  '其他':     'Other',
}

// ─── Portfolio（基础组合） ─────────────────────────────────────────────────────
export const PORTFOLIOS = [

  // ── OBID_T / OBIDTFXD ──
  {
    code:          'OBIDTFXD_D302',
    description:   '代客外汇交易（跨境联动业务）',
    descriptionEn: 'Client FX Trading (Cross-Border Linkage)',
    book:          'OBIDTFXD',
    businessUnit:  'OBID_T',
    accountType:   '交易账户',
    accountTypeEn: 'Trading Account',
    highlight:     false,
  },
  {
    code:          'OBIDTFXD_D303',
    description:   '人民币现钞交易',
    descriptionEn: 'CNY Banknotes Trading',
    book:          'OBIDTFXD',
    businessUnit:  'OBID_T',
    accountType:   '交易账户',
    accountTypeEn: 'Trading Account',
    highlight:     false,
  },
  {
    code:          'OBIDTFXD_D601',
    description:   '代客外汇交易wash组合',
    descriptionEn: 'Client FX Trading – Wash Portfolio',
    book:          'OBIDTFXD',
    businessUnit:  'OBID_T',
    accountType:   '交易账户',
    accountTypeEn: 'Trading Account',
    highlight:     true,
  },
  {
    code:          'OBIDTFXD_D501',
    description:   '代客外汇交易sales组合',
    descriptionEn: 'Client FX Trading – Sales Portfolio',
    book:          'OBIDTFXD',
    businessUnit:  'OBID_T',
    accountType:   '交易账户',
    accountTypeEn: 'Trading Account',
    highlight:     true,
  },
  {
    code:          'OBIDLFXR_D001',
    description:   '利润结转账户（每日结转利润）',
    descriptionEn: 'Profit Transfer Account (Daily P&L)',
    book:          'OBIDTFXD',
    businessUnit:  'OBID_T',
    accountType:   '交易账户',
    accountTypeEn: 'Trading Account',
    highlight:     false,
  },

  // ── OBID_I / OBIDIFIR ──
  {
    code:          'OBIDIFIR_H001',
    description:   '持有到期政府债券',
    descriptionEn: 'HTM Government Bonds',
    book:          'OBIDIFIR',
    businessUnit:  'OBID_I',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
  {
    code:          'OBIDIFIR_H002',
    description:   '持有到期公司债券',
    descriptionEn: 'HTM Corporate Bonds',
    book:          'OBIDIFIR',
    businessUnit:  'OBID_I',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     true,
  },

  // ── OBID_L / OBIDL_MML ──
  {
    code:          'OBIDLMML_D001',
    description:   '流动性管理拆入拆借',
    descriptionEn: 'Liquidity Mgmt – Interbank',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
  {
    code:          'OBIDLMML_D002',
    description:   '流动性管理掉期业务',
    descriptionEn: 'Liquidity Mgmt – FX Swaps',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
  {
    code:          'OBIDLMML_D003',
    description:   '央行票据 Certificate Bank Indonesia (SBI)',
    descriptionEn: 'Central Bank Bills (SBI)',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
  {
    code:          'OBIDLMML_D004',
    description:   '央行票据 Certificate Deposit Bank Indonesia (CDBI)',
    descriptionEn: 'Central Bank Certificates (CDBI)',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     true,
  },
  {
    code:          'OBIDLMML_D005',
    description:   'Term Deposit (TD)',
    descriptionEn: 'Term Deposit (TD)',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
  {
    code:          'OBIDLMML_D006',
    description:   'Deposit Facility (DF)',
    descriptionEn: 'Deposit Facility (DF)',
    book:          'OBIDL_MML',
    businessUnit:  'OBID_L',
    accountType:   '银行账户',
    accountTypeEn: 'Banking Account',
    highlight:     false,
  },
]

// ─── 便捷查询方法 ─────────────────────────────────────────────────────────────

/** 按 book code 获取该 book 下所有 portfolio */
export function getPortfoliosByBook(bookCode) {
  return PORTFOLIOS.filter(p => p.book === bookCode)
}

/** 按 businessUnit code 获取该业务单元下所有 book */
export function getBooksByBusinessUnit(buCode) {
  return BOOKS.filter(b => b.businessUnit === buCode)
}

/** 按 businessUnit code 获取该业务单元下所有 portfolio */
export function getPortfoliosByBusinessUnit(buCode) {
  return PORTFOLIOS.filter(p => p.businessUnit === buCode)
}

/** 获取所有 portfolio（扁平列表，含上层信息） */
export function getAllPortfolios() {
  return PORTFOLIOS.map(p => {
    const book = BOOKS.find(b => b.code === p.book) || {}
    const bu   = BUSINESS_UNITS.find(b => b.code === p.businessUnit) || {}
    return { ...p, bookName: book.name, businessUnitName: bu.name }
  })
}

/**
 * 树形结构：Entity → BusinessUnit[] → Book[] → Portfolio[]
 * 便于下拉树组件直接使用
 */
export function getBookTree() {
  return {
    ...ENTITY,
    children: BUSINESS_UNITS.map(bu => ({
      ...bu,
      children: getBooksByBusinessUnit(bu.code).map(book => ({
        ...book,
        children: getPortfoliosByBook(book.code),
      })),
    })),
  }
}
