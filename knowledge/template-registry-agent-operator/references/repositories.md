# 仓库来源

优先把 Git 托管平台提供的 clone address 原样交给 Registry：

```bash
template-registry prompt repository add --id official --source https://github.com/yeisme/prompt-templates --revision main --trust official --json
template-registry prompt repository add --id team --source ssh://git@github.com/OWNER/team-prompts.git --revision main --trust user_trusted --json
template-registry prompt repository add --id personal --source git@github.com:OWNER/personal-prompts.git --revision main --trust user_trusted --json
template-registry prompt repository add --id shorthand --source github.com/OWNER/prompt-templates --revision main --trust user_trusted --json
```

同步后再搜索，不从仓库网页正文猜模板：

```bash
template-registry prompt repository sync --id official --json
template-registry prompt search --query 'image generation' --locale en --json
```

兼容地址 `github://owner/repository`、`git+https://...`、`git+ssh://...` 和
`git+file://...` 继续可用。`file://...` 表示本地目录来源，语义不同于本地 Git 仓库。

source 必须是 repository clone address。拒绝 `/tree/<branch>`、release/ZIP 页面、URL
query、fragment、HTTP userinfo 和 SSH password。SSH username（通常为 `git`）可以保留；
凭据由本地 Git/SSH 或 Registry credential 配置持有，不进入会话、日志和提示包。
