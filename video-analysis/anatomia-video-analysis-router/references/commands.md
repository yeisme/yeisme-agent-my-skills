# Commands

Released CLI only. Ordinary users hold a service endpoint and a key file; they do not configure provider credentials.

```
anatomia login --endpoint https://anatomia.example.com --key-file /absolute/private/anatomia-access.key
anatomia doctor --json
anatomia analyze file --file /absolute/path/demo.mp4 --to ./anatomia-output/demo --json
```

Detached automation:

```
anatomia source upload --file /absolute/path/demo.mp4 --json
anatomia analysis start --source source:demo --json
anatomia analysis status analysis:demo --json
anatomia analysis watch analysis:demo --events
anatomia analysis cancel analysis:demo --expected-version 3 --json
anatomia analysis result analysis:demo --to ./anatomia-output/demo --json
```

`analyze file` owns upload, start, wait, and download. A running or HTTP 202 analysis means wait or resume; do not start a duplicate job with the same source.
