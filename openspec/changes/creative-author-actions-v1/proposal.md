# 变更提案：五个作者动作与六类内容方法

## Why

当前创作入口暴露了大量细分 Skill 名称，作者需要先理解内部路由才能开始写作；小说、剧本、自媒体和教学内容也容易被套用同一套叙事模板。批准的改造要求把作者可见入口收敛为写作、规划、审稿、修订、整理五个自然动作，同时保留内部 phase/operation 字段和最小领域方法。这样 Agent 可以按内容类型选择真实方法，并在本地或远程 Auctra 服务上保持同一候选、审稿和保存边界。

## What Changes

- 在既有 `creative-writing-router` 与 `creative-role-task-map` 上定义五个显示动作：写作、规划、审稿、修订、整理；稳定的 `phase`、`operation` 和 owner 字段不改名。
- 为小说、剧本、小红书单篇、课件、PPT 讲稿、长期讲课视频六类内容定义默认 primary 方法、按需资料和内容型验收，避免默认启动全套审稿、人物建模或图谱。
- 将教程、教学演讲和课程系列参考收敛到 `tutorial-writer` 的共享普通参考；不新增 CLI、存储表或竞争 Router。
- 在作者侧说明本地 CLI 与远程 MCP/HTTP 的选择，明确生成、采纳、保存版本和下载的边界；远程客户端不要求安装 Auctra CLI，也不能依赖服务端路径。
- 统一自然词显示和帮助解释，并为源、调用引用、profile 清理和宿主验证保留可执行实施任务；本 change 不修改生成 runtime、副本、profile 或产品代码。

## In Scope

- `.skills/yeisme/creative-writing-core/creative-writing-router/` 的路由协议与动作显示。
- `.skills/yeisme/creative-writing-core/creative-writing-router/references/creative-role-task-map.md` 的六类内容映射。
- `.skills/yeisme/content-writing/tutorial-writer/` 及其 `references/teaching-and-presentation.md`。
- 相关现有 `xhs-note-writer`、`xhs-orchestrator`、`screenplay-scene-writer`、小说 writer 的引用迁移计划。
- 源引用扫描、技能结构验证和宿主 profile/runtime 同步的交接要求。

## Non-Goals

- 本 change 不实现 Auctra 服务、MCP/HTTP action、授权、长任务或文件传输。
- 不修改 `.agents/skills/`、`.claude/skills/`、任何运行副本、真实项目 profile、小说正文、剧本正文或产品代码。
- 不删除专业 Skill 的能力；退出常驻 profile 的具体变更由宿主 profile owner 在实现阶段按合同执行。
- 不把课件、PPT 或长视频课程变成新的内容模型或渲染产品。

## Success Criteria

1. 五个作者动作可被自然语言映射，且每次只选择一个主要方法与必要约束。
2. 六类内容各有明确产物、检查和反模板边界；教学三类共享同一 `tutorial-writer` 参考。
3. 本地/远程路径均说明候选、审稿、采纳、保存和下载语义，未实现部分标为待实现而非当前支持。
4. 源调用引用、自然词和验证入口有完整实施任务，所有任务在本 change 初始状态保持未勾选。
5. 本 owner 的 OpenSpec change 通过 `openspec validate creative-author-actions-v1 --strict --no-interactive` 后，才可作为后续 Skills 实现的合同输入。
