# 提示词安装（默认推荐）

这是当前面向大多数用户的默认安装方式。

核心思路很简单：

1. 把下面这段提示词复制给你的 AI 助手
2. 让它先问你要安装到哪个代理
3. 再按对应代理选择正确的安装路径

## 复制给 AI 的提示词

```text
你现在是我的 VibeSkills 安装助手。
仓库地址：https://github.com/foryourhealth111-pixel/Vibe-Skills

在执行任何安装命令前，你必须先问我：
“你要把 VibeSkills 安装到什么代理里？可选：codex、claude-code、opencode、其他代理（generic）。”

规则：
1. 在我明确回答目标代理之前，不要开始安装。
2. 先判断当前系统是 Windows 还是 Linux / macOS，并使用对应命令格式。
3. 如果我选择 `codex`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host codex`
   - 然后执行 `bash ./check.sh --host codex --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 不要让我安装 `hookify`、`everything-claude-code`、`claude-code-settings`、`ralph-loop` 这类未经官方 Codex 能力证明的 hook/plugin 面。
   - 只围绕 Codex 当前可公开证明的本地 settings、MCP 和 CLI 依赖给建议。
   - 如果需要在线模型能力，告诉我去 `~/.codex/settings.json` 的 `env` 或本地环境变量里配置 `OPENAI_API_KEY`、`OPENAI_BASE_URL` 等值，不要让我把密钥发到聊天里。
4. 如果我选择 `claude-code`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host claude-code`
   - 然后执行 `bash ./check.sh --host claude-code --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这只是 preview scaffold，不是 full closure。
   - 明确告诉我：安装器只会写 `settings.vibe.preview.json` 作为示例，不会覆盖真实 `settings.json`。
   - 不要要求我把 API key 直接发到聊天里。
   - 应该告诉我打开 `~/.claude/settings.json`，只在 `env` 下补充需要的字段，并保留我原有的设置。
   - 如果需要参考示例，只能让我参考 `~/.claude/settings.vibe.preview.json`，不能整文件覆盖。
5. 如果我选择 `opencode`：
   - Linux / macOS 使用 `bash ./scripts/bootstrap/one-shot-setup.sh --host opencode`
   - 然后执行 `bash ./check.sh --host opencode --profile full --deep`
   - Windows 使用对应的 `pwsh` 命令。
   - 明确告诉我：这是 runtime-core 路径，不是宿主闭环。
6. 如果我选择“其他代理”或不在支持列表内：
   - 优先使用 `generic` lane，或者改为指导我走手动复制安装
   - 不要伪装成已经完成宿主级接入。
7. 对于 `claude-code`、`opencode`、`generic` 这些非 Codex lane，你必须先明确提醒我：
   - `url`、`apikey`、`model` 必须由我自己在本地宿主配置或本地环境变量里填写
   - 不要要求我在聊天里粘贴这些敏感值
   - 如果这三项没有在本地配置好，不能把环境描述成已完成 online readiness。
8. 安装完成后，请用简洁中文告诉我：
   - 目标代理
   - 实际执行的命令
   - 已完成的部分
   - 仍需我手动处理的部分
9. 不要把宿主插件、MCP 注册、provider 凭据伪装成已经自动完成。
```

## 这条路径适合谁

- 想让 AI 帮你判断安装路径的人
- 不想先研究 install matrix 的人
- 想先装起来，再看哪些能力还要自己补的人

## 这条路径会帮你做到什么

- 先确认目标代理，避免默认装错 lane
- 自动选择 `codex` / `claude-code` / `opencode` / `generic`
- 跑安装和检查命令
- 诚实告诉你哪些还是宿主侧工作

## 它不会假装替你完成什么

下面这些仍然可能是用户侧或宿主侧动作：

- 宿主本地配置填写
- MCP 注册与授权
- `url` / `apikey` / `model` 的本地填写
- 非 Codex lane 的宿主级闭环接入

## 第二条主路径

如果你不想让 AI 执行安装，或者当前环境离线、无管理员权限、宿主不在支持列表里，请改看：

- [`manual-copy-install.md`](./manual-copy-install.md)

## 高级参考

如果你要看更细的 lane truth 和高级安装边界，再看：

- [`recommended-full-path.md`](./recommended-full-path.md)
- [`../cold-start-install-paths.md`](../cold-start-install-paths.md)
