# GitHub 提交与 iPhone 预览说明

## 1. 必填信息

学习通答案处必须写：

- GitHub 仓库链接（完整 URL）
- 本人 GitHub 账号名称

缺任意一项，期末成绩计 0 分。提交前请把下面两处替换为真实信息：

- `README.md` 第 10 节
- `report/移动应用开发基础-20240313140-章瑞-期末大作业.docx` 中表 1.1 的 GitHub 账号 / 仓库链接

## 2. 用 GitHub Desktop 上传（无需命令行）

1. 安装 GitHub Desktop，登录本人账号。
2. `File > Add local repository`，选择本目录。
3. 仓库已经包含本地 Git 历史；点击 `Publish repository`。
4. 仓库名建议：`fanzhendong-memory`，可见性选 Public（老师需核查）。
5. 发布后复制仓库 URL，填入 README 与报告。

## 3. 用 Git 命令行上传

```bash
git remote add origin https://github.com/<你的用户名>/fanzhendong-memory.git
git branch -M main
git push -u origin main
```

## 4. 开启 GitHub Pages（iPhone 安装 PWA）

1. 仓库 `Settings > Pages`。
2. Build and deployment 选择 **GitHub Actions**。
3. 推送后等待 `Deploy PWA to GitHub Pages` 完成。
4. 得到 `https://<你的用户名>.github.io/fanzhendong-memory/`。
5. iPhone Safari 打开该地址 → 分享 → **添加到主屏幕**。

> 注意：这是 PWA，不是原生 iOS `.ipa`。HarmonyOS `.hap` 不能安装到 iPhone。
