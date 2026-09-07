# 语言约定

- Agent 编译、preview、导出和下游模型投递只使用 `locale=en`。
- 中文译文位于 solution 的 `docs/template-zh-CN.md`，用于人类审阅，不注册为模板，不进入 contract、catalog template 列表或内容 digest。
- `solution.json.locales.zh-CN` 的标题、摘要、用法和别名属于显示信息，不代表存在中文可编译模板。
- 英文模板可以绑定中文或其他语言的资料。最终产物语言由 contract 字段决定，与模板 locale 分离。
- 已发布旧双语 exact ref 可以继续 inspect。创建或更新会话时若出现 `TEMPLATE_LOCALE_REVIEW_ONLY`，改用同版本 `locale=en`；若出现 `TEMPLATE_ENGLISH_REQUIRED`，选择已有英文模板和英文 contract 的新版本。

不要读取中文译文后手工拼接成临时模板。这样会绕过 contract、digest、版本和可重复编译保证。
