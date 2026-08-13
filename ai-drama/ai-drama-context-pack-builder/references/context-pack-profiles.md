# AI 做剧上下文包 Profile

## 选择规则

每次只选择一个 profile。上下文包服务具体下游，不是项目备份或百科导出。

| `pack_profile` | 适用下游 | 必须包含 | 默认排除 |
| --- | --- | --- | --- |
| `series-development` | `ai-drama-format-strategist`、`ai-drama-showrunner` | 形态/类型合同、主题、世界规则、核心人物、长期问题、制作边界 | 全部场景细节、历史镜头证据 |
| `episode-planning` | `ai-drama-showrunner`、`ai-drama-story-architecture` | 季度状态、上集结果、本集功能、人物状态、活跃悬念、下集承诺 | 无关支线百科、完整旧集正文 |
| `scene-drafting` | `screenplay-scene-writer` | accepted beat、场景目标、人物欲望/秘密/知识边界、前后场连接、可拍限制 | 全季规划全文、无关视觉资产 |
| `director-planning` | `ai-drama-director` | accepted scene、观众目标、人物行动、空间、道具、表演和制作限制 | 未接受候选、无关世界设定 |
| `visual-production` | `ai-drama-visual-language`、视频参考导演 | ShotIntent、主体/风格/reference 版本、构图/动作、连续性和负面约束 | 完整剧本、未冻结主体候选 |
| `review-repair` | `ai-drama-critic-panel`、连续性监督 | frozen candidate、rubric、旧 revision、findings、修复范围、预算轮次 | 其他评委私有输出、未授权全文 |
| `assembly-delivery` | `ai-drama-edit-and-sound`、`ai-drama-producer` | 已接受镜头/音频/字幕 refs、时间线、技术规格、rights/cost/readiness | 创作候选池、无关研究材料 |

## 最小化测试

对每个候选字段询问：

1. 删除它是否会让下游改变人物、事实、镜头、成本或验收判断？
2. 它是否属于当前阶段，而不是以后可能有用？
3. 它是否有 current owner ref、版本和来源等级？
4. 它是否可以用摘要/ref 替代全文或 bytes？

若前三问均为否，应排除；若第四问为是，应只保留摘要/ref。

## 重建条件

- Auctra canon/scene/character revision 变化；
- Scaena ShotIntent、SubjectVersion、ProductionGraph 或 production profile 变化；
- StyleLens、DirectorProfile、rights、permission 或 cost policy 变化；
- Inferrum generation、ContextPack freshness 或 citation 失效；
- 下游 target skill、phase 或 artifact 改变。
