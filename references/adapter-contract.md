# Embedded MCU Adapter Contract

Use this contract when creating a build/flash skill for an embedded MCU ecosystem.

## Required CLI Shape

Every generated tool should expose these commands:

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

Compatibility aliases are recommended:

```text
build -> make
flash -> download
```

Recommended shared options:

```text
--project PATH
--tool-root PATH
--config-file PATH
--json
--dry-run
```

Backend-specific aliases are allowed, for example `--mrs`, `--cubeide`, `--idf`, `--openocd`, or `--probe`.

## Command Semantics

- `doctor`: Locate required tools and report missing pieces without modifying the project.
- `inspect`: Read project metadata and locate artifacts.
- `make`: Compile using the closest command-line equivalent of the IDE build button.
- `remake`: Clean/rebuild using the native backend.
- `rebuild`: Alias for `remake`.
- `clean`: Clean using the native build backend.
- `download`: Program a built artifact. Support `--dry-run` even when hardware is unavailable.
- `config-example`: Print local configuration JSON.

## Structured Output

When `--json` is supported, include:

```json
{
  "status": "success|blocked|failed",
  "project_profile": {
    "workspace_root": "",
    "workspace_os": "",
    "build_system": "",
    "toolchain": "",
    "target_mcu": "",
    "artifact_path": "",
    "artifact_kind": ""
  },
  "tools": {},
  "diagnostics": []
}
```

## Path Policy

Do not hard-code a user's private project path or install path in a public skill.

Resolve paths in this order:

1. CLI arguments.
2. Local config file such as `.embedded_mcu_tool.json`.
3. Environment variables.
4. Common install paths.
5. `PATH`.

Local config files with personal paths should not be committed to public repositories.

## Backend Examples

- MounRiver/WCH: Use Eclipse CDT headless build via `eclipsec.exe`, then WCH OpenOCD for flash.
- STM32CubeIDE: Use `stm32cubeidec` or Eclipse CDT headless build, then STM32CubeProgrammer CLI or OpenOCD.
- ESP-IDF: Use `idf.py build`, `idf.py flash`, and `idf.py monitor`.
- PlatformIO: Use `pio run`, `pio run -t upload`, and `pio device monitor`.
- Keil MDK: Use `UV4.exe -b` for build and Keil/ULINK/J-Link/OpenOCD tools for flash.
