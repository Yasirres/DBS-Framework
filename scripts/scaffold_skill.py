#!/usr/bin/env python3
"""Create a new, explicitly unfinished DBS skill; never overwrite a destination."""
import argparse
import json
from pathlib import Path
import re
import sys

from validate_skill import valid_name

SOURCE = Path(__file__).resolve().parent.parent
PLATFORMS = ('generic', 'claude', 'chatgpt', 'codex')


def scaffold(name, output, platform, description):
    if not valid_name(name):
        raise ValueError('name must be portable lowercase kebab-case, 1-64 characters')
    if platform not in PLATFORMS:
        raise ValueError('unknown platform')
    if (not description.strip() or len(description) > 1024
            or any(c in description for c in '<>\r\n')):
        raise ValueError('description must be nonempty, <=1024 characters, without newlines or angle brackets')
    template_path = SOURCE / 'templates' / f'{platform}-skill-template.md'
    template = template_path.read_text(encoding='utf-8')
    values = {'name': name, 'title': name.replace('-', ' ').title(),
              'description_json': json.dumps(description, ensure_ascii=False)}
    def replace(match):
        if match[1] not in values:
            raise ValueError(f'unknown template marker: {match[1]}')
        return values[match[1]]
    content = re.sub(r'\{\{(\w+)\}\}', replace, template)
    adapter = None
    if platform != 'generic':
        adapter = (SOURCE / 'references' / 'platforms' / f'{platform}.md').read_text(encoding='utf-8')
        # Framework-maintenance links are prose in a standalone generated package.
        adapter = re.sub(r'\[([^\]]+)\]\(\.\./\.\./templates/[^)]+\)', r'\1 (in DBS Framework)', adapter)
    output = Path(output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    destination = output / name
    destination.mkdir(exist_ok=False)
    # All reads and rendering occur before the new destination is created. If a write
    # fails, leave the partial new directory for inspection; never delete user data.
    (destination / 'SKILL.md').write_text(content, encoding='utf-8')
    if adapter is not None:
        folder = destination / 'references' / 'platforms'
        folder.mkdir(parents=True)
        (folder / f'{platform}.md').write_text(adapter, encoding='utf-8')
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('name')
    parser.add_argument('--output', type=Path, default=Path.cwd(), help='parent directory for the new skill')
    parser.add_argument('--platform', choices=PLATFORMS, default='generic')
    parser.add_argument('--description', required=True, help='what the capability does and when to use it')
    args = parser.parse_args(argv)
    try:
        destination = scaffold(args.name, args.output, args.platform, args.description)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 1
    print(f'Created draft: {destination}')
    print('Complete all TODOs, then validate without --allow-draft before use.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
