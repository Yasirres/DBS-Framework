"""Behavioral tests for local tooling; no model or network calls."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from scaffold_skill import scaffold
from validate_skill import frontmatter, validate


class ToolTests(unittest.TestCase):
    def setUp(self):
        # Restricted Windows tokens can lose access to tempfile's private ACL.
        # An explicit workspace fixture root inherits that workspace's permissions.
        fixture_root = os.environ.get('DBS_TEST_DIR')
        if fixture_root:
            parent = Path(fixture_root).resolve()
            parent.mkdir(parents=True, exist_ok=True)
            self.base = parent / ('dbs-test-' + uuid.uuid4().hex)
            self.base.mkdir()
            def cleanup():
                if self.base.is_symlink() or self.base.resolve().parent != parent:
                    raise RuntimeError('test cleanup must stay in its fixture root')
                shutil.rmtree(self.base)
            self.addCleanup(cleanup)
        else:
            self.temp = tempfile.TemporaryDirectory()
            self.addCleanup(self.temp.cleanup)
            self.base = Path(self.temp.name)

    def minimal(self):
        root = self.base / 'sample'
        root.mkdir()
        (root / 'SKILL.md').write_text('---\nname: sample\ndescription: "Summarize supplied text when requested."\n---\n# Sample\n', encoding='utf-8')
        return root

    def test_repository_valid(self):
        self.assertEqual(validate(ROOT, repository=True), ([], []))

    def test_repository_rejects_each_missing_file(self):
        # Independent inventory: this must catch omissions from REQUIRED itself.
        expected = '''SKILL.md README.md CONTRIBUTING.md LICENSE .gitignore
ATTRIBUTION.md CHANGELOG.md .github/workflows/ci.yml
docs/VALIDATION.md tests/test_tools.py
references/dbs-principles.md references/testing-guide.md
references/platforms/claude.md references/platforms/chatgpt.md references/platforms/codex.md
scripts/validate_skill.py scripts/scaffold_skill.py
templates/generic-skill-template.md templates/claude-skill-template.md
templates/chatgpt-skill-template.md templates/codex-skill-template.md'''.split()
        root = self.base / 'repository'
        for relative in expected:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        self.assertEqual(validate(root, repository=True), ([], []))
        for relative in expected:
            with self.subTest(missing=relative):
                target = root / relative
                original = target.read_bytes()
                target.unlink()
                try:
                    errors, _ = validate(root, repository=True)
                    message = ('missing exact-case SKILL.md file' if relative == 'SKILL.md'
                               else f'missing required file: {relative}')
                    self.assertIn(message, errors)
                finally:
                    target.write_bytes(original)

    def test_standalone_skill_does_not_require_repository_files(self):
        root = self.minimal()
        self.assertEqual(validate(root), ([], []))
        self.assertTrue(validate(root, repository=True)[0])

    def test_all_platforms_are_self_contained_drafts(self):
        for platform in ('generic', 'claude', 'chatgpt', 'codex'):
            with self.subTest(platform=platform):
                dest = scaffold(f'sample-{platform}', self.base, platform, 'Summarize supplied input when requested.')
                errors, warnings = validate(dest, allow_draft=True)
                self.assertEqual(errors, [])
                self.assertTrue(warnings)
                self.assertTrue(validate(dest)[0])

    def test_existing_destination_unchanged(self):
        dest = scaffold('sample', self.base, 'generic', 'Create summaries.')
        original = (dest / 'SKILL.md').read_bytes()
        with self.assertRaises(FileExistsError):
            scaffold('sample', self.base, 'generic', 'Changed description.')
        self.assertEqual(original, (dest / 'SKILL.md').read_bytes())

    def test_invalid_names_cannot_escape(self):
        for name in ('../escape', '/absolute', 'C:\\escape', 'bad_name', 'Bad', '', 'con', 'a' * 65):
            with self.subTest(name=name), self.assertRaises(ValueError):
                scaffold(name, self.base, 'generic', 'Valid description.')
        self.assertEqual(list(self.base.iterdir()), [])

    def test_description_round_trip(self):
        description = 'لخّص النص "عند الطلب": Unicode and \\ paths.'
        dest = scaffold('sample', self.base, 'generic', description)
        self.assertEqual(frontmatter((dest / 'SKILL.md').read_text(encoding='utf-8'))['description'], description)

    def test_bad_descriptions_rejected_before_writes(self):
        for value in ('', ' ', 'line\nbreak', '<tag>', 'x' * 1025):
            with self.subTest(value=value[:20]), self.assertRaises(ValueError):
                scaffold('sample', self.base, 'generic', value)
        self.assertEqual(list(self.base.iterdir()), [])

    def test_missing_entrypoint(self):
        self.assertTrue(validate(self.base)[0])

    def test_frontmatter_errors(self):
        for text in ('# no header', '---\nname: sample',
                     '---\nname: sample\nname: duplicate\ndescription: hi\n---',
                     '---\nname: sample\ndescription: >\n  multiline\n---',
                     '---\nname: sample\ndescription: "unterminated\n---'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                frontmatter(text)

    def test_description_limit_and_angle_brackets(self):
        root = self.minimal()
        for value in ('x' * 1025, '<tag>'):
            (root / 'SKILL.md').write_text('---\nname: sample\ndescription: ' + json.dumps(value) + '\n---\n# Sample\n', encoding='utf-8')
            self.assertTrue(validate(root)[0])

    def test_link_resolution_and_escape(self):
        root = self.minimal()
        guide = root / 'guide.md'
        for link in ('missing.md', '../outside.md', '%2e%2e/outside.md'):
            guide.write_text(f'[reference]({link})\n', encoding='utf-8')
            self.assertTrue(validate(root)[0])
        guide.write_text('[core](SKILL.md)\n[web](https://example.com)\n[section](#title)\n', encoding='utf-8')
        self.assertEqual(validate(root)[0], [])

    def test_case_mismatch(self):
        root = self.minimal()
        (root / 'guide.md').write_text('[core](skill.md)\n', encoding='utf-8')
        self.assertTrue(validate(root)[0])

    def test_example_links_in_code_are_not_followed(self):
        root = self.minimal()
        (root / 'guide.md').write_text('Example: `[label](missing.md)`\n```md\n[label](missing.md)\n```\n', encoding='utf-8')
        self.assertEqual(validate(root)[0], [])

    def test_bad_python_is_not_executed(self):
        root = self.minimal()
        (root / 'broken.py').write_text('def broken(:\n', encoding='utf-8')
        self.assertTrue(validate(root)[0])

    def test_symlink_rejected(self):
        root = self.minimal()
        outside = self.base / 'outside.md'
        outside.write_text('outside', encoding='utf-8')
        try:
            (root / 'linked.md').symlink_to(outside)
        except OSError:
            self.skipTest('symlink creation unavailable in this host')
        self.assertTrue(validate(root)[0])

    def test_bom_rejected_with_diagnostic(self):
        root = self.minimal()
        entry = root / 'SKILL.md'
        entry.write_text('\ufeff' + entry.read_text(encoding='utf-8'), encoding='utf-8')
        self.assertTrue(validate(root)[0])

    def test_cli_exit_codes_and_other_working_directory(self):
        script = ROOT / 'scripts' / 'validate_skill.py'
        for args, expected in (([], 2), ([str(self.base)], 1), ([str(ROOT), '--repository'], 0)):
            result = subprocess.run([sys.executable, str(script), *args], cwd=self.base, capture_output=True, text=True)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / 'scaffold_skill.py'),
                                 'cli-sample', '--output', str(self.base), '--description', 'Create summaries.'],
                                cwd=self.base, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.base / 'cli-sample' / 'SKILL.md').is_file())


if __name__ == '__main__':
    unittest.main()
