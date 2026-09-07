# video-shotcraft 完整集成示例

目标源：`https://github.com/Vincentwei1021/video-shotcraft`。首次检查至少读取 repository metadata、README、`SKILL.md`、生产 pipeline、镜头库索引、LICENSE 和资产 attribution。当前 canary 固定提交：

```text
5f047c7cfe10d6616fe59160a750fcfaea510b2e
```

## 1. 分类

`video-shotcraft` 是外部完整 Skill，不是 Prompt repository。它同时包含 Remotion 实现、镜头卡、音频、工作台和剪映导出。因此：

- 不向 `template-registry prompt repository add` 传这个仓库；
- 不复制上游 Prompt、卡片正文、TSX、音频或模板；
- 固定并安装外部 Skill；
- 用官方 `product-promo-shot-design-beta` 生成 brief 和 shot plan；
- 实际页面采集、编码、渲染、剪辑与交付留给外部 Skill 或 Scaena/Remotion owner。

## 2. 只追问会改变合同的选择

先确认：

1. 交付完整宣传片还是单镜头；
2. `template_adaptation`、`agent_directed` 或 `guided_collaboration`；
3. 时长、画幅、输出语言、音频和数据口径。

产品 facts、页面状态、品牌 tokens 和公开资产能从来源确定时直接登记。用户已点名的镜头卡作为硬约束，不重复询问。Agent 推荐与来源事实分开，preset 仍须用户确认。

## 3. 可复用资产

Exact solution：

```text
promptrepo://official/video/product-promo-shot-design-beta@1.0.0-beta.1?locale=en
```

Roles：

- `brief` → `product_promo_brief.v1`
- `shot-plan` → `product_promo_shot_plan.v1`

Recipe：`video-shotcraft-product-promo.recipe.json`。`shot-plan.accepted_brief_json` 绑定 `brief` 的实际 step output；第一步未运行时第二步必须保持 `needs_step_output`。

## 4. 来源注入

- 产品 README、公开网页、截图或资料导入当前 session。
- 固定提交中的 `gallery/api/library.json` 导入并绑定 `shot-plan.shot_library_index_json`。
- `shot_library_revision` 保存完整 40 位提交，不用短 SHA 猜补。
- 镜头计划必须保存 card name、style key、卡片文档、demo path、preview status 和 library revision。

## 5. 权利与权限

- 上游源码是 Apache-2.0；Remotion 有独立许可。
- 上游 attribution 中无法逐文件确认的音频不得进入完整 portable package。
- 演示截图不代表目标产品数据可发布；敏感数据在采集前虚构、脱敏或冻结。
- 上游要求 subagent 终检，但 Yeisme 只有在用户当前请求明确授权子 Agent 时才派发；无授权时由当前 Agent inline 审查并记录限制。
- 编译、Skill 安装、执行、费用、发布、展示页提交和资产接受分别授权。

## 6. 验收

必须证明：

- 中文 `产品宣传片` 能找到英文 exact ref；
- preset 未确认时 readiness 是 `needs_confirmation`；
- 第一轮 compile 的 `brief` ready、`shot-plan` 为 `needs_step_output`；
- 导入并确认实际 brief 后两步都 ready；
- 两轮 compile 的 `provider_calls=0`，portable package 均通过 verify；
- 上游 revision 或镜头库 digest 改变只使相关 shot plan 和下游执行过期。
