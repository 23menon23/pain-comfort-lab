"""Execute every notebook top to bottom on the tiny test model."""
from pathlib import Path

import nbformat
import pytest
from nbclient import NotebookClient

NOTEBOOKS = sorted((Path(__file__).resolve().parent.parent / 'notebooks').glob('*.ipynb'))


@pytest.mark.parametrize('path', NOTEBOOKS, ids=[p.stem for p in NOTEBOOKS])
def test_notebook_runs(path, tmp_path):
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=900, kernel_name='python3',
                            resources={'metadata': {'path': str(path.parent)}})
    client.execute()
    for cell in nb.cells:
        if cell.cell_type == 'code':
            for output in cell.get('outputs', []):
                assert output.get('output_type') != 'error', f'{path.name}: {output.get("ename")}: {output.get("evalue")}'
