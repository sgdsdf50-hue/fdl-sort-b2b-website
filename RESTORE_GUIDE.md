# FDL SORT 全站恢复指南

本指南说明如何将网站 fdlsorterai.com 恢复到 2026-06-25 11:22 的黄金备份状态。

## 1. 代码恢复 (GitHub)
如果 `main` 分支被意外修改或破坏，请执行：
```bash
git fetch --all
git reset --hard fdlsorterai-golden-backup-2026-06-25-1122
git push origin main --force
```

## 2. Vercel 部署恢复
Vercel 会在上述 Git 推送后自动构建。若需手动指向特定部署：
1. 进入 Vercel 控制台。
2. 找到与 SHA `f746f77` 对应的部署。
3. 点击 "Promote to Production"。

## 3. R2 资源恢复
若 R2 资源损坏，请从备份压缩包重新上传至对应 Bucket。

## 4. 验证步骤
恢复后请对照 `restore-checklist.md` 进行逐项检查。
