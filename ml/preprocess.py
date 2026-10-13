"""Text preprocessing: cleaning, case folding, stopword filtering, stemming.

Logika ini dibuat IDENTIK dengan web/preprocess.js supaya prediksi offline
di browser sama persis dengan model Python.
"""
import re
from pathlib import Path

from nltk.stem import PorterStemmer

STOPWORDS = set(
    (Path(__file__).parent / "stopwords.txt").read_text().split()
)
_stemmer = PorterStemmer(mode=PorterStemmer.ORIGINAL_ALGORITHM)

RE_URL = re.compile(r"https?://\S+|www\.\S+")
RE_MENTION = re.compile(r"@\w+")
RE_HASHTAG = re.compile(r"#\w+")  # hapus hashtag beserta katanya
RE_RT = re.compile(r"\brt\b")
RE_HTML = re.compile(r"&\w+;")
RE_NUM = re.compile(r"\d+")
RE_NONALPHA = re.compile(r"[^a-z\s]")
RE_SPACE = re.compile(r"\s+")


def clean(text: str) -> str:
    """Tahap 1 Cleaning + Tahap 2 Case folding."""
    t = str(text)
    t = RE_URL.sub(" ", t)
    t = RE_MENTION.sub(" ", t)
    t = RE_HASHTAG.sub(" ", t)
    t = RE_HTML.sub(" ", t)
    t = t.lower()                 # case folding
    t = RE_RT.sub(" ", t)
    t = RE_NUM.sub(" ", t)        # angka
    t = RE_NONALPHA.sub(" ", t)   # tanda baca & simbol/emoji
    return RE_SPACE.sub(" ", t).strip()


def filter_stem(text: str) -> list[str]:
    """Tahap 3 Filtering (stopword) + Tahap 4 Stemming (Porter)."""
    out = []
    for w in text.split():
        if len(w) < 2 or w in STOPWORDS:
            continue
        out.append(_stemmer.stem(w))
    return out


def preprocess(text: str) -> str:
    return " ".join(filter_stem(clean(text)))


if __name__ == "__main__":
    s = "RT @user: Climate change is REAL!!! 2030 goals https://t.co/x #GreenEconomy &amp; renewables are amazing"
    print(clean(s))
    print(preprocess(s))
