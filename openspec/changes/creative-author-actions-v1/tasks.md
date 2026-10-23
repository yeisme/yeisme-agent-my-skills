# 实施任务

本清单属于 `CONTRACT` 阶段的可执行后续计划；所有实现任务当前均为 `[ ]`，不得在本阶段勾选。根五 change strict gate 通过后，才允许进入 Skills source 实现。禁止修改运行副本、profiles、Auctra/Scaena 产品代码、真实作品或其它 owner 合同。

## 1. 共享作者动作与六类内容

- [x] 1.1 **PHASE:** `BACKEND`；**OWNER:** creative-writing-core source writer；**OWNED PATHS:** `.skills/yeisme/creative-writing-core/creative-writing-router/SKILL.md`, `.skills/yeisme/creative-writing-core/creative-writing-router/references/creative-role-task-map.md`；**IMPLEMENTED:** 五个作者动作、稳定 route fields、单 primary/constraint 约束与审稿/整理 gate 语义。
- [x] 1.2 **PHASE:** `BACKEND`；**OWNER:** creative-writing-core source writer；**IMPLEMENTED:** 六类内容默认 primary、教学三类共享 tutorial reference、反模板边界与按需资料。

## 2. 教学、PPT 与课程系列 reference

- [ ] 2.1 **PHASE:** `BACKEND`；**OWNER:** content-writing source writer；**OWNED PATHS:** `.skills/yeisme/content-writing/tutorial-writer/references/teaching-and-presentation.md`、必要的 `.skills/yeisme/content-writing/tutorial-writer/SKILL.md`；**SHARED READ PATHS:** 本 change `design.md`、现有 tutorial-writer、content-writing AGENTS；**FORBIDDEN PATHS:** runtime copies、profiles、其它 content writer、产品代码。**依赖:** root 五 change strict gate；**变更:** 增加教学/演讲、PPT 页级讲稿、课程系列的共享普通 reference，覆盖目标、学习顺序、例子、讲义/口播、步骤、页间衔接、预计时长、复习、练习与答案；**验收:** 三类请求按需读取同一 reference；不新增内容模型、CLI、存储表或渲染器；不套短视频强钩子；**FOCUSED_VERIFICATION:** `python3 scripts/validate_skills.py`（`.skills/yeisme`）；**EVIDENCE_TARGET:** reference diff 与 `tasks.md`；**STOP_CONDITION:** source validator 和 reference link 检查通过即停；**INTEGRATION_DEPENDENCY:** creative router 1.2 完成后接入六类 route，不同步 runtime。
- [x] 2.1 **PHASE:** `BACKEND`；**OWNER:** content-writing source writer；**IMPLEMENTED:** 新增 `content-writing/tutorial-writer/references/teaching-and-presentation.md`，并在 tutorial-writer 中按需链接；覆盖教学、PPT 页级讲稿和课程系列。
## 3. 所有源调用引用与自然词

- [x] 3.1 **PHASE:** `BACKEND`；**OWNER:** creative-writing-core source writer；**IMPLEMENTED:** owned router/map caller references no longer use retired starter/router names and use `chinese-novel-setting-editor`.
- [x] 3.2 **PHASE:** `BACKEND`；**OWNER:** creative-writing-core source writer；**IMPLEMENTED:** author-facing route text uses natural action/content vocabulary without changing machine fields or history/prose contracts.

## 4. Local/remote authoring handoff

- [ ] 4.1 **PHASE:** `CONTRACT`；**OWNER:** creative-writing-core source writer；**OWNED PATHS:** creative-writing-router runtime guidance/references；**SHARED READ PATHS:** Auctra service target contract（approved plan §6–10）、novel/drama runtime guidance；**FORBIDDEN PATHS:** Auctra product code、profiles、runtime copies、真实服务。**依赖:** Auctra `auctra-local-remote-authoring-v2` strict gate；**变更:** 描述本地 CLI 与远程 MCP/HTTP 的 tools/list、search `input_schema`、capabilities/resource、input/download、长任务 status、typed failure 和本地降级；**验收:** 远程客户端无需 CLI 或服务端路径；生成/accept/apply/saved version/export-download 分离；服务不可用不伪造回执、不另建同名作品；未实现行为标 pending；**FOCUSED_VERIFICATION:** `python3 scripts/validate_repository.py`；**EVIDENCE_TARGET:** guidance diff 与 service contract cross-reference；**STOP_CONDITION:** Auctra implementation 可直接消费文字且没有当前支持误述即停；**INTEGRATION_DEPENDENCY:** 等 Auctra implementation 和远程 B2/B3/B6 旅程后再做 integration verification。

- [ ] 4.2 **PHASE:** `CONTRACT`；**OWNER:** creative-writing-core source writer；**OWNED PATHS:** 本 change `proposal.md`、`design.md`、`tasks.md`、`specs/creative-author-actions/spec.md`；**SHARED READ PATHS:** novel/drama changes、root/Auctra service contract；**FORBIDDEN PATHS:** implementation source、profiles、runtime copies、产品代码。**依赖:** 1.1–4.1；**变更:** 保持全部实现 checkbox 为 `[ ]`，记录 owner、owned/shared/forbidden paths、依赖、验收、focused verification、evidence target、stop condition 与 integration dependency；**验收:** strict 校验通过，规格覆盖五动作、六内容类型、教学 reference、local/remote guidance、调用迁移与验证入口；**FOCUSED_VERIFICATION:** `cd .skills/yeisme && openspec validate creative-author-actions-v1 --strict --no-interactive`；**EVIDENCE_TARGET:** change directory 与最终结构化输出；**STOP_CONDITION:** strict 通过后结束 CONTRACT，不宣称 Skills 已实现；**INTEGRATION_DEPENDENCY:** root 五 change gate 是后续 source implementation 的唯一入口。

## 依赖、状态与范围锁

依赖图：`1.1 → 1.2 → 3.1/3.2`；`2.1` 可与 `1.1` 并行；`4.1` 等待 Auctra target contract；`4.2` 收尾。当前实现已完成动作路由、六类内容方法、教学/PPT/课程 reference、creative source caller migration、local/remote source guidance 和自然词；profile/runtime sync、Auctra service integration 与真实作者旅程仍为 host/integration dependency。
