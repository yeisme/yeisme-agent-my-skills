## 视觉意图契约 (visual_intent.v1)

本路由器是推荐的公共入口。路由后输出 `eikona.visual_intent.v1` 意图的 `skill_chain`、`scenario` 和未决输入，不直接产出最终 prompt 或调用 provider。

详见 `references/visual-intent-contract.md`（意图契约）和 `references/role-outputs.md`（角色输出模板）。

编译意图到工作流：

```bash
eikona workflow import intent -f visual-intent.yaml --out workflow.yaml --agent
eikona workflow validate -f workflow.yaml --agent
eikona workflow plan -f workflow.yaml --agent
```
