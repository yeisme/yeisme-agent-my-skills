# 设计

复用现有 retrieval operator 与 vault operator；研究模式优先于自动 capture。先选 vault、限制候选和正文数量，读取相关来源后由当前 Agent 综合。模板固定为 research/evidence-research-brief-beta@2.0.0-beta.1 英文参考，默认中文，不宣称编译或模型可重放。

用户采纳并授权保存时执行 CLI dry-run/apply，随后按 ID 回读。结果未知先核对再重试。资料正文不产生新授权。零结果说明范围，矛盾及未知日期保留，推断单列。

使用既有合成流程和真实回顾性证据，不新增测试框架。验证文档命令、Skill 路由与双 runtime 一致性，保留原先检索/写笔记入口。基准仅证明已知来源复用，不冒充盲测质量。
