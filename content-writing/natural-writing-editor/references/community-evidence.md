# 社区方案证据与纳入策略

核验日期：2026-08-19；2026-09-04 增补核验 sepia。所有来源按精确提交审阅；本 skill 是第一方原创综合，不复制未授权提示词、范文或大型词表。

## 已审阅来源

| 来源 | 固定提交 | 许可证 | 吸收的高层原则 | 不直接吸收的部分 |
| --- | --- | --- | --- | --- |
| [blader/humanizer](https://github.com/blader/humanizer) | `e2e92e7b4b8229253ed5c8e81dc65463fdeddda5` | MIT | 保真优先、作者声音证据、模式误判保护 | 35 类完整清单不放入主 skill |
| [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) | `8da1f030185bdfe8471220585162991eaeb970e9` | MIT | 删除优先、具体化、强力清理作为可选档 | “禁用全部副词/被动/破折号”等绝对规则 |
| [op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh) | `91f3d394db8419c20d67ebe22a96cf8fee0a404b` | MIT | 中文常见模式覆盖、专项审阅价值 | 不默认加载完整 24 类流程，不与主流程叠加改写 |
| [B1lli/remove-ai-flavor-writing-skill](https://github.com/B1lli/remove-ai-flavor-writing-skill) | `5edd9fa055292cdb854b210e806ad4fb64910bbe` | MIT | 结构→声音→句壳→词语→结尾、局部修改、文体豁免 | 宣传段和过度流程化交互 |
| [yyx20202020/natural-writing-skill](https://github.com/yyx20202020/natural-writing-skill) | `71af993050cc0885eee98c2b421a965e7fde2b43` | MIT | 任务/强度/范围分离、受保护内容、质量门 | 不复制其提示词、脚本或文件结构 |
| [av8d-levelup/voice-guard-zhtw](https://github.com/av8d-levelup/voice-guard-zhtw) | `8f2eceee24d362be268b37ac2f08074382d746eb` | MIT | 作者主动保护层、机械召回与人工判断分层 | AI 指数不作为质量结论，繁中地域规则不设为全局默认 |
| [ruodou233/de-ai-taste](https://github.com/ruodou233/de-ai-taste) | `2a7c9154e8d48354a7ddf9778bb17ac2c62dd20d` | MIT | 信号需满足门槛、语境豁免、正式建议与观察项分开 | 不复制其大规模信号库，不自动执行更新检查 |
| [OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL](https://github.com/OUBIGFA/De-AI-Prompt-Enhancer-Writer-Booster-SKILL) | `b050eefa88af3709ec24fc0b353740ccb151f563` | 未声明 | 仅作为用户指定的行为对照和 canary | 不复制提示词、范文、规则文本或脚本 |
| [Nanako0129/sepia](https://github.com/Nanako0129/sepia) | `0326635aa2cee589e6f525af1ec6089d51944f3c` | MIT | 虚构叙事三遍架构协议+30 特征 rubric（StoryScope 实证）、工程 venue 域规则、分模型指纹，作为按需参考层 | 不安装 4 个 operation wrapper 与 plugin 包装；不复制其文本进第一方；不从文本反推作者模型；不把检测器分数当验收 |

`.skills/imported/text-writing/good-writing/` 同样缺少明确上游许可证且含完整参考范文，只允许用户明确要求时本地按需研究，不进入默认运行时，也不把范文内容转写到第一方 skill。

`.skills/imported/text-writing/sepia/` 通过 `scripts/skills.sh import` 只引入 canonical 单目录（SKILL.md + references + LICENSE），不进 profile、不出现在默认运行时；由本 skill 的「与社区技能的关系」条款按文本类型触发加载，中文普通散文默认不触发。

## 纳入新社区方案的门槛

每个候选必须完成：

1. 记录仓库 URL、精确提交、核验日期和许可证；
2. 说明它相对现有分类带来的唯一增量；
3. 区分可复用原则、可引用实现和不可再分发内容；
4. 检查是否引入绝对禁词、检测器规避、虚构细节或作者模仿风险；
5. 把新规则转成至少一个正例和一个误判负例；
6. 先作为 source-layer canary 或按需参考，不直接加入 root profile；
7. 通过 `quality-gates.md` 的保真和人工偏好回归后，才合并进第一方分类。

## 维护决策

- 相同目的的完整 humanizer 默认只保留一个 active primary；
- `sepia` 保持源层参考定位：升级须换钉新提交并重走本门槛，wrapper 与 plugin 包装始终不引入；
- 社区词表只用于召回，不成为硬性规则；
- 高星数和热度只是候选信号，不代表规则正确；
- 没有许可证的仓库只能做行为层观察，不能复制内容；
- 新模型带来的新模式优先补进 reference 和回归用例，不膨胀主 `SKILL.md`；
- 任何更新若提高“去味分数”却降低事实准确率、作者偏好或场景适配，应回退该规则。
