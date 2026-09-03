# Eikona Image Skills

Eikona 图片生成与视觉资产工作流，覆盖视觉路由、主体/产品资产、文件提示词、资产生命周期、Gateway 和社媒视觉导演。

选模型先跑 `eikona models list --source adapted --all`；本机默认看 `eikona auth list` 与 `eikona models default show`。空 `models.lock` 不是未适配。

建议下一阶段与 `yeisme-eikona-cli-runtime` 一起拆成 `eikona-skills` 独立仓库。
