# Commands

Released CLI only. Every leaf supports `--json`, `--agent`, `--events`, and `--explain`; pick exactly one. All paths are local; no provider or credential is involved.

Grayscale numeric derivation and human-viewable preview (single-shot window 3-10 seconds, source <=30fps, output long edge <=1280):

```
anatomia video grayscale derive --source /absolute/path/shot.mp4 --start 500000 --end 4500000 --to ./gray-out --json
anatomia video grayscale derive --source /absolute/path/shot.mp4 --start 500000 --end 4500000 --to ./gray-out --chunk-frames 64 --preview-to ./preview.mp4 --agent
anatomia video grayscale preview --source /absolute/path/shot.mp4 --start 500000 --end 4500000 --to ./preview.mp4 --json
```

Shot segmentation evidence, listing, and per-shot materialization:

```
anatomia video shots detect --source /absolute/path/ep1.mp4 --source-ref source:ep1 --to ./shot-list.json --agent
anatomia video shots detect --source /absolute/path/ep1.mp4 --source-ref source:ep1 --threshold 0.4 --min-shot 500000 --json
anatomia video shots list --from ./shot-list.json --agent
anatomia video shots extract --source /absolute/path/ep1.mp4 --from ./shot-list.json --to ./shots-out --json
```

Per-purpose placeholder keyframes (`thumbnail,character,composition,action,text,scene,style`):

```
anatomia video placeholders extract --source /absolute/path/ep1.mp4 --source-ref source:ep1 --shot-ref source:ep1:shot:0 --start 500000 --end 1500000 --purpose thumbnail,character --agent
anatomia video placeholders extract --source /absolute/path/ep1.mp4 --source-ref source:ep1 --shot-ref source:ep1:shot:0 --start 500000 --end 1500000 --purpose text --stride 400000 --to ./selection.json --json
```

Start/end and stride are microseconds. `--source-ref` and `--shot-ref` are stable identity refs you choose once and reuse, not file paths.
