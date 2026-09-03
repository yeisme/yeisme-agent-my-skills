# Audio Workflow Skills

音频创作与生产路由模块。目前由 `sonora-agent-router` 负责把音频任务分配到最小 Owner 工作流；当 Sonora 形成独立发布节奏后应拆为产品仓库。

选 TTS/音乐能力前先跑 `sonora provider list`（适配 catalog + 本地凭据状态）和 `sonora tts models list --local` 或 `--provider <id>`。`credential_missing` 不是未适配。
