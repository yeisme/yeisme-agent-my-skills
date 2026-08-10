---
name: ai-drama-continuity-supervisor
description: Use when checking or repairing AI drama continuity across characters, identity, costume, props, space, time, action direction, lighting, sound, subtitles, and episode versions.
---

# AI Drama Continuity Supervisor

## 目标

把连续性当成 production gate，而不是生成后凭感觉检查。跨镜头的角色、服装、道具、空间、时间、动作、光线、声音和字幕必须能从事实 refs 推导。

## 工作流

1. 读取 `references/continuity-evidence.md`，再读取 CanonSnapshot、SubjectVersion、StyleVersion、Scene/Shot refs 和已接受 artifact。
2. 建立 continuity matrix：事实、来源、适用镜头、前后状态和检查结果。
3. 区分 `pass`、`warn`、`block`、`unknown`、`stale`，不要把 unknown 当 pass。
4. 给出最小 repair proposal：重新绑定、局部重抽、改镜头、改时间线或请求人工确认。
5. 输出 finding/evidence，不直接修改 canonical state 或接受资产。

## 必须阻塞

- 主体身份或服装无法确认；
- 关键道具、伤口、位置、时间或动作方向冲突；
- subject/style/reference/preflight 版本过期；
- artifact 缺少 digest、来源或 owner receipt；
- 音画字幕时间无法复算。

## 验证

```bash
cd /workspaces/yeisme-agent/agent/scaena
task test:architecture
task test:integration
```
