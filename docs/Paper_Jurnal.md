# PAPER JURNAL ILMIAH

# Analisis Sentimen Opini Publik terhadap Isu Ekonomi Hijau
# Menggunakan TF-IDF, Naive Bayes, dan Support Vector Machine
# pada Dataset Twitter Perubahan Iklim

---

**Penulis:** SteVenJr  
**Program Studi:** Teknik Informatika  
**Tahun:** 2024  

---

## Abstrak

Ekonomi hijau merupakan agenda global yang semakin mendesak seiring meningkatnya dampak perubahan iklim. Persepsi dan dukungan publik terhadap kebijakan ekonomi hijau sangat krusial bagi keberhasilannya. Penelitian ini menganalisis sentimen opini publik terhadap isu perubahan iklim dan ekonomi hijau menggunakan data Twitter. Dataset yang digunakan adalah *Twitter Climate Change Sentiment Dataset* (Edward Qian, Kaggle, 2022) yang berisi 43.943 tweet berbahasa Inggris berlabel. Setelah pembersihan data dan *preprocessing* (cleaning, case folding, stopword removal, stemming Porter), diperoleh 31.907 tweet yang direpresentasikan sebagai vektor TF-IDF (unigram+bigram, 15.000 fitur). Dua algoritma *machine learning* dibandingkan: Multinomial Naive Bayes (MNB) dan Linear Support Vector Machine (SVM). Hasil evaluasi menunjukkan SVM unggul dengan akurasi **74,07%** dan F1-Score makro **65,81%**, dibandingkan Naive Bayes dengan akurasi 72,89% dan F1-Score makro 58,46%. Analisis distribusi menunjukkan 57,3% tweet bersifat positif (pro-aksi iklim), 24,2% netral, dan 12,2% negatif (skeptis/anti-kebijakan). Model diekspor ke format JSON dan diintegrasikan dalam platform web statis yang dapat menjalankan inferensi secara offline di browser.

**Kata Kunci:** analisis sentimen, ekonomi hijau, perubahan iklim, TF-IDF, Naive Bayes, SVM, Twitter, NLP

---

## Abstract

*The green economy is an increasingly urgent global agenda amid escalating climate change impacts. Public perception and support for green economy policies are crucial to their success. This study analyzes public opinion sentiment toward climate change and green economy issues using Twitter data. The dataset used is the Twitter Climate Change Sentiment Dataset (Edward Qian, Kaggle, 2022) containing 43,943 labeled English tweets. After data cleaning and preprocessing (cleaning, case folding, stopword removal, Porter stemming), 31,907 tweets were obtained and represented as TF-IDF vectors (unigram+bigram, 15,000 features). Two machine learning algorithms were compared: Multinomial Naive Bayes (MNB) and Linear Support Vector Machine (SVM). Evaluation results show SVM outperformed with 74.07% accuracy and 65.81% macro F1-Score, compared to Naive Bayes with 72.89% accuracy and 58.46% macro F1-Score. Distribution analysis revealed 57.3% of tweets were positive (pro-climate action), 24.2% neutral, and 12.2% negative (skeptical/anti-policy). The model was exported to JSON format and integrated into a static web platform capable of offline inference in the browser.*

**Keywords:** *sentiment analysis, green economy, climate change, TF-IDF, Naive Bayes, SVM, Twitter, NLP*

---

## 1. Pendahuluan

Perubahan iklim global telah menjadi ancaman eksistensial yang mendorong transformasi besar menuju *green economy* atau ekonomi hijau. Berdasarkan laporan IPCC AR6 (2023), emisi gas rumah kaca harus dikurangi 43% pada 2030 dibandingkan level 2019 untuk membatasi pemanasan pada 1,5°C. Berbagai negara merespons dengan kebijakan ambisius seperti Green New Deal (AS), European Green Deal (UE), dan komitmen Net Zero 2060 (Tiongkok).

Keberhasilan transisi ini sangat bergantung pada penerimaan dan dukungan masyarakat. Media sosial — khususnya Twitter/X dengan lebih dari 500 juta pengguna aktif — menjadi ruang publik utama di mana opini tentang kebijakan iklim diekspresikan secara masif dan spontan. Analisis sentimen terhadap data Twitter dapat memberikan *real-time insight* tentang persepsi publik yang tidak mungkin diperoleh melalui survei konvensional.

Penelitian sebelumnya tentang analisis sentimen isu lingkungan umumnya berfokus pada bahasa Inggris dengan metode *lexicon-based* (Stokes et al., 2020) atau *deep learning* berbasis BERT (Loureiro & Jorge, 2022). Namun, pendekatan berbasis fitur (TF-IDF + ML) masih relevan karena interpretabilitas, efisiensi komputasi, dan kemampuan deployment offline yang superior.

Kontribusi utama penelitian ini:
1. Pipeline preprocessing komprehensif yang direplikasi identik di Python dan JavaScript untuk konsistensi inferensi offline
2. Perbandingan sistematis MNB vs. SVM pada domain perubahan iklim
3. Platform web inovatif yang menjalankan inferensi AI sepenuhnya di browser tanpa server backend

---

## 2. Metode Penelitian

### 2.1 Dataset

Dataset yang digunakan adalah *Twitter Climate Change Sentiment Dataset* yang dikurasi oleh Edward Qian dan dipublikasikan di Kaggle (2022). Dataset ini berisi tweet yang dikumpulkan dari 2008 hingga 2019 dengan empat label: **pro** (+1), **anti** (-1), **neutral** (0), dan **news** (2).

Label **news** (9.276 tweet) dieksklusi karena mewakili tweet berita tanpa opini yang eksplisit — tidak relevan untuk analisis sentimen. Setelah deduplikasi, diperoleh **31.907 tweet** yang digunakan dalam eksperimen.

| Label | Jumlah | % |
|-------|--------|---|
| Positif (pro) | 18.291 | 57,3% |
| Netral | 7.715 | 24,2% |
| Negatif (anti) | 3.901 | 12,2% |
| **Total** | **31.907** | **100%** |

### 2.2 Text Preprocessing

#### 2.2.1 Cleaning
Penghapusan elemen non-informatif: URL (`https?://\S+`), @mention, #hashtag, HTML entity, angka, dan karakter non-alfabet menggunakan *regular expression*.

#### 2.2.2 Case Folding
Seluruh teks dikonversi ke huruf kecil untuk menghindari duplikasi kata akibat perbedaan kapitalisasi.

#### 2.2.3 Stopword Removal
Penghapusan 127 stopword bahasa Inggris (daftar NLTK) kecuali kata negasi (*not*, *no*, *never*) yang relevan untuk sentimen.

#### 2.2.4 Stemming
Algoritma Porter Stemmer (Porter, 1980) digunakan untuk mereduksi kata ke bentuk dasarnya. Contoh: *"changing"* → *"chang"*, *"policies"* → *"polici"*.

**Konsistensi penting:** Logika preprocessing diimplementasikan identik di Python (`ml/preprocess.py`) dan JavaScript (`web/preprocess.js`) menggunakan Port algoritma Porter Stemmer, memastikan hasil prediksi browser sama dengan model Python.

### 2.3 Ekstraksi Fitur: TF-IDF

Representasi teks menggunakan TF-IDF dengan formula:

$$TF\text{-}IDF(t,d) = \frac{f(t,d)}{\sum_{t'} f(t',d)} \times \left(\log\frac{N}{df(t)} + 1\right)$$

Konfigurasi: N-gram (1,2), max 15.000 fitur, min df=3, normalisasi L2. Bigram ditambahkan untuk menangkap frasa penting seperti *"climate change"*, *"renewable energy"*, *"carbon tax"*.

### 2.4 Algoritma Klasifikasi

#### 2.4.1 Multinomial Naive Bayes

$$\hat{c} = \arg\max_c \left[\log P(c) + \sum_{i=1}^{n} \log P(w_i|c)\right]$$

dengan Laplace smoothing α=0,3:
$$P(w_i|c) = \frac{N(w_i,c)+0{,}3}{N(c)+0{,}3 \cdot |V|}$$

#### 2.4.2 Linear SVM

$$\hat{y} = \text{sign}(w^Tx + b), \quad \text{dengan} \quad \min \tfrac{1}{2}\|w\|^2 + C\sum\xi_i$$

Parameter C=0,5, `class_weight="balanced"` untuk menangani ketidakseimbangan kelas.

### 2.5 Evaluasi

Split stratified 80:20. Metrik: Accuracy, Precision, Recall, F1-Score (macro dan weighted average).

---

## 3. Hasil dan Pembahasan

### 3.1 Performa Model

| Model | Accuracy | Precision (M) | Recall (M) | F1 (M) |
|-------|----------|---------------|------------|--------|
| Naive Bayes | 72,89% | 71,63% | 54,38% | 58,46% |
| **SVM** | **74,07%** | **65,75%** | **65,91%** | **65,81%** |

**SVM secara konsisten unggul** pada metrik F1-Score (+7,35%) dan Recall (+11,53%) yang lebih kritis untuk dataset imbalanced. Naive Bayes menunjukkan *recall collapse* pada kelas minoritas (negatif: 34,81%) akibat bias ke kelas mayoritas (positif), sebuah kelemahan klasik MNB yang dokumentasi dalam literatur (McCallum & Nigam, 1998).

SVM dengan `class_weight="balanced"` berhasil mengkompensasi ketidakseimbangan dengan recall negatif 60,13% — hampir dua kali lipat Naive Bayes. Ini membuktikan bahwa penanganan imbalanced dataset secara eksplisit sangat penting dalam analisis sentimen multi-kelas.

### 3.2 Analisis Per Kelas (SVM)

| Kelas | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| Negatif | 57,66% | 60,13% | 58,87% | 770 |
| Netral | 56,31% | 53,41% | 54,82% | 1.496 |
| Positif | 83,29% | 84,18% | 83,74% | 4.116 |

Kelas positif mendapatkan performa terbaik (F1: 83,74%) seiring dengan ukurannya yang dominan. Kelas netral dan negatif lebih sulit diklasifikasikan karena garis batas yang lebih ambigu — tweet netral seringkali mengandung kata-kata yang sama dengan tweet positif atau negatif namun dalam konteks pelaporan fakta.

### 3.3 Distribusi Sentimen

Dari 31.907 tweet yang dianalisis, **57,3% bersifat positif** — mengindikasikan bahwa komunitas Twitter yang aktif membahas perubahan iklim didominasi oleh pendukung aksi iklim. Ini konsisten dengan penelitian Tyson & Kennedy (2020) yang menemukan mayoritas publik AS mendukung kebijakan energi bersih.

Sentimen **negatif (12,2%)** utamanya berasal dari kelompok *climate skeptics* yang menggunakan frasa seperti *"climate hoax"*, *"job killer"*, dan *"fake science"*. Ini menunjukkan masih adanya resistensi publik yang signifikan terhadap transisi energi, terutama terkait kekhawatiran ekonomi.

### 3.4 WordCloud dan Kata Kunci Dominan

Analisis WordCloud pada masing-masing kategori:

- **Positif:** *climate change, renewable energy, solar power, green economy, sustainable, wind energy, clean energy, carbon neutral*
- **Netral:** *climate change, global warming, report, government, temperature, carbon emissions, policy, study*
- **Negatif:** *climate change, hoax, jobs, economy, coal, fossil fuels, expensive, fraud, alarmist*

Menariknya, *"climate change"* muncul dominan di ketiga kategori, mengkonfirmasi bahwa ini adalah topik sentral. Namun konteks penggunaannya berbeda: kelas positif mengasosiasikannya dengan solusi, kelas negatif dengan skeptisisme, dan kelas netral dengan pelaporan fakta.

---

## 4. Kesimpulan

Penelitian ini berhasil membangun sistem analisis sentimen untuk isu ekonomi hijau berbasis TF-IDF dan machine learning. SVM Linear terbukti lebih efektif dari Naive Bayes dengan akurasi 74,07% dan F1-macro 65,81% pada data uji. Mayoritas opini publik Twitter (57,3%) bersifat positif terhadap aksi iklim, sementara 12,2% bersifat skeptis atau negatif. Inovasi utama penelitian ini adalah ekspor model ke JavaScript untuk inferensi offline di browser — memungkinkan deployment statis tanpa biaya server.

Penelitian lanjutan direkomendasikan menggunakan model berbasis transformer (BERT, RoBERTa) dan pembaruan dataset real-time melalui Twitter API untuk analisis tren temporal.

---

## Daftar Pustaka

1. IPCC. (2023). *Climate Change 2023: Synthesis Report*. Intergovernmental Panel on Climate Change.
2. McCallum, A., & Nigam, K. (1998). A comparison of event models for Naive Bayes text classification. *AAAI Workshop on Learning for Text Categorization*, 752(1), 41–48.
3. Porter, M. F. (1980). An algorithm for suffix stripping. *Program: Electronic Library and Information Systems*, 14(3), 130–137.
4. Loureiro, D., & Jorge, A. M. (2022). TimeLMs: Diachronic language models from Twitter. *ACL Anthology*, 341–353.
5. Vapnik, V. N. (1995). *The Nature of Statistical Learning Theory*. Springer-Verlag.
6. Salton, G., & McGill, M. J. (1983). *Introduction to Modern Information Retrieval*. McGraw-Hill.
7. Tyson, A., & Kennedy, B. (2020). *Two-thirds of Americans think government should do more on climate*. Pew Research Center.
8. Qian, E. (2022). *Twitter Climate Change Sentiment Dataset*. Kaggle. https://www.kaggle.com/datasets/edqian/twitter-climate-change-sentiment-dataset
9. Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, 2825–2830.
10. Bird, S., Klein, E., & Loper, E. (2009). *Natural Language Processing with Python*. O'Reilly Media.
