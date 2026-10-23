---
name: cli-output-taste
description: "Use when designing, implementing or reviewing CLI resource discovery, tables, narrow terminals, actionable errors, next commands and shell completion; do not use for graphical UI design or routine CLI operation."
---

# CLI Output Taste

## 使用场景与输入

设计或修改资源发现、默认输出、错误恢复、Tab 补全时使用。先读取 owner 的命令树、资源查询、现有输出合同与相关测试；记录实际二进制版本。普通 CLI 操作、网页和全屏 TUI 不使用本 Skill。

## 工作流

1. 从真实注册信息确认 canonical 命令。资源读取使用 `list`、`get <id>`、`describe <id>`；保留独立的 `watch`、`inspect`、`download` 等语义，不机械改写已发布文件/视频合同。
2. 让列表、对象查询与补全消费同一只读目录。人读、`--agent`、`--json`、`--events`、`--explain` 从同一投影派生；协议细节以 `ai-native-cli-output-contract` 为准。
3. 人读 list 第一列给下一个命令原样接受的完整 id。固定列顺序，默认最多 20 行，窄屏逐条堆叠；截断与过滤分别计数。状态必须有文字，遵守 `NO_COLOR`，不能用 count 代替列表。
4. 只给一个真实、可粘贴 Next，和 actions 使用同一个值；保留查询范围并正确转义 id。选第一项已配置资源，否则第一项。空结果给清除过滤或已有创建入口；缺必填信息时用该入口的 `--help`，不输出伪装成可执行命令的占位符。
5. 缺参和未知 id 给缺失字段、可见的已知 id、恢复动作和 exit 2。权限拒绝不泄露不可见 id。目录失败不能伪装为空目录，未知 id 不能伪装成成功的空详情。
6. Tab 是目录的只读视图：250ms 查询预算、50 条上限、稳定排序、前缀过滤；不联网、不初始化或迁移状态、不读取秘密值。失败静默返回零候选；非路径位置使用 NoFileComp。

## 输出与验证

交付实际命令、实现 diff 和行为证据。锁定 80/120 列、长 id、空/过滤/截断目录、缺参/未知 id、Next 范围、stdout/stderr 分离与补全失败。小目录三种输出 id 集合相同；大目录用人读 `--all` 对齐机器结果；补全对齐同一快照下前 50 个匹配 id。

## 边界

- 不为统一外观新建跨仓 runtime、资源数据库或另一棵命令树。
- 不解析人读表生成机器结果；不调用文档中的写入或付费示例做语法校验。
- 本轮获批迁移中，旧详情 show 隐藏保留一个功能发布版本，机器字段及 command identity 保持；help、Next、补全菜单和正常文档只推荐 canonical 命令。补丁版本不提前删除。
- 安装 completion 不改 shell rc；doctor 区分文件存在与 shell 可发现。源码通过与 PATH 安装版通过分别报告。
- 产品实现留在 owner；本 Skill 只维护设计判断与验收规则。
