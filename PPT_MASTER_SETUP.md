# PPT Master 项目级安装与验证

## 安装来源

- 官方仓库：https://github.com/hugohe3/ppt-master
- 版本：6.8.0
- 上游提交：`5e8856be0da8e6bc85c4aa28acc614478f7b7137`
- 项目级位置：`.agents/skills/ppt-master/`
- 官方 README 推荐的安装器命令（已执行）：

```bash
DISABLE_TELEMETRY=1 npx --yes skills add hugohe3/ppt-master --skill ppt-master --agent codex --copy --yes
```

已完整复制 13,051 个文件，并与上述上游提交逐文件比对一致。保留上游许可证、署名、脚本、工作流、参考文档和模板；未修改上游 Skill。安装器元数据保存在 `skills-lock.json`。更新时使用安装器并重新审查，勿在当前项目运行上游 `update_repo.py`（该脚本面向独立的上游 Git 克隆）。

## 审查范围

已读取官方 README、SKILL.md、安装说明和依赖清单，检查目录、符号链接、大文件及入口/完整性检查/更新脚本。未发现明显的恶意命令或安装钩子，未发现符号链接；这属于静态抽查，不是完整安全审计。官方依赖均通过启用 TLS 验证的 pip 安装到独立虚拟环境，没有执行远程 shell 安装脚本。

Skill 包含可选的联网图片、网页和语音工具以及本地 Web 编辑器，本次没有启动这些功能、配置凭据或调用外部 AI 服务。脚本会记录项目级命令输出到 `validation/workflow.log`，勿通过命令传入秘密。PyMuPDF 的 AGPL/商业许可说明见上游 requirements.txt；本仓库只保存依赖清单，不分发虚拟环境。

## 环境恢复

从当前项目根目录执行，复用现有检出；无需新建 Git worktree。

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-ppt-master.lock.txt
.venv/bin/python -m pip check
.venv/bin/python .agents/skills/ppt-master/scripts/attribution_guard.py
```

已验证 Python 3.12.14、python-pptx 1.0.2；完整依赖版本保存在 `requirements-ppt-master.lock.txt`。`.venv/`、字节码和真实 `.env` 文件不提交 Git。

当前云环境已有 `soffice`（LibreOfficeDev 26.8 alpha）、`pdftoppm`、`pdftotext` 和 Noto CJK 中文字体。换用其他基础环境时需另行提供 LibreOffice、Poppler 与中文字体。安装依赖及访问 GitHub 需要平台授权网络模式，保持继承的代理与 TLS 配置。

在当前仓库目录启动新的 Codex 任务，以便扫描项目级 Skill。当前任务已通过直接读取 SKILL.md 和调用脚本使用它，但尚未验证新任务中的自动识别；无需重启操作系统。

## 一页中文测试

测试源为 `output/skill_smoke_20261101/svg_output/01_test.svg`，仅用于安装验证，不是正式辩论 PPT。

从项目根目录重建：

```bash
.venv/bin/python .agents/skills/ppt-master/scripts/svg_quality_checker.py output/skill_smoke_20261101 --quick-generate --canonical-authoring --stage final --json
.venv/bin/python .agents/skills/ppt-master/scripts/svg_to_pptx.py output/skill_smoke_20261101 --quick-generate --no-notes -o output/ppt-master-smoke.pptx
soffice --headless --convert-to pdf --outdir output output/ppt-master-smoke.pptx
pdftoppm -png -singlefile -scale-to 1280 output/ppt-master-smoke.pdf output/ppt-master-smoke
pdftotext output/ppt-master-smoke.pdf -
```

验证结果：

- 完整性检查和 `pip check` 通过。
- SVG 最终检查：1 页通过，0 错误、0 警告；PPTX postflight 通过。
- 通过 python-pptx 重新读取，确认 1 页、4 个原生文字框（包含中文标题和正文）、2 个原生形状，无图片对象；PPTX ZIP 完整性通过。
- LibreOffice 成功导出 PDF，中文文本提取完整，PNG 预览已人工检查。
- 初始中英混排测试句在当前 LibreOfficeDev 预览中出现部分中文缺字，而 PPTX XML 内文字完整。最终测试使用全中文句子并通过预览。中英混排兼容性仍需在目标 PowerPoint/稳定版 LibreOffice 中复测，不能宣称已通过。
- 字体缓存曾提示 `Fontconfig error: No writable cache directories`，未阻止本次导出。

本测试使用基本圆角矩形和椭圆验证可编辑性，无需预设复杂形状、图标、渐变、滤镜或逐字强调。图片生成、素材搜索、语音、动画及正式演示文稿制作未验证。
