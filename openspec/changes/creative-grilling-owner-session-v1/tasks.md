# Skills 实施任务

以下实现均未执行。唯一写入 owner 是本仓库 `creative-writing-core/`；不写 `auctra-novel/`、`ai-drama/`、产品代码或宿主生成 runtime。一个实施者负责源内容与相关 validator，默认串行；无隐式子 Agent。

## 1. 共享协议与兼容

- [ ] 1.1 **Owner：Skills source；输入：旧 v0.1 三类合同；输出：可选 owner-session companion 合同。** 修改共享 contracts reference，保留旧 route/brief/handoff 字段与例子。验收：旧 consumer 不需要接受新必填字段，binding 有版本、来源、权限与 typed actions。验证：扩展并运行 `python3 creative-writing-core/creative-grilling/scripts/validate_creative_grilling_matrix.py`；失败复查兼容字段和误执行 shell 字符串。
- [ ] 1.2 **Owner：Skills source；依赖：1.1；输出：恢复/重开 Frontier 协议。** 更新现有 frontier/depth references；验收：同轮依赖、稳定 ref、旧 source、角色身份和未知转试写均有例子。验证：同一矩阵 validator，加人工执行恢复/重开 transcript canary；失败定位语义依赖与 owner 状态混淆，不新增私有状态文件。

## 2. 领域共创

- [ ] 2.1 **Owner：Skills source；依赖：1.2；输出：小说全阶段问法。** 更新既有 novel entry/frontiers，覆盖想法、人物、结构、章节、场景、成稿、修订与中途进入。验收：每个阶段至少一条有代价的选择、一条未知转 proof 场景，不能预问下游问题。验证：矩阵 validator 与小说合成 transcript canary；失败只修对应阶段，不复制领域状态引擎。
- [ ] 2.2 **Owner：Skills source；依赖：1.2；输出：做剧专用阶段问法。** 扩展既有 manga-drama frontiers 和 ai-drama decision map，保留短剧/电视/电影/单元/喜剧/音频差异。验收：明确领域零重复路由，不把所有做剧变成漫剧，不增加竞争 Router。验证：矩阵 validator 与至少电影、漫剧、音频剧三类 canary；失败复查媒介/受众推断。
- [ ] 2.3 **Owner：Skills source；依赖：2.1、2.2；输出：writer 往返与项目反馈规则。** 输入已确认阶段范围和授权，输出便携 handoff 与候选后重开范围。验收：访谈不代写、不自动 accept、不创建子 Agent，当前反馈不跨项目；未来 F1/F2/F3 明确未实现。验证：proof-return、reject-all、baseline-best、反馈冲突 canary；失败回到权限/来源/作用域判断。

## 3. 宿主适配与验证

- [ ] 3.1 **Owner：Skills source；依赖：1.1、2.3；输出：宿主无关动作与问答适配说明。** 验收：有控件用控件、无控件用编号文本；owner 缺能力返回 needs_contract 或 legacy handoff，不猜命令。验证：用 portable fake owner 与无 Plan 控件 transcript 走完整流程；失败复查隐藏宿主依赖。不得把宿主私有脚本写入可移植 Skill。
- [ ] 3.2 **Owner：Skills source；依赖：3.1；输出：扩展的静态矩阵与可审阅 canary 说明。** 复用既有 validator，至少覆盖新/旧 binding、无项目、stage entry、同轮依赖、stale、上游重开、拒绝全部、未知/proof、writer 往返、匿名反馈和越权。验收：旧 CG-01–CG-14 保留，新增用例不是仅检索词语就宣称交互有效。验证：矩阵 validator 与 `python3 scripts/validate_repository.py`；失败分类为本次、既有或环境，不改无关子模块。
- [ ] 3.3 **Owner：Skills source；依赖：3.2；输出：来源文档、元数据和最终规格状态。** 元数据经仓库生成工具维护；宿主同步留给宿主 adapter，不手写 runtime。验收：旧名称兼容、新增功能状态诚实、回滚可只关闭 binding。验证：`openspec validate creative-grilling-owner-session-v1 --strict --no-interactive`、source scoped diff 和前述验证；没有实现/真实 canary 证据时不勾选。

## 依赖与证据

1.1 → 1.2 → 2.1/2.2 → 2.3 → 3.1 → 3.2 → 3.3。2.1/2.2 内容可分别准备，但共享协议、validator 和发布输入由单一 owner 串行整合。源内容测试不依赖真实 Auctra、模型或外部读者；人工 transcript 使用合成内容与简短结论，不保存原始模型提示或私人会话。
