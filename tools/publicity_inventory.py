"""Find publicity candidates in local text; candidates are never verified outcomes."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

EXTENSIONS = {'.md', '.txt', '.csv', '.tsv'}
SKIP = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'lib', 'src', 'assets', 'tests', 'dist', '.build'}
SKIP_PREFIXES = ('cue-generation-', 'cue-beat-alignment-', 'stemlab-', 'DanceMoves', 'blender-temp', 'Meshy_', 'workspace-temp', '.venv', 'node_modules')
TERMS = re.compile(r'publicity|airplay|broadcast|playlist|published|coverage|review|article|interview|featured|played|aired|psychreg|fyff|v2radio', re.I)
STRONG = re.compile(r'was played|has played|played (?:on|at)|airplay (?:verified|confirmed)|verified airplay|published (?:article|review|essay|contribution|outcome)|(?:published|publication).*https?://|article (?:published|live)|station.log|fyff|psychreg|v2radio|coverage.*verified|broadcast.*confirmed', re.I)


def inventory(root: Path) -> dict:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f'Inventory root is not an existing directory: {root}')
    result = {'schema_version': 1, 'root': str(root), 'files': [], 'candidates': [], 'unavailable': [], 'skipped_directories': []}
    def unavailable(error):
        result['unavailable'].append({'path': str(error.filename), 'error': str(error)})
    for folder, directories, files in os.walk(root, onerror=unavailable, followlinks=False):
        # Embedded source checkouts are engineering inputs, not campaign evidence.
        if Path(folder) != root and ((Path(folder) / '.git').exists() or (Path(folder) / 'pyproject.toml').exists()):
            result['skipped_directories'].append(str(Path(folder).relative_to(root)))
            directories[:] = []
            continue
        retained = []
        for name in directories:
            path = Path(folder) / name
            if name in SKIP or name.startswith(SKIP_PREFIXES) or path.is_symlink():
                result['skipped_directories'].append(str(path.relative_to(root)))
            else:
                retained.append(name)
        directories[:] = sorted(retained)
        for name in sorted(files):
            path = Path(folder) / name
            if path.suffix.lower() not in EXTENSIONS or path.is_symlink():
                continue
            relative = str(path.relative_to(root))
            try:
                if path.stat().st_size > 2_000_000:
                    result['unavailable'].append({'path': relative, 'error': 'text exceeds 2 MB inventory limit'})
                    continue
                data = path.read_bytes()
                content = data.decode('utf-8-sig', errors='strict')
            except (OSError, UnicodeError) as error:
                result['unavailable'].append({'path': relative, 'error': str(error)})
                continue
            matches = []
            for number, line in enumerate(content.splitlines(), 1):
                if TERMS.search(line):
                    matches.append({'line': number, 'text': line[:2000], 'truncated': len(line) > 2000, 'strong_candidate': bool(STRONG.search(line))})
            result['files'].append({'path': relative, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(), 'candidate_lines': len(matches)})
            if matches:
                result['candidates'].append({'path': relative, 'state': 'candidate_detected', 'matches': matches})
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    options = parser.parse_args()
    records = inventory(options.root)
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'files': len(records['files']), 'candidate_files': len(records['candidates']), 'unavailable': len(records['unavailable']), 'state': 'candidate_detected'}))
