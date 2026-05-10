# molecule-workflow-retro

Provides the `/retro` slash command — a weekly retrospective generator that synthesises learnings from `molecule-skill-cron-learnings` into an actionable report.

## How it works

`/retro` reads all entries from `~/.molecule/cron-learnings.jsonl`, groups them by week, and produces:

- **What went well** — recurring patterns in positive learnings
- **What to improve** — recurring warnings or mistakes
- **Action items** — concrete next steps with owners

Designed to be run at end-of-week or end-of-sprint.

## Install

### In org template (org.yaml)

```yaml
plugins:
  - molecule-workflow-retro
```

**Recommended:** Install `molecule-skill-cron-learnings` first so there is data to retrospective.

### From URL (community install)

```
github://Molecule-AI/molecule-ai-plugin-molecule-workflow-retro
```

## Usage

```
/retro
```

Produces a retrospective in the current conversation.

## Commands

- `/retro` — generate weekly retrospective from learnings

## Architecture

```
skills/
  cron-retro/         # Skill definition (SKILL.md + scripts/)
adapters/
  claude_code.py      # Registers /retro command
```

## Runtime

- `claude_code` — primary

## Known issues

See [known-issues.md](known-issues.md).

## License

Business Source License 1.1 — © Molecule AI.
