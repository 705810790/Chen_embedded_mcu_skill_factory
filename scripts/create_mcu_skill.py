#!/usr/bin/env python3
"""Generate a Codex skill skeleton for an embedded MCU build/flash workflow."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "SKILL.md.tpl"


DEFAULTS: dict[str, Any] = {
    "skill_name": "example-mcu-skill",
    "display_name": "Example MCU Skill",
    "ecosystem": "an embedded MCU",
    "tool_script": "mcu_tool.py",
    "description": "Build, inspect, and flash embedded MCU projects. Use when Codex needs to operate a vendor IDE or command-line toolchain through a deterministic helper.",
    "adapter_notes": "Fill in the native build and flash backend for this MCU ecosystem.",
}


def slug(value: str) -> str:
    text = value.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "mcu-skill"


def render(text: str, data: dict[str, Any]) -> str:
    for key, value in data.items():
        text = text.replace("{{" + key + "}}", str(value))
    return text


def load_adapter(path: Path | None) -> dict[str, Any]:
    data = dict(DEFAULTS)
    if path:
        data.update(json.loads(path.read_text(encoding="utf-8")))
    data["skill_name"] = slug(data["skill_name"])
    if not data["tool_script"].endswith(".py"):
        data["tool_script"] += ".py"
    return data


def write_tool_stub(path: Path, data: dict[str, Any]) -> None:
    content = f'''#!/usr/bin/env python3
"""
Tool stub for {data["display_name"]}.

Replace backend placeholders with the ecosystem-specific implementation while
keeping the public command shape stable: doctor, inspect, make, remake, clean,
download, config-example. build and flash are compatibility aliases.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def command_config_example(args):
    print(json.dumps({{"project": "D:/path/to/project", "tool_root": "C:/path/to/tool"}}, indent=2))
    return 0


def not_implemented(name):
    def inner(args):
        print(f"{{name}} is not implemented for this adapter yet.")
        return 2
    return inner


def build_parser():
    parser = argparse.ArgumentParser(description="{data["display_name"]} helper")
    parser.add_argument("--project", type=Path, default=Path.cwd(), help="project path")
    parser.add_argument("--tool-root", type=Path, default=None, help="vendor tool root")
    parser.add_argument("--config-file", type=Path, default=None, help="local JSON config")
    parser.add_argument("--json", action="store_true", help="emit JSON where supported")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("doctor", "inspect", "make", "remake", "rebuild", "clean", "download", "build", "flash"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--dry-run", action="store_true", help="print command without running it")
        cmd.set_defaults(func=not_implemented(name))
    sub.add_parser("config-example").set_defaults(func=command_config_example)
    return parser


def main():
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
'''
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an embedded MCU Codex skill skeleton.")
    parser.add_argument("--adapter", type=Path, default=None, help="adapter JSON file")
    parser.add_argument("--out", type=Path, required=True, help="output parent directory")
    args = parser.parse_args()

    data = load_adapter(args.adapter)
    skill_dir = args.out / data["skill_name"]
    (skill_dir / "scripts").mkdir(parents=True, exist_ok=True)
    (skill_dir / "references").mkdir(parents=True, exist_ok=True)

    skill_text = render(TEMPLATE.read_text(encoding="utf-8"), data)
    (skill_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")
    (skill_dir / "references" / "adapter-contract.md").write_text(
        (ROOT / "references" / "adapter-contract.md").read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    write_tool_stub(skill_dir / "scripts" / data["tool_script"], data)
    print(skill_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
