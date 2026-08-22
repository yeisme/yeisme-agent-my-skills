# Commands

Build packages from an eligible frozen revision. Do not overwrite a visible package on partial failure.

```
anatomia revision package prepare revision:demo --json
anatomia package show package:demo --json
anatomia package handoff prepare package:demo --target scaena --json
anatomia handoff show handoff:demo --json
```

Allowed `--target` values are `scaena`, `eikona`, `sonora`, and `mediahub` (legacy alias for the neutral media-package export; the mediahub product was retired 2026-08-22). Anatomia returns provider-neutral refs and receipts; it does not write the target owner's private state.
