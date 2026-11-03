# 独立 Operator Skill 升级

先以安装版 commands/inputSchema 确认 skill.status、skill.update、skill.adopt、skill.recover 是否存在。旧版本缺能力时明确版本缺口，不覆盖已有目录。

```bash
template-registry prompt skill status --json
plan=$(template-registry prompt skill update --dry-run --json)
printf '%s\n' "$plan"
```

核对预览后，用同一项目和同一 runtime 应用：

```bash
plan_digest=$(printf '%s' "$plan" | jq -er '.data.plan_digest')
template-registry prompt skill update --expected-plan-digest "$plan_digest" --json
```

用户新增文件、改正文或权限都会阻止升级。未知目录不删除，不提供 force。缺少基线的旧安装使用 skill.adopt 预览；只认领与内置已知包 manifest 一致的完整文件集合。不能把任意本地文件声明为旧版来绕过保护。

transaction_pending 不是 writer 已终止的证明。读取 skill.status 的 transaction_id，等待原操作或显式调用 skill.recover（JSON 输入包含 transaction_id）。跨进程锁串行处理；恢复不会覆盖中断后编辑。profile 管理的项目使用原 manager，不由 Registry 接管。

状态、计划与回执只含文件身份、版本及 digest。不会把 Skill 正文、源资料或凭据写进普通日志。
