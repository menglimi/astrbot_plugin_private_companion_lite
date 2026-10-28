# 我会永远陪着你 Lite

<div align="center">
  <img src="./logo.png" alt="我会永远陪着你 Lite" width="180">
</div>

面向 AstrBot 的核心陪伴版本。让角色在日常对话之外，也能持续生活、记住共同经历，并在合适的时候主动联系。

Lite 保留核心聊天、记忆、关系、生活、日程、主动联系、分段回复与语音能力；配置通过 AstrBot 官方插件配置页完成。

> ## 使用前请先阅读 Wiki
>
> [打开插件 Wiki](https://vue.syuan.org)
>
> Wiki 同时介绍完整版能力；Lite 的功能范围、安装方式与配置入口以本页和 [Lite 核心配置指南](docs/LITE_CONFIGURATION.md) 为准。

**[基础信息与支持](#一基础信息与支持) · [产品定位](#二产品定位) · [安装与首次使用](#三安装与首次使用) · [核心工作方式](#四核心工作方式) · [Lite 版本边界](#五lite-版本边界) · [指令速查](#六聊天功能指令速查) · [数据与安全](#七数据权限与常见排障) · [开发与项目结构](#八开发验证与项目结构)**

---

## 一、基础信息与支持

### 基础信息

| 项目 | 当前信息 |
| --- | --- |
| 插件名 | `astrbot_plugin_private_companion` |
| 显示名 | 我会永远陪着你 Lite |
| 当前版本 | `7.0.0+lite`（Lite 独立版本） |
| AstrBot 版本 | `>= 4.27.2` |
| 支持平台 | `aiocqhttp`（OneBot v11）、`qq_official`、`qq_official_webhook` |
| 配置入口 | AstrBot 官方插件配置页 |
| 数据存储 | Lite 核心运行资料与插件代码分开保存 |
| 版本边界 | 不含七项内置拓展能力和「陪伴小屋」页面 |
| 开发者 | `menglimi` |

### 文档与支持

- 使用说明：[插件 Wiki](https://vue.syuan.org)
- Lite 配置：[核心配置指南](docs/LITE_CONFIGURATION.md)
- 源代码：[Lite 独立仓库](https://github.com/menglimi/astrbot_plugin_private_companion_lite)
- 版本记录：[CHANGELOG.md](CHANGELOG.md)
- 问题反馈与交流群：QQ 群 `1097283005`
- 自愿支持：[爱发电](https://ifdian.net/a/xuhaun)

赞助完全自愿，不影响插件功能、更新或技术支持。

---

## 二、产品定位

Lite 面向希望保留核心陪伴体验、通过 AstrBot 官方配置管理插件的用户。普通对话沿用 AstrBot 主回复流程；插件维护角色生活与关系上下文、核心记忆、主动联系和回复表达。

- **对话连续**：支持私聊、群聊、多 Bot 与多人格，并按会话权限决定是否接管消息。
- **角色生活**：维护角色状态、睡眠、日程、日记、梦境与重要日期。
- **记忆与关系**：记录有来源的事实和共同经历，区分私聊与群聊的可见范围。
- **主动联系**：结合角色生活、日程和近期互动形成联系候选，并遵循授权、免打扰和频率设置。
- **表达与媒体**：支持分段回复、TTS，以及普通图片、音频、视频和文档理解。

---

## 三、安装与首次使用

### 3.1 安装方式

Lite 与完整版使用同一插件身份 `astrbot_plugin_private_companion`，属于替换安装的两个版本。不要把它们作为两个同名插件同时加载。切换版本前，先用 AstrBot 备份插件配置和运行资料。

- Lite 仓库：<https://github.com/menglimi/astrbot_plugin_private_companion_lite>
- Git 安装地址：<https://github.com/menglimi/astrbot_plugin_private_companion_lite>
- ZIP 安装包：<https://github.com/menglimi/astrbot_plugin_private_companion_lite/archive/refs/heads/main.zip>

手动安装时，将插件目录放入 AstrBot 插件目录，并保持目录名为 `astrbot_plugin_private_companion`。依赖由 `requirements.txt` 声明，使用 AstrBot 的 Python 环境。

### 3.2 首次配置

1. 在 AstrBot 中连接 Bot、选择可用的聊天模型并配置人格。
2. 打开插件的官方配置页，在「账号与会话」中添加 Bot 账号和私聊目标。
3. 添加人格映射：`persona_id` 使用 AstrBot 人格 ID；`role_id` 用于稳定关联角色与记忆。
4. 保存后启用接管并重载插件。未启用接管或配置尚未完成时，普通消息继续走 AstrBot 原有流程。
5. 按需配置分段、TTS、天气、新闻、戳一戳，以及记忆、生活和主动联系偏好。高级配置见 [Lite 核心配置指南](docs/LITE_CONFIGURATION.md)。

私聊发送 `companion_bind` 可查看当前平台实例、Bot 账号与参与者等配置资料；该命令只展示资料，不修改配置。

如果启动失败，请查看 AstrBot 日志中的错误 `code` 和核心偏好配置说明。偏好条目会整体校验与写入；配置错误时不会只应用一部分。

### 3.3 旧资料边界

Lite 不提供完整版的旧版资料迁移向导，也不会由安装流程迁移或清理冻结的旧资料。切换版本前请自行备份；不要将旧版资料目录当作 Lite 的迁移来源。

---

## 四、核心工作方式

| 方向 | Lite 提供的能力 |
| --- | --- |
| 对话 | 私聊、获准群聊、多 Bot 与多人格；普通回复沿用 AstrBot 主回复流程 |
| 角色生活 | 状态、睡眠、日程、日记、梦境、重要日期与成长记录 |
| 关系与记忆 | 角色关系、来源事实、共同经历及按会话范围检索 |
| 主动联系 | 结合生活和互动形成候选，受用户授权、免打扰时段与频率设置约束 |
| 回复表达 | 分段、TTS、普通图片/音频/视频与常见文档理解 |

Lite 的高级核心偏好通过 AstrBot 官方插件配置页管理。配置组、生效范围、字段 ID 与示例见 [Lite 核心配置指南](docs/LITE_CONFIGURATION.md)。

---

## 五、Lite 版本边界

本版本不包含 `Content`、`Image`、`Screen`、`Reality`、`Together`、`Game`、`Live` 七项内置拓展能力，也不包含「陪伴小屋」、其他插件页面或页面管理路由。这里的 `Image` 指生图与图像编辑拓展；普通聊天中的图片理解仍属于核心媒体理解。

Lite 不提供摄像头、本地音频设备、米家等拓展集成。配置、状态统计和资料维护请使用 AstrBot 官方配置页及宿主提供的功能。

---

## 六、聊天功能指令速查

### 私聊

| 指令 | 用途 |
| --- | --- |
| `陪伴 帮助` | 查看可用指令 |
| `陪伴 状态`、`陪伴 能力列表` | 查询角色状态或当前可用能力 |
| `陪伴 日程`、`陪伴 查看日程` | 查询当前角色日程 |
| `生成日程`、`刷新日程`、`重新生成日程` | 按当前配置生成或刷新日程 |
| `陪伴 日记`、`陪伴 梦境` | 查询近期日记或梦境 |
| `陪伴 记忆 <线索>`、`陪伴 长期记忆 <线索>`、`陪伴 片段 <线索>` | 按线索查询可访问的记忆 |
| `陪伴 主动判定` | 查询当前主动联系候选与拦截原因 |
| `陪伴 答疑 <问题>` | 根据当前可用配置和运行资料排查问题 |
| `陪伴 日期列表` | 查询当前角色的重要日期 |

### 群聊

| 指令 | 用途 |
| --- | --- |
| `陪伴群 帮助`、`陪伴群 状态`、`陪伴群 话题` | 查看帮助、状态或近期群内话题 |
| `陪伴群 黑话 <词>`、`陪伴群 片段 <线索>` | 查询当前群可见的词语或共同经历 |
| `陪伴群 关闭LLM`、`陪伴群 开启LLM` | 临时封锁或恢复本群 LLM 回复；需安装管理员 |
| `陪伴群 LLM状态` | 查询本群临时封锁状态 |

查询结果受当前会话权限和本轮实际可用工具约束。

---

## 七、数据、权限与常见排障

### 7.1 数据与隐私

- Lite 的核心运行资料与插件代码分开保存；安装或切换版本不会替用户清理冻结资料。
- 私聊记忆不会带入群聊；群聊只使用当前群可见且已授权的资料。
- `companion_bind` 只显示用于配置的身份资料，不执行绑定或修改。
- 主动联系受会话授权、安静时段和频率规则约束。平台返回结果未知时，不会因超时自动重复投递。

### 7.2 常见问题

遇到问题时先查看 AstrBot 控制台日志。反馈时请提供插件版本、发生时间和脱敏日志。

| 现象 | 优先检查 |
| --- | --- |
| 插件没有接管消息 | 官方插件配置页中的接管开关、账号与会话、人格映射及重载状态 |
| 私聊或群聊没有回复 | 平台连接、目标绑定、人格映射、群聊授权和 AstrBot 核心消息日志 |
| 主动联系没有发出 | 用户授权、主动联系开关、免打扰时段、额度和候选拦截原因 |
| TTS 没有触发 | 官方配置页的语音模型、语种和 TTS 开关 |
| 配置没有生效 | 核心偏好中的配置组、生效范围、目标/角色 ID、字段 ID 与错误日志 |

---

## 八、开发验证与项目结构

### 8.1 项目结构

| 路径 | 用途 |
| --- | --- |
| `main.py` | AstrBot 插件入口、生命周期与事件接入 |
| `astrbot_host/` | AstrBot SDK 适配、配置桥接与消息处理 |
| `companion_v2/` | 平台无关的核心对话、记忆、关系、生活和主动任务 |
| `tests/`、`fixtures/` | Lite 回归测试与合成夹具 |
| `tools/` | Lite 交付包构建、校验与测试脚本 |
| `docs/` | Lite 配置与仓库维护说明 |

### 8.2 构建与验证

文本文件统一使用 UTF-8 无 BOM、LF 和末尾换行。构建和验证产物应放在源码目录之外：

```powershell
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$release = Join-Path $env:TEMP "companion-lite-release-$stamp"
$verification = Join-Path $env:TEMP "companion-lite-verification-$stamp"
$astrbotSdk = 'C:\path\to\AstrBot\backend\app'
python -X utf8 tools/build_v2_release.py --output $release
python -X utf8 tools/verify_v2_release.py --release $release --extract-to $verification --sdk $astrbotSdk --run-tests
```

验证会校验归档清单、文件哈希、编码和 Lite 组成，并在隔离资料目录中运行回归测试。

Lite 基于 [7.0.0 正式版主仓库](https://github.com/menglimi/astrbot_plugin_private_companion) 的核心代码维护。共享核心代码的后续更新按 Lite 的功能边界单独验证后再纳入。
