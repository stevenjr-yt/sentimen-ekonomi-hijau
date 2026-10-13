# LAPORAN PROYEK
# ANALISIS SENTIMEN OPINI PUBLIK TERHADAP ISU EKONOMI HIJAU
# MENGGUNAKAN METODE TF-IDF, NAIVE BAYES, DAN SVM

---

**Nama Proyek:** SentimentGreen – Platform Analisis Sentimen Ekonomi Hijau  
**Dataset:** Twitter Climate Change Sentiment Dataset (Edward Qian, Kaggle, 2022)  
**Metode:** TF-IDF + Multinomial Naive Bayes & Linear SVM  
**Tanggal:** Oktober 2024  

---

## BAB I – PENDAHULUAN

### 1.1 Latar Belakang

Perubahan iklim dan transisi menuju ekonomi hijau (*green economy*) merupakan isu global yang semakin mendesak. Laporan IPCC (2023) menyatakan bahwa batas kenaikan suhu 1,5°C akan terlampaui dalam dekade ini jika tidak ada tindakan radikal. Berbagai kebijakan telah diluncurkan — dari Paris Agreement, carbon pricing, hingga insentif kendaraan listrik — namun keberhasilannya sangat bergantung pada dukungan opini publik.

Media sosial Twitter/X menjadi salah satu barometer utama opini publik global. Jutaan tweet tentang iklim, energi terbarukan, dan kebijakan lingkungan diposting setiap hari. Analisis sentimen terhadap tweet-tweet tersebut dapat memberikan *insight* berharga bagi pembuat kebijakan, peneliti, dan aktivis lingkungan.

Proyek ini membangun sistem analisis sentimen berbasis *machine learning* yang:
1. Menganalisis tweet berbahasa Inggris tentang perubahan iklim
2. Mengklasifikasikan sentimen menjadi **positif**, **negatif**, atau **netral**
3. Membandingkan performa dua algoritma: **Multinomial Naive Bayes** dan **Linear SVM**
4. Menyajikan hasil dalam platform web yang dapat diakses publik secara real-time dengan model berjalan offline di browser

### 1.2 Rumusan Masalah

1. Bagaimana distribusi sentimen opini publik terhadap isu perubahan iklim dan ekonomi hijau di Twitter?
2. Algoritma mana (Naive Bayes atau SVM) yang memberikan akurasi lebih tinggi untuk klasifikasi sentimen tweet?
3. Kata-kata kunci apa yang paling dominan muncul pada masing-masing kategori sentimen?

### 1.3 Tujuan

1. Membangun pipeline *text preprocessing* yang efektif untuk data tweet
2. Melatih dan membandingkan model Naive Bayes dan SVM
3. Mengevaluasi model menggunakan metrik Accuracy, Precision, Recall, dan F1-Score
4. Memvisualisasikan hasil dengan pie chart dan WordCloud
5. Menyajikan model secara online melalui platform web berbasis JavaScript offline

### 1.4 Manfaat

- **Akademik:** Kontribusi metodologi analisis sentimen pada domain ekonomi hijau
- **Praktis:** Dashboard real-time untuk memantau opini publik terhadap kebijakan iklim
- **Sosial:** Membantu aktivis dan NGO memahami persepsi masyarakat

---

## BAB II – TINJAUAN PUSTAKA

### 2.1 Ekonomi Hijau

*Green economy* didefinisikan UNEP sebagai ekonomi yang menghasilkan peningkatan kesejahteraan manusia dan kesetaraan sosial, sekaligus secara signifikan mengurangi risiko lingkungan dan kelangkaan ekologi. Pilar utamanya meliputi energi terbarukan, transportasi listrik, pertanian berkelanjutan, dan bangunan hijau.

### 2.2 Analisis Sentimen

Analisis sentimen (*opinion mining*) adalah bidang NLP yang bertujuan mengidentifikasi dan mengekstrak opini subjektif dari teks. Tiga pendekatan utama:

1. **Lexicon-based:** Menggunakan kamus kata bersentimen (SentiWordNet, VADER)
2. **Machine learning berbasis fitur:** TF-IDF + Naive Bayes / SVM
3. **Deep learning:** BERT, RoBERTa, IndoBERT

Pendekatan berbasis fitur (TF-IDF + ML) dipilih dalam proyek ini karena:
- Interpretable dan transparan
- Dapat diekspor ke format ringan untuk inferensi offline di browser
- Performa kompetitif pada dataset terbatas
- Tidak memerlukan GPU untuk inferensi

### 2.3 TF-IDF (Term Frequency-Inverse Document Frequency)

TF-IDF adalah metode representasi teks yang mengkuantifikasi pentingnya sebuah kata dalam dokumen relatif terhadap korpus.

#### 2.3.1 Term Frequency (TF)

$$TF(t, d) = \frac{f(t, d)}{\sum_{t' \in d} f(t', d)}$$

Di mana:
- $f(t, d)$ = frekuensi term $t$ dalam dokumen $d$
- $\sum_{t'} f(t', d)$ = jumlah total term dalam dokumen $d$

#### 2.3.2 Inverse Document Frequency (IDF)

$$IDF(t) = \log\left(\frac{N}{df(t)}\right) + 1$$

Di mana:
- $N$ = jumlah total dokumen dalam korpus
- $df(t)$ = jumlah dokumen yang mengandung term $t$
- $+1$ = smoothing untuk menghindari nol

#### 2.3.3 TF-IDF

$$TF\text{-}IDF(t, d) = TF(t, d) \times IDF(t)$$

#### 2.3.4 Normalisasi L2

Vektor TF-IDF dinormalisasi dengan norma Euclidean:

$$\hat{v} = \frac{v}{\|v\|_2} = \frac{v}{\sqrt{\sum_{i} v_i^2}}$$

Sehingga panjang dokumen tidak mempengaruhi bobot fitur.

### 2.4 Multinomial Naive Bayes (MNB)

Berdasarkan Teorema Bayes:

$$P(c \mid d) = \frac{P(d \mid c) \cdot P(c)}{P(d)}$$

Dengan asumsi independensi fitur (naive assumption):

$$P(c \mid d) \propto P(c) \prod_{i=1}^{n} P(w_i \mid c)$$

Estimasi probabilitas bersyarat dengan **Laplace Smoothing** (α = 0.3):

$$P(w_i \mid c) = \frac{N(w_i, c) + \alpha}{N(c) + \alpha |V|}$$

Di mana:
- $N(w_i, c)$ = jumlah kemunculan kata $w_i$ pada kelas $c$
- $N(c)$ = jumlah total kata pada kelas $c$
- $|V|$ = ukuran vocabulary
- $\alpha = 0.3$ = parameter Laplace smoothing

**Klasifikasi:** $\hat{c} = \arg\max_c \left[\log P(c) + \sum_{i} \log P(w_i \mid c)\right]$

(Digunakan log untuk stabilitas numerik)

### 2.5 Linear SVM (Support Vector Machine)

SVM mencari hyperplane optimal yang memaksimalkan margin antara kelas:

**Primal problem:**
$$\arg\min_{w,b,\xi} \frac{1}{2}\|w\|^2 + C \sum_{i=1}^{n} \xi_i$$

**Subject to:**
$$y_i(w^T x_i + b) \geq 1 - \xi_i, \quad \xi_i \geq 0$$

Di mana:
- $w$ = vektor bobot (normal hyperplane)
- $b$ = bias
- $C$ = parameter regularisasi (C = 0.5 digunakan)
- $\xi_i$ = slack variable untuk data yang tidak dapat dipisahkan linear

**Margin:** $\frac{2}{\|w\|}$ — dimaksimalkan dengan meminimalkan $\|w\|^2$

**Keputusan:** $\hat{y} = \text{sign}(w^T x + b)$

Untuk multi-class (3 kelas), digunakan strategi **One-vs-Rest (OvR)**:
- Tiga binary classifier dilatih: positif vs rest, negatif vs rest, netral vs rest
- Kelas dengan skor keputusan tertinggi dipilih

### 2.6 Porter Stemmer

Porter Stemmer (1980) adalah algoritma rule-based untuk mengubah kata ke bentuk dasarnya melalui serangkaian tahap suffix-stripping:

Tahap 1a: `sses→ss`, `ies→i`, `s→` (jika kondisi terpenuhi)  
Tahap 1b: `eed→ee` (jika m>0), `ed→` / `ing→` (jika ada vokal di stem)  
Tahap 2-5: Suffix penghapusan bertahap dengan kondisi berbasis *measure* m

Di mana *measure* m = jumlah konsonan-vokal-konsonan sequence dalam stem.

---

## BAB III – METODOLOGI

### 3.1 Dataset

| Atribut | Nilai |
|---------|-------|
| Nama | Twitter Climate Change Sentiment Dataset |
| Sumber | Kaggle (Edward Qian, 2022) |
| Jumlah total | 43.943 tweet |
| Label asli | pro (+1), anti (-1), neutral (0), news (2) |
| Label digunakan | positif (+1), negatif (-1), netral (0) |
| Label dibuang | news (2) — 9.276 tweet |
| Jumlah digunakan | 31.907 tweet (setelah cleaning & deduplikasi) |
| Bahasa | Inggris |
| Periode | 2008–2019 |

**Distribusi setelah filtering:**

| Label | Jumlah | Persentase |
|-------|--------|------------|
| Positif (pro) | 18.291 | 57.3% |
| Netral | 7.715 | 24.2% |
| Negatif (anti) | 3.901 | 12.2% |

### 3.2 Alur Preprocessing

#### 3.2.1 Tahap 1 – Text Cleaning

Menghapus elemen non-informatif dari teks:
- URL: `https://t.co/xxx`, `www.xxx`
- @mention: `@username`
- #hashtag: `#ClimateChange`
- HTML entities: `&amp;`, `&lt;`
- Retweet marker: `RT`
- Angka: `2030`, `100%` → dihapus
- Tanda baca & simbol: `!`, `?`, `$`, emoji → dihapus

#### 3.2.2 Tahap 2 – Case Folding

Seluruh teks diubah ke lowercase:  
`"Solar Energy is GREAT"` → `"solar energy is great"`

#### 3.2.3 Tahap 3 – Stopword Removal

Menghapus kata-kata frekuensi tinggi yang tidak membawa makna sentimen (NLTK English stopwords, 127 kata). Beberapa kata negasi seperti *not*, *no*, *never* **dipertahankan** karena relevan untuk sentimen.

#### 3.2.4 Tahap 4 – Stemming (Porter)

Mengubah kata ke bentuk dasar:  
`"changing"` → `"chang"` | `"renewables"` → `"renew"` | `"policies"` → `"polici"`

### 3.3 Ekstraksi Fitur

**TF-IDF Vectorizer** dengan konfigurasi:
- N-gram: (1,2) — unigram dan bigram
- Max features: 15.000
- Min document frequency: 3
- Sublinear TF: False (linear TF)
- Normalisasi: L2

### 3.4 Pembagian Dataset

Split stratified (menjaga proporsi kelas):
- **Data latih:** 80% = 25.525 tweet
- **Data uji:** 20% = 6.382 tweet

Random state = 42 (reproducible)

### 3.5 Training

**Multinomial Naive Bayes:**
- Laplace smoothing: α = 0.3
- Fit pada matriks TF-IDF training

**Linear SVM:**
- Parameter C = 0.5 (regularisasi sedang)
- Class weight: "balanced" (menangani imbalanced dataset)
- Random state = 42

---

## BAB IV – HASIL DAN PEMBAHASAN

### 4.1 Metrik Evaluasi

#### 4.1.1 Accuracy

$$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} = \frac{\text{Jumlah prediksi benar}}{\text{Total sampel uji}}$$

#### 4.1.2 Precision

$$\text{Precision} = \frac{TP}{TP + FP}$$

Proporsi prediksi positif yang benar-benar positif.

#### 4.1.3 Recall (Sensitivity)

$$\text{Recall} = \frac{TP}{TP + FN}$$

Proporsi sampel positif aktual yang berhasil terdeteksi.

#### 4.1.4 F1-Score

$$F1 = \frac{2 \times \text{Precision} \times \text{Recall}}{\text{Precision} + \text{Recall}}$$

Harmonic mean dari precision dan recall.

#### 4.1.5 Macro Average

$$\text{Macro-avg} = \frac{1}{K} \sum_{k=1}^{K} \text{metric}_k$$

Rata-rata sama untuk semua kelas (sensitif terhadap kelas minoritas).

### 4.2 Hasil Evaluasi

#### 4.2.1 Naive Bayes

| Kelas | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Negatif | 0.7976 | 0.3481 | 0.4846 | 770 |
| Netral | 0.6071 | 0.3429 | 0.4383 | 1.496 |
| Positif | 0.7443 | 0.9405 | 0.8310 | 4.116 |
| **Accuracy** | | | **0.7289** | 6.382 |
| Macro avg | 0.7163 | 0.5438 | 0.5846 | 6.382 |
| Weighted avg | 0.7186 | 0.7289 | 0.6971 | 6.382 |

#### 4.2.2 Linear SVM (Model Terbaik)

| Kelas | Precision | Recall | F1-Score | Support |
|-------|-----------|--------|----------|---------|
| Negatif | 0.5766 | 0.6013 | 0.5887 | 770 |
| Netral | 0.5631 | 0.5341 | 0.5482 | 1.496 |
| Positif | 0.8329 | 0.8418 | 0.8374 | 4.116 |
| **Accuracy** | | | **0.7407** | 6.382 |
| Macro avg | 0.6575 | 0.6591 | **0.6581** | 6.382 |
| Weighted avg | 0.7387 | 0.7407 | 0.7396 | 6.382 |

### 4.3 Analisis Perbandingan

| Metrik | Naive Bayes | SVM | Selisih |
|--------|-------------|-----|---------|
| Accuracy | 72.89% | **74.07%** | +1.18% |
| Precision Macro | **71.63%** | 65.75% | -5.88% |
| Recall Macro | 54.38% | **65.91%** | +11.53% |
| F1 Macro | 58.46% | **65.81%** | +7.35% |

**SVM lebih unggul** berdasarkan F1-Score Macro (+7.35%), yang merupakan metrik utama untuk dataset imbalanced. SVM memberikan recall yang jauh lebih baik untuk kelas minoritas (negatif dan netral), menunjukkan kemampuan generalisasi yang superior.

Naive Bayes memiliki precision lebih tinggi tetapi recall sangat rendah pada kelas negatif (34.81%), artinya banyak tweet negatif yang salah diklasifikasikan sebagai positif (bias ke kelas mayoritas).

### 4.4 Distribusi Sentimen Dataset

Berdasarkan analisis terhadap 31.907 tweet:

| Sentimen | Jumlah | Persentase | Interpretasi |
|----------|--------|------------|--------------|
| Positif | 18.291 | 57.3% | Dukungan terhadap aksi iklim & energi hijau |
| Netral | 7.715 | 24.2% | Berita/laporan tanpa opini |
| Negatif | 3.901 | 12.2% | Penolakan/skeptisisme terhadap kebijakan iklim |

**Mayoritas tweet (57.3%) bersifat positif**, mengindikasikan dukungan publik yang signifikan terhadap agenda ekonomi hijau. Sentimen negatif (12.2%) umumnya berasal dari kelompok skeptis iklim dan mereka yang memandang kebijakan hijau merugikan ekonomi.

### 4.5 Kata Kunci Dominan (WordCloud)

**Sentimen Positif:** climate change, renewable energy, solar power, clean energy, green economy, sustainable, wind energy, electric vehicle, carbon neutral, net zero

**Sentimen Netral:** climate change, global warming, temperature, carbon, emissions, report, study, government, policy

**Sentimen Negatif:** climate change, hoax, expensive, jobs, economy, coal, fossil fuels, fraud, alarmist

---

## BAB V – KESIMPULAN DAN SARAN

### 5.1 Kesimpulan

1. **SVM (LinearSVC) adalah model terbaik** dengan accuracy 74.07% dan F1-Score macro 65.81%, unggul dari Naive Bayes dalam semua metrik utama kecuali precision.

2. **Opini publik mayoritas positif (57.3%)** — masyarakat global cenderung mendukung agenda ekonomi hijau dan aksi iklim.

3. **Pipeline TF-IDF (unigram+bigram, 15.000 fitur)** efektif untuk representasi tweet setelah preprocessing komprehensif (cleaning, case folding, stopword removal, stemming).

4. **Ketidakseimbangan dataset** (positif 57% vs negatif 12%) menjadi tantangan utama, diatasi dengan class_weight="balanced" pada SVM.

5. **Model berhasil diekspor ke JSON** dan berjalan offline di browser menggunakan JavaScript murni, memungkinkan deployment statis di Vercel tanpa biaya server.

### 5.2 Saran

1. **Penambahan data negatif dan netral** untuk menyeimbangkan distribusi kelas
2. **Fine-tuning BERT** (khususnya Climate-BERT) untuk hasil yang lebih akurat
3. **Perluasan domain** ke bahasa Indonesia dengan IndoBERT
4. **Pembaruan real-time** menggunakan Twitter API untuk memantau tren sentimen terkini
5. **Analisis temporal** untuk melihat pergeseran sentimen sebelum/sesudah peristiwa iklim besar (COP, IPCC report)

---

## LAMPIRAN

### A. Contoh Hasil Preprocessing

| Tweet Asli | Setelah Cleaning | Setelah Stemming |
|------------|------------------|------------------|
| RT @user: Solar energy is GREAT! #GreenEnergy https://t.co/x | solar energy is great | solar energi great |
| Climate change is a HOAX created by fake scientists 2019 | climate change is a hoax created by fake scientists | climat chang hoax creat fake scientist |
| Government announces new renewable energy targets for 2030 | government announces new renewable energy targets for | govern announc new renew energi target |

### B. Konfigurasi Eksperimen

```python
# TF-IDF
TfidfVectorizer(ngram_range=(1,2), min_df=3, max_features=15000, sublinear_tf=False)

# Naive Bayes
MultinomialNB(alpha=0.3)

# SVM
LinearSVC(C=0.5, class_weight="balanced", random_state=42)

# Split
train_test_split(test_size=0.2, random_state=42, stratify=y)
```

### C. Rumus Lengkap Porter Stemmer (Step 1a-5)

| Step | Kondisi | Suffix → Replacement |
|------|---------|----------------------|
| 1a | - | sses→ss, ies→i, [^s]s→ε |
| 1b | m>0 | eed→ee |
| 1b | has vowel | ed→ε, ing→ε, then: at→ate, bl→ble, iz→ize |
| 1c | has vowel | y→i |
| 2 | m>0 | ational→ate, tional→tion, ... |
| 3 | m>0 | icate→ic, ative→ε, alize→al, ... |
| 4 | m>1 | al, ance, ence, er, ic, able, ible, ant, ... → ε |
| 5a | m>1 | e→ε |
| 5b | m>1 and not (*o) | ll→l |

---

*Laporan ini disusun sebagai bagian dari proyek analisis sentimen ekonomi hijau. Dataset: Twitter Climate Change Sentiment Dataset (Kaggle, Edward Qian). Kode sumber tersedia di GitHub.*
