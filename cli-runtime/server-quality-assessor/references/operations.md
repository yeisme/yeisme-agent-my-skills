# 运行与恢复

先检查 `server-quality doctor --json`。领域状态由 CLI 管理，不手写 SQLite、JSON 配置、事件或评估记录。

登记使用 asset add、asset bind、endpoint add。绑定保存已有 SSH 密钥路径和 known_hosts 引用，不包含私钥文本。目标必须有明确地址集合；内网需要显式 allow-private。实际采集使用专用 forced-command 公钥和远端管理员持有的 policy。

`deployment --asset <asset> --output <empty-directory>` 只导出脚本、policy 和 user systemd units。审核后由授权操作者部署。生成成功不表示安装成功，timer enabled 不表示真实采集通过。user timer 在注销后的存活还依赖管理机的 linger 配置。

系统每分钟触发，单轮45秒，进程锁与服务共同防重叠。长任务被中断后保留原 run 状态，下一轮标记 interrupted；不伪造中断时段。主机密钥变化和权限拒绝阻断绑定，核验后明确 rebind，不自动降级密钥校验。

通知配置通过 `notify configure` 标准输入写入用户级0600配置；不把完整 URL 或 Authorization 放进命令参数、报告、截图或日志。三次失败建立事件，三次成功发送一次恢复；未变化不刷屏。维护窗口只抑制消息，不删除事实。

`backup create` 使用一致性快照，`backup verify --file <backup>` 在临时目录恢复检查，不覆盖活动库。异机副本及外部心跳系统未验证时分别保留 blind spot。实际恢复与生产文件替换需要明确目标授权。

任何吞吐压测、生产盘写测试、付费风控查询、系统升级、重启或防火墙修改，先给计划和预期证据，不借 Skill 自动执行。
