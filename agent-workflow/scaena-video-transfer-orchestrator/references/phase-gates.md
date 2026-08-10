# 视频转绘阶段门禁参考

该文件供 `scaena-video-transfer-orchestrator` 按需读取。它描述测试项目的交互阶段，不拥有 Scaena canonical state。

## 阶段表

| 阶段 | 允许动作 | 必须阻塞的动作 | 进入证据 | 退出证据 |
| --- | --- | --- | --- | --- |
| `package_ready` | `scaena.transfer.adaptation.propose`、展示上下文 | 重新拆解、生成 | package path、digest | package validate=`ok` |
| `adaptation_pending` | `scaena.transfer.style.preview` | 直接批量生成主体或视频 | context projection | adaptation brief ref |
| `style_sampling` | `scaena.transfer.job.watch`、四张样本完成后 `scaena.transfer.style.lock` | 批量资产冻结 | style/market refs | four artifact refs + explicit style lock |
| `style_locked` | `scaena.transfer.asset_batch.plan` | 无计划批量生成 | explicit style-lock decision | locked style ref |
| `asset_batch_planned` | `scaena.transfer.asset_batch.generate` | 直接绑定 episode/shot | six-subject plan | explicit generation confirmation |
| `asset_batch_running` | `scaena.transfer.job.watch` | 生成哨兵镜头 | Eikona job ref | at least six identity artifact refs |
| `assets_review` | 比较候选、记录 feedback、生成 correction candidate | 自动 accept/freeze | artifact refs/digests | human review decision |
| `shot_preview_running` | `scaena.transfer.job.watch` | 整集生成、导出 | one 2–5 second shot intent + candidate refs | preview artifact ref |
| `shot_review` | `scaena.transfer.shot_review.record` | 自动进入 final | preview + findings | accepted/revise decision |
| `prompt_revision` | `scaena.transfer.prompt_revision.propose`，确认后重跑哨兵镜头 | 直接进入整集 | redacted reason codes | revised sentinel accepted |
| `final_generation` | 仅对已批准、已冻结、已 preflight 的请求执行 | 改写 canonical、跳过 review | immutable bundle + approval | Scaena pending-review receipt |

## 必备检查

### Package

- 归档路径必须是项目相对路径。
- 必须存在 `patches/characters/characters.json`、`patches/scenes/scenes.json` 和至少一个 `patches/episodes/*.json`。
- 角色、场景、分集和镜头数量不能为零。
- 对外只暴露 `decomposition-package:sha256:<digest>`，不暴露本地绝对路径。

### Market adaptation

- 韩国市场与视觉风格分别版本化。
- 原阿根廷姓名、脸、学校标识、车牌、西班牙语公告和地域物件不能直接进入韩国版本。
- 人物关系、行动功能、动作顺序和情绪因果是默认继承项。
- “B 只改外貌”不能被扩展成自动改写故事或关系。

### Asset candidate

- Primary character 至少需要 front、three-quarter、profile、full-body、neutral/core expression 和 default wardrobe。
- Candidate 需要来源、权限、model、reference role、digest 和 review 状态。
- Eikona accepted candidate 不等于 Scaena frozen subject。

### Video input

- 本地 CLI 可把显式传入的单个项目外普通文件直接复制/去重进项目 CAS；不得要求复制、symlink 或 hardlink staging，原始路径不得持久化。
- source video 必须先登记、分析、冻结并绑定 asset/blob/revision。
- `reference_video` 只能使用 opaque durable ref、revision、角色和时间区间。
- 本地路径、`file://` 和任意 HTTPS URL 只能用于受控 admission/bridge，不能直接冒充 durable `reference_video` ref。
- bundle 必须固定 prompt、capability、shot、subject/style/reference 版本和 idempotency key。

## Handoff 形状

```text
status=<ok|running|requires_action|blocked|failed>
phase=<phase>
package_ref=<ref>
adaptation_ref=<ref|none>
style_ref=<ref|none>
candidate_set_ref=<ref|none>
shot_ref=<ref|none>
bundle_ref=<ref|none>
blocking_findings=<codes/refs>
next_command=<real command or owner tool>
evidence_refs=<refs>
```
