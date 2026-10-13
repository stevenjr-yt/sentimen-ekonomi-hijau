# 🌿 SentimentGreen – Analisis Sentimen Ekonomi Hijau

Platform analisis sentimen berbasis AI untuk mendeteksi opini publik terhadap isu **perubahan iklim** dan **ekonomi hijau** dari data Twitter/X.

🔗 **Live Demo:** [sentimentgreen.vercel.app](https://sentimentgreen.vercel.app)

---

## ✨ Fitur
- 🤖 **Model AI Offline** – SVM + Naive Bayes, berjalan 100% di browser tanpa server
- 🔍 **Analisis Tunggal** – Input tweet langsung, hasil instan
- 📂 **Analisis Batch** – Upload CSV ribuan tweet sekaligus
- 📊 **Dashboard** – Pie chart, bar chart perbandingan, confusion matrix
- 🔒 **Privasi** – Tidak ada data dikirim ke server

## 📁 Struktur Proyek
```
sentimen-ekonomi-hijau/
├── data/           # Dataset Twitter Climate Change Sentiment (Kaggle)
├── ml/             # Pipeline Python (preprocessing, training, export)
│   ├── preprocess.py
│   ├── train.py
│   ├── download_data.py
│   └── generate_synthetic.py
├── web/            # Website statis (Vercel)
│   ├── index.html
│   ├── style.css
│   ├── preprocess.js   # Preprocessing identik dengan Python
│   ├── inference.js    # TF-IDF + SVM/NB offline
│   ├── app.js
│   └── model/          # Model JSON (dihasilkan train.py)
│       ├── model.json
│       └── metrics.json
├── results/        # Grafik, confusion matrix, wordcloud
├── docs/           # Laporan, paper, studi literatur
├── models/         # Model .pkl (sklearn)
├── vercel.json
└── requirements.txt
```

## 🚀 Cara Jalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Download dataset (butuh kaggle.json)
```bash
python ml/download_data.py
```

### 3. Training model
```bash
cd ml && python train.py
```

### 4. Buka website lokal
```bash
cd web && python -m http.server 8080
# Buka http://localhost:8080
```

## 📊 Hasil Model
| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| SVM (LinearSVC) | **74.07%** | 65.75% | 65.91% | **65.81%** |
| Naive Bayes | 72.89% | 71.63% | 54.38% | 58.46% |

## 🧠 Teknologi
- **ML:** scikit-learn (TF-IDF, LinearSVC, MultinomialNB)
- **Frontend:** HTML/CSS/JS (Vanilla, no framework)
- **Inference:** Porter Stemmer + TF-IDF + SVM/NB offline di browser
- **Dataset:** [Twitter Climate Change Sentiment Dataset](https://www.kaggle.com/datasets/edqian/twitter-climate-change-sentiment-dataset) (Edward Qian, Kaggle)
- **Deploy:** Vercel (static)

## 📄 Dokumen
- 📋 `docs/Laporan_Project.md` – Laporan teknis lengkap
- 📰 `docs/Paper_Jurnal.md` – Paper ilmiah format jurnal
- 📚 `docs/Studi_Literatur.md` – Review literatur terkait

## 📜 Lisensi
MIT License – Free to use for academic purposes.
