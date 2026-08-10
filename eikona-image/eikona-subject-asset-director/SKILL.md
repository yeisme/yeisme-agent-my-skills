---
name: eikona-subject-asset-director
description: Use when creating or repairing Eikona character identity sheets, subject reference packs, wardrobe/location/prop/style candidates, per-subject reference bundles, consistency review evidence, or correction candidates for Scaena/Auctra workflows, especially before episode/shot generation or after identity drift.
---

# Eikona 主体资产导演

为可复用主体生成“可比较、可审阅、可交接”的候选和修复产物。Eikona 不决定 Scaena production freeze，也不把 Auctra canon 改写为视觉事实。

## 输入

- Purpose：`subject_candidate`、`look_development`、`consistency_assessment` 或 `correction`。
- Auctra accepted visual brief/source refs，或 Scaena frozen subject/preflight/correction refs。
- Subject kind/tier、required views/slots、reference images、allowed/forbidden variation、rights、model/size/aspect/candidate count。

缺 accepted source、Scaena readiness 或 correction authority 时，先返回 owner blocker；不要自行补写 canon 或 production state。

## 输出

- Candidate plan：subject、view roles、wardrobe/location/prop/style variants、reference roles、candidate count。
- Review packet：artifact refs、objective checks、missing inputs、comparison order。
- Eikona commands：dry-run/fixture、真实 run、review、feedback、handoff。
- Scaena handoff：purpose、source/preflight/correction refs、artifact refs/digests、rights、下一步 human review/freeze/consistency action。

## 工作流

### 1. 先确认允许的 purpose

- `subject_candidate` / `look_development`：要求 Auctra accepted source/brief；不要求 frozen subject，但产物必须 non-production。
- `consistency_assessment`：要求 source shot asset 与 frozen subject/style/reference refs。
- `correction`：要求 Scaena correction plan、source asset、finding refs 和 preserve refs。
- `shot_visual` / `episode_visual` / `cover_visual` / `motion_visual`：若属于 Scaena production，先交给 `$scaena-subject-asset-readiness`；没有 current passed preflight 时停止。

### 2. 规划候选包而不是直接画剧集镜头

读取 [subject-pack.md](references/subject-pack.md)。Primary character 通常需要 front、three-quarter、profile、full-body、neutral/core expressions 和 default wardrobe；secondary 使用轻量包。Location、prop、wardrobe 和 style 使用各自 anchor slots。

每个候选方向只改变一组可审阅变量。不要同时改变脸型、发型、年龄、服装、画风和光线，导致无法知道用户接受了什么。

### 3. 建立 reference-role 与 prompt-file 计划

- 加载 `eikona-file-prompt-workflow`，按 `prompts/scaena/<asset-type>/<subject-ref>/` 分类保存 README、候选 prompt 和 runbook。
- 标记 reference 的角色：identity、wardrobe、style、location layout、prop geometry、source correction。
- 保留 reference 顺序；不要把所有图都当等权风格图。
- 一个 `.md`/`.txt` 文件对应一个候选方向；runbook/prompt source/evidence 由 Eikona CLI 创建，不手写结构化 metadata。
- Prompt 只使用允许公开给 provider 的 source facts；不要包含完整 canon、隐藏剧透、credential、provider payload 或内部推理。

Eikona 默认模型使用完整 canonical ref：`openai/gpt-5.4-image-2`。`gpt-5.4-image-2` 与 `gpt-image-2` 是接受的短别名；历史 `openai:gpt-image-2` 只作为兼容输入。网关其他模型必须复制 `/v1/models` 的完整 ID；`openai:gpt-5.4-image-2` 是禁止的歧义形式。

### 4. 先 fixture/dry-run，再真实生成

进入 `cli/eikona`，读取本地 `AGENTS.md`，确认实际命令 help。单个 prompt 文件：

```bash
eikona generate \
  --model fixture:image \
  --input prompts/scaena/subject-candidate/<subject-ref>/prompts/01-candidate-a.md \
  --size 2k \
  --aspect 2:3 \
  --dry-run \
  --json

eikona generate \
  --use-channel openai \
  --model openai/gpt-5.4-image-2 \
  --ref subject=./references/source-subject.png \
  --reference-mode generate \
  --input prompts/scaena/subject-candidate/<subject-ref>/prompts/01-candidate-a.md \
  --size 2k \
  --aspect 2:3 \
  --quality high \
  --json
```

需要 reference image 时使用 installed version 支持的 `--reference-image` 语法，并保留顺序。候选集合使用已有 runbook：

```bash
eikona run -f prompts/scaena/subject-candidate/<subject-ref>/runbook.yaml --dry-run --json
eikona run -f prompts/scaena/subject-candidate/<subject-ref>/runbook.yaml --background --json
eikona wait <run_id> --json
```

真实生成默认使用 `openai/gpt-5.4-image-2`。不要为 Scaena 专门创建 provider script 或另一套 scenario command。

真实生成前先检查新 Eikona 的用户级 channel readiness：

```bash
eikona auth check openai --agent
eikona models readiness openai/gpt-5.4-image-2 --channel openai --agent
eikona providers doctor openai --channel openai --model openai/gpt-5.4-image-2 --probe --agent
```

用户级 channel 尚未配置时，必须显式提示用户通过 stdin 保存 key；不要隐式读取 `OPENAI_API_KEY`，也不要推荐 `--from-env OPENAI_API_KEY`：

```bash
read -rsp 'OpenAI-compatible API key: ' EIKONA_API_KEY; echo
printf '%s\n' "$EIKONA_API_KEY" | eikona auth set openai \
  --protocol openai \
  --base-url http://dev.qxtech.cc:26160/v1 \
  --api-key-stdin \
  --default-model openai/gpt-5.4-image-2 \
  --json
unset EIKONA_API_KEY
```

`PROVIDER_UNAVAILABLE`、`PROVIDER_AUTH_MISSING` 或 readiness degraded 时必须保留原始失败 run 和 reference lineage；
修复 provider 后重试同一 prompt/reference，不得静默删除参考图、改用短模型名或换成其他模型。

### 5. 生成 review packet，禁止机器自动选定

```bash
eikona review packet <run_id> --json
eikona assets list <run_id> --agent
```

按 artifact 比较 identity、face/hair、silhouette、wardrobe、location layout、prop geometry、style adherence、view completeness 与 obvious artifacts。机器分项 assessment 只能作为 evidence；用户/Scaena 必须做明确 decision。

记录反馈：

```bash
eikona feedback accept <run_id> --artifact <artifact_id> --reason identity_anchor --reason view_completeness --json
eikona feedback reject <run_id> --artifact <artifact_id> --reason identity_drift --json
```

不要把 Eikona accept 描述成 Scaena frozen 或 shot accepted。

### 6. Handoff 回 Scaena，而不是改写 Scaena 状态

```bash
eikona assets handoff <artifact_id> --agent
```

Handoff 必须带 artifact/run refs、digest、mime/dimensions、permission、lineage、feedback、source brief 或 Scaena preflight/correction refs。Scaena 再执行 candidate review/freeze 或 consistency review；本 skill 不手写 `.scaena`、不调用数据库、不自批。

项目文件必须通过 typed asset flow 写入。不要直接复制用户级 runstore 的绝对路径，也不要把 `--output-dir` 当成 production acceptance：

```bash
eikona assets handoff eikona://artifacts/<run_id>/artifact_001 --audience agent --json
eikona assets stage eikona://artifacts/<run_id>/artifact_001 \
  --to outputs/characters/korea-v1/<subject-id>.png \
  --json
eikona assets apply eikona://artifacts/<run_id>/artifact_001 \
  --project current \
  --to outputs/characters/korea-v1/<subject-id>.png \
  --yes \
  --json
```

`assets apply` 只表示项目文件已写入；主体冻结仍由 Scaena readiness/consistency gate 完成。

### 7. Correction 只改指定 drift

Correction plan 要求：

- 保留 source asset 和 prior assessment；
- 明确 preserve：identity、pose、location、camera、lighting 等；
- 只修 finding 指定维度；
- 输出 derived candidate；
- handoff 后重新进入 Scaena consistency review。

## 边界

- 不修改 Auctra canon、Scaena freeze/binding/review 或 Studio Backend job state。
- 不在没有 Scaena preflight 时生成 Scaena production episode/shot asset。
- 不用相似度总分替代逐维度 evidence 与人工 decision。
- 不把 accepted/rejected 机器标签隐式写入 visual memory；只有显式 human feedback 才能成为 memory evidence。
- 不复刻未经授权的真实个人或受版权保护角色。

## 验证

- Candidate set 覆盖 required view/slot，且每个 artifact 可回溯 source/brief/run/digest。
- Handoff 与 request/preflight/correction refs 一致；缺失或 mismatch 时 fail closed。
- Scaena production context 无 preflight 时输出 route/blocker，不输出 production prompt 或真实 generation command。
- 最终回复区分 `candidate accepted by Eikona`、`frozen by Scaena`、`shot accepted by Scaena`。
