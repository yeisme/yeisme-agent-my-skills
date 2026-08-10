---
name: ai-drama-showrunner
description: Use when planning an AI drama season, multi-episode arc, episode function, long-term character change, suspense, payoff, production priority, or next-episode handoff.
---

# AI Drama Showrunner

## 目标

管理持续生长的故事生态：世界规则、长线人物变化、季度主题、单集功能、悬念兑现和制作优先级。Showrunner 负责方向和取舍，不直接成为 provider scheduler。

## 工作流

1. 读取 CanonSnapshot、已完成 episode、角色状态和未兑现伏笔。
2. 定义 season/arc promise、episode question、局部 payoff 和末尾 hook。
3. 为每集分配人物变化、冲突升级、信息释放、视觉/声音重点和生产风险。
4. 检查集间因果、悬念债务、角色成长速度和制作资源冲突。
5. 输出 `ShowrunnerPlan` 与 episode proposals，交给 Dramaturge/Auctra/Scaena owner。

## 质量门槛

- 每集必须有独立可感知的情绪弧；
- 长线悬念必须标注预计兑现窗口和风险；
- 不能靠新增设定无限延长故事；
- 关键人物变化必须由事件和选择驱动；
- 计划必须能降级成可生产的短集，而不是只在概念层成立。

## 边界与验证

不复制 canonical story、不直接 dispatch provider、不自动接受 episode。验证使用对应 owner 的 OpenSpec 和测试：

```bash
cd /workspaces/yeisme-agent/agent/scaena
task test:architecture
```
