"""Pipeline lengkap: load -> preprocessing -> TF-IDF -> train NB & SVM -> evaluasi
-> visualisasi (pie chart, wordcloud, confusion matrix) -> ekspor model offline (JSON).

Jalankan:  python ml/train.py
"""
import json
import pickle
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, precision_recall_fscore_support)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from wordcloud import WordCloud

from preprocess import clean, preprocess

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "twitter_sentiment_data.csv"
RES = ROOT / "results"
MOD = ROOT / "models"
WEB = ROOT / "web" / "model"
for d in (RES, MOD, WEB):
    d.mkdir(parents=True, exist_ok=True)

LABELS = ["negatif", "netral", "positif"]
MAP = {-1: "negatif", 0: "netral", 1: "positif"}  # 2 (news) dibuang
COLORS = {"negatif": "#ff6b6b", "netral": "#94a3b8", "positif": "#34d399"}

# 1. LOAD -------------------------------------------------------------------
df = pd.read_csv(DATA)
print("Raw:", df.shape, "\n", df["sentiment"].value_counts())
raw_n = len(df)
df = df[df["sentiment"].isin(MAP)].copy()
df["label"] = df["sentiment"].map(MAP)
df = df.drop_duplicates(subset="message")

# 2. PREPROCESSING ----------------------------------------------------------
df["clean"] = df["message"].map(clean)
df["text"] = df["message"].map(preprocess)
df = df[df["text"].str.len() > 0]
df[["tweetid", "message", "clean", "text", "label"]].head(10).to_csv(
    RES / "contoh_preprocessing.csv", index=False)
print("After cleaning:", len(df))

# 3. SPLIT 80/20 ------------------------------------------------------------
X_tr, X_te, y_tr, y_te = train_test_split(
    df["text"], df["label"], test_size=0.2, random_state=42, stratify=df["label"])

# 4. TF-IDF -----------------------------------------------------------------
vec = TfidfVectorizer(ngram_range=(1, 2), min_df=3, max_features=15000,
                      sublinear_tf=False, token_pattern=r"(?u)\b\w+\b")
Xtr = vec.fit_transform(X_tr)
Xte = vec.transform(X_te)

# 5. TRAINING ---------------------------------------------------------------
models = {
    "naive_bayes": MultinomialNB(alpha=0.3),
    "svm": LinearSVC(C=0.5, class_weight="balanced", random_state=42),
}
metrics = {"dataset": {
    "raw": raw_n, "used": len(df), "train": len(X_tr), "test": len(X_te),
    "distribution": df["label"].value_counts().to_dict(),
    "vocab": len(vec.vocabulary_)}}

for name, m in models.items():
    m.fit(Xtr, y_tr)
    pred = m.predict(Xte)
    p, r, f, _ = precision_recall_fscore_support(y_te, pred, average="macro")
    pw, rw, fw, _ = precision_recall_fscore_support(y_te, pred, average="weighted")
    rep = classification_report(y_te, pred, output_dict=True)
    cm = confusion_matrix(y_te, pred, labels=LABELS)
    metrics[name] = {
        "accuracy": accuracy_score(y_te, pred),
        "precision_macro": p, "recall_macro": r, "f1_macro": f,
        "precision_weighted": pw, "recall_weighted": rw, "f1_weighted": fw,
        "per_class": {k: rep[k] for k in LABELS},
        "confusion_matrix": cm.tolist()}
    print(f"\n== {name} ==\n", classification_report(y_te, pred, digits=4))

    fig, ax = plt.subplots(figsize=(5, 4.3))
    ax.imshow(cm, cmap="Greens")
    ax.set_xticks(range(3), LABELS); ax.set_yticks(range(3), LABELS)
    for i in range(3):
        for j in range(3):
            ax.text(j, i, cm[i, j], ha="center", va="center",
                    color="white" if cm[i, j] > cm.max() / 2 else "black")
    ax.set_xlabel("Prediksi"); ax.set_ylabel("Aktual")
    ax.set_title(f"Confusion Matrix - {name.replace('_', ' ').title()}")
    fig.tight_layout(); fig.savefig(RES / f"cm_{name}.png", dpi=150); plt.close(fig)

    with open(MOD / f"{name}.pkl", "wb") as fh:
        pickle.dump(m, fh)
with open(MOD / "tfidf.pkl", "wb") as fh:
    pickle.dump(vec, fh)

best = max(("naive_bayes", "svm"), key=lambda k: metrics[k]["f1_macro"])
metrics["best_model"] = best

# 6. VISUALISASI ------------------------------------------------------------
dist = df["label"].value_counts().reindex(LABELS)
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(dist, labels=[l.title() for l in LABELS], autopct="%1.1f%%", startangle=90,
       colors=[COLORS[l] for l in LABELS], wedgeprops=dict(width=0.55, edgecolor="w"))
ax.set_title("Distribusi Sentimen Opini Publik\nIsu Perubahan Iklim & Ekonomi Hijau")
fig.savefig(RES / "pie_sentimen.png", dpi=150, bbox_inches="tight"); plt.close(fig)

# distribusi prediksi model terbaik pada data uji
pred_best = models[best].predict(Xte)
pd_ = pd.Series(pred_best).value_counts().reindex(LABELS)
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(pd_, labels=[l.title() for l in LABELS], autopct="%1.1f%%", startangle=90,
       colors=[COLORS[l] for l in LABELS], wedgeprops=dict(width=0.55, edgecolor="w"))
ax.set_title(f"Distribusi Prediksi Sentimen Data Uji ({best})")
fig.savefig(RES / "pie_prediksi.png", dpi=150, bbox_inches="tight"); plt.close(fig)

wc_kw = dict(width=1200, height=600, background_color="#0b1220", max_words=150,
             collocations=False, colormap="YlGn")
words_all = " ".join(df["clean"].map(lambda t: " ".join(
    w for w in t.split() if len(w) > 2 and w not in __import__("preprocess").STOPWORDS)))
WordCloud(**wc_kw).generate(words_all).to_file(str(RES / "wordcloud_all.png"))
top_words = {}
for lab, cmap in zip(LABELS, ["Reds", "Greys", "Greens"]):
    txt = " ".join(df.loc[df.label == lab, "clean"].map(lambda t: " ".join(
        w for w in t.split() if len(w) > 2 and w not in __import__("preprocess").STOPWORDS)))
    wc = WordCloud(**{**wc_kw, "colormap": cmap}).generate(txt)
    wc.to_file(str(RES / f"wordcloud_{lab}.png"))
    top_words[lab] = [[w, round(float(s), 4)] for w, s in list(wc.words_.items())[:60]]
metrics["top_words"] = top_words

# model comparison bar
fig, ax = plt.subplots(figsize=(7, 4))
keys = ["accuracy", "precision_macro", "recall_macro", "f1_macro"]
x = np.arange(len(keys))
for i, (n, c) in enumerate([("naive_bayes", "#60a5fa"), ("svm", "#34d399")]):
    v = [metrics[n][k] for k in keys]
    ax.bar(x + i * 0.38, v, 0.38, label=n, color=c)
    for xi, vi in zip(x, v):
        ax.text(xi + i * 0.38, vi + 0.01, f"{vi:.3f}", ha="center", fontsize=8)
ax.set_xticks(x + 0.19, ["Accuracy", "Precision", "Recall", "F1"]); ax.set_ylim(0, 1)
ax.legend(); ax.set_title("Perbandingan Naive Bayes vs SVM")
fig.tight_layout(); fig.savefig(RES / "perbandingan_model.png", dpi=150); plt.close(fig)

with open(RES / "metrics.json", "w") as fh:
    json.dump(metrics, fh, indent=2, default=float)

# 7. EKSPOR MODEL OFFLINE (JSON untuk browser) -------------------------------
vocab = sorted(vec.vocabulary_, key=vec.vocabulary_.get)
nb, svm = models["naive_bayes"], models["svm"]
r4 = lambda a: np.round(a, 5).tolist()
export = {
    "labels": list(nb.classes_),
    "vocab": vocab,
    "idf": r4(vec.idf_),
    "ngram": [1, 2],
    "nb": {"class_log_prior": r4(nb.class_log_prior_),
           "feature_log_prob": r4(nb.feature_log_prob_)},
    "svm": {"coef": r4(svm.coef_), "intercept": r4(svm.intercept_)},
    "stopwords": sorted(__import__("preprocess").STOPWORDS),
}
with open(WEB / "model.json", "w") as fh:
    json.dump(export, fh, separators=(",", ":"))
web_metrics = {k: v for k, v in metrics.items()}
with open(WEB / "metrics.json", "w") as fh:
    json.dump(web_metrics, fh, default=float)

# sampel uji untuk verifikasi konsistensi JS vs Python
samp = df.loc[X_te.index[:200], ["message"]].copy()
samp["py_text"] = X_te[:200].values
samp["py_nb"] = nb.predict(Xte[:200]); samp["py_svm"] = svm.predict(Xte[:200])
samp.to_json(RES / "consistency_samples.json", orient="records")
print("\nBest:", best, json.dumps({k: metrics[best][k] for k in keys}, indent=1))
