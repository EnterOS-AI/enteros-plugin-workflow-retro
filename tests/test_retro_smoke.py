#!/usr/bin/env python3
"""
Smoke tests for molecule-workflow-retro.

Rationale for limited test coverage: This is a command/skill-only plugin with no
executable hooks or business logic. The "logic" is prose documentation in
commands/retro.md and skills/cron-retro/SKILL.md. See tests/README.md for
full rationale.

Run: python tests/test_retro_smoke.py
"""
import os
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts'))


class TestPluginManifest(unittest.TestCase):
    """Verify plugin.yaml is well-formed."""

    @classmethod
    def setUpClass(cls):
        import yaml
        manifest_path = os.path.join(REPO_ROOT, 'plugin.yaml')
        with open(manifest_path) as f:
            cls.manifest = yaml.safe_load(f)

    def test_plugin_yaml_loads(self):
        self.assertIsInstance(self.manifest, dict)

    def test_name(self):
        self.assertEqual(self.manifest['name'], 'molecule-workflow-retro')

    def test_version_semver(self):
        v = self.manifest['version']
        self.assertRegex(v, r'^\d+\.\d+\.\d+$')

    def test_description_present(self):
        self.assertGreater(len(self.manifest.get('description', '')), 20)

    def test_runtime_claude_code(self):
        self.assertIn('claude_code', self.manifest.get('runtimes', []))

    def test_command_declared(self):
        self.assertIn('retro', self.manifest.get('commands', []))

    def test_skill_declared(self):
        self.assertIn('cron-retro', self.manifest.get('skills', []))

    def test_tags(self):
        tags = self.manifest.get('tags', [])
        self.assertIn('molecule', tags)


class TestRetroCommand(unittest.TestCase):
    """Verify /retro command file exists and documents required sections."""

    CMD_PATH = os.path.join(REPO_ROOT, 'commands', 'retro.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.CMD_PATH))

    def test_has_frontmatter(self):
        import yaml
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertTrue(content.startswith('---'))
        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)
        _, frontmatter, _ = parts
        data = yaml.safe_load(frontmatter)
        self.assertIsInstance(data, dict)

    def test_frontmatter_name(self):
        import yaml
        with open(self.CMD_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertEqual(data['name'], 'retro')

    def test_body_has_steps(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        # Should document the 5 main steps
        self.assertIn('Compute', content)
        self.assertIn('Format', content)
        self.assertIn('Post as a new GitHub issue', content)

    def test_standing_rules_present(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        self.assertIn('Standing rules', content)

    def test_github_issue_title_format(self):
        with open(self.CMD_PATH) as f:
            content = f.read()
        # Retro posts as a GitHub issue with a specific format
        self.assertIn('Cron retro:', content)
        self.assertIn('labels', content.lower())


class TestCronRetroSkill(unittest.TestCase):
    """Verify cron-retro skill exists and is well-formed."""

    SKILL_PATH = os.path.join(REPO_ROOT, 'skills', 'cron-retro', 'SKILL.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.SKILL_PATH))

    def test_has_frontmatter(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        self.assertEqual(len(parts), 3)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertIsInstance(data, dict)

    def test_frontmatter_name(self):
        import yaml
        with open(self.SKILL_PATH) as f:
            content = f.read()
        parts = content.split('---', 2)
        _, frontmatter, body = parts
        data = yaml.safe_load(frontmatter)
        self.assertEqual(data['name'], 'cron-retro')

    def test_body_has_computation_items(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        # Should document what metrics to compute
        self.assertIn('Time-to-merge', content)
        self.assertIn('Code-review findings', content)

    def test_body_has_format_section(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        self.assertIn('Format', content)

    def test_body_has_cron_expression(self):
        with open(self.SKILL_PATH) as f:
            content = f.read()
        # Weekly Sunday cron
        self.assertIn('23:00', content)
        self.assertIn('cron', content)


class TestAdapter(unittest.TestCase):
    """Verify Claude Code adapter exists."""

    ADAPTER_PATH = os.path.join(REPO_ROOT, 'adapters', 'claude_code.py')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.ADAPTER_PATH))

    def test_imports_agentskills_adaptor(self):
        with open(self.ADAPTER_PATH) as f:
            content = f.read()
        self.assertIn('AgentskillsAdaptor', content)


class TestKnownIssues(unittest.TestCase):
    """Verify known-issues.md structure."""

    KI_PATH = os.path.join(REPO_ROOT, 'known-issues.md')

    def test_file_exists(self):
        self.assertTrue(os.path.isfile(self.KI_PATH))

    def test_has_active_issues_section(self):
        with open(self.KI_PATH) as f:
            self.assertIn('Active Issues', f.read())

    def test_has_severity_definitions(self):
        with open(self.KI_PATH) as f:
            content = f.read()
        self.assertIn('Severity Definitions', content)
        self.assertIn('P0', content)
        self.assertIn('P1', content)


class TestValidatePlugin(unittest.TestCase):
    """Smoke-test validate-plugin.py."""

    def test_exits_zero(self):
        import subprocess
        result = subprocess.run(
            [sys.executable, os.path.join(REPO_ROOT, '.molecule-ci', 'scripts', 'validate-plugin.py')],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        self.assertEqual(result.returncode, 0, f"stdout: {result.stdout}\nstderr: {result.stderr}")
        self.assertIn('molecule-workflow-retro', result.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
