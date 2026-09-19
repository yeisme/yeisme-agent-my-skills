## Remote client image upload

先用已安装版本的 `eikona upload --help`、MCP discovery 与 `eikona://docs/local-media-upload` 确认能力。开发版实现不代表当前发布包已包含；缺命令或 backing 时报告能力缺口，交回 Eikona owner，不把客户端路径传给远程服务。

选择 PNG/JPEG/WebP 文件后，MCP 使用 `asset.upload.begin` 创建会话，客户端按返回的传输合同 HTTP PUT 文件字节，再用 `asset.upload.complete` 获得 `eikona://asset/<id>`。MCP JSON 不携带 base64 文件。CLI 等价路径：

```bash
eikona upload send ./reference.png --endpoint https://images.example.test --key-file /absolute/private/eikona-access.key --scope project-a --agent
eikona upload status upl_0123456789abcdef --endpoint https://images.example.test --key-file /absolute/private/eikona-access.key --scope project-a --agent
eikona upload abort upl_0123456789abcdef --endpoint https://images.example.test --key-file /absolute/private/eikona-access.key --scope project-a --agent
eikona upload cleanup --endpoint https://images.example.test --key-file /absolute/private/eikona-access.key --scope project-a --agent
```

Owner 通过 `eikona config upload set/unset/show` 配置 `local|s3|disabled`，用 `eikona config upload doctor --agent` 检查配置。local 需 `public_base_url`，字节落服务端受控磁盘且无需 S3；既有 S3 配置与 presigned PUT 保留，不在失败后静默切换后端。创建或变更真实服务配置、凭据仍遵循用户权限；上传使用明确具备 `media-upload-v1` 与项目 scope 的 access key，旧生成 key 不自动扩权。key 文件应为绝对路径、用户拥有、非 symlink、0600；不把 owner bearer 发给 S3，不跟随上传重定向，不输出传输 URL、grant、凭据或私有路径。

断流后先查状态，再用同文件与同幂等键重试；local PUT 从头传输，不声称字节偏移续传。元数据冲突先检查文件；过期或取消需新键新会话。abort/cleanup 只清理未完成数据，保留完成资产。使用 canonical asset ref 接入现有 edit/worker/delivery；上传完成不授予 rights、review 或付费生成权限，也不证明 URL-only provider 可达。缺 delivery route 时保留 blocker，交回 owner 修复，不触发付费探测或丢弃引用。

local 上传的资源限制通过同一配置命令管理：`max_concurrent_uploads` 控制同一上传根目录跨进程共享的传输/图片解码并发，`min_free_bytes` 控制 PUT 前的磁盘余量检查。默认分别为 4 和 64 MiB。HTTP 503 `UPLOAD_BUSY` 时遵循 `Retry-After` 并重试原会话；507 `UPLOAD_STORAGE_FULL` 时先由 owner 恢复磁盘容量，再重试。不得通过删除完成资产或扩大权限解决容量问题；doctor 仍只说明配置，不证明部署存储可用。

