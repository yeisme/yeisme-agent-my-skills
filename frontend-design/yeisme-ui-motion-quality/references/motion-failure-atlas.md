# Motion Failure Atlas

| 症状 | 常见原因 | 首选修复 | 证据 |
| --- | --- | --- | --- |
| 点击后没有即时反馈 | 先等待请求或入场动画 | 立即提交本地 pending/pressed 状态，业务结果仍以后端为准 | interaction test |
| 打开像“飞入” | 位移过大或使用 bounce | 收敛到 4–8px、opacity、ease-out | fixed screenshot |
| 关闭后焦点丢失 | unmount 早于 focus return | 让 primitive 管理关闭和焦点回收 | keyboard test |
| 快速切换显示旧内容 | 目标、请求或动画没有隔离 | 以最新 target/revision 收敛，旧响应不可覆盖 | rapid-toggle test |
| 表格筛选跳动 | 直接修改布局高度或手写 timeout | 使用连续布局方案，保留 row key 和稳定列宽 | desktop/mobile screenshot |
| 页面滚动被带走 | overlay 没有滚动锁或出口动画改变高度 | 使用 Sheet/Dialog primitive 和 bounded transform | browser interaction |
| reduced-motion 仍有位移 | 只为正常路径写动画 | 增加 `prefers-reduced-motion` 分支并关闭非必要运动 | reduced-motion test |
| 动画看起来像假的成功 | success 动画早于服务端 receipt | 只在 authoritative success projection 后播放状态动画 | API + browser evidence |
| 动画偶发卡顿 | 大量重渲染、布局读写、SVG 直接变换 | 使用性能规则、包装 SVG、减少 transient state 订阅 | profiler/console evidence |
| 每个元素同时动 | 没有 staging hierarchy | 只保留一个主运动；必要 stagger 控制在短、少量、可跳过 | screenshot review |
