# 语言与目录

Agent 编译正文固定为 `prompts/<role>.en.md`，contract 固定为 `contracts/<role>.en.json`。中文人工审阅译文固定为 `docs/template-zh-CN.md`；多 role 包可以使用 `docs/templates/<role>.zh-CN.md`，但这些文件都不注册为 template。

中文译文首部写明：

```markdown
> 人工审阅译文。编译与 Agent 投递以 `../prompts/main.en.md` 为准；本文件不注册为模板、不进入 catalog，也不参与编译。
```

三个语言层面分别处理：模板骨架用英文；变量值可用任意语言；最终产物语言由显式字段控制。不要通过创建 `zh-CN` template 来表达中文输出需求。

`solution.json.locales.zh-CN` 只保存中文显示文案。使用 `template-registry solution locale describe` 维护，不能手写 metadata。
