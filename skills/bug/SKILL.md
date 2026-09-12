---
name: bug
description: >-
  Capture a bug report without diagnosing or fixing it. Use only when the
  user invokes /bug or $bug. Do not file a sticky-note issue unprompted.
disable-model-invocation: true
---

# /bug

Do not diagnose, investigate, plan, or fix. Run the capture script with the
user's arguments unchanged:

```
node "${CURSOR_PLUGIN_ROOT}/commands/bug.mjs" <arguments>
```

If `CURSOR_PLUGIN_ROOT` is unset, run `commands/bug.mjs` relative to this
Synapse checkout.

Reply with the script's stdout (the issue URL) in one short line. If the script
fails, report its stderr. Stop. Do not create the issue or comment
`@bug-bandaid` yourself — the script does that unless the user opted out
(`--no-kick`, "capture only", "no bandaid", or equivalent).
