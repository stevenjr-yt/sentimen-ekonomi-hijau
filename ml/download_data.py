"""Unduh Twitter Climate Change Sentiment Dataset dari Kaggle.
Butuh ~/.kaggle/kaggle.json (Kaggle > Settings > API > Create New Token).
"""
import subprocess
import sys
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"
DATA.mkdir(exist_ok=True)
subprocess.run([sys.executable, "-m", "kaggle", "datasets", "download",
                "-d", "edqian/twitter-climate-change-sentiment-dataset",
                "-p", str(DATA), "--unzip"], check=True)
print("Dataset tersimpan di", DATA)
