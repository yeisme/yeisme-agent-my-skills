# Knowledge Skills

知识与可复用内容资产路由模块。负责权限感知的检索、ContextPack、Prompt Repository owner 交接与证据边界，不把搜索结果、模板候选或预览直接提升为 canonical fact。

Prompt Template 相关入口：

- `yeisme-prompt-repository-router`：判断正文、公共合同、Registry 和领域消费者的 canonical owner。
- `template-registry-agent-operator`：从自然语言需求和资料开始，完成确认、英文模板编译、导出与接续。
- `template-registry-template-author`：新建或修订英文 Agent 模板、中文人工审阅译文和 CLI-authored contract/catalog metadata。
