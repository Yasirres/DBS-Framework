#!/usr/bin/env python3
"""Validate the documented DBS package profile; never execute target code."""
import argparse
import ast
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

NAME = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z')
RESERVED = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)),
            *(f'lpt{i}' for i in range(1, 10))}
MARKER = re.compile(r'\bTODO\b|\bFIXME\b|\{\{[^{}]+\}\}')
LINK = re.compile(r'(?<!!)\[[^\]\n]*\]\(([^\s)]+)\)')
REQUIRED = ['SKILL.md', 'README.md', 'CONTRIBUTING.md', 'LICENSE', '.gitignore',
            'ATTRIBUTION.md', 'CHANGELOG.md', '.github/workflows/ci.yml',
            'docs/PUBLISHING.ar.md', 'docs/VALIDATION.md', 'tests/test_tools.py',
            'references/dbs-principles.md', 'references/testing-guide.md',
            'scripts/validate_skill.py', 'scripts/scaffold_skill.py']
REQUIRED += [f'references/platforms/{p}.md' for p in ('claude', 'chatgpt', 'codex')]
REQUIRED += [f'templates/{p}-skill-template.md' for p in ('generic', 'claude', 'chatgpt', 'codex')]
SKIP = {'.git', '__pycache__', '.venv', 'venv', '.pytest_cache'}


def valid_name(value):
    return bool(NAME.fullmatch(value)) and len(value) <= 64 and value not in RESERVED


def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        raise ValueError('SKILL.md must start with --- frontmatter')
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise ValueError('frontmatter closing --- is missing') from None
    result = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        match = re.fullmatch(r'(name|description):\s*(.+)', line)
        if not match:
            raise ValueError('profile accepts only name and description on single lines')
        key, raw = match.groups()
        if key in result:
            raise ValueError(f'duplicate frontmatter field: {key}')
        if raw.startswith('"'):
            try:
                value = json.loads(raw)
            except json.JSONDecodeError:
                raise ValueError(f'{key}: use a JSON-compatible double-quoted string') from None
        else:
            if (raw[:1] in "'|>!&*[{%@`" or ': ' in raw or ' #' in raw
                    or raw.lower() in {'null', 'true', 'false', '~'}):
                raise ValueError(f'{key}: unsupported scalar; use a double-quoted string')
            value = raw
        if not isinstance(value, str) or not value.strip() or '\n' in value or '\r' in value:
            raise ValueError(f'{key} must be a nonempty single-line string')
        result[key] = value
    if set(result) != {'name', 'description'}:
        raise ValueError('name and description are required')
    return result


def exact_file(root, relative):
    current = root
    for part in Path(relative).parts:
        if not current.is_dir() or part not in {p.name for p in current.iterdir()}:
            return False
        current = current / part
    return current.is_file() and not current.is_symlink()


def validate(root, repository=False, allow_draft=False):
    errors, warnings = [], []
    root = Path(root)
    if root.is_symlink():
        return ['package root cannot be a symlink'], []
    root = root.resolve()
    if not root.is_dir():
        return [f'not a directory: {root}'], []
    if not exact_file(root, 'SKILL.md'):
        return ['missing exact-case SKILL.md file'], []
    # Reject symlinks before reading any package resources.
    files = []
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(part in SKIP for part in rel.parts):
            continue
        if path.is_symlink():
            errors.append(f'{rel.as_posix()}: symlinks are not supported')
        elif path.is_file():
            files.append(path)
    if errors:
        return errors, warnings
    try:
        text = (root / 'SKILL.md').read_text(encoding='utf-8')
        fields = frontmatter(text)
        if not valid_name(fields['name']):
            errors.append('name must be portable lowercase kebab-case, 1-64 characters')
        if len(fields['description']) > 1024 or any(c in fields['description'] for c in '<>'):
            errors.append('description must be <=1024 characters without angle brackets')
        if len(text.splitlines()) >= 500:
            errors.append('SKILL.md must be below 500 lines')
    except (OSError, UnicodeError, ValueError) as exc:
        errors.append(str(exc))
    if repository:
        for rel in REQUIRED:
            if not exact_file(root, rel):
                errors.append(f'missing required file: {rel}')
    for path in sorted(files):
        rel = path.relative_to(root).as_posix()
        if path.suffix not in {'.md', '.py'}:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            errors.append(f'{rel}: {exc}')
            continue
        if path.suffix == '.py':
            try:
                ast.parse(text, filename=rel)
            except SyntaxError as exc:
                errors.append(f'{rel}:{exc.lineno}: {exc.msg}')
            continue
        if rel.startswith('templates/'):
            continue
        # Draft markers are enforced in executable instructions, not prose about TODOs.
        if path.name == 'SKILL.md' and MARKER.search(text):
            (warnings if allow_draft else errors).append(f'{rel}: unfinished draft markers')
        # Exclude fenced examples, where links are illustrative rather than navigational.
        prose = re.sub(r'```.*?```', '', text, flags=re.S)
        prose = re.sub(r'`[^`\n]*`', '', prose)
        for link in LINK.findall(prose):
            try:
                parsed = urlsplit(link)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                # abspath normalizes dot segments without correcting wrong filename
                # case on Windows; resolve() would hide that portability defect.
                target = Path(os.path.abspath(path.parent / unquote(parsed.path)))
                target_rel = target.relative_to(root)
                if not exact_file(root, target_rel):
                    errors.append(f'{rel}: missing or case-mismatched link: {link}')
            except (ValueError, OSError):
                errors.append(f'{rel}: invalid or escaping link: {link}')
    return errors, warnings


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path)
    parser.add_argument('--repository', action='store_true', help='require the complete DBS repository layout')
    parser.add_argument('--allow-draft', action='store_true', help='warn instead of failing on starter markers')
    args = parser.parse_args(argv)
    try:
        errors, warnings = validate(args.path, args.repository, args.allow_draft)
    except OSError as exc:
        errors, warnings = [str(exc)], []
    for warning in warnings:
        print(f'WARNING: {warning}')
    for error in errors:
        print(f'ERROR: {error}', file=sys.stderr)
    print(f'{"FAIL" if errors else "PASS"}: {len(errors)} errors, {len(warnings)} warnings')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
