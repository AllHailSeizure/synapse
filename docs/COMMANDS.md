# Synapse capture skills

This index lives in `docs/` rather than `commands/` because Cursor publishes
slash items from skills, not from leftover command markdown.

`/bug` and `/patch` are skills with `disable-model-invocation: true`, so they
only run when the user types them. Cursor already ships `/debug`. Codex
invokes the same skills as `$bug`, `$patch`, and `$debug`. The capture
scripts stay in `commands/*.mjs`.

| Slash | Purpose |
| --- | --- |
| [`/bug`](../skills/bug/SKILL.md) | Run `commands/bug.mjs` with the user's arguments. Creates a GitHub issue and comments `@bug-bandaid` unless they opted out. |
| [`/patch`](../skills/patch/SKILL.md) | Same capture as `/bug`, but comments `@fastpatch`. |

`/weedeat` moved to its own plugin: [`weedeat`](https://github.com/AllHailSeizure/weedeat).
