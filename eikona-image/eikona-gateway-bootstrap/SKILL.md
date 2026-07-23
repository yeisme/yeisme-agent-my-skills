---
name: eikona-gateway-bootstrap
description: Use when a user provides an image gateway base URL, API key, channel name, or exact image model ID and wants an agent to install, configure, verify, or reuse Eikona across projects without writing provider scripts or storing credentials in repositories.
---

# Eikona 网关快速接入

把用户提供的 OpenAI-compatible 图像网关接入 Eikona 用户级 auth store，验证准确模型路由，并把后续生成交给 Eikona evidence、review、feedback 和 handoff 链路。

## 输入

- 网关 `base-url`、API key、可选 channel 名；默认 channel 使用 `gateway`。
- 网关公开的准确 model ID、协议/transport 说明，以及当前项目目录。
- 可选的低成本 smoke prompt；真实生成前必须获得用户对潜在费用的明确同意。

只缺少 model ID 时，要求用户提供网关模型列表或文档中的准确 ID。`Nano Banana Pro` 是产品称呼，不是可安全猜测的 model ID。

## 工作流

1. 检查 Eikona，并初始化用户级配置；不要默认创建项目级配置：

```bash
eikona --version
eikona init --user --json
```

2. 选择 Eikona model ref：
   - GPT Image 默认使用 `openai:gpt-image-2`。
   - 普通 OpenAI-compatible gateway 使用 `openai:<exact-model-id>`。
   - ImageRouter 使用 `imagerouter:<exact-model-id>`。
   - OpenRouter 使用 `openrouter:<exact-model-id>`。
   - 前缀表示 Eikona adapter，不表示营销名称；不要把 `Nano Banana Pro` 自动改写成任何猜测 ID。

3. 只通过 stdin 保存 key。未显式传入 `--config` 时，Eikona 默认把 channel 和 local secret 写入用户级 `~/.eikona/`；Agent 应启动该命令并把用户提供的 key 写入进程 stdin，不能把 key 放入参数、项目文件或 shell credential script。人工终端可运行：

```bash
read -rsp 'Gateway API key: ' EIKONA_API_KEY; echo
printf '%s\n' "$EIKONA_API_KEY" | eikona auth set gateway \
  --protocol openai \
  --base-url https://gateway.example.com/v1 \
  --api-key-stdin \
  --default-model openai:gpt-image-2 \
  --json
unset EIKONA_API_KEY
```

把 `--default-model` 替换为网关公开的准确 Eikona model ref。只有用户明确要求隔离 channel 时才使用 `eikona --config <path> auth set ...`。不要运行 `eikona auth env`，因为它会把 secret 输出到 stdout。

4. 读取脱敏状态并注册当前项目：

```bash
eikona auth check gateway --agent
eikona config inspect --agent
eikona projects register . --agent
```

5. 根据网关协议做真实 smoke generation。GPT Image 的 OpenAI Images-compatible 示例：

```bash
eikona "minimal geometric product image, white background, no text" \
  --channel gateway \
  --model openai:gpt-image-2 \
  --size 1024x1024 \
  --set api=images \
  --wait \
  --agent
```

网关明确要求 Chat Completions multimodal transport 时，使用准确 model ID：

```bash
eikona "minimal geometric product image, white background, no text" \
  --channel gateway \
  --model openai:<exact-model-id> \
  --size 1024x1024 \
  --set api=chat \
  --wait \
  --agent
```

ImageRouter 示例只替换准确 ID，不猜 Nano Banana 型号：

```bash
eikona "minimal geometric product image, white background, no text" \
  --channel gateway \
  --model imagerouter:<exact-model-id> \
  --size 1024x1024 \
  --wait \
  --agent
```

6. smoke 成功后，把视觉任务交给 `eikona-product-asset-director` 或匹配的垂直场景 director。切换项目时只需在新项目运行：

```bash
eikona projects register . --agent
```

项目移动后，根据 `projects list` 返回的 project ID 修复根路径：

```bash
eikona projects list --json
eikona projects repair-root <project_id> --root /new/project/path --json
```

## 输出

- channel、protocol、base URL、credential configured 状态、准确 model ref、transport、project ID 和下一条真实 Eikona 命令。
- 只报告脱敏事实；不得输出 key、Authorization header、secret value、provider 原始响应或完整思维链。

## 边界

- 不写 Python、JavaScript、curl、base64 解码或下载脚本代替 Eikona。
- 不把 key 写入仓库、项目 `.eikona/config.yaml`、命令参数、日志、trace、run evidence 或 skill 输出。
- 不调用 `auth env`，不从 human output 解析状态；agent 自动化使用 `--json`、`--agent` 或 `--events`。
- 如果当前 Eikona runtime 无法把该 channel、adapter 或 transport 路由到网关，停止生成并交给 `yeisme-eikona-cli-runtime`；不要绕过 Eikona 直接调用网关。

## 验证

- `auth check` 只显示 configured/resolved 状态，不显示 secret。
- smoke run 返回 `run_id`、结构化状态和下一步命令。
- 第二个项目无需重新输入 key，只需注册项目并复用 channel。
