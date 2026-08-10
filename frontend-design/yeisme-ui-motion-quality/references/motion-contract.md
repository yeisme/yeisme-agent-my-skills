# Motion Contract

每个非 trivial 交互只保留一个主要运动意图。契约描述状态转换，不描述“感觉高级”之类不可验收的审美判断。

```yaml
motion:
  owner: ContextDeck.SheetContent
  intent: continuity
  trigger: select-row
  from: detail(channel-a)
  to: detail(channel-b)
  properties: [opacity, transform]
  duration: normal
  easing: ease-out
  distance: 4px
  interrupt: settle-latest-target
  reduced_motion: opacity-only
  focus: preserve-sheet-and-focus-target
  layout: no-shift
  acceptance:
    - old-query-cannot-overwrite-new-target
    - rapid-row-selection-settles-on-latest-target
    - close-returns-focus-to-trigger
```

## 字段规则

- `owner`：真实渲染组件或 primitive，不写业务页面泛称。
- `intent`：只能是 `feedback`、`continuity`、`hierarchy`、`status` 之一。
- `from/to`：描述用户可观察状态；不能把动画状态当成服务器状态。
- `properties`：默认 `[opacity, transform]`；加入 `height`、`width`、`layout` 需要记录理由。
- `duration`：使用 `fast`、`normal`、`slow` token，不在业务组件里散落毫秒值。
- `interrupt`：必须说明快速重复操作、切换目标、卸载或请求失败时如何收敛。
- `reduced_motion`：至少是 `opacity-only` 或 `none`。
- `acceptance`：写成可观察断言，能映射到 Storybook、Playwright 或明确人工检查。

## 常用默认值

| 场景 | 时长 | 运动 | 限制 |
| --- | --- | --- | --- |
| hover/focus/press | fast | opacity、颜色、scale 0.98–1 | 不影响可访问焦点 |
| row/card selected | fast | background、border、opacity | 不移动表格列 |
| panel/dialog enter | normal | opacity + 4–8px transform | 不遮挡标题和焦点 |
| panel/dialog exit | fast/normal | opacity + 小位移 | 先保存焦点与关闭事实 |
| list insert/remove/filter | normal | item continuity | 不用逐项长 stagger |
| loading/status | tokenized | spinner/progress | 不暗示成功或完成 |
