# Test Coverage Rationale — molecule-workflow-retro

## Why This Plugin Has Limited Unit-Test Coverage

`molecule-workflow-retro` is a **command/skill-only plugin**. Its "logic" is prose
documentation in `commands/retro.md` and `skills/cron-retro/SKILL.md` — a structured
weekly-retrospective template, not executable Python code.

There are no hooks, no Python functions, and no adapters with testable business logic.
The adapter (`adapters/claude_code.py`) is a one-line import of AgentskillsAdaptor.

## What We Test (and Why)

| What | Why |
|------|-----|
| `plugin.yaml` schema | Verifies manifest, command (`retro`), skill (`cron-retro`), runtimes |
| `commands/retro.md` frontmatter + sections | Ensures /retro command is registered and documented |
| `skills/cron-retro/SKILL.md` frontmatter + metrics | Ensures cron-retro skill is registered with computation items |
| `adapters/claude_code.py` import | Verifies Claude Code adapter is wired |
| `known-issues.md` structure | P0-P3 severity definitions for retro-specific failure modes |
| `validate-plugin.py` exit 0 | Smoke test — shared CI validator passes |

## What We Cannot Unit-Test (and What Would Help)

- **Metrics computation** — requires GitHub API access, gh CLI, and local cron-learnings.jsonl.
  Write integration tests in `workspace-template/` that mock gh responses.

- **Issue posting** — requires GitHub credentials. Mock in integration tests.

- **Trend detection** — the retro computes "trend vs prior week" by comparing two datasets.
  If you add Python logic for this, add unit tests.

## If You Add Business Logic

If you add Python hooks or data-processing functions to this plugin, add:
1. Unit tests for the new functions
2. Mock tests for GH API / gh CLI calls
3. Integration tests in `workspace-template/`

See `molecule-freeze-scope` or `molecule-careful-bash` for examples of
full test suites in plugin repos.
