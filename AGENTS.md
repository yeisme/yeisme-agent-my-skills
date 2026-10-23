# Yeisme Skills 聚合仓库

本仓拥有 Skills 源目录、可移植 manager、发布索引与聚合校验。第一方独立 Skills 子仓保持自己的 AGENTS.md、校验与 CI；产品源码、私人笔记和运行数据不进入本仓。

修改 Skill 正文默认中文，保留稳定名称、frontmatter 字段和必要中英触发词。第三方源、许可证和公开引用保持原文。profile 与 runtime 由宿主 CLI 管理，不在聚合源内手工维护生成副本。

本地验证入口为 `python3 scripts/validate_repository.py`；具体子仓使用 `python3 scripts/validate_skills.py`。按改动选择检查，不执行 race、自动安装外部 Skills、生产访问、发布或推送。普通 CI 不启用付费 Provider。

完成标准：来源与引用可解析、名称兼容、受影响结构检查通过。发布结果、远端 CI 和消费者安装验证分别报告；本地检查不代表已经发布。
