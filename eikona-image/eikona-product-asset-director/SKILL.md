---
name: eikona-product-asset-director
description: Use when an agent building a website, application, documentation site, developer tool, or product repository needs to generate, capture, review, reuse, and safely apply visual assets through Eikona, including hero images, feature illustrations, social cards, empty states, icons, backgrounds, and product mockups.
---

# Eikona 产品资产导演

把产品代码、页面用途和品牌约束转成 Eikona visual brief，完成候选生成、审稿、反馈、复用和安全交付，避免 agent 为每个项目重复编写 provider 脚本。

开始前读取 `cli/eikona/docs/commands/agent-operability.md` 并现场收集适用证据。`configured`、fixture 或历史快照都不能授权真实 provider run；任何非 fixture 的 `generate`、`run --background` 或 workflow execution 都需要用户对指定 provider/model 和潜在费用的明确同意。

## 输入

- 当前项目、框架、目标页面或组件、资产用途和目标路径。
- 品牌色、字体、参考图、尺寸、透明背景、文案安全区、禁用元素和素材权限。
- 可选 channel/model；未配置可用 provider 时先交给 `eikona-gateway-bootstrap`。

## 场景路由

| 请求 | 资产类型 | 默认关注点 |
| --- | --- | --- |
| Landing page 主视觉 | `landing_hero` | 标题留白、响应式裁切、品牌一致性 |
| 功能区插画 | `feature_illustration` | 与功能语义一致、系列一致性 |
| 社交分享图 | `social_card` | 平台尺寸、标题安全区 |
| 空状态 | `empty_state` | 轻量、可读、不抢主操作 |
| 产品截图包装 | `product_mockup` | 截图真实性、设备框和背景 |
| UI/游戏小资产 | `ui_asset` | 尺寸、透明度、边缘质量 |
| 文档概念图 | `docs_illustration` | 解释性、主题一致性 |

小红书交给 `eikona-xhs-visual-router`，Auctra/小说内容交给 `eikona-auctra-visual-router`，连续空间分镜交给 `eikona-ultrawide-storyboard-director`。

## 工作流

1. 只读检查项目框架、页面、现有视觉 token、资产目录、目标尺寸和 `.gitignore`。确认参考素材权限，不把未知权限素材提交给 provider。
   - 如果已有 Codex/imagegen 或设计师交付的临时图片，先加载 `eikona-asset-lifecycle`，捕获为 run artifact；不要重新生成或直接复制进项目。
2. 注册项目并读取可用 channel：

```bash
eikona projects register . --agent
eikona auth list --agent
eikona auth check gateway --agent
```

3. 形成 visual brief：目标、主体、构图、标题安全区、色彩、风格、尺寸、裁切策略、禁用项和目标文件。用户未指定尺寸时使用原生 `2k`；用户明确给出其他 size 时原样保留。默认真实模型使用 `openai/gpt-5.4-image-2`；`gpt-5.4-image-2` 与 `gpt-image-2` 作为兼容短别名，用户指定其他模型时必须使用网关准确 model ID。
   - 输入图是要被局部修改或重绘的画布时，使用 `reference_mode=edit`。
   - 输入图只提供风格、布局、主体或品牌语言，且目标是全新画布时，使用 `reference_mode=generate`；产品 UI canary 默认属于这一类。
   - 网关不支持参考输入时，不得静默删除 reference。先保留失败证据并报告能力缺口；只有用户接受后，才把可见约束转写为明确 brief，创建独立的纯文生图 run，并标注无法保证像素级或 identity/style 一致性。
4. 加载 `eikona-file-prompt-workflow`，将 brief 索引和 3–4 个候选方向保存到 `prompts/product/<asset-type>/<collection>/`。一个候选一个 prompt 文件，模型和尺寸写入 runbook。
5. 先检查集合展开。获得 paid/live gate 的明确同意后，才生成真实候选。产品 hero 示例：

```bash
eikona run -f prompts/product/landing-hero/local-first-cli/runbook.yaml --dry-run --agent
# Only after explicit approval for the configured provider/model and potential cost:
eikona run -f prompts/product/landing-hero/local-first-cli/runbook.yaml --background --agent
```

网关模型不是 GPT Image 时，保留相同 Eikona 流程，只替换准确 model ref 和网关要求的 `--set api=responses|images|chat`；不要猜 Nano Banana model ID，也不要假设纯文生图成功等于参考输入可用。

6. 获取 review packet，按实际使用场景检查主体、品牌、文字伪影、文案安全区、桌面/移动裁切、尺寸和版权风险：

```bash
eikona review packet <run_id> --agent
```

7. 记录接受和拒绝理由：

```bash
eikona feedback accept <run_id> --artifact <artifact_id> --reason composition --reason brand_fit --reason prompt_alignment --agent
eikona feedback reject <run_id> --artifact <artifact_id> --reason brand_fit --reason text_quality --agent
```

8. 先读取 path-free handoff，再确认项目内目标路径并 apply：

```bash
eikona assets handoff <artifact_handle> --audience agent --agent
eikona assets apply <artifact_handle> --project current --to public/images/hero.png --yes --agent
```

禁止 agent 自己下载、base64 解码或复制 provider 产物。目标路径必须位于已注册项目内。

外部候选图必须先经过 `eikona artifacts import`，再执行 handoff、review、显式 `library save` 或项目 apply。捕获本身不代表接受或长期保存。

9. 只有用户明确接受视觉方向且预计复用时才提升 recipe：

```bash
eikona recipes promote <run_id> --artifact <artifact_id> --as product-hero-clean-editorial --agent
```

跨项目复用前重新检查品牌归属、素材权限和用户许可；优先复用构图、prompt skill 或 recipe，不默认复制源图。

## 输出

- 资产类型、分类 prompt 目录、集合 README、候选 prompt 文件、runbook、channel/model、run ID、候选 review 结论、feedback 决策、artifact handle、目标路径和 handoff/apply 结果。
- 使用结构化 Eikona 输出，不保存 raw provider payload、隐藏提示、private tool arguments 或完整思维链。

## 边界

- 不直接调用 provider SDK，不创建临时生成脚本，不绕过 Eikona evidence。
- 不自动覆盖项目文件；`assets apply` 前必须确认目标路径并使用 `--yes`。
- 不把 exploratory 场景包装为成熟能力；优先完成一个真实资产进入仓库的闭环。
- 不把 Eikona CLI/runtime bug 塞进场景 skill；运行时问题交给 `yeisme-eikona-cli-runtime`。
- 例行自动化用 `--agent`；非终态 run 用 `eikona watch <run_id> --events` 观察；脚本/CI 用 `--json --compact`（共存期内裸 `--json` 仍是 legacy full）；取证用 `--json --full`。

## 验证

- 一次任务必须产出 `run_id`、review packet、feedback decision、artifact handle 和项目 handoff。
- 换项目时复用用户级 channel，不复制 key 或 provider 配置到仓库。
- 用户可从 Eikona 证据定位最终资产来源、选择理由和 apply 目标。

## 视觉意图输出

本导演输出 `eikona.visual_intent.v1` 意图的创意约束字段（canvas、content_constraints、references、reference_mode、review_rubric），不直接产出最终 prompt 或调用 provider。

产品 UI canary 默认值：canvas `2k` `16:9`，text_density `low`，unknown_secondary_copy `leave_blank`，forbid_pseudo_cjk `true`，reference_mode `generate`，review_rubric `native_resolution` + `title_legibility` + `no_pseudo_cjk`。

编译：`eikona workflow import intent -f visual-intent.yaml --out workflow.yaml --agent`。契约详见 `../eikona-visual-router/references/visual-intent-contract.md`。
