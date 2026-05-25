#!/bin/bash
# 删除残留的 git 锁文件（由沙箱 git add 遗留）
LOCK="/Users/wuwenky/Documents/Claude/Projects/DEMO FOR 雅加达/GIT-RG/.git/index.lock"
if [ -f "$LOCK" ]; then
  rm "$LOCK" && echo "✓ 已清理 index.lock"
fi

cd "/Users/wuwenky/Documents/Claude/Projects/DEMO FOR 雅加达/GIT-RG"

git add \
  frontend/package.json \
  frontend/package-lock.json \
  frontend/src/locales/en-US.json \
  frontend/src/locales/zh-CN.json \
  frontend/src/views/pnl-attribution/AttributionReport.vue

git commit -m "feat: 实现归因分析报告导出功能

- 安装 xlsx (SheetJS) 库
- 替换 exportTable() 占位函数，实现真实 Excel 导出
  - 树形数据递归展平，层级缩进可视
  - 双行表头 + 列分组合并单元格（市场数据×4、交易活动×4、PL结果×7）
  - 自动合计行，数值列求和
  - 列宽自适应，文件名含情景名和日期
- 新增 i18n key: exportSuccess（中英文）"

git push origin main && echo "✅ 推送完成"
