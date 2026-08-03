---
name: creative-writing-installer
description: Use when promoting or removing the minimum creative-writing skills for cli/auctra through declarative profiles and scripts/skills.sh after an agent identifies a required skill that is not active in the current runtime.
---

# 中文创作技能安装器

把 agent 已经选定的最小 skill 加入 Auctra profile，再由脚本生成双 runtime。不要手工编辑生成副本。

## 输入

- Agent 推荐的缺失 skill、目标任务、当前 `cli/auctra` profile 和用户授权状态。
- 需要一次性按需读取，还是长期提升为 active 的判断。

## 工作流

1. 先确认来源和当前 profile：

```bash
scripts/skills.sh resolve <skill-name>
scripts/skills.sh profile show cli/auctra
```

2. 一次性任务优先直接读取来源 `SKILL.md`，不要为了单次使用扩大 active runtime。
3. 只有高频、会话启动必需或 Auctra owner 明确要求时，才在用户同意后提升：

```bash
scripts/skills.sh profile add cli/auctra <skill-name> --dry-run
scripts/skills.sh profile add cli/auctra <skill-name>
scripts/skills.sh sync-subprojects
scripts/skills.sh validate-subprojects-runtime
```

4. 不再需要的 skill 通过 profile 降级：

```bash
scripts/skills.sh profile remove cli/auctra <skill-name> --dry-run
scripts/skills.sh profile remove cli/auctra <skill-name>
scripts/skills.sh sync-subprojects
scripts/skills.sh validate-subprojects-runtime
```

## 质量门槛

- 不为一个写作任务批量启用整套无关 skills。
- 不手写 `.agents/skills/**` 或 `.claude/skills/**`。
- 不把 agent 的语义路由重新编码成 shell set 或固定评分表。
- 展示给用户的命令必须真实可运行。

## 边界

- 不执行登录、发布、私信、采集、刷量或平台互动。
- Auctra 项目状态仍通过 Auctra CLI 修改，不手写 `.auctra/**`。
- 安装器只报告 profile 与 runtime 结果，不声称稿件已经完成。

## 验证

- `scripts/skills.sh profile show cli/auctra` 包含预期 skill。
- `scripts/skills.sh validate-profiles` 通过。
- `scripts/skills.sh validate-subprojects-runtime` 通过。
