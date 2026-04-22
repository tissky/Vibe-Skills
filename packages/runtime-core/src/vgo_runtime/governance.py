from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RuntimeGovernanceProfile:
    mode: str
    governance_scope: str = 'root_governed'
    freeze_before_requirement_doc: bool = True


def normalize_runtime_mode(mode: str | None) -> str:
    normalized = str(mode or 'interactive_governed').strip() or 'interactive_governed'
    if normalized != 'interactive_governed':
        raise ValueError(f'unsupported runtime mode: {mode}')
    return 'interactive_governed'


def choose_internal_grade(task_type: str, task: str | None = None) -> str:
    normalized = str(task_type).strip().lower()
    task_lower = str(task or '').strip().lower()
    xl_markers = (
        'multi-agent',
        'parallel',
        'wave',
        'batch',
        'autonomous',
        'benchmark',
        'end-to-end',
        'e2e',
        'cross-host',
        'multi-host',
        'host-native',
        'install to runtime',
        'runtime to install',
        'from install to runtime',
        '从安装到运行',
        '全链路',
        '端到端',
    )
    l_markers = (
        'debug',
        'bug',
        'fix',
        'repair',
        'patch',
        'review',
        'code review',
        'implement',
        'build',
        'upgrade',
        'update',
        'modify',
        'change',
        'install',
        'integrat',
        'router',
        'routing',
        'runtime',
        'workflow',
        'contract',
        'gate',
        'regression',
        'verification',
        'threshold',
        'confidence',
        'classification',
        'scoring',
        'heuristic',
        'windows',
        'claude',
        'codex',
        '修复',
        '修改',
        '安装',
        '运行时',
        '路由',
        '回归',
        '验证',
        '阈值',
        '置信度',
        '分类',
        '评分',
    )

    if task_lower and any(marker in task_lower for marker in xl_markers):
        return 'XL'
    if normalized in {'coding', 'debug', 'review', 'research'}:
        return 'L'
    if task_lower and any(marker in task_lower for marker in l_markers):
        return 'L'
    if task and len(str(task)) > 180:
        return 'L'
    return 'M'


def build_governance_profile(mode: str | None, *, governance_scope: str = 'root_governed') -> RuntimeGovernanceProfile:
    return RuntimeGovernanceProfile(
        mode=normalize_runtime_mode(mode),
        governance_scope=governance_scope or 'root_governed',
    )
