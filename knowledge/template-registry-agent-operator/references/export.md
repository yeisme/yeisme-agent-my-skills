# 导出、验证与接续

export 的 compile_id 指向已经生成的编译记录。输出路径位于项目内，默认不覆盖已有文件。

- portable：默认模式，携带提示词、步骤、复现配置和允许复制的资料。
- references：显式选择的轻量包，外部依赖必须由接收方重新提供；它不是隐私脱敏模式。
- prompt：导出选定 ready 步骤的单条提示词；不允许将待回填步骤冒充可直接执行。

目录和 ZIP 都需要 bundle verify。验证检查逐文件 digest、可搬运路径、DAG、模板合同和完整包的重新渲染一致性。

session list/show/resume 用于同项目接续；bundle import 用于新项目，导入时不会运行包内容，并要求接收方重新确认。资料缺失或版本不兼容时保留明确缺口，不手改 manifest 绕过校验。

私有内容通过 MCP resources 显式读取，或 session read 写入指定本地文件。普通输出和运行证据只保留引用、状态、digest 与脱敏结论。
