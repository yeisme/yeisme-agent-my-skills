---
name: radar-operator
description: "Use when a user mentions the retired Short-Drama Radar, radar CLI, 短剧雷达 or Morning Edition and needs the retirement notice or routing to manju-hotlist; never operate or reinstall the old project."
---

# Radar 退役兼容说明

2026-10-01用户批准本地Short-Drama Radar退役。旧工作区、gitlink、Git metadata、target profile和活跃登记已退出；本Skill原名仅保留一个发布周期的兼容通知，不是可运行的operator。

## 替代路径

今天热门漫剧榜、原始名次、来源日期、人工输入或同口径变化转交`manju-hotlist`，由当前助手复用`tools/manju-hotlist/`固定脚本。在Yeisme工作区根执行：

```bash
bun run tools/manju-hotlist/cli.ts sources --json
bun run tools/manju-hotlist/cli.ts doctor --json
```

用户明确要求刷新时使用新Skill的`collect`，不恢复或安装旧产品。新工具没有个人评分、Morning Edition、watch/reader状态、数据库、Agent服务或生产assignment；不要把轻量榜单描述为完整替代这些已退役能力。

## 保留与禁止

- 不运行旧`radar`CLI，不建议旧工作区fallback、MCP/HTTP连接、schedule或assignment创建。
- 不重建旧目录、target profile、后台服务或OS任务，不安装凭据、不登录，不删除用户级旧数据、远程仓或历史项目。
- Auctra/Scaena历史文件导入合同继续保留；只按对应owner规则处理已有文件，不让新榜单工具生成旧文件。
- MicroDrama Radar是第三方榜单来源，与本地退役产品不同；保留其来源、链接、适配与快照。
- 来源双轮24小时仍是独立质量待办，不代表旧项目需恢复，也不声称持续性已通过。

## 恢复边界

本地恢复只能由用户另行明确要求，先查根固定目标恢复脚本的dry-run和私有备份，不自行读取秘密或把备份上传。参考`tools/manju-hotlist/docs/retirement.md`；本地退役不等于远程删除、发布或部署。
