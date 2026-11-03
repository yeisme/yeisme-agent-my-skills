# 按精确模板读取完整教程

MCP：发现 template_registry_guide，传入 ref 与 role，显式 resources/read 返回的 URI；随后 inspect，按 agenda 补齐资料和确认。优先使用已连接工具，不在没有 CLI 的客户端运行安装命令。

CLI：

```bash
template-registry prompt commands --operation guide --json
template-registry prompt guide --ref 'promptrepo://official/general/structured-summary-beta@2.0.0-beta.1?locale=en' --role main --section overview --output summary-overview.md --json
```

--output 是 CLI 显式导出选项，路径属于当前项目，不覆盖已有文件。MCP guide 不接受 output，正文通过资源读取。读取指南不需要先创建会话，也不要求该模板可编译。

GUIDE_NOT_FOUND 表示此快照缺教程；GUIDE_UNSUPPORTED 表示来源缺读取能力；GUIDE_STALE 表示快照或教程已改变，重新发现并核对版本；不得自行换模板版本。旧安装没有 guide 时使用现有 inspect 与文档入口，并明确版本缺口。

stdio 与 Streamable HTTP 使用相同操作；HTTP 由宿主配置私有 token 文件和 loopback /mcp 地址。资料路径属于 server project，安装解析器、凭据配置和 author-root 登记由宿主执行。不得假设客户端文件已在服务端；文本可直接导入，二进制传输须使用已公布合同。

交付时报告模板/角色、已确认与缺失输入、原 session、输出位置和 next step。远程取包使用返回的 compile/package resource；服务器路径不是客户端下载位置。

section 可选 overview、inputs、example、checks、recovery、full。省略时保留全文行为。digest 始终对应全文，content_digest 对应实际所选字节；GUIDE_SECTION_UNAVAILABLE 表示旧教程没有该角色的稳定章节标记，不按任意 Markdown 标题猜测。
