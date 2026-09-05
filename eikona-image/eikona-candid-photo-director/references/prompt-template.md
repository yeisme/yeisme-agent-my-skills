# 提示词模板绑定约定

模板正文的 canonical 归属是模板仓库 `data/yeisme-prompt-templates/solutions/image/candid-portrait-matrix/prompts/main.en.md`（promptrepo 解决方案包；`main.zh-CN.md` 是人工审阅译文，不进入编译）。`sample_matrix.py` 加载该模板并把采样结果绑定为 `{{变量}}`；本技能不内嵌模板正文。本文档解释绑定关系与设计意图。

## 绑定映射

| 模板变量 | 来源 |
| --- | --- |
| `subject` | `--subject` / `--subject-text`（默认 `kr-ins-default`） |
| `aspect` | `--aspect`，默认 9:16 |
| `expression` … `state`（12 维） | 采样器当次采中的取值 |

渲染后若残留任何 `{{...}}` 则直接报错退出；模板新增变量时必须同步 `render_prompt` 的 bindings。

## 设计要点

- **主体段独立**：主体由参数注入，服装风格紧随其后，保证「人」的描述集中在一段，方便换主体重跑同 seed 做对比。
- **画面段按叙事顺序**：先场景与瞬间（发生什么），再镜头语言（怎么看），再前景、光线、色彩、摄影状态（画面质感）。
- **前景遮挡是硬规则**：模板中逐字保留「自然侵入、明显遮挡、不完整展示」，因为采样矩阵本身只选了前景类型，遮挡行为必须显式声明。
- **禁用段全量保留**：九条负向约束逐字出现在每张提示词中，不依赖模型记忆。
- 文件命名 `NN-<combo>.md`：序号供人读，combo 哈希供机器去重与回放。

## 修改模板

只改模板仓库的 `main.*.md`，然后用 template-registry `contract refresh` 更新 digest；不要在本技能里另存模板副本。既有批次的 prompt 文件不回填——用同 seed 重跑生成新文件，manifest.json 中的 combo 不变则说明采样未受影响（combo 只对数据哈希，不含模板正文；模板变更以 contract digest 为准）。
