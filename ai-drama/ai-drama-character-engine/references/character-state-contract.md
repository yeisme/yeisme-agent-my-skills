# Character State Contract

最小状态包括：`desire`、`fear`、`secret`、`value`、`boundary`、`knowledge`、`resource`、`relationship_refs`、`voice_notes`、`current_emotion` 和 `revision`。

任何状态变化必须关联 event/beat ref。缺少事实来源时输出 `unknown`，不能猜测后写入 canonical state。
