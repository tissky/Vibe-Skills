from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'packages' / 'contracts' / 'src'
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from vgo_contracts.adapter_descriptor import AdapterDescriptor


def test_adapter_descriptor_requires_id() -> None:
    descriptor = AdapterDescriptor(
        id='codex',
        default_target_root='~/.codex',
        default_target_root_env='CODEX_HOME',
        default_target_root_kind='host-home',
    )
    assert descriptor.id == 'codex'
    assert descriptor.default_target_root == '~/.codex'
    assert descriptor.default_target_root_env == 'CODEX_HOME'
    assert descriptor.default_target_root_kind == 'host-home'


def test_adapter_descriptor_normalizes_optional_target_root_metadata() -> None:
    descriptor = AdapterDescriptor(
        id=' codex ',
        default_target_root=' ~/.codex ',
        default_target_root_env=' CODEX_HOME ',
        default_target_root_kind=' host-home ',
    )

    assert descriptor.id == 'codex'
    assert descriptor.default_target_root == '~/.codex'
    assert descriptor.default_target_root_env == 'CODEX_HOME'
    assert descriptor.default_target_root_kind == 'host-home'


def test_host_profiles_expose_discoverable_entries_as_presentational_surface() -> None:
    import json

    profiles = [
        ROOT / 'adapters' / 'codex' / 'host-profile.json',
        ROOT / 'adapters' / 'claude-code' / 'host-profile.json',
        ROOT / 'adapters' / 'cursor' / 'host-profile.json',
        ROOT / 'adapters' / 'windsurf' / 'host-profile.json',
        ROOT / 'adapters' / 'openclaw' / 'host-profile.json',
        ROOT / 'adapters' / 'opencode' / 'host-profile.json',
    ]

    for profile_path in profiles:
        payload = json.loads(profile_path.read_text(encoding='utf-8'))
        discoverable_entries = payload['discoverable_entries']
        assert discoverable_entries['shared_source'] == 'config/vibe-entry-surfaces.json'
        assert discoverable_entries['authority_owner'] == 'vibe'
        assert discoverable_entries['presentational_only'] is True
