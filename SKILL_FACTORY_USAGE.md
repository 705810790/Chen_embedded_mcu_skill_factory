# Embedded MCU Skill Factory Usage

Use this folder to generate a new Codex skill skeleton for an MCU ecosystem.

## Generate From Existing Adapter

```powershell
python scripts\create_mcu_skill.py --adapter adapters\stm32-cubeide.json --out E:\AI agent\Skill_合集
python scripts\create_mcu_skill.py --adapter adapters\esp-idf.json --out E:\AI agent\Skill_合集
python scripts\create_mcu_skill.py --adapter adapters\wch-mounriver.json --out E:\AI agent\Skill_合集
```

## Create A New Adapter

Copy one JSON file under `adapters\`, then change:

- `skill_name`
- `display_name`
- `ecosystem`
- `tool_script`
- `description`
- `adapter_notes`

Then run `create_mcu_skill.py` again.

## Implementation Rule

The generated tool is a skeleton. Replace the placeholder backend with real logic, but keep the command shape stable:

```text
doctor
inspect
make
remake
rebuild
clean
download
config-example
```

Keep `build` as a compatibility alias for `make`, and `flash` as a compatibility alias for `download`.

Always support `--dry-run` for make/remake/download.
