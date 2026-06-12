# Chen_embedded_mcu_skill_factory

Chen_embedded_mcu_skill_factory 是一个面向 AI 的嵌入式 MCU Skill 生成器。它把不同芯片生态中的编译、重新编译、下载、工程检查抽象成同一套命令：`doctor / inspect / make / remake / download`，用于快速组装 STM32、ESP32、WCH、PlatformIO、Keil、IAR 等开发流程 Skill。

## 背景

不同 MCU 生态的工具链差异很大：STM32CubeIDE、ESP-IDF、PlatformIO、Keil、IAR、MounRiver Studio 都有自己的工程结构、编译命令和下载工具。

但从 AI 自动化角度看，它们需要的能力高度相似：

- 检查工具链是否存在
- 识别工程结构和目标芯片
- 编译或重新编译
- 找到 `.elf/.hex/.bin` 等产物
- 下载烧录
- 在没有硬件时 dry-run 命令

Chen_embedded_mcu_skill_factory 的目标就是把这些共性抽象成模板，让以后制作新的 MCU Skill 时不用重新设计结构，只需要替换对应生态的 adapter 和工具后端。

## 适用场景

- 想为新的 MCU 生态制作 Codex Skill
- 想统一 STM32、ESP32、WCH、PlatformIO 等工具入口
- 想让 AI 用同一种习惯执行 `make / remake / download`
- 想把厂商 IDE 的编译下载流程封装成脚本
- 想创建可分享、无个人路径硬编码的 Skill

## 一键安装

安装到当前 AI 环境：

```powershell
帮我安装 https://github.com/705810790/Chen_embedded_mcu_skill_factory.git 的skill
```

如果需要设置为全局在任意文件夹调用的 skill：

```powershell
帮我安装 https://github.com/705810790/Chen_embedded_mcu_skill_factory.git 的skill 到全局目录下
```

## 项目结构

```text
Chen_embedded_mcu_skill_factory/
├── README.md
├── SKILL_FACTORY_USAGE.md           # 使用说明
├── adapters/
│   ├── esp-idf.json                 # ESP-IDF 示例
│   ├── stm32-cubeide.json           # STM32CubeIDE 示例
│   └── wch-mounriver.json           # WCH/MounRiver 示例
├── references/
│   └── adapter-contract.md          # 通用命令协议
├── scripts/
│   └── create_mcu_skill.py          # Skill 骨架生成器
└── templates/
    └── SKILL.md.tpl                 # SKILL.md 模板
```

## 快速开始

进入目录：

```powershell
cd "E:\AI agent\Skill_合集\Chen_embedded_mcu_skill_factory"
```

生成 STM32CubeIDE Skill 骨架：

```powershell
python scripts\create_mcu_skill.py --adapter adapters\stm32-cubeide.json --out "E:\AI agent\Skill_合集"
```

生成 ESP-IDF Skill 骨架：

```powershell
python scripts\create_mcu_skill.py --adapter adapters\esp-idf.json --out "E:\AI agent\Skill_合集"
```

生成 WCH/MounRiver Skill 骨架：

```powershell
python scripts\create_mcu_skill.py --adapter adapters\wch-mounriver.json --out "E:\AI agent\Skill_合集"
```

## AI 推荐用法

让 AI 为某个新生态制作 Skill 时，推荐先让 AI 读取：

```text
references/adapter-contract.md
templates/SKILL.md.tpl
adapters/xxx.json
```

再要求 AI 实现对应工具后端。

示例提示：

```text
使用 Chen_embedded_mcu_skill_factory，为 STM32CubeIDE 工程生成一个 Skill。命令保持 doctor / inspect / make / remake / download，并把 build 作为 make 的兼容别名，flash 作为 download 的兼容别名。
```

规则：

- 生成器只生成骨架，不等于已经实现真实编译下载。
- 真实后端需要根据具体生态补充，例如 `idf.py`、`stm32cubeidec`、`STM32_Programmer_CLI`、`pio`、`UV4.exe`。
- 所有新工具都应该支持 `--dry-run`。
- 不要在 Skill 中写死个人工程路径和安装路径。

## 通用命令协议

所有生成的工具都应该尽量支持：

```powershell
python scripts\xxx_tool.py doctor
python scripts\xxx_tool.py inspect
python scripts\xxx_tool.py make
python scripts\xxx_tool.py remake
python scripts\xxx_tool.py clean
python scripts\xxx_tool.py download --dry-run
python scripts\xxx_tool.py download
python scripts\xxx_tool.py config-example
```

兼容别名：

```powershell
python scripts\xxx_tool.py build       # 等同于 make
python scripts\xxx_tool.py rebuild     # 等同于 remake
python scripts\xxx_tool.py flash       # 等同于 download
```

## 新增生态

复制一个 adapter：

```powershell
copy adapters\stm32-cubeide.json adapters\my-chip.json
```

修改字段：

```json
{
  "skill_name": "my-chip-mcu",
  "display_name": "My Chip MCU",
  "ecosystem": "My Chip Vendor IDE",
  "tool_script": "my_chip_tool.py",
  "description": "Build, inspect, and download My Chip MCU projects.",
  "adapter_notes": "Describe native build and download backend here."
}
```

然后生成：

```powershell
python scripts\create_mcu_skill.py --adapter adapters\my-chip.json --out "E:\AI agent\Skill_合集"
```

## 安装为 Codex Skill

这个项目本身更像 Skill 工厂，不是某个芯片的最终开发 Skill。可以把它放到 Codex skills 目录，让 AI 在需要创建新 MCU Skill 时调用它。

推荐给 AI 的提示方式：

```text
使用 Chen_embedded_mcu_skill_factory，帮我为 ESP-IDF 创建一个可编译、可下载、可 dry-run 的 Skill 骨架。
```

## 注意事项

- 生成出来的工具脚本是占位骨架，需要继续实现真实后端。
- 不同厂商 IDE 的“编译按钮”行为不同，优先寻找官方 CLI 或 headless build。
- 下载命令必须支持 `--dry-run`，避免无硬件时误判。
- 公开分享前检查 README、SKILL.md 和脚本中是否含有私人路径。
