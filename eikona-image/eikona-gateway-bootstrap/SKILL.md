---
name: eikona-gateway-bootstrap
description: Use when a user provides an image gateway base URL, API key, channel name, or exact image model ID and wants an agent to install, configure, verify, diagnose reference-image support, or reuse Eikona across projects without writing provider scripts or storing credentials in repositories.
---

# Eikona 网关快速接入

开始前先读取 `cli/eikona/docs/commands/agent-operability.md`，并报告该文档定义的 evidence vector 与 conservative effective level。`configured=pass` 或 `remote_probed=degraded` 不能授权生成；只有用户明确同意潜在费用时，才可以进入 paid/live gate。

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
eikona init --user --agent
```

2. 先列出代码已适配的模型，再复制网关准确 ID。不要把空 `models.lock` 或未配置 channel 当成未适配：

```bash
eikona models list --source adapted --all --agent
eikona models list --source adapted --provider openai --all
eikona auth list --agent
```

3. 选择 Eikona model ref：
   - GPT Image 默认使用 `openai/gpt-5.4-image-2`。
   - bare 短别名 `gpt-5.4-image-2` / `gpt-image-2` 已在 Eikona 0.6.0 从主入口移除；所有配置与证据只写 slash canonical ref（v1 handoff 域保留独立 alias policy）。
   - 对 GPT Image，provider-colon 和重复 provider 前缀形式一律在联网前拒绝；不要为 canonical ref 添加 provider 前缀。
   - 如果 `/v1/models` 返回的完整 ID 是 `openai/gpt-5.4-image-2`，必须把该 slash ID 原样复制到 Eikona。
   - ImageRouter 使用 `imagerouter:<exact-model-id>`。
   - OpenRouter 使用 `openrouter:<exact-model-id>`。
   - 前缀表示 Eikona adapter，不表示营销名称；不要把 `Nano Banana Pro` 自动改写成任何猜测 ID。

4. 只通过受保护 stdin 或已存在的 mode-0600 key file 授权保存 key。未显式传入 `--config` 时，Eikona 默认把 channel 和 local secret 写入用户级 `~/.eikona/`；Agent 不得读取、缓存或转发 key，也不能把它放入参数、项目文件或 shell credential script。用户在受保护的交互 stdin 中输入 key 后可运行：

```bash
eikona auth set gateway \
  --protocol openai \
  --base-url https://gateway.example.invalid/v1 \
  --api-key-stdin \
  --default-model openai/gpt-5.4-image-2 \
  --agent
```

把 `--default-model` 替换为网关公开的准确 Eikona model ref。只有用户明确要求隔离 channel 时才使用 `eikona --config <path> auth set ...`。不要运行 `eikona auth env`，因为它会把 secret 输出到 stdout。

私有或开发网关必须由用户提供其 HTTPS base URL 和准确 model ID；Skill 不得硬编码内网或明文 endpoint。其授权方式仍为受保护 stdin 或已有 mode-0600 key file，且 agent 不读取 key 内容。

provider-colon、重复 provider 前缀或未知 model ref 是歧义错误形式，必须在联网前失败；canonical slash ref 可直接提交。

5. 读取脱敏状态并注册当前项目：

```bash
eikona auth check gateway --agent
eikona config inspect --agent
eikona projects register . --agent
eikona models readiness openai/gpt-5.4-image-2 --channel gateway --agent
```

6. 先把纯文生图作为独立基线。只有用户任务需要参考图、且用户同意潜在费用时，才继续验证参考输入；不要把三种能力混成一次 smoke：

| 能力 | Eikona 请求 | 首选接口 | 结论 |
| --- | --- | --- |
| 纯文生图 | 无 `--ref` 的 `image.generate` | `/images/generations` | 证明模型和基础路由可用，不证明图生图可用 |
| 编辑式图生图 | `--ref` + `--reference-mode edit` | multipart `/images/edits` | 输入图是待修改画布 |
| 参考图条件生成 | `--ref` + `--reference-mode generate` | `/responses` multimodal `input_image` | 输入图只提供风格、布局或主体指导 |

编辑能力 smoke：

```bash
eikona generate --use-channel gateway --model openai/gpt-5.4-image-2 --ref ./reference.png --reference-mode edit --size 1024x1024 --prompt "Keep the source composition and make the background warmer." --agent
```

参考条件生成 smoke：

```bash
eikona generate --use-channel gateway --model openai/gpt-5.4-image-2 --ref style=./reference.png --reference-mode generate --size 2k --aspect 16:9 --prompt "Create a new product page using only the reference's visual language." --agent
```

7. 根据网关协议做真实 smoke generation。GPT Image 的 OpenAI Images-compatible 示例：

```bash
eikona "minimal geometric product image, white background, no text" \
  --channel gateway \
  --model openai/gpt-5.4-image-2 \
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

8. smoke 成功后，把视觉任务交给 `eikona-product-asset-director` 或匹配的垂直场景 director。切换项目时只需在新项目运行：

```bash
eikona projects register . --agent
```

项目移动后，根据 `projects list` 返回的 project ID 修复根路径：

```bash
eikona projects list --agent
eikona projects repair-root <project_id> --root /new/project/path --agent
```

## 参考图失败诊断

1. 使用 `eikona inspect <run_id> --brief --agent` 读取当前 CLI 暴露的脱敏失败摘要（深度取证才用 `--json --full`），并结合 `eikona providers doctor <provider> --agent`。如果输出没有明确区分 endpoint 或 transport，就保持 `unknown/degraded`；不要只凭“带参考图失败”猜根因。
2. 只有现有证据明确标识 `/images/edits` 为 unsupported 时，才能说明编辑接口不可用。任务意图是“新生成并参考风格”时，可以在获得用户同意后用新的 `--reference-mode generate` run 验证另一语义路径。
3. 只有现有证据明确标识 multimodal reference input 不受支持时，才记录该 channel 的对应能力缺口。不要继续手工轮换 transport，也不要声称已保留参考图一致性。
4. 用户接受语义降级后，创建一个新的无 `--ref` run，并把参考图中的可见约束转写为明确产品 brief。失败 run 保留用于审计；认证、限流、内容拒绝、超时、TLS 或 malformed response 不是参考图不支持的证据，不得通过删除参考图掩盖。

## 输出

- channel、protocol、base URL、credential configured 状态、准确 model ref、transport、project ID 和下一条真实 Eikona 命令。
- 只报告脱敏事实；不得输出 key、Authorization header、secret value、provider 原始响应或完整思维链。

## 边界

- 不写 Python、JavaScript、curl、base64 解码或下载脚本代替 Eikona。
- 不把 key 写入仓库、项目 `.eikona/config.yaml`、命令参数、日志、trace、run evidence 或 skill 输出。
- 不调用 `auth env`，不从 human output 解析状态；例行 agent 自动化使用 `--agent`，观察非终态 run 用 `--events`，脚本/CI 用 `--json --compact`（共存期内裸 `--json` 仍是 legacy full），取证用 `--json --full`。
- 如果当前 Eikona runtime 无法把该 channel、adapter 或 transport 路由到网关，停止生成并交给 `yeisme-eikona-cli-runtime`；不要绕过 Eikona 直接调用网关。
- 不把纯文生图成功描述成编辑式图生图或参考图条件生成成功；三种能力必须分别验证和报告。

## 验证

- `auth check` 只显示 configured/resolved 状态，不显示 secret。
- smoke run 返回 `run_id`、结构化状态和下一步命令。
- 第二个项目无需重新输入 key，只需注册项目并复用 channel。
