---
name: api-contract-parallel-workflow
description: Use when a feature needs frontend/backend parallel development, OpenAPI or other API contracts, typed clients, mocks, fixtures, error-state coverage, or compatibility checks between an interface and its implementation.
---

# API 契约并行开发工作流

把 API contract 当作前后端共享边界。先冻结可验证的请求、响应、错误、权限和状态，再让前端使用 mock/service layer、后端实现真实服务；禁止两边各自维护一套字段解释。

## 规范源层级

按以下优先级选择唯一规范源：

1. 项目已批准的 OpenAPI、IDL、schema 或协议文件。
2. 通过 schema 生成的 typed client、类型、mock、fixture 和文档。
3. 具体后端实现、前端类型或测试 fixture 只能作为验证对象，不能反向成为未审查的第二份规范。

若项目使用代码优先，要求从代码生成 OpenAPI 或等价 contract，并把生成命令和兼容检查写入任务；不要手工维护一份会过期的 `API_SPEC.md`。

## 工作流

### 1. 盘点现有合同

读取最近的 `AGENTS.md`、API 文件、路由/controller、DTO/schema、client、mock、fixture、迁移和测试。确认 contract owner、生成工具、版本策略、认证方式和本地启动命令。

### 2. 从 UI 状态倒推接口覆盖

对每个用户行为列出：

| UI 或客户端状态 | 接口需要表达的内容 |
| --- | --- |
| loading | 请求边界、超时和取消行为 |
| empty | 空结果的合法 response，不把空和错误混淆 |
| success | 字段、排序、筛选、分页和缓存语义 |
| error | 稳定 error code、message、retryable 和 details |
| permission denied | 状态码、脱敏和下一步动作 |
| conflict / duplicate | 幂等键、版本冲突或业务冲突语义 |

### 3. 冻结 contract

至少定义：

- method、path、path/query/header/body 参数和必填性；
- response schema、nullable、枚举、分页、排序和时间/金额格式；
- error code、HTTP status、retryable、trace/request id 和脱敏边界；
- 认证、角色、workspace/project/run scope 和资源权限；
- 幂等、并发、重复请求、超时重试和版本兼容策略；
- 示例 payload、fixture、边界值和失败样例。

稳定字段、命令、RPC/API 方法或事件发生生成性变更时，先遵守 `yeisme-evolutionary-change-policy`，补齐弃用、迁移和回滚路径。

### 4. 生成并行材料

使用项目已有的生成器生成 typed client、frontend types、mock server、fixture 和文档。生成文件不手工改；若生成器不存在，先记录最小可行替代方案和后续补齐任务。

前端 lane 必须：

- 所有请求通过 service/client 层；
- 使用 contract 类型和 mock，不直接在组件里散落 `fetch` 或字段转换；
- 覆盖 loading、empty、error、permission 和 success；
- 以真实 response shape 编写交互和测试。

后端 lane 必须：

- 从 contract 实现 handler/controller、校验、service、repository 和迁移；
- 不为“方便前端”悄悄改变字段、状态码或错误结构；
- 对重复请求、并发、权限、审计和失败重试添加测试；
- 使用项目规定的 ORM/数据库访问边界。

### 5. 在集成前做兼容检查

先运行 contract lint、生成器、schema diff 或项目等价命令，再分别运行前后端 focused tests。集成时使用真实 API 验证状态码、response schema、认证、权限、空态、错误和重试；不要只验证 200 成功路径。

### 6. 工作区与阶段性提交

前后端 lane 的默认工作区按运行时风险分配，而不是按目录机械拆分：

| lane | 默认工作区 | 隔离要求 |
| --- | --- | --- |
| frontend/client preview | 当前 checkout/current branch | 保持 dev server、浏览器预览和未提交视觉迭代可见；所有请求先经过 service/mock layer |
| backend service/worker/daemon | `feature/<topic>` 独立 branch/worktree | 独立端口、数据库/缓存、运行目录、日志和进程组；热加载不得重启或覆盖前端服务 |
| contract/generator | contract owner 选择的单一 workspace | 只允许一个规范写入者；typed client、mock、fixture 和文档从规范生成 |

开始并行前，记录 `workspace_mode`、`owned_paths`、`shared_read_paths`、`forbidden_paths`、端口、数据目录、启动命令和验证命令。若后端必须依赖当前工作区的未提交客户端或共享生成物，先建立 contract checkpoint，或明确记录当前工作区单 writer 例外；不要让两个 worktree 同时写同一生成文件。

阶段性 checkpoint 默认按以下顺序形成：

1. contract/schema ready；
2. client previewable with mock；
3. backend behavior plus focused tests；
4. real integration and error-state/visual verification。

每个 checkpoint 只提交所属路径和一个意图；子 agent 只返回 checkpoint manifest，由 root 按仓库授权执行实际提交。推送、PR、合并和删除 worktree 不属于并行 lane 的默认动作。

## Handoff 格式

把交接写成短表，而不是长篇口头说明：

| lane | 输入 | owned paths | 输出 | 阻塞条件 |
| --- | --- | --- | --- | --- |
| contract | PRD、UI Spec、现有 schema | contract/生成配置 | 冻结的 schema、版本和生成命令 | 未决业务或权限规则 |
| frontend | contract、mock、UI Spec | client、hooks、pages、components | 页面与状态测试 | contract 未冻结 |
| backend | contract、data spec | handler/service/repository/migrations | API、业务测试、迁移 | 数据或权限规则未定 |
| integration | 前后端结果 | 测试与证据目录 | 真实联调证据和差异列表 | 任一 lane 未完成 |

## 反漂移规则

- 不重复定义 `user_name` 与 `username` 这类同义字段；统一命名并记录迁移。
- 不把 mock 的宽松字段当成真实 API 行为；mock 必须来自 contract。
- 不用前端自定义的 `user_id`、workspace、role 或权限结果替代服务端身份判断。
- 不把“后端已完成”当作前端可用；生成材料、fixture 和 focused tests 必须成功。
- 不将未批准的破坏性字段删除或重命名混入普通实现。
- 不让后端 hot reload、数据库迁移、缓存、端口或日志污染仍在预览的客户端工作区。
- 不把两个 lane 的并行写入误认为“隔离”；共享 contract、生成物和测试入口仍必须有明确 owner。

## 验证

先使用 owner 声明的真实命令。通用的最小检查是：

```bash
git diff --check
```

然后运行项目的 contract lint/generate、前端类型检查、后端 focused tests 和集成测试。集成及更高层测试按 `project-integration-test-evidence` 写入 owner 的 `temp/integration-test-runs/<run-id>/`，并脱敏环境变量、token、Authorization、原始 provider payload 和私有提示词。
