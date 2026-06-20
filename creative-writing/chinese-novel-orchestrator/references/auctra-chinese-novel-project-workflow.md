# Auctra 中文小说项目工作流

本参考用于把中文小说 skills 的创作方法落到 Auctra 本地项目。原则：skills 负责方法论和作者材料，Auctra 负责结构化状态、run evidence、review、version 和 export。

## 1. 新建或进入项目

如果用户已经在 Auctra 项目内，先查看状态：

```bash
auctra project status --json
auctra project next --json
```

如果需要新建中文小说项目，用 Auctra CLI 创建项目状态：

```bash
auctra project init ./my-novel --template novel --title "作品名" --genre "玄幻悬疑" --audience "中文网文长篇读者" --style "克制、具象、有悬念" --json
```

不要手写 `.auctra/project.yaml`。

## 2. 作者材料与项目圣经

项目圣经、读者契约、大纲、章节卡等是 author-facing artifacts，可以作为普通 Markdown 作者材料维护。需要进入 Auctra 结构化校验时，使用现有表单和知识图谱命令：

```bash
auctra form new character --to forms/characters.md --json
auctra form new worldbuilding --to forms/worldbuilding.md --json
auctra form check forms/characters.md --template novel_series --strict --json
auctra asset build character --from forms/characters.md --json
auctra kg check-consistency --json
auctra kg check-obligations --json
```

表单模板只是起点，填充和修订时必须保留用户确认的设定、人物知识边界和禁写规则。

## 3. 章节写作

新章节应先有章节目标、场景卡和上下文，再进入生成或人工写作。

可用命令：

```bash
auctra text new chapter --title "第001章 标题" --json
auctra material add --kind outline --title "第001章场景卡" --from ./outline/ch-001-scene-card.md --json
auctra material link <material-id> <unit-id> --json
auctra text brief <unit-id> --json
auctra text generate <unit-id> --runtime pi --json
```

章节候选必须进入 review。不要把候选稿直接说成已采纳正文。

## 4. Review 与采纳

每次生成、分析或改写后先查看 review：

```bash
auctra review --status pending --json
auctra text run <run-id> --json
auctra chapter handoff ch_001 --audience agent --json
```

需要采纳时给出明确建议和理由，由用户决定是否运行：

```bash
auctra review accept <review-item-id> --note "采纳原因" --json
auctra review reject <review-item-id> --reason "拒绝原因" --json
auctra review partial <review-item-id> --diff ./my-edits.md --json
```

## 5. 校验和导出

导出前至少检查连续性、叙事义务和健康状态：

```bash
auctra kg health-check --strict --json
auctra text export <unit-id> --format markdown --to ./dist --json
auctra chapter export markdown --to ./dist
```

如果存在 blocking 问题，不要建议强制导出，除非用户明确要求保留已知风险。

## 禁止事项

- 不直接写 `.auctra/**`、SQLite rows、review 决策、run evidence 或 export manifest。
- 不自动 accept review，不自动覆盖正文。
- 不保存完整思维链、原始提示词、供应商载荷或私有工具参数。
- 不把中文小说方法论硬编码进 Auctra core；方法论属于 skills。
