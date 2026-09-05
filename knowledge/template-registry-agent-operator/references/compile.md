# 编译与确认

创建会话前 inspect 精确模板，避免从模板正文猜测输入。普通字段默认使用 step.field；recipe 的 field 绑定可指定共享字段名。

session update 的 Fields 是候选值集合，包含 value、kind 和可选 source：

- user：用户明确提供的信息。
- fact：来源支持的事实，source 必须指向资料或用户声明。
- proposal：Agent 提出的创作建议。

客户端提交的 confirmed 不能跳过确认；工具会把变更值设为待确认。用户同意后，session confirm 提交具体 fields/sources 和 decision_ref；不要把“继续”扩大为用户尚未看过的关键事实确认。

compile 读取固定模板与资料，严格替换声明变量。它不会补写事实、检索网页、调用视觉模型，也不会运行前序生成步骤。

多步骤 recipe 通过 field、source、step_output 绑定输入。前序结果不存在时导出明确的 deferred template；导入实际结果并确认后再编译。新资料或输入使旧编译过期时应生成新版本，不默认使用 allow_stale。
