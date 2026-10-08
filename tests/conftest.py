import os
import sys
from pathlib import Path

# Every test uses the tiny random model: no download, CPU only.
os.environ.setdefault('PCLAB_TEST_MODEL', '1')
os.environ.setdefault('MPLBACKEND', 'Agg')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
