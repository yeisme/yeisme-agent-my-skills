---
name: scaena-subject-asset-readiness
description: Use when planning, reviewing, or operating Scaena character, location, prop, wardrobe, style, storyboard, shot, episode, cover, or motion asset work, especially before any production visual generation or when subject identity, reference assets, freeze state, shot bindings, generation preflight, or consistency is missing or uncertain.
---

# Scaena 主体资产就绪门禁

先确定可复用主体资产，再允许剧集生产。不要把成功命令、图片数量、Eikona feedback、Auctra acceptance、legacy `approved` 或相似度总分当成 Scaena production readiness。

## 输入

- Scaena project、ProductionGraph、episode/shot/requirement 或已有 `resume_ref`。
- 视觉用途：`subject_candidate`、`look_development`、`shot_visual`、`episode_visual`、`cover_visual` 或 `motion_visual`。
- 已知 Auctra source refs、Eikona artifacts、Scaena assets/versions/bindings/preflight/consistency refs。

## 输出

返回紧凑门禁结果：

```text
status=<ready|blocked|candidate_only|stale>
purpose=<purpose>
subject_readiness=<passed|blocked|unknown>
missing_subject_refs=<refs>
missing_slots=<subject/slot>
frozen_version_refs=<refs>
generation_preflight_ref=<ref|none>
blocking_codes=<codes>
allowed_next_mode=<subject_candidate|look_development|production|none>
next_command=<real supported command>
evidence_refs=<refs>
```

## 工作流

### 1. 先识别 owner 和用途

- Auctra 负责 accepted story identity、canon facts 与 visual brief。
- Eikona 负责 provider run、artifact、feedback、assessment 与 visual memory。
- Scaena 负责 production subject version、human freeze、shot binding、generation admission、consistency review 与 correction lineage。

如果请求是 Scaena episode/shot/cover/motion production，必须继续执行本门禁。不要直接进入 storyboard director、prompt 编写或 provider generation。

### 2. 检查当前真实状态

进入 `agent/scaena`，读取本地 `AGENTS.md`，只使用已安装版本真实支持的命令。先检查 help，再读取最窄投影：

```bash
scaena help
scaena asset center --project <project-path> --agent
scaena character bible show --project <project-path> --character <character-ref> --json
scaena production graph show <production-graph-ref> --json
scaena shot board --project <project-path> --episode <episode-ref> --agent
scaena visual pack plan --graph <production-graph-ref> --json
```

如果 installed version 已提供 subject readiness、freeze、binding 或 preflight command，使用其 help 中的真实语法。若不存在，返回 `capability_missing` 和 owning OpenSpec `scaena-subject-asset-readiness`；不要编造命令或手写 `.scaena`/SQLite 状态。

### 3. 区分 bootstrap 与 production

- `subject_candidate`、`subject_reference`、`look_development`：可在 accepted source/rights 就绪后自举；产物只能进入 candidate review。
- `shot_visual`、`episode_visual`、`cover_visual`、`motion_visual`、production storyboard keyframe：必须有 current passed generation preflight。

当主体未冻结时，最多路由到 `$eikona-subject-asset-director` 生成可比较候选；不得把候选绑定到 episode/shot。

### 4. 应用主体门禁

读取 [readiness-gates.md](references/readiness-gates.md)。至少检查：

- accepted source version/digest；
- unique active frozen project style；
- required primary/secondary subject versions；
- wardrobe continuity variants；
- recurring location 与 story-critical prop anchors；
- rights/permission；
- exact shot bindings；
- model reference capability；
- current graph/binding/subject versions；
- blocking continuity findings。

任一 production-required fact 缺失时，返回第一组可操作 blockers，并把 `allowed_next_mode` 限制为 candidate/lookdev/repair。不要因为 `visual pack plan` 或旧 render 命令返回 success 就放行。

### 5. 把 fail-open 当成缺陷

以下任一情况都不是“可继续”：

- production visual request 的 `reference_asset_refs` 或 `style_pack_ref` 为空；
- named required subject 没有 frozen version；
- request 没有 `generation_preflight_ref` 或 preflight 已 stale；
- `--confirm` 是唯一生成前置条件；
- fixture/direct ingest accepted 被当成 frozen；
- Eikona accepted candidate 被当成 Scaena production accepted；
- 机器一致性总分直接触发 accept。

发现上述行为时，停止 production generation，记录 bypass path、affected refs 和 owner-call risk。若任务是实现/修复，路由到 Scaena owning OpenSpec；若任务是操作，返回主体候选或 repair 的下一步。

### 6. 生产请求必须固定版本

只有 current passed preflight 才允许继续。确认 request 固定：

```text
generation_preflight_ref/digest
subject_version_bindings
reference_asset_version_refs
style_pack_version_ref
requirement_version_refs
expected_graph_version
```

plan 与 submit 都要检查；submit 前状态变化必须返回 stale，不能自动换成“最新角色”。

### 7. 生成后回到一致性审阅

镜头产物默认进入 human consistency review。逐主体检查 identity、face/hair、silhouette、wardrobe、location layout、prop geometry、style、shot fit 与 rights。机器 assessment 只能分流；correction 创建 derived candidate，不覆盖 source asset。

### 8. 结束时给出可恢复 handoff

只返回 refs、blockers、allowed mode、下一条真实命令与 evidence。不要粘贴完整 canon、raw prompt、provider payload、embedding、private path、credential 或完整模型推理。

## 边界

- 不直接调用 provider SDK，不手写 Eikona/Scaena structured state。
- 不把 legal `SubjectBinding` 当作视觉身份冻结。
- 不让 background exception 覆盖 named/close-up/recurring/continuity-relevant subject。
- 不因用户要求“先出几张看看”而把 lookdev 伪装成 production asset。
- 不自动接受、冻结、改绑、批量重绘或写入 visual memory。

## 验证

- 每个 production entrypoint 都必须有 bypass-negative evidence；blocked 时 owner call count 为零。
- exact test name 必须先用 `go test -list` 确认存在；宽泛或零命中 `-run` 不算证据。
- first-support 必须覆盖 restart、two-project isolation、stale preflight、correction lineage 和标准 integration evidence 六件套。
