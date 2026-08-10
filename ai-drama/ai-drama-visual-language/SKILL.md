---
name: ai-drama-visual-language
description: Use when translating AI drama shot intent into Eikona visual briefs, subject/style/reference bindings, keyframe candidate sets, storyboard layouts, visual continuity checks, and review handoff.
---

# AI Drama Visual Language

## 目标

把导演的叙事决策编译成可生成、可比较、可连续的视觉候选。视觉描述必须包含主体、动作、空间、镜头、光线、色彩、负面约束和 continuity refs。

## 工作流

1. 读取 `ShotIntent`、frozen SubjectVersion、StyleVersion、reference refs 和 ProductionConstraintProfile。
2. 生成多个候选 brief，固定 seed、模型 ref、候选数和成本策略。
3. 使用 Eikona 生成候选并建立 CandidateSet；新命令必须显式使用 `--use-channel <channel>`、canonical 模型 ref `openai/gpt-5.4-image-2`、明确 `--size`/`--aspect`，参考图只作为 `--reference-mode generate` 的 guidance。`gpt-5.4-image-2` 与 `gpt-image-2` 仅作为兼容短别名。
4. 通过 `eikona review packet`、`eikona assets handoff`、`eikona assets stage` 和 `eikona assets apply` 管理证据与项目落盘；不要直接读取或复制用户级 runstore 的绝对路径。
5. 生成 contact sheet、visual assessment 和 continuity findings。
6. 输出 review packet 和 accepted feedback handoff；不能把 artifact、library item 或项目文件直接当作 Scaena production accepted。

最小主体候选命令：

```bash
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

## 质量门槛

- 未冻结主体/风格/reference 或 preflight stale 时不得进入 production shot；
- 角色身份、服装、道具、空间和视线必须有 continuity refs；
- 视觉美观不能覆盖动作可读性和镜头叙事意图；
- provider partial failure 必须保留 lineage，不得静默重派；
- 参考图模式失败时必须保留失败 run；只有用户明确接受语义降级，才能另起无参考图的 text-to-image run；
- 所有候选评分都要绑定 CandidateSet、rubric 和 evidence。

## 现有命令验证

```bash
cd /workspaces/yeisme-agent/cli/eikona
eikona workflow draw -f .eikona/workflows/pilot.yaml --seed 20260807 --json
eikona review packet <run_id> --with-assessment --json
go test ./internal/workflow ./internal/runtime ./internal/assessment
```

这些命令验证 Eikona 底座，不代表真实多评委生产能力已经启用。
