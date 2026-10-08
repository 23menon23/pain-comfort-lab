"""Point every link in the lab at your repository's real location.

It replaces whatever owner/repo the files currently use (read from CITATION.cff),
so you can run it again if you rename or move the repository.

Usage (from the repository root):
    python tools/set_repo_url.py your-github-name/your-repo-name
"""
import sys
from pathlib import Path

PLACEHOLDER = 'GITHUB_USER/pain-comfort-lab'

if len(sys.argv) != 2 or '/' not in sys.argv[1]:
    sys.exit('Usage: python tools/set_repo_url.py <owner>/<repo>')

target = sys.argv[1].strip('/')
root = Path(__file__).resolve().parent.parent
for line in (root / 'CITATION.cff').read_text(encoding='utf-8').splitlines():
    if line.startswith('repository-code:'):
        PLACEHOLDER = line.split('github.com/')[-1].strip().strip('"').strip('/')
files = [root / 'README.md', root / 'CITATION.cff', root / '.zenodo.json', root / 'RELEASING.md']
files += sorted((root / 'notebooks').glob('*.ipynb')) + sorted((root / 'docs').glob('*.md'))

changed = 0
for path in files:
    if not path.exists():
        continue
    text = path.read_text(encoding='utf-8')
    if PLACEHOLDER in text:
        path.write_text(text.replace(PLACEHOLDER, target), encoding='utf-8')
        changed += 1
        print('updated', path.relative_to(root))
print(f'Done: {changed} file(s) now point to https://github.com/{target}')
