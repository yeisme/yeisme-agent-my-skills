# 数据库交互性能：少查、少搬、少锁、可重放

用于关系型数据库模型、GORM repository、预算/配额、队列、连接池和迁移优化。产品规格优先；本参考不授权修改生产数据、启动收费服务、执行迁移或运行 race。

## 输入与输出

输入：owner 的 AGENTS/spec、准确 revision 与 dirty 边界、访问模式、状态机、所有 writer、事务/锁序、规模与性能证据。

输出：静态发现和假设分栏、数据权威/不变量、候选模型与查询预算、迁移/恢复/回滚、原子任务、真实验证结果及未验证项。没有数据库实测不得承诺倍率或将竞争窗口描述成线上事故。

## 最小流程

1. 先分类数据：权威可变状态、不可变账本/事件、可重建投影、大对象、短期缓存。一个事实一个 owner；三平面/多服务不自动意味着分库。
2. 列关键访问模式：scope、过滤、排序、页大小、必要列、期望一致性与总量语义。先测 SQL 次数、rows/bytes、尾延迟和锁，再选择优化。
3. 先修正确性，再减少访问/搬运/锁内工作；外部 I/O 在短事务提交后执行，以持久化意图、幂等结果和 reconciliation 恢复。
4. 用同负载 baseline/candidate/rollback 评估，保留错误、失败和 skip；专用时序/检索/副本仅在证据充分且 owner 批准后引入。

## 查询与 ORM

- 列表 Select 必需列，详情/正文按需读；本页 parent IDs → 批量选最新 child versions → 批量关联摘要，禁止每行查询或全历史加载后求最新。
- 保留摘要、排序、空值、权限与 scope。不能为“快”删除 digest 或只保留 COUNT。批量 IN 按参数上限分块并给出 SQL 上界公式，不无限 Preload。
- 精确 total 可显式 opt-in，但旧合同默认不变；未请求总数不能伪装为 0。沿用已稳定 keyset，排序加唯一 ID，不把所有分页推倒重写。
- 状态迁移显式 Updates/零值列选择、scope/state/version 条件、RowsAffected；0 行读回分类。禁止 Save 覆盖整行、read-check 后仅按 ID 无条件写。
- 一次业务事务向所有 repository 传同一 tx，不偷用 root DB/另开池；锁内不做 Provider、对象存储或慢网络。若 prepared runtime 要求真实 root-created transaction seal，最外层必须走 owner 的 sealed transaction helper，子 service/savepoint 继承同一 seal；“已是 gorm.Transaction”不代表受信任，不能为通过 guard 而降级 managed root 或手工复制 Settings。测试应到达真实末项 DML 后注错，不把 seal 提前拒绝的空回滚当作端到端原子性证据。
- CreateInBatches 按 bytes、参数上限、锁时长、WAL/RSS 确定，复用现有实现。PrepareStmt 仅有界实验：GORM/驱动双层 cache、SQL 形状数、IN 长度、代理模式与关闭结果。
- 不全局关闭默认事务或跳过正确性 hooks。普通业务保留 owner ORM；PG 专用 COPY/DDL/session 原语需要明确例外、参数绑定、固定/allowlist 标识符与隔离适配器。

## 预算与配额

- 热准入可用数据库内同步汇总，reserve/commit/release/未知结果/补差与差量记录、状态 CAS、必要账本/audit/outbox 同事务维护；Redis 不能成为余额真相。
- 先固定原策略有效期、period、currency、金额精度、enforcement、warning 和 late settlement 归属，不擅改成按月或按新键拆成多个共享 cap。
- 所有 writer（含 legacy、修复、period rollover、终态回调）及其实际 composition root 必须入清单。事务内重建 service/repository 也须保留可信显式依赖；新 reserve 没有 policy 不证明历史输入或 replay 也在受管域外。commit/release 只能一个合法终态；相同身份重放无重复 delta，不同结算身份冲突。
- 将某入口明确限制为 unbound legacy 来源时，创建、ID重放和直接 application/Composer 准入复用同一 repository 资格规则；拒绝其他policy/Attempt/price/spend绑定与已消费金额，不只核金额、币种和基础关联。重放比较完整来源身份，不改写历史行；合法hold状态和cap余量保持原合同。Provider零调用负例用本地fixture证明，预检不能冒充覆盖外部Submit全程的预算锁。
- 过期处理须与审批使用同一 parent→items 锁序；发现的ID/状态/revision仅为hint，锁内重新核scope、当前状态、cutoff及revision，再CAS并检查RowsAffected。分页发现有界不代表总量有界；原合同处理全部时须继续全部页，错误返回此前已完成计数，不把savepoint成功称最外层已提交。
- 多项审批/结算不能机械循环单项 writer：先核全量 Attempt/policy/head/reservation/price/enterprise 锁序与跨项累积，permit 的同 policy 重入不能当跨 policy 嵌套授权。数据库 guard 的拒绝只能证明 fail closed，不能冒充入口可用或全 writer 覆盖。
- 新旧协议混跑也要入锁图：新路径持 reservation 后等 price、旧路径持 price 后等 reservation，可形成独立于 enterprise 的环。若兼容期不能统一总序，可在显式新路径的首次反向行锁使用 NOWAIT 并整体回滚，保留旧默认；批量先锁固定去重集合、确认全部命中并持续持有，后续只重取同集合。排序不等于消环；NOWAIT 不保证表锁不等待，不能吞 55P03、改成业务成功或自动重试。同步 opposing-edge 探针与真实死锁、单笔与批量、前缀模拟与完整旧命令应分别报告。
- 保守 tenant 排他围栏只能串行化遵守同一围栏的路径，并非全图证明；Explain 等持 policy 锁的读取也须按该合同进场。提前取 tenant EX 后，还须核旧路径是否先持 parent/items 再请求 tenant SHARE，不能把原环换成新环。成功 savepoint 的锁会留到最外事务；内部返回不是外层提交，权限前 busy/重放阻塞和同租户串行化成本须明确披露。
- 写维护必须绑定真实当前 actor/session、独立审批、完整 snapshot CAS、一次消费与审计；自报 actor/approve 字符串不是授权。HTTP认证与执行捕获同一control owner，热请求只验证其实际pool/代次/fingerprint，不借新owner重建；凡完整fingerprint失效的服务，其cache key须用同边界失效，避免安全503无法经健康重组恢复。CLI只消费受认证API，不另建local写捷径；已提交domain-failure必须先投影安全receipt再失败退出，数据库/审计失败无receipt。字段白名单不足以防恶意远端将已知session/CSRF/reason反射进safe ID，所有renderer之前拒绝已知私密值；该检查不是任意未知秘密/编码变形防护。把已存在的 root 事务体拆成私有同 executor 原语后再接鉴权，不在外层 check 后另开 root 事务。某些校验以“提交 blocked 后返回 domain error”为原义，必须区分 committed-domain-failure 与数据库/审计失败，保留前者回执而让后者整体回滚。
- 维护锁序不能以未授权的非事务副作用为代价：将drain/advisory锁获取与setval等非事务marker推进拆开；前者可按既有顺序先取，后者须在当前身份、双方资格、审批状态与expiry通过且非receipt replay后才执行。拒绝事务回滚不会撤销sequence marker；用真实PG拒绝例验证marker前后不变，不只比较业务表。已授权晚失败仍可能保守推进，需明确披露。
- 独立审批的双方资料应在同一事务中一次有序捕获；先验证当前调用者，回执未命中才用已捕获事实作完整资格检查，避免先锁当前用户再补锁另一用户。尾部只复核捕获的有效期限，不在审计后重新查询。NOWAIT 可保守拒绝竞争但不证明全图无死锁；已提交回放仍认证当前调用者，不因另一方未来撤权再次执行业务。
- 完整行hash只能发现当前差异，不能证明policy/funding改后恢复的历史ABA。增强快照使用显式登记、单调永久counter及独立版本路径；共享funding用per-funding见证，不向全部policy扇出。合法source更新、删除重插、换ID应推进已登记counter并保留墓碑，true no-op fence不递增；旧pending证明不能当新版本资格，已提交结果仍遵守当前身份鉴权重放。首次登记与旧RR必须通过实际源行的早期写锁/MVCC fence串行化，不能把counter缺失当零或在hot path建schema。
- SQLite外层OR REPLACE会传播到触发器内部UPDATE：额外counter UNIQUE可能删除另一永久见证，额外source UNIQUE可能产生固定探针以外的victim。安装资格要核完整unique键集合、顺序、collation、partial/expression及未知counter trigger，而非只看某个正确索引存在。PG永久历史见证（包括复用的旧counter）须拒绝UNLOGGED、RLS、继承/partition、rewrite及外来trigger等未资格化结构；拒绝不等于修复，不改历史checksum，也不声称防御管理员安装后DDL。
- 回执的相同字段双写不等于完整性保护；将规范化结果摘要绑定既有不可变审计事件并在回放点读核对，明确点校验不是整链验证。若数据库时间戳进入摘要，入库前固定精度、编码时统一时区，不能在读回不一致后放宽摘要比较；历史默认认证时间仍必须是拒绝的哨兵。
- 不可变消费账本未必含未结算 hold；重建明确 canonical baseline、差量日志、来源唯一身份与核对规则，不能假称只 SUM spend 即可。
- 重建用一致快照 baseline + 同一快照 checkpoint + 可证明提交顺序的增量；时间戳/UUID/预分配全局 sequence 不等于提交水位。批次/时间有界、checkpoint CAS、幂等续跑。
- shadow → parity → 旧 writer 的 DB-level fence → 追赶 → 原子激活。只靠部署清单不足以保证旧 binary 不绕过；具体 guard 需 owner 设计与 PG 证明。
- 缺失/drift 不当 0；停止新准入同时允许已有工作受控收敛。回滚先 fence/drain/parity，不能只关开关部署不写汇总的旧实例。保留新增事实，不原地改账。

## 队列与租约

- claim 和 expired reclaim **都**有界：短事务选有限 IDs，带仍到期/state 谓词更新，不无界 UPDATE、不在一事务排空积压。
- GORM clause 优先表达 SKIP LOCKED；保留 CAS 与每次独立 fence。按 due time + 唯一 ID 排序，batch 不超实际执行槽位。
- 先画 callback/cancel/settle/claim 的锁图，再统一总序；不能为 SKIP LOCKED 先锁 Job 后锁 Attempt 反转已有顺序。真实多会话交错覆盖，不以单连接 SQLite 证明 PG。
- completion/renew/retry/release 均验证精确 claim token/generation、scope/state/expiry，worker_ref 不等于独占 fence。
- 提交后执行外部工作，按 at-least-once + sink 幂等设计；未知外部接单只 reconcile，不盲重投或宣称跨系统 exactly-once。
- SKIP LOCKED 不保证严格 FIFO：记录最老年龄、饥饿与 scope 进展，损坏头部隔离，不无界扫描跳过。

## Pool、schema 与迁移

- 先看现行合同是否由应用管理 pool；新增配置必须先有增量 spec，未设置保持旧行为，明确零值/负值/duration、owned/borrowed 生命周期和关闭者。
- 连接预算累加所有 API/worker/迁移/双槽实例，给管理、备份、故障恢复留量；看 DBStats WaitCount/WaitDuration 窗口增量、锁、I/O/WAL 与 p99，不是连接越多越快。
- 强一致预算、权限/撤权、幂等、结算与写后读固定主库；副本仅为显式允许延迟查询设计 lag/降级，不能隐形安装读写路由。
- schema 探测移到 prepared snapshot，绑定 DB identity/migration digest/runtime generation，迁移后刷新；required schema 缺失仍 fail closed，不能缓存动态权限/余额。
- concurrent index 不能塞事务 migration；新增执行模式需同固定物理 session 的单执行者保护、timeout/取消、持久化状态与恢复。事务代理不支持 session 语义时拒绝。
- 索引同名/IF NOT EXISTS 不证明有效，核对定义、predicate/columns、indisvalid/indisready；DDL 完成记录前崩溃可验证补记，invalid/异定义显式恢复，旧 checksum 不改。
- SQLite 的隐藏 rowid 也是唯一冲突身份；recursive_triggers=OFF 下 REPLACE 可能隐式删除另一业务键的行，不能只覆盖模型主键/幂等键。对来源与不可变日志分别验证 INSERT/UPDATE、受管 victim/写入者、负 rowid 和不受管兼容；修复用新增原子迁移，不改历史 checksum。
- 既有表预检不能只认列名与索引名：核类型、模型要求的 NULL/PK/CHECK、完整有效立即唯一索引与 schema 归属，缺陷直接拒绝而不让 AutoMigrate 重建现有表。比较固定 CHECK 形态时保留 token 种类和边界，带引号标识符不能冒充整段表达式或字符串字面量。保守形态检查不等于完整 SQL 解析或物理 schema 等价证明。

## 验证与停止条件

优先 owner 现有 runner/helper/evidence。矩阵至少覆盖页大小/历史长度/热点、worker 数、过期积压、崩溃重放、旧 writer/旧 fence、迁移中断与回退。记录 SQL/rows/bytes、p50/p95/p99、成功吞吐、错误/拒绝、锁、DBStats delta、CPU/RSS/I/O/WAL、恢复耗时。实验前冻结判据、相同负载、至少三个独立重复，不能以 CPU 100% 为目标。

长时实验冻结源码与实际 test/build 依赖闭包，前后 digest 与 tracked-state 变化使本轮证据失效，即使测试 exit0、数值看似改善也不得推广。其他任务或自动诊断可能修改当前 checkout；必要时使用保留 dirty 来源的独立副本、原 replacement 相对路径、只读进程视图及独立缓存/evidence。不得通过恢复文件、缩小摘要范围或删校验制造相等；副本不是独立提交 revision，same-UID 摘要/只读挂载不是 attestation。完整性、局部非退化与生产容量三者分开，饱和拒绝要完整保留。

PG 专属行为用 opt-in disposable PG 普通多会话测试；没有环境则 pending，不能以 SQLite/全 skip/零匹配 `go test -run` 当通过。适配器明确 PG-only 时验证 SQLite fail-closed，不用方言名称/事务ID替身伪造真实 Flush/锁语义。默认不运行 race；当前人类明确强烈要求时才在指定范围运行一次，失败不自动重试。

Flush 末尾证明须区分观察点：最后 SQL 之前可在同一真实 executor 回读完整事实，最后 SQL 成功后只保留内存观察与 CPU tail；callback 注错不是 COMMIT 拒绝，GORM 回调无 SQL也不是底层驱动无 SQL的全面证明。上游 tracing 可能派生 context，验证父标记继承和 writer/tx 的同一派生 context，不错误要求入口指针恒等。对已冻结的 source capture，业务幂等不自动等于所有 housekeeping 表零写；若既有合同每次重放新增 sealed transaction，逐次按真实 xid 验证恰一新行、旧行不变及其余完整快照不变，不忽略该表或为了造绿删除行。测试 helper 不得用 Background 覆盖调用方的 setup deadline。

正确性、scope、幂等、账本或恢复不变量失败立即停止推广；性能退化回到可验证旧路径并保留证据，不能通过删除事实、放宽 SLO 或引入更多系统掩盖问题。
