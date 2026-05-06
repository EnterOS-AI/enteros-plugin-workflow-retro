# molecule-workflow-retro — Weekly Retrospective Generator

`molecule-workflow-retro` provides the `/retro` slash command — a weekly
retrospective generator. It reads from `molecule-cron-learnings` JSONL files
and synthesises a structured retro: what went well, what didn't, and action items.

**Version:** 1.0.0
**Runtime:** `claude_code`

---

## Repository Layout

```
molecule-workflow-retro/
├── plugin.yaml              — Plugin manifest
├── skills/
│   └── cron-retro/
│       └── SKILL.md         — Retro synthesis skill
└── commands/
    └── retro.md            — /retro slash command
```

---

## What It Does

### The /retro Command

Run `/retro` in any Claude Code session to generate a weekly retrospective.
It reads learnings from `~/.claude/projects/<project>/cron-learnings.jsonl`
and produces:

- **What went well**: Patterns across positive learnings
- **What didn't**: Patterns across negative learnings
- **Action items**: Concrete next steps for the next week

### Prerequisites

Install `molecule-cron-learnings` first — the retro reads learnings that must
be written by the cron-learnings plugin each tick.

---

## Development

### Prerequisites

- Python 3.11+
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-molecule-workflow-retro`

### Setup

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-molecule-workflow-retro.git
cd molecule-ai-plugin-molecule-workflow-retro

python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
```

### Pre-Commit Checklist

```bash
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"

python3 -c "
import re, sys
with open('plugin.yaml') as f:
    content = f.read()
patterns = [r'sk.ant', r'ghp.', r'AKIA[A-Z0-9]']
if any(re.search(p, content) for p in patterns):
    print('FAIL: possible credentials found')
    sys.exit(1)
print('No credentials: OK')
"
```

---

## Release Process

1. Review changes: `git log origin/main..HEAD --oneline`
2. Bump `version` in `plugin.yaml` (semver)
3. Commit: `chore: bump version to X.Y.Z`
4. Tag and push: `git tag vX.Y.Z && git push origin main --tags`
5. Create GitHub Release with changelog

---

## Known Issues

See `known-issues.md` at the repo root.
