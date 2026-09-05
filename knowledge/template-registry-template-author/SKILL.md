---
name: template-registry-template-author
description: Use when creating, translating, revising, validating, or versioning a Template Registry prompt solution, especially when an English Agent template, Chinese human review translation, companion contract, catalog metadata, or backward-compatible locale migration is required.
---

# Template Registry Template Author

创建和维护可由 Agent 稳定编译的 promptrepo solution。正文 owner 是模板内容仓；所有结构化 metadata 由 Template Registry CLI 生成，本 Skill 不手写 `repository.json`、`solution.json`、contract 或 `catalog.json`。

## 开始

先确认 owner、版本状态和现有消费引用：

```bash
template-registry catalog validate --repository . --json
template-registry prompt inspect --ref 'promptrepo://official/<package>/<solution>@<version>?locale=en' --json
```

新方案默认采用：

```text
solutions/<package>/<solution>/
  prompts/main.en.md
  contracts/main.en.json
  docs/template-zh-CN.md
  docs/README.md
  solution.json
```

`prompts/main.en.md` 是唯一 Agent 编译正文。`docs/template-zh-CN.md` 是逐节对应的人工审阅译文，不注册、不建立中文 contract、不参与 catalog template 列表或 digest。英文模板可以接收中文资料；产物语言由字段明确声明。

## 新建流程

1. 明确 job、artifact、目标消费者、role、输入、输出要求、rights、maturity 和已知失败。
2. 人工编写英文模板，变量名使用稳定英文 `{{name}}`。要求模型给结论和可审查依据，不要求隐藏推理。
3. 编写中文审阅译文，保留变量、约束、输出结构、安全边界和失败条件，并在文件首行标注 review-only 身份。
4. 用 CLI 注册英文模板和中文显示文本：

```bash
template-registry solution add --repository . --package <package> --id <solution> --version 1.0.0 --category <category> --locale en --title '<English title>' --summary '<English summary>' --prompt-path solutions/<package>/<solution>/prompts/main.en.md --role main --json
template-registry solution locale describe --repository . --package <package> --id <solution> --locale zh-CN --title '<中文标题>' --summary '<中文摘要>' --usage '<中文用法>' --json
```

5. 用 CLI 初始化并维护英文 contract：

```bash
template-registry contract init --repository . --package <package> --id <solution> --role main --locale en --license <license> --permission preview --json
template-registry contract input set --repository . --package <package> --id <solution> --role main --locale en --name <field> --type string --required --label-en '<English label>' --label-zh-CN '<中文标签>' --json
template-registry contract validate --repository . --package <package> --id <solution> --role main --locale en --json
```

6. 建立公开、虚构、非敏感的 valid/invalid fixtures；运行 catalog build/validate 和消费者 canary。

## 修改与翻译

- 已发布版本的正文、contract、rights、locale 或 template digest 不原地改写；创建新版本并保留 replacement/rollback 说明。
- 英文正文变化后同步更新中文审阅译文。自动翻译只能作为待审草稿。
- 中文标题、摘要、usage 和 aliases 用 `solution locale describe` 修改；不能为了中文搜索重新注册中文模板。
- 已发布旧双语 ref 保留兼容性。未发布方案可以用 `solution locale remove --locale zh-CN` 移除中文模板绑定，再把孤立正文移到 `docs/template-zh-CN.md`。

## 验证

```bash
template-registry contract validate --repository . --package <package> --id <solution> --role main --locale en --json
template-registry catalog build --repository . --json
template-registry catalog validate --repository . --json
```

还要确认：

- catalog 中该 role 的 template locale 只有 `en`；
- `docs/template-zh-CN.md` 的变量集合与英文正文一致；
- 普通 CLI、Agent、events 和测试证据不包含模板正文或真实输入；
- 目标 Scaena、Eikona、Auctra、Sonora、Pinax 或 Registry 流程用 exact `locale=en` ref 完成 provider-free inspect/validate/preview/compile。

## 按需参考

- [语言与目录](references/locale-and-layout.md)
- [发布前检查](references/validation.md)
