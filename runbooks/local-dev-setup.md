# Local Development Setup

This runbook covers setting up a local development environment for
`molecule-workflow-retro`.

---

## Prerequisites

- Python 3.11+
- `gh` CLI authenticated
- Write access to `Molecule-AI/molecule-ai-plugin-molecule-workflow-retro`

---

## Clone & Bootstrap

```bash
git clone https://github.com/Molecule-AI/molecule-ai-plugin-molecule-workflow-retro.git
cd molecule-ai-plugin-molecule-workflow-retro
```

---

## Validating Plugin Structure

```bash
python3 -c "import yaml; yaml.safe_load(open('plugin.yaml'))"
echo "plugin.yaml OK"
```

---

## Testing the Retro Skill

The harness wrapper is provided by the Molecule AI platform at runtime.
To test:

1. Install `molecule-cron-learnings` first (prerequisite)
2. Install `molecule-workflow-retro` in a test workspace
3. Add mock learnings to `~/.claude/projects/<project>/cron-learnings.jsonl`:
   ```jsonl
   {"tick": "2026-04-21T00:00Z", "role": "sdk-lead", "learnings": ["CI timeout was 2min — too short for integration tests"]}
   {"tick": "2026-04-21T01:00Z", "role": "sdk-lead", "learnings": ["PR template now has Testing section"]}
   ```
4. Run `/retro` and verify output has three sections (went well, didn't, actions)

---

## Troubleshooting

### Retro has no learnings to synthesise

- Verify `molecule-cron-learnings` is installed and writing to the JSONL file
- Check the path `~/.claude/projects/<project>/cron-learnings.jsonl` exists
- If the project directory is wrong, check the workspace config

### Empty action items

- The retro needs at least one "what didn't" learning to generate action items
- Add more learnings or check the learnings parser

---

## Related

- `molecule-cron-learnings` — prerequisite; writes learnings each tick
- `skills/cron-retro/SKILL.md` — retro synthesis skill
- `commands/retro.md` — /retro slash command
