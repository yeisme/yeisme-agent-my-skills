# Commands

Read a registered ref, then ask one bounded question. These paths require a composed canonical runtime; typed unavailable is a truthful result, not a cue to invent MCP or start a new analysis.

```
anatomia source show source:demo --json
anatomia analysis status analysis:demo --json
anatomia video probe --source source:demo --json
anatomia video understand --source source:demo --question "What changes in this shot?" --json
anatomia video inspect --source source:demo --start 0 --end 1500000 --json
anatomia video compare --base-source source:demo --head-source source:other --json
```

HTTP 202 means read the same operation; do not resubmit the question. Do not pass a local filesystem path to these commands.
