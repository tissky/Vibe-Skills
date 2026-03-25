# Host Plugin and Host Configuration Policy

This document answers only three questions:

- which hosts are on the current public support surface
- what the repo currently handles automatically
- what still must be completed locally by the host side

## Current Public Surface

- `codex`
- `claude-code`
- `cursor`
- `windsurf`

Other agents should not currently be described as having an official install closure.

## Global Principle

- install the repo-governed payload first
- add host-local configuration only as needed
- if a capability is not stably, publicly, and verifiably owned by the repo, do not write it as a default install requirement

## Codex

- currently the strongest path
- guidance stays centered on local settings, MCP, and optional CLI enhancements
- hooks remain frozen; that is not an install failure

## Claude Code

- supported install-and-use path
- not integrated by “adding a pile of host plugins”
- does not overwrite the real `~/.claude/settings.json`
- hooks remain frozen; that is not an install failure

## Cursor

- supported install-and-use path
- does not overwrite the real `~/.cursor/settings.json`
- Cursor-native plugins, settings, and extension surfaces remain managed on the Cursor side
- hooks remain frozen; that is not an install failure

## Windsurf

- supported install-and-use path with runtime-adapter integration
- default root is `~/.codeium/windsurf`
- the repo currently owns only shared runtime payload plus optional materialization of `mcp_config.json` and `global_workflows/`
- Windsurf-native local settings remain managed on the Windsurf side

## Recommended Community Wording

- the current version supports `codex`, `claude-code`, `cursor`, and `windsurf`
- `codex` follows the governed path
- `claude-code` and `cursor` have a supported install-and-use path
- `windsurf` has a supported install-and-use path with runtime-adapter integration
- hooks remain frozen across the current public surface; that is not a user install failure
- provider `url` / `apikey` / `model` values stay local and should not be pasted into chat
