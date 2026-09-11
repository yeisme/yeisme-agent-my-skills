# 任务

- [x] 1.1 更新本 owner 的工作流正文及入口，保留既有命令与权限语义。
- [x] 1.2 验证来源边界、采纳后保存、失败核对及模板参考限制。
- [x] 1.3 运行 owner 的文档/Skill 校验及 OpenSpec strict 校验，记录证据。

校验：两份 Skill quick_validate、validate-custom、validate-profiles、OpenSpec strict 全部通过。sync-root 与 sync-target cli/pinax 完成，两个 runtime 的目标正文与 source 逐字节一致。一次误写目标 pinax 被 CLI 拒绝，纠正后完成；未创建额外 profile。场景检查覆盖有界来源、采纳后保存、未知结果核对、首轮未测量和模板引用限制。不声称独立模型盲评；无发布。
