# AI 做剧矩阵路由示例

## 1. 美式犯罪悬疑剧

请求：开发 8 集美式犯罪悬疑剧，每集约 50 分钟，先完成 pilot 和 series bible。

```text
format_profile: us-hour-drama
genre_lens.primary: crime-mystery
phase: series_plan
artifact: series_bible
context_pack_profile: series-development
primary_skill: ai-drama-showrunner
compatible_skill: ai-drama-story-architecture
canonical_owner: story_canon_owner
```

不应加载 Director、Visual、Edit/Sound 或 Production Orchestrator，直到进入对应阶段。

## 2. 竖屏复仇短剧

请求：做 60 集竖屏复仇短剧，先确定前 10 集的回报和钩子。

若集长、受众和核心类型未定：先路由 `ai-drama-format-strategist`。合同接受后：

```text
format_profile: vertical-short-drama
phase: series_plan
artifact: episode_arc_1_10
context_pack_profile: series-development
primary_skill: ai-drama-showrunner
compatible_skill: ai-drama-story-architecture
```

## 3. AI 漫剧镜头生产

请求：已有接受的场景稿，把第三场做成 8 镜头的漫剧分镜和关键帧方案。

```text
format_profile: manga-drama
phase: director_plan
artifact: shot_intent_set
context_pack_profile: director-planning
primary_skill: ai-drama-director
compatible_skill: ai-drama-visual-language
canonical_owner: story_canon_owner proposal / production_owner intent
```

导演提案接受后，下一 stage 才以 `ai-drama-visual-language` 为 primary。

## 4. 电影想法

请求：一个失忆消防员发现自己可能参与纵火，帮我先搭电影结构。

```text
format_profile: feature-film
phase: define
artifact: story_architecture
context_pack_profile: series-development
primary_skill: ai-drama-story-architecture
compatible_skill: ai-drama-character-engine
```

## 5. 一次性缺少 active Skill

目标 Skill 在宿主可信本地 catalog 中存在但未 active：

```text
resolution_status: resolved_local_on_demand
activation_plan: absent
```

直接按需读取 source，不执行持久化 activation。

## 6. 高频项目启用

用户明确要求为当前创作项目长期启用 `ai-drama-showrunner`：

```text
resolution_status: needs_profile_promotion
activation_plan.authorization_state: approved_current_request
activation_plan.activation_scope: project
activation_plan.preview_action: required
```

宿主先通过 activation adapter 预览；确认 scope、版本和冲突后再 apply。Router 不生成宿主命令，也不把 project 级能力扩大到 workspace/global。

## 7. 外部 Skill 缺失

本地 source 没有必需能力：

```text
resolution_status: needs_install_decision
status: blocked
```

列出普通 Agent fallback 和候选来源；不得在做剧 production run 中联网下载或热安装。

## 8. 宿主没有启用适配器

目标 Skill 需要持久化启用，但宿主没有声明 `skill_activation.preview/apply`：

```text
resolution_status: needs_profile_promotion
activation_plan.status: adapter_unavailable
status: needs_activation_decision
```

返回 proposal 和手工下一步，不猜测命令或配置文件。
