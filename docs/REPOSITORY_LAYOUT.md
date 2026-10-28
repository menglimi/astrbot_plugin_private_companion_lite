# Lite 目录约定

- `main.py`：唯一 AstrBot 入口。
- `astrbot_host/`：SDK 与平台适配、事件处理、官方配置桥接。
- `companion_v2/`：核心对话、记忆、生活、关系与任务领域。
- `tests/`：Lite 回归与合成夹具；按 `tools/test_lite_release.py` 运行。
- `tools/`：Lite 构建、归档校验与统一测试。
- `docs/`：Lite 配置与维护说明。

本分支不维护 pages 和七项拓展实现。测试必须使用隔离资料根；发布产物存放在源码目录之外。历史数据库结构保留以兼容已有核心资料，不代表提供旧拓展能力。
