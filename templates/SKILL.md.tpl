---
name: {{skill_name}}
description: {{description}}
---

# {{display_name}}

Use this skill for {{ecosystem}} embedded MCU projects. Prefer the bundled command-line helper over guessing IDE or toolchain internals.

## Tool

Run:

```powershell
python scripts\{{tool_script}} --help
```

The helper follows a common embedded MCU workflow:

```text
doctor -> inspect -> make -> download
```

Command aliases:

```text
make      compile
remake    clean and compile again
rebuild   alias for remake
download  program firmware to the target
build     compatibility alias for make
flash     compatibility alias for download
```

## Path Policy

Do not hard-code private project paths or install paths in this skill. Resolve paths in this order:

1. CLI arguments.
2. Local config file.
3. Environment variables.
4. Common install paths.
5. `PATH`.

Generate a local config example:

```powershell
python scripts\{{tool_script}} config-example
```

## Standard Workflow

Check tools:

```powershell
python scripts\{{tool_script}} doctor
```

Inspect project:

```powershell
python scripts\{{tool_script}} inspect
```

Preview make:

```powershell
python scripts\{{tool_script}} make --dry-run
```

Make:

```powershell
python scripts\{{tool_script}} make
```

Remake:

```powershell
python scripts\{{tool_script}} remake
```

Preview download:

```powershell
python scripts\{{tool_script}} download --dry-run
```

Download:

```powershell
python scripts\{{tool_script}} download
```

## Adapter Notes

{{adapter_notes}}

## AI Rules

- Run `doctor` before build or flash.
- Run `inspect` before editing build files.
- Prefer the native command-line equivalent of the IDE build button.
- Treat `--dry-run` as the first step for flash.
- Do not claim build or flash success without checking command exit status and final output.
- If hardware is missing, report the hardware/probe error separately from build errors.
