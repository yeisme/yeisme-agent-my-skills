# 发布前检查

检查英文正文和中文译文的占位符集合一致，contract 只声明实际占位符。example 使用公开、虚构、非敏感内容；敏感字段不声明 default、example 或 enum。

执行：

```bash
template-registry contract validate --repository . --package <package> --id <solution> --role <role> --locale en --json
template-registry catalog build --repository . --json
template-registry catalog validate --repository . --json
```

随后使用目标消费者的真实命令验证 exact `locale=en` 引用。验证只证明合同和集成可用；没有真实模型或生产 evidence 时，maturity 不能提升为 `mature`。

已发布版本发生正文、contract、rights、locale 或 digest 变化时创建新版本。旧 exact ref 保留，迁移说明必须给出替代 ref 和回滚路径。
