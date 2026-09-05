# 导入与分析

以 `template-registry prompt commands --json` 的 source.import / source.analyze schema 为准。可用输入是 path、url、text，三者选一；复杂输入通过 stdin 传入。

source.import 支持 bind 指向 step.field，并可用 step_output 把实际产物绑定到前序步骤。资料修改会取消相关确认并使旧编译过期。

PDF/DOCX 缺少本地解析组件时，doctor 会报告。用户明确要求安装后使用：

```bash
template-registry prompt parser install --json
```

图片或扫描页需要观察时，读取 source resource 和返回的 page resources。工具返回的 page_locations 是原始页码；不要把扫描页数组下标当成原文页码。回填 text 和 locations，等待用户确认观察是否可用于当前任务。

宿主不能处理时，保留 needs_analysis。用户可通过 analysis configure 选择本地/外部后端；只有显式 source analyze 的 configured 后端会发送资料到该配置服务。默认不自动发送。

公开 URL 获取不能访问本机私有服务或携带 URL 用户密码。动态网页的薄内容需要已配置网页获取适配器或宿主回填，不能把导航栏当成正文。音视频与需登录平台不属于当前输入支持范围。
