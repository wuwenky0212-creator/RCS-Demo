#!/bin/bash
set -e
cd "/Users/wuwenky/Documents/Claude/Projects/DEMO FOR 雅加达/GIT-RG"

git remote set-url origin https://github.com/wuwenky0212-creator/RCS-Demo.git

git add \
  frontend/src/views/base-data/TaxRuleConfig.vue \
  frontend/src/locales/en-US.json \
  frontend/src/locales/zh-CN.json

git commit -m "fix: 税务规则配置-税基「名义本金」改为「资本利得」；新增按钮重复加号问题修复"

git push origin main && echo "✅ 推送完成，Vercel 将自动触发部署"
