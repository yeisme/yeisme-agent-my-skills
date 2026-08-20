# Commands

Review immutable revisions. Do not modify prior revisions or exported manifests by hand.

```
anatomia analysis delivery show analysis:demo --json
anatomia revision validate revision:demo --json
anatomia revision review create revision:demo --json
anatomia revision review export review:demo --json
anatomia revision review verify review:demo --input ./review-verification.json --json
anatomia revision freeze revision:demo --expected-version 3 --reviewer reviewer:owner --evidence review-receipt:demo --json
anatomia revision fork revision:demo --json
```

Unavailable, partial, or blocked means show the blocker; do not freeze around it. Identity and rights claims stay reviewable until an authorized actor confirms them.
