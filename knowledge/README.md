# Knowledge Skills

企业多模态知识路由模块。负责权限感知的检索、ContextPack、证据和 Owner 交接，不把搜索结果直接提升为 canonical fact。

- [template-registry-agent-operator](template-registry-agent-operator/SKILL.md)：使用 Template Registry CLI 或本地 MCP 选择模板、导入资料、确认输入、编译、导出提示包并接续会话。无需其他 Yeisme 产品。

```bash
npx skills add https://github.com/yeisme/yeisme-agent-my-skills --skill template-registry-agent-operator
```
