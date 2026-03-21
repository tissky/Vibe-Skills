# 安装路径：高级 host / lane 参考

> 大多数用户现在先看两条主路径：
> - [`one-click-install-release-copy.md`](./one-click-install-release-copy.md)
> - [`manual-copy-install.md`](./manual-copy-install.md)

这条路的默认答案仍然是：**先走 `codex` lane**。

因为当前只有它具备完整的 governed-with-constraints install/check/bootstrap。

## 现在的 lane 区分

- `codex`：正式推荐满血路径
- `claude-code`：preview scaffold 路径
- `generic` / `opencode`：runtime-core-only 路径

因此，推荐满血不再等于“所有 host 都走同一条脚本”，而是：

- 正式闭环需求走 `codex`
- 预览接入 Claude Code 走 `claude-code`
- 只要 canonical runtime-core 就走 `generic`

## 推荐命令

### Codex

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

### Claude Code 预览

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

### Generic Runtime-Core

```powershell
pwsh -File .\install.ps1 -HostId generic -Profile full
pwsh -File .\check.ps1 -HostId generic -Profile full
```

```bash
bash ./install.sh --host generic --profile full
bash ./check.sh --host generic --profile full
```

## 必须说清楚的边界

### Codex

- repo 会尽量完成 runtime、settings、MCP materialization 和 deep doctor
- 但在线能力所需的 provider secrets 仍有 host-managed 部分
- 对 Codex，不要把未经官方证明的 hook/plugin 面当成标准安装要求
- Codex 当前应只围绕 `~/.codex` 本地设置、官方 MCP 注册和可选 CLI 依赖来增强
- 如果需要在线模型能力，优先在 `~/.codex/settings.json` 的 `env` 下或本地环境变量里配置：
  - `OPENAI_API_KEY`
  - `OPENAI_BASE_URL`
  - 以及按需使用的其他本地 provider 变量
- 不要要求用户把这些密钥直接贴到聊天里

### Claude Code

- repo 现在会 scaffold preview `settings.vibe.preview.json` 和 hooks
- repo 不会覆盖真实的 `settings.json`
- 但这不是 Claude Code full closure
- 启用 AI 治理层时，用户应自己打开 `~/.claude/settings.json`，只在 `env` 下补充所需字段
- 常见需要本地填写的字段：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
  - 如宿主连接需要，再补 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`
- 允许参考 `~/.claude/settings.vibe.preview.json`，但不能整文件覆盖
- 不要要求用户把 API key 贴到聊天里

### Generic / OpenCode

- repo 只安装 runtime-core
- 默认写到中性目录，不写宿主专属状态
- 用户必须自己在目标 agent 中配置 URL、API key、model

## AI 治理层提示

对 `claude-code`、`generic`、`opencode` 这些非 governed Codex lane，AI 智能治理层必须提醒用户三件事：

- 你需要自己在本地宿主配置或本地环境变量里填写 `url`
- 你需要自己在本地宿主配置或本地环境变量里填写 `apikey`
- 你需要自己在本地宿主配置或本地环境变量里填写 `model`
- 不要要求用户在聊天里直接提供这些值

如果这些值没有在本地配置好，不能把环境描述成“已完成 online readiness”。
