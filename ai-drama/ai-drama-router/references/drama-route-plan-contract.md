# DramaRoutePlan 合同

## 目的

`DramaRoutePlan` 是 Agent 的语义路由结果，不是 canonical story 或生产状态。它可以被宿主转换为自己的 skill plan projection，但持久化必须由 Owner capability adapter 校验和执行。

## 字段

```text
schema_version: ai-drama.route-plan.v1
goal
medium
format_profile
genre_lens:
  primary
  secondary?
phase
artifact
task_role
context_pack_profile?
primary_skill:
  name
  source_kind
  source_ref
  version_or_digest
  resolution_status
compatible_skill?: same shape
style_lens_skill?: same shape
canonical_owner
owner_binding?
input_refs[]
missing_inputs[]
gates[]
activation_plan?
owner_action
next_action
status
```

多阶段任务增加 `stage_plans[]`，每个元素包含 `stage_kind`、一个 `primary_skill`、最多一个 `compatible_skill`、输入/输出合同、Owner 和 gate。

## 状态

`resolution_status`：

- `active`
- `resolved_local_on_demand`
- `needs_profile_promotion`
- `needs_install_decision`
- `missing`
- `conflict`
- `stale`

顶层 `status`：

- `ready`
- `needs_input`
- `needs_context`
- `needs_activation_decision`
- `blocked`
- `stale`

## 不变量

1. 每个 stage 恰好一个 primary，最多一个 compatible constraint。
2. constraint 不得拥有或修改 primary 的 canonical artifact。
3. source ref、version/digest 和 owner 必须可追溯；未知时不能伪造 `ready`。
4. activation plan 与 production plan 分离；启用 Skill 不代表允许 provider call 或 canonical mutation。
5. plan 中不包含 Skill body、raw prompt、完整剧本、provider payload、凭据、私有路径或完整思维链。

## Host projection

转换到宿主运行时计划时，只传输：Skill name/ref/version/digest/source kind、stage、logical owner、可选 owner binding、input/output contract、compatibility basis 和 pinned 状态。

宿主运行时不应依赖 Router 的文件路径或读取完整 `SKILL.md` 来恢复生产状态，也不应重新执行语义发现。Router 包不得内置某个宿主产品名、仓库路径、profile 文件或私有命令。
