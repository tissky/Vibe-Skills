# 冷启动安装路径

这份文档只回答冷启动阶段最重要的问题：当前支持哪个宿主、该走哪条路径。

## 一句话结论

暂时只支持两个宿主：

- `codex`
- `claude-code`

其中：

- `codex`：正式推荐路径
- `claude-code`：预览指导路径

如果你要装到其他代理，当前版本应视为不支持，而不是改走隐藏 lane。

## 路径一：Codex

Windows:

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId codex
pwsh -File .\check.ps1 -HostId codex -Profile full -Deep
```

Linux / macOS:

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host codex
bash ./check.sh --host codex --profile full --deep
```

你会得到：

- governed payload
- 可选的 provider seed 写入
- MCP active profile 物化
- deep health check

你不会得到：

- hook 安装（当前作者仍在处理兼容性，所以这个安装面暂未开放；这不是你的安装失败）

## Codex 的正确后续动作

- 打开 `~/.codex/settings.json`
- 如果只是基础在线 provider，先看 `env` 下的 `OPENAI_API_KEY`、`OPENAI_BASE_URL`
- 如果还要启用治理 AI 在线层，可按需再补这些可选增强设置：
  - `VCO_AI_PROVIDER_URL`
  - `VCO_AI_PROVIDER_API_KEY`
  - `VCO_AI_PROVIDER_MODEL`
- `OPENAI_*` 不等于 `VCO_AI_PROVIDER_*`
- 不要把密钥贴到聊天里
- 未补的官方 MCP 注册或治理 AI 在线层配置，默认都应视为按需启用的增强项

## 路径二：Claude Code

Windows:

```powershell
pwsh -File .\scripts\bootstrap\one-shot-setup.ps1 -HostId claude-code
pwsh -File .\check.ps1 -HostId claude-code -Profile full -Deep
```

Linux / macOS:

```bash
bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code
bash ./check.sh --host claude-code --profile full --deep
```

你会得到：

- runtime payload
- preview guidance health check

你不会得到：

- 自动覆盖真实 `settings.json`
- hook 安装（当前作者仍在处理兼容性，所以这个安装面暂未开放；这不是你的安装失败）
- 自动插件 provision
- 自动 MCP 宿主注册
- 自动 provider secret 写入

## Claude Code 的正确后续动作

- 打开 `~/.claude/settings.json`
- 只在 `env` 下补你需要的字段
- 常见是 `VCO_AI_PROVIDER_URL`、`VCO_AI_PROVIDER_API_KEY`、`VCO_AI_PROVIDER_MODEL`
- 如宿主连接需要，再补 `ANTHROPIC_BASE_URL`、`ANTHROPIC_AUTH_TOKEN`
- 当前版本不会再生成 `settings.vibe.preview.json`
- 不要把密钥贴到聊天里
- 未补的 MCP、provider 或治理 AI 在线层配置，默认都应视为按需启用的增强项

## 冷启动阶段最重要的边界

- `HostId` / `--host` 决定宿主语义，不是路径名决定
- 当前没有其他宿主的公开安装入口
- hook 安装面当前仍在作者处理兼容性，所以暂未开放；这表示边界尚未开放，不表示安装出错
- 如果本地还没配好治理 AI 的 `url` / `apikey` / `model`，不能描述成“已完成治理 AI online readiness”
- 对 `codex`，`OPENAI_*` 已配置最多只能说明基础在线 provider 已就绪，不能顺带声称治理 AI 在线层也已就绪
- 未补的官方 MCP 注册、`VCO_AI_PROVIDER_*` 或其他本地 provider 配置，应优先表述成可选增强设置，而不是安装告警
