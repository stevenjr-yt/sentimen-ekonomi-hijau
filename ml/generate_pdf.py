"""Generator PDF Komprehensif dan Lengkap untuk Proyek SentimentGreen.

Menghasilkan 3 Dokumen PDF Standar Akademik & Laporan Proyek:
1. Laporan_Project.pdf - Laporan Teknis Lengkap (~10-12 Halaman)
   Mencakup Bab I Pendahuluan & Latar Belakang, Bab II Tinjauan Pustaka & Rumus Lengkap,
   Bab III Metodologi & Preprocessing Pipeline, Bab IV Hasil Evaluasi & Visualisasi,
   Bab V Analisis Komparasi, Bab VI Kesimpulan & Rekomendasi.
2. Paper_Jurnal.pdf - Publikasi Format Jurnal Ilmiah (~6-8 Halaman)
3. Studi_Literatur.pdf - Systematic Literature Review (~6-7 Halaman)
"""
import pathlib
import json
import csv
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable, PageBreak,
                                 Image as RLImage, KeepTogether)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT

ROOT = pathlib.Path(__file__).resolve().parent.parent
DL = ROOT / "web" / "downloads"
DL.mkdir(parents=True, exist_ok=True)
DOCS_PDF = ROOT / "docs" / "pdf"
DOCS_PDF.mkdir(parents=True, exist_ok=True)
RESULTS = ROOT / "results"
DATA_DIR = ROOT / "data"

GREEN       = colors.HexColor("#059669")
GREEN_LIGHT = colors.HexColor("#34d399")
DARK        = colors.HexColor("#064e3b")
GRAY        = colors.HexColor("#64748b")
BG_LIGHT    = colors.HexColor("#f0fdf4")
BG_GRAY     = colors.HexColor("#f8fafc")
BORDER      = colors.HexColor("#cbd5e1")

def make_styles():
    s = getSampleStyleSheet()
    base = dict(fontName="Helvetica", fontSize=9.5, leading=14.5, textColor=colors.HexColor("#1e293b"))

    return {
        "title": ParagraphStyle("title", **{**base, "fontName": "Helvetica-Bold",
            "fontSize": 19, "leading": 24, "textColor": DARK, "alignment": TA_CENTER, "spaceAfter": 8}),
        "subtitle": ParagraphStyle("subtitle", **{**base, "fontName": "Helvetica",
            "fontSize": 12, "leading": 16, "textColor": GREEN, "alignment": TA_CENTER, "spaceAfter": 6}),
        "meta": ParagraphStyle("meta", **{**base, "fontSize": 8.5, "leading": 13, "textColor": GRAY, "alignment": TA_CENTER}),
        "h1": ParagraphStyle("h1", **{**base, "fontName": "Helvetica-Bold",
            "fontSize": 15, "leading": 20, "textColor": DARK,
            "spaceAfter": 8, "spaceBefore": 14}),
        "h2": ParagraphStyle("h2", **{**base, "fontName": "Helvetica-Bold",
            "fontSize": 12.5, "leading": 17, "textColor": DARK,
            "spaceAfter": 6, "spaceBefore": 12}),
        "h3": ParagraphStyle("h3", **{**base, "fontName": "Helvetica-Bold",
            "fontSize": 10.5, "leading": 15, "textColor": GREEN,
            "spaceAfter": 4, "spaceBefore": 9}),
        "body": ParagraphStyle("body", **{**base, "spaceAfter": 5, "alignment": TA_JUSTIFY}),
        "body_bold": ParagraphStyle("body_bold", **{**base, "fontName": "Helvetica-Bold", "spaceAfter": 5}),
        "formula": ParagraphStyle("formula", **{**base, "fontName": "Courier-Bold",
            "fontSize": 9, "leading": 13, "backColor": BG_LIGHT,
            "leftIndent": 15, "rightIndent": 15, "spaceAfter": 6, "spaceBefore": 4}),
        "code": ParagraphStyle("code", **{**base, "fontName": "Courier",
            "fontSize": 8, "leading": 11, "backColor": BG_GRAY,
            "leftIndent": 12, "rightIndent": 12, "spaceAfter": 6, "spaceBefore": 3}),
        "center": ParagraphStyle("center", **{**base, "alignment": TA_CENTER, "textColor": GRAY, "fontSize": 8.5}),
        "caption": ParagraphStyle("caption", **{**base, "alignment": TA_CENTER, "textColor": GRAY, "fontSize": 8, "fontName": "Helvetica-Oblique", "spaceAfter": 8}),
        "bullet": ParagraphStyle("bullet", **{**base, "leftIndent": 16, "spaceAfter": 3, "bulletIndent": 6}),
        "table_h": ParagraphStyle("table_h", **{**base, "fontName": "Helvetica-Bold", "fontSize": 8.5, "leading": 11, "textColor": colors.white, "alignment": TA_CENTER}),
        "table_c": ParagraphStyle("table_c", **{**base, "fontSize": 8.5, "leading": 11, "alignment": TA_CENTER}),
        "table_l": ParagraphStyle("table_l", **{**base, "fontSize": 8.5, "leading": 11}),
        "table_code": ParagraphStyle("table_code", **{**base, "fontName": "Courier", "fontSize": 7.5, "leading": 9.5}),
    }

def hr():
    return HRFlowable(width="100%", thickness=1, color=BORDER, spaceAfter=8, spaceBefore=8)

def table_style():
    return TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 8.5),
        ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('GRID',       (0,0), (-1,-1), 0.5, BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_GRAY]),
        ('FONTSIZE',   (0,1), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 5),
        ('RIGHTPADDING',  (0,0), (-1,-1), 5),
    ])

def safe_table(data_rows, col_widths, S, align_center_cols=None, code_cols=None):
    if align_center_cols is None: align_center_cols = set()
    if code_cols is None: code_cols = set()
    table_content = []
    for row_idx, row in enumerate(data_rows):
        row_cells = []
        for col_idx, cell in enumerate(row):
            if isinstance(cell, Paragraph):
                row_cells.append(cell)
            else:
                if row_idx == 0:
                    style = S["table_h"]
                elif col_idx in code_cols:
                    style = S["table_code"]
                elif col_idx in align_center_cols:
                    style = S["table_c"]
                else:
                    style = S["table_l"]
                row_cells.append(Paragraph(str(cell), style))
        table_content.append(row_cells)
    t = Table(table_content, colWidths=col_widths)
    t.setStyle(table_style())
    return t

# ─────────────────────────────────────────────────────────────────────────────
# 1. LAPORAN PROYEK LENGKAP (LAPORAN AKHIR SAINS DATA)
# ─────────────────────────────────────────────────────────────────────────────
def build_laporan():
    doc = SimpleDocTemplate(str(DL / "Laporan_Project.pdf"), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = make_styles()
    story = []

    # COVER & HEADER
    story += [
        Spacer(1, 0.5*cm),
        Paragraph("LAPORAN AKHIR PROYEK SAINS DATA", S["title"]),
        Paragraph("ANALISIS SENTIMEN OPINI PUBLIK TERHADAP ISU EKONOMI HIJAU DAN PERUBAHAN IKLIM MENGGUNAKAN TF-IDF, MULTINOMIAL NAIVE BAYES, DAN LINEAR SUPPORT VECTOR MACHINE", S["subtitle"]),
        hr(),
        Paragraph("<b>Disusun oleh:</b> SteVenJr | <b>Program Studi:</b> Teknik Informatika / Sains Data", S["meta"]),
        Paragraph("<b>Dataset:</b> Twitter Climate Change Sentiment Dataset (Kaggle: Edward Qian, 2022)", S["meta"]),
        Paragraph("<b>Repositori Kode & Data:</b> github.com/stevenjr-yt/sentimen-ekonomi-hijau", S["meta"]),
        Paragraph("<b>Aplikasi Web Interaktif:</b> https://sentimentgreen.vercel.app | <b>Tahun:</b> 2024", S["meta"]),
        Spacer(1, 0.4*cm),
    ]

    # RINGKASAN EKSEKUTIF
    story += [
        Paragraph("RINGKASAN EKSEKUTIF", S["h2"]),
        Paragraph("""Laporan ini menyajikan dokumentasi menyeluruh dari perancangan, eksperimentasi, evaluasi, dan implementasi sistem analisis sentimen terhadap opini publik terkait isu ekonomi hijau dan perubahan iklim pada media sosial Twitter. Proyek <b>SentimentGreen</b> memanfaatkan dataset riil sebanyak 43.943 tweet mentah dari Kaggle. Setelah proses penyaringan kelas news dan deduplikasi ketat, diperoleh 31.907 sampel valid (20.580 sentimen positif, 7.478 netral, dan 3.849 negatif). Pipeline preprocessing komprehensif dibangun meliputi pembersihan noise (cleaning), case folding, stopword removal dengan preservasi kata negasi, serta Porter stemming. Fitur diekstrak menggunakan TF-IDF unigram-bigram berdimensi 15.000 fitur. Model Linear Support Vector Machine (SVM) dengan pembobotan kelas seimbang berhasil mengungguli Multinomial Naive Bayes (MNB) dengan akurasi 74,07% berbanding 72,89% dan F1-Score makro 65,81% berbanding 58,46%. Keunggulan paling menonjol tampak pada recall kelas minoritas negatif yang mencapai 60,13% pada SVM berbanding hanya 34,81% pada MNB. Model akhir diekspor ke dalam bobot JSON murni sehingga inferensi dapat berjalan 100% offline di browser pengguna tanpa kebutuhan server komputasi aktif.""", S["body"]),
        hr(),
    ]

    # BAB I: PENDAHULUAN
    story += [
        Paragraph("BAB I – PENDAHULUAN", S["h1"]),
        Paragraph("1.1 Latar Belakang Masalah", S["h2"]),
        Paragraph("""Perubahan iklim global merupakan salah satu tantangan eksistensial terbesar peradaban modern. Berdasarkan laporan Intergovernmental Panel on Climate Change (IPCC AR6, 2023), emisi gas rumah kaca global harus ditekan sebesar 43% sebelum tahun 2030 agar ambang batas kenaikan suhu rata-rata permukaan bumi tidak melampaui 1,5°C di atas tingkat pra-industri. Dalam menjawab krisis ini, masyarakat global merumuskan transisi menuju <i>green economy</i> (ekonomi hijau)—suatu model pembangunan sosio-ekonomi yang memprioritaskan energi terbarukan, transportasi nol emisi, elektrifikasi massal, instrumen pasar karbon, dan efisiensi sumber daya lingkungan (UNEP, 2011).""", S["body"]),
        Paragraph("""Meskipun secara konseptual didukung oleh konsensus ilmiah internasional, implementasi kebijakan ekonomi hijau di lapangan senantiasa menghadapi tantangan polarisasi opini masyarakat. Biaya awal transisi energi, perubahan gaya hidup, subsidi kendaraan listrik, dan penutupan industri bahan bakar fosil kerap memicu resistensi, skeptisisme, atau kekhawatiran ekonomi di kalangan publik. Media sosial, khususnya Twitter/X, telah menjadi panggung utama diskursus publik di mana jutaan opini, kritik, dan sentimen masyarakat diartikulasikan secara spontan setiap harinya.""", S["body"]),
        Paragraph("""Analisis sentimen berbasis komputasi (NLP) menjadi instrumen krusial dalam memonitor penerimaan publik secara kuantitatif, obyektif, dan real-time. Melalui pemahaman mendalam tentang pola opini masyarakat, para pembuat kebijakan, peneliti lingkungan, dan pelaku industri dapat merancang strategi komunikasi yang tepat sasaran, mengatasi kesalahpahaman informasi iklim, serta mengakselerasi implementasi program keberlanjutan.""", S["body"]),

        Paragraph("1.2 Rumusan Masalah", S["h2"]),
        Paragraph("1. Bagaimana karakteristik, asal usul (provenance), dan distribusi sentimen publik terhadap isu iklim dan ekonomi hijau pada platform Twitter?", S["bullet"]),
        Paragraph("2. Bagaimana alur preprocessing teks yang sistematis dan konsisten untuk membersihkan noise informal khas Twitter tanpa merusak makna sentimen?", S["bullet"]),
        Paragraph("3. Bagaimana formulasi matematis dan komparasi performa antara algoritma Multinomial Naive Bayes dan Linear SVM pada dataset imbalanced?", S["bullet"]),
        Paragraph("4. Mengapa Support Vector Machine menghasilkan F1-Score makro yang lebih superior dalam mendeteksi kelas minoritas (negatif & netral)?", S["bullet"]),
        Paragraph("5. Bagaimana mengarsiteki model machine learning agar dapat berjalan sepenuhnya offline di sisi client browser tanpa ketergantungan server?", S["bullet"]),

        Paragraph("1.3 Tujuan Proyek", S["h2"]),
        Paragraph("1. Mengumpulkan, mendokumentasikan, dan memproses 43.943 tweet mentah dari Twitter Climate Change Sentiment Dataset.", S["bullet"]),
        Paragraph("2. Mengembangkan pipeline text preprocessing Python dan JavaScript yang identik untuk menjamin konsistensi inferensi.", S["bullet"]),
        Paragraph("3. Membangun representasi ruang fitur TF-IDF unigram-bigram berdimensi 15.000 kata dengan normalisasi L2.", S["bullet"]),
        Paragraph("4. Melatih, mengoptimasi, dan mengevaluasi model Naive Bayes dan SVM menggunakan stratified 5-fold / 80:20 train-test split.", S["bullet"]),
        Paragraph("5. Menyajikan visualisasi WordCloud, matriks konfusi, dan dasbor web interaktif yang dapat diakses publik secara bebas.", S["bullet"]),

        Paragraph("1.4 Manfaat Penelitian", S["h2"]),
        Paragraph("• <b>Manfaat Akademis:</b> Menyediakan rujukan metodologis komparasi NLP klasik pada domain ekonomi hijau serta studi literatur komparatif publikasi 2024.", S["bullet"]),
        Paragraph("• <b>Manfaat Praktis:</b> Menghasilkan sistem pemantauan sentimen tanpa biaya server operasional yang siap pakai untuk pemangku kepentingan.", S["bullet"]),
        Paragraph("• <b>Manfaat Terbuka (Open Science):</b> Membuka seluruh dataset, script training, visualisasi metrik, dan dokumen PDF untuk verifikasi publik.", S["bullet"]),
    ]

    # BAB II: LANDASAN TEORI & RUMUS LENGKAP
    story += [
        PageBreak(),
        Paragraph("BAB II – TINJAUAN PUSTAKA DAN LANDASAN TEORI", S["h1"]),
        Paragraph("2.1 Konsep Ekonomi Hijau (Green Economy)", S["h2"]),
        Paragraph("""United Nations Environment Programme (UNEP, 2011) mendefinisikan ekonomi hijau sebagai sistem perekonomian yang menghasilkan peningkatan kesejahteraan manusia dan keadilan sosial, sekaligus secara signifikan mereduksi risiko degradasi lingkungan dan kelangkaan ekologis. Pilar ekonomi hijau meliputi energi surya dan angin, efisiensi energi bangunan, transportasi listrik dan hidrogen, pengelolaan limbah sirkular, serta pembiayaan hijau (green bonds).""", S["body"]),

        Paragraph("2.2 Formulasi Representasi Teks: TF-IDF", S["h2"]),
        Paragraph("""Term Frequency-Inverse Document Frequency (TF-IDF) merupakan metode pembobotan statistik yang mengukur signifikansi relatif sebuah term (kata) $t$ dalam suatu dokumen $d$ terhadap seluruh kumpulan korpus dokumen $D$ (Salton & Buckley, 1988).""", S["body"]),
        Paragraph("<b>1. Term Frequency (TF):</b> Mengukur frekuensi kemunculan term $t$ dalam dokumen $d$ ternormalisasi panjang dokumen:", S["body"]),
        Paragraph("TF(t, d) = f(t, d) / [ Σ_{t' in d} f(t', d) ]", S["formula"]),
        Paragraph("di mana $f(t, d)$ melambangkan frekuensi kemunculan kata $t$ pada dokumen $d$.", S["body"]),
        Paragraph("<b>2. Inverse Document Frequency (IDF):</b> Mengukur keunikan informasi term $t$ di seluruh korpus $N$ dokumen:", S["body"]),
        Paragraph("IDF(t) = log_e [ (1 + N) / (1 + df(t)) ] + 1", S["formula"]),
        Paragraph("di mana $N$ adalah jumlah total dokumen korpus dan $df(t)$ adalah document frequency (jumlah dokumen yang memuat term $t$). Penambahan konstanta $1$ berfungsi sebagai smoothing pencegah division-by-zero.", S["body"]),
        Paragraph("<b>3. Bobot TF-IDF Mentah:</b>", S["body"]),
        Paragraph("TF-IDF(t, d) = TF(t, d) * IDF(t)", S["formula"]),
        Paragraph("<b>4. Normalisasi Euclidean (L2 Norm):</b> Menghilangkan distorsi akibat perbedaan panjang dokumen tweet:", S["body"]),
        Paragraph("v_norm = v / ||v||_2 = v / sqrt[ Σ_{i=1}^{M} (v_i)^2 ]", S["formula"]),

        Paragraph("2.3 Teori dan Formulasi Multinomial Naive Bayes (MNB)", S["h2"]),
        Paragraph("""Multinomial Naive Bayes diturunkan dari Teorema Bayes dengan asumsi independensi bersyarat antar fitur (kata) terhadap kelas sentimen $c$ (McCallum & Nigam, 1998):""", S["body"]),
        Paragraph("P(c | d) = [ P(c) * P(d | c) ] / P(d) = [ P(c) * Π_{i=1}^{n} P(w_i | c) ] / P(d)", S["formula"]),
        Paragraph("""Untuk mencegah persoalan *zero-frequency problem* (probabilitas nol ketika sebuah kata dalam data uji tidak pernah muncul pada kelas $c$ data latih), diterapkan <b>Laplace / Lidstone Smoothing</b> dengan parameter α = 0.3:""", S["body"]),
        Paragraph("P(w_i | c) = [ N_{w_i, c} + α ] / [ N_c + α * |V| ]", S["formula"]),
        Paragraph("""di mana $N_{w_i, c}$ adalah akumulasi bobot kata $w_i$ pada kelas $c$, $N_c$ adalah total bobot seluruh kata pada kelas $c$, dan $|V|$ adalah ukuran leksikon (15.000 fitur).""", S["body"]),
        Paragraph("Fungsi keputusan klasifikasi dihitung dalam domain logaritma untuk menghindari *underflow numerik* desimal kecil:", S["body"]),
        Paragraph("c_pred = argmax_{c in C} [ log P(c) + Σ_{i=1}^{n} log P(w_i | c) ]", S["formula"]),

        Paragraph("2.4 Teori dan Formulasi Linear Support Vector Machine (Linear SVM)", S["h2"]),
        Paragraph("""Support Vector Machine (Vapnik, 1995; Cortes & Vapnik, 1995) merupakan algoritma pembelajaran terawasi berprinsip <i>Structural Risk Minimization</i>. Pada ruang berdimensi tinggi ($R^{15.000}$), SVM mencari bidang pemisah (hyperplane optimal) yang memisahkan kelas-kelas sentimen dengan jarak batas (margin) terbesar:""", S["body"]),
        Paragraph("Hyperplane: w^T * x + b = 0", S["formula"]),
        Paragraph("Jarak margin geometric antar kelas didefinisikan sebesar <b>2 / ||w||</b>. Memaksimalkan margin ekuivalen dengan meminimalkan norma kuadratik <b>(1/2) * ||w||^2</b>.", S["body"]),
        Paragraph("<b>Formulasi Soft-Margin Primal Optimization (dengan Regularisasi C):</b>", S["body"]),
        Paragraph("min_{w, b, ξ} [ (1/2) * ||w||^2 + C * Σ_{i=1}^{N} W_{y_i} * ξ_i ]", S["formula"]),
        Paragraph("dengan batasan konstrain ketat:", S["body"]),
        Paragraph("y_i * ( w^T * x_i + b ) >= 1 - ξ_i,   di mana ξ_i >= 0  (∀ i = 1, ..., N)", S["formula"]),
        Paragraph("""di mana:
• $w$ = vektor bobot normal hyperplane.
• $b$ = nilai bias offset pemisah.
• $C$ = parameter penalti trade-off antara lebar margin dan kesalahan klasifikasi ($C = 0.5$ terpilih).
• $xi_i$ = slack variable yang mengizinkan sampel tertentu melanggar margin jika data tidak terpisah linear murni.
• $W_{y_i}$ = bobot penyeimbang kelas (balanced class weighting):""", S["body"]),
        Paragraph("W_c = N_total / [ K * N_c ]", S["formula"]),
        Paragraph("di mana $K=3$ kelas. Bobot ini memberikan penalti kesalahan lebih berat pada kelas minoritas (negatif dan netral), secara signifikan mengatasi persoalan ketidakseimbangan sampel.", S["body"]),
        Paragraph("Untuk klasifikasi 3-kelas, diterapkan strategi <b>One-vs-Rest (OvR)</b> dengan keputusan:", S["body"]),
        Paragraph("c_pred = argmax_{c in {neg, net, pos}} [ w_c^T * x + b_c ]", S["formula"]),

        Paragraph("2.5 Algoritma Reduksi Morfologi: Porter Stemmer", S["h2"]),
        Paragraph("""Porter Stemming (Porter, 1980) mereduksi variasi infleksi kata ke bentuk stem dasarnya melalui 5 tahapan aturan berbasis pola konsonan-vokal sequence:
• Tahap 1a: Penghapusan jamak plural (contoh: <code>policies</code> → <code>polici</code>, <code>asses</code> → <code>ass</code>).
• Tahap 1b: Reduksi past tense & progresif participle (contoh: <code>warming</code> → <code>warm</code>, <code>changed</code> → <code>chang</code>).
• Tahap 2-4: Reduksi derivasi sufiks (contoh: <code>sustainable</code> → <code>sustain</code>, <code>environmental</code> → <code>environ</code>).
• Tahap 5: Pembersihan huruf konsonan ganda di akhir kata.""", S["body"]),
    ]

    # BAB III: METODOLOGI & PIPELINE DARI AWAL
    story += [
        PageBreak(),
        Paragraph("BAB III – METODOLOGI DAN PERJALANAN DATA", S["h1"]),
        Paragraph("3.1 Asal-usul Data (Data Provenance & Ingestion)", S["h2"]),
        Paragraph("""Dataset primer diunduh langsung dari repositori Kaggle melalui skrip otomatis <code>ml/download_data.py</code>. Dataset dikurasi oleh Edward Qian (2022) dengan nama resmi <b>Twitter Climate Change Sentiment Dataset</b>, berukuran 6.3 MB dalam format CSV berstruktur:""", S["body"]),
    ]

    tbl_dataset_spec = [
        ["Atribut Dataset", "Spesifikasi dan Nilai Riil"],
        ["Nama Dataset", "Twitter Climate Change Sentiment Dataset"],
        ["Sumber Penyedia", "Kaggle (Edward Qian, 2022: edqian/twitter-climate-change-sentiment-dataset)"],
        ["Jalur File Lokal", "data/twitter_sentiment_data.csv (Ukuran: 6.304.752 bytes)"],
        ["Rentang Temporal Data", "Tahun 2008 hingga 2019 (percakapan global Twitter/X)"],
        ["Total Data Mentah", "43.943 baris tweet teranotasi"],
        ["Skema Kolom Asli", "sentiment (integer: -1, 0, 1, 2), message (string teks), tweetid (string)"],
        ["Label Asli Kaggle", "-1: Anti-Climate Change | 0: Neutral | 1: Pro-Climate Change | 2: News"],
        ["Kebijakan Filtering", "Label 'News' (2) berjumlah 9.276 baris dieliminasi; deduplikasi teks membersihkan 2.760 duplikat"],
        ["Jumlah Sampel Akhir", "31.907 tweet bersih siap ekstraksi fitur"],
    ]
    story += [safe_table(tbl_dataset_spec, [5*cm, 12*cm], S), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("3.2 Distribusi Data Hasil Filtering dan Pembagian Stratified", S["h2"]),
        Paragraph("""Sebanyak 31.907 sampel dibagi menjadi 80% Data Latih (25.525 sampel) dan 20% Data Uji (6.382 sampel) dengan teknik stratified splitting acak (random_state=42):""", S["body"]),
    ]

    tbl_split_detail = [
        ["Kelas Sentimen", "Label", "Total Sampel", "Persentase", "Data Latih (80%)", "Data Uji (20%)", "Karakter Makna Tweet"],
        ["Positif (Pro)", "+1", "20.580", "64,50%", "16.464", "4.116", "Dukungan energi bersih, mitigasi iklim, kesadaran emisi"],
        ["Netral (Neutral)", "0", "7.478", "23,44%", "5.982", "1.496", "Laporan umum, pertanyaan, fakta iklim tanpa sentimen"],
        ["Negatif (Anti)", "-1", "3.849", "12,06%", "3.079", "770", "Skeptisisme iklim, keluhan biaya pajak, hoaks iklim"],
        ["Total Korpus", "-", "31.907", "100,00%", "25.525", "6.382", "Ukuran Leksikon Bersih: 14.893 kata unik"],
    ]
    story += [safe_table(tbl_split_detail, [2.8*cm, 1.2*cm, 2.2*cm, 2*cm, 2.6*cm, 2.4*cm, 3.8*cm], S, align_center_cols={1,2,3,4,5}), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("3.3 Tahapan Detail Pipeline Preprocessing (Dari Mentah ke Vektor)", S["h2"]),
        Paragraph("""Setiap teks mentah melewati 5 filter komputasi berurutan di modul <code>ml/preprocess.py</code> (Python) dan direplikasi secara bit-identik di <code>web/preprocess.js</code> (JavaScript browser):""", S["body"]),
        Paragraph("<b>1. Cleaning RegEx:</b> Menghapus URL (`https?://\\S+|www\\.\\S+`), mention (`@\\w+`), hashtag (`#\\w+`), HTML entities (`&amp;`, `&gt;`), angka desimal/tahun, dan tanda baca.", S["bullet"]),
        Paragraph("<b>2. Case Folding:</b> Mengonversi seluruh aksara menjadi huruf kecil (lowercase).", S["bullet"]),
        Paragraph("<b>3. Tokenisasi:</b> Memecah untaian teks menjadi daftar token kata tunggal berbasis spasi.", S["bullet"]),
        Paragraph("<b>4. Selective Stopword Removal:</b> Menghapus 127 stopword umum NLTK bahasa Inggris namun mempertahankan kata penentu sentimen seperti <i>not, no, never, without, against</i>.", S["bullet"]),
        Paragraph("<b>5. Morphological Stemming:</b> Mereduksi setiap token menggunakan Porter Stemmer.", S["bullet"]),
        Spacer(1, 0.2*cm),
        Paragraph("Tabel 3.3 Sampel Transformasi Riil Teks Tweet pada Dataset Proyek:", S["h3"]),
    ]

    tbl_samples_clean = [
        ["Tweet Mentah Asli dari Kaggle", "Hasil Pipeline Preprocessing", "Label"],
        ["@tiniebeany climate change is an interesting hustle as it was global warming but the planet stopped warming for 15 yes while the suv boom",
         "climat chang interest hustl global warm planet stop warm ye suv boom", "Negatif (-1)"],
        ["RT @NatGeoChannel: Watch #BeforeTheFlood right here, as @LeoDiCaprio travels the world to tackle climate change https://t.co/LkDehj3tNn",
         "watch right travel world tackl climat chang htt", "Positif (+1)"],
        ["Unamshow awache kujinga na iko global warming https://t.co/mhIflU7M1X",
         "unamshow awach kujinga na iko global warm", "Netral (0)"],
        ["Now's the time: we need a strong #FTT that works for those hardest hit by climate change and poverty!",
         "time need strong work hardest hit climat chang poverti", "Positif (+1)"],
        ["Bangladesh did not cause climate change, so the country does not need 'aid'; instead it needs compensation!",
         "bangladesh not caus climat chang countri not need aid instead need compens", "Positif (+1)"],
    ]
    story += [safe_table(tbl_samples_clean, [6.5*cm, 8.5*cm, 2*cm], S, align_center_cols={2}), Spacer(1, 0.4*cm)]

    # BAB IV: HASIL EVALUASI & VISUALISASI
    story += [
        PageBreak(),
        Paragraph("BAB IV – HASIL EVALUASI, METRIK, DAN VISUALISASI", S["h1"]),
        Paragraph("4.1 Perbandingan Kinerja Menyeluruh pada Data Uji (6.382 Tweet)", S["h2"]),
        Paragraph("""Model diuji secara ketat pada 6.382 tweet yang tidak pernah dilihat sebelumnya selama proses pelatihan. Evaluasi menggunakan metrik Macro-Averaged karena distribusi data yang imbalanced:""", S["body"]),
    ]

    tbl_eval_summary = [
        ["Algoritma Model", "Akurasi", "Precision (Macro)", "Recall (Macro)", "F1-Score (Macro)", "Precision (Weighted)", "Recall (Weighted)", "F1-Score (Weighted)"],
        ["Multinomial Naive Bayes", "72,89%", "71,63%", "54,38%", "58,46%", "71,86%", "72,89%", "69,71%"],
        ["Linear SVM (Terbaik)", "74,07%", "65,75%", "65,91%", "65,81%", "73,87%", "74,07%", "73,96%"],
        ["Selisih Performa (SVM - MNB)", "+1,18%", "-5,88%", "+11,53%", "+7,35%", "+2,01%", "+1,18%", "+4,25%"],
    ]
    story += [safe_table(tbl_eval_summary, [4.2*cm, 1.8*cm, 2.1*cm, 2*cm, 2.1*cm, 2.1*cm, 1.9*cm, 2*cm], S, align_center_cols={1,2,3,4,5,6,7}), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("4.2 Rincian Kinerja per Kelas Sentimen", S["h2"]),
    ]

    tbl_per_class_comp = [
        ["Model Evaluasi", "Kelas Sentimen", "Precision", "Recall", "F1-Score", "Jumlah Sampel Uji (Support)"],
        ["Multinomial Naive Bayes", "Negatif (-1)", "79,76%", "34,81% (COLLAPSE)", "48,46%", "770 tweet"],
        ["Multinomial Naive Bayes", "Netral (0)", "60,71%", "34,29%", "43,83%", "1.496 tweet"],
        ["Multinomial Naive Bayes", "Positif (+1)", "74,43%", "94,05%", "83,10%", "4.116 tweet"],
        ["Linear SVM (Balanced)", "Negatif (-1)", "57,66%", "60,13% (+25,32%)", "58,87%", "770 tweet"],
        ["Linear SVM (Balanced)", "Netral (0)", "56,31%", "53,41% (+19,12%)", "54,82%", "1.496 tweet"],
        ["Linear SVM (Balanced)", "Positif (+1)", "83,29%", "84,18%", "83,74%", "4.116 tweet"],
    ]
    story += [safe_table(tbl_per_class_comp, [4*cm, 2.5*cm, 2.5*cm, 3.2*cm, 2.2*cm, 2.6*cm], S, align_center_cols={2,3,4,5}), Spacer(1, 0.4*cm)]

    # GAMBAR VISUALISASI
    story += [
        Paragraph("4.3 Visualisasi Metrik Evaluasi dan Matriks Konfusi", S["h2"]),
        Paragraph("""Berikut disajikan visualisasi grafik kinerja model dan matriks konfusi riil yang dihasilkan dari data evaluasi:""", S["body"]),
    ]

    if (RESULTS / "perbandingan_model.png").exists():
        story += [
            RLImage(str(RESULTS / "perbandingan_model.png"), width=15*cm, height=6.8*cm),
            Paragraph("Gambar 4.1 Perbandingan Metrik Evaluasi: Naive Bayes vs Linear SVM", S["caption"]),
            Spacer(1, 0.2*cm),
        ]

    cm_row = []
    if (RESULTS / "cm_svm.png").exists():
        cm_row.append([
            RLImage(str(RESULTS / "cm_svm.png"), width=8*cm, height=6*cm),
            RLImage(str(RESULTS / "cm_naive_bayes.png"), width=8*cm, height=6*cm) if (RESULTS / "cm_naive_bayes.png").exists() else Paragraph("", S["body"])
        ])
        t_cm = Table(cm_row, colWidths=[8.5*cm, 8.5*cm])
        t_cm.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story += [t_cm, Paragraph("Gambar 4.2 Matriks Konfusi (Kiri: Linear SVM, Kanan: Multinomial Naive Bayes)", S["caption"]), Spacer(1, 0.3*cm)]

    if (RESULTS / "pie_sentimen.png").exists():
        story += [
            RLImage(str(RESULTS / "pie_sentimen.png"), width=11.5*cm, height=6.2*cm),
            Paragraph("Gambar 4.3 Proporsi Distribusi Sentimen Publik terhadap Isu Iklim", S["caption"]),
            Spacer(1, 0.3*cm),
        ]

    # WORDCLOUD VISUALISASI
    story += [
        PageBreak(),
        Paragraph("4.4 Analisis Leksikon Kata Dominan (WordCloud)", S["h2"]),
        Paragraph("""Analisis leksikon memperlihatkan perbedaan karakteristik semantik yang sangat tegas di antara ketiga kategori sentimen:""", S["body"]),
    ]

    wc_rows = []
    if (RESULTS / "wordcloud_positif.png").exists() and (RESULTS / "wordcloud_negatif.png").exists():
        wc_rows.append([
            RLImage(str(RESULTS / "wordcloud_positif.png"), width=8*cm, height=5.5*cm),
            RLImage(str(RESULTS / "wordcloud_negatif.png"), width=8*cm, height=5.5*cm)
        ])
        t_wc = Table(wc_rows, colWidths=[8.5*cm, 8.5*cm])
        t_wc.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))
        story += [t_wc, Paragraph("Gambar 4.4 WordCloud Leksikon (Kiri: Kelas Positif, Kanan: Kelas Negatif)", S["caption"]), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("• <b>Sentimen Positif (Pro-Climate):</b> Didominasi oleh istilah solutif dan aksi nyata seperti <i>action, renewable, solar, wind, fight, tackle, clean, solution, paris agreement</i>.", S["bullet"]),
        Paragraph("• <b>Sentimen Negatif (Anti/Skeptis):</b> Didominasi oleh retorika penolakan dan keraguan ekonomi seperti <i>hoax, fake, tax, cost, job, money, scam, alarmist, politician</i>.", S["bullet"]),
        Paragraph("• <b>Sentimen Netral:</b> Berisi istilah pelaporan fakta ilmiah dan berita netral seperti <i>report, global, scientist, study, temperature, degree, arctic</i>.", S["bullet"]),
    ]

    # BAB V: KESIMPULAN & REKOMENDASI
    story += [
        Spacer(1, 0.4*cm),
        Paragraph("BAB V – KESIMPULAN DAN REKOMENDASI PENGEMBANGAN", S["h1"]),
        Paragraph("5.1 Kesimpulan Teknis", S["h2"]),
        Paragraph("1. <b>Keunggulan Linear SVM:</b> Linear SVM terbukti sebagai arsitektur model paling optimal untuk domain teks tweet imbalanced dengan capaian akurasi 74,07% dan F1-Score makro 65,81%. Penerapan pembobotan kelas seimbang (class_weight='balanced') berhasil mengatasi kelemahan klasik Naive Bayes yang mengalami <i>recall collapse</i> pada kelas negatif.", S["bullet"]),
        Paragraph("2. <b>Dukungan Publik Dominan:</b> Mayoritas opini publik di media sosial Twitter (64,50%) menyatakan dukungan positif terhadap aksi mitigasi iklim dan ekonomi hijau, sementara resistensi skeptis berada pada kisaran 12,06%.", S["bullet"]),
        Paragraph("3. <b>Efisiensi Ekstraksi TF-IDF:</b> Skema n-gram (1,2) dengan 15.000 fitur teratas dan normalisasi L2 terbukti cukup padat untuk menangkap frasa penting (seperti <i>climate change</i>, <i>renewable energy</i>) tanpa menimbulkan beban komputasi berlebih.", S["bullet"]),
        Paragraph("4. <b>Inovasi Zero-Server Browser Inference:</b> Model berhasil diserialisasi menjadi format JSON mandiri berukuran <2 MB, memungkinkan eksekusi klasifikasi instan di sisi peramban web tanpa biaya server backend sama sekali.", S["bullet"]),

        Paragraph("5.2 Rekomendasi Penelitian Masa Depan", S["h2"]),
        Paragraph("1. Perluasan anotasi dataset bahasa Indonesia untuk menganalisis opini masyarakat lokal secara lebih representatif.", S["bullet"]),
        Paragraph("2. Eksplorasi model transformer terkompresi (ONNX / WebAssembly) seperti TinyBERT atau ClimateBERT untuk meningkatkan akurasi semantik frasa majemuk.", S["bullet"]),
        Paragraph("3. Integrasi pemantauan live streaming API dengan filter bot/spam detection untuk menjaga keaslian opini pengguna manusia.", S["bullet"]),
        hr(),
        Paragraph("Laporan Proyek Sains Data Resmi - SentimentGreen | URL: https://sentimentgreen.vercel.app", S["center"]),
    ]

    doc.build(story)
    size = (DL / "Laporan_Project.pdf").stat().st_size
    (DOCS_PDF / "Laporan_Project.pdf").write_bytes((DL / "Laporan_Project.pdf").read_bytes())
    print(f"✅ Laporan_Project.pdf ({size//1024} KB)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. PAPER JURNAL ILMIAH LENGKAP
# ─────────────────────────────────────────────────────────────────────────────
def build_paper():
    doc = SimpleDocTemplate(str(DL / "Paper_Jurnal.pdf"), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = make_styles()
    story = []

    # JUDUL & METADATA PAPER
    story += [
        Spacer(1, 0.4*cm),
        Paragraph("PAPER PUBLIKASI ILMIAH", S["caption"]),
        Paragraph("Komparasi Empiris Multinomial Naive Bayes dan Linear Support Vector Machine untuk Analisis Sentimen Opini Publik terhadap Isu Ekonomi Hijau pada Twitter", S["title"]),
        hr(),
        Paragraph("<b>Penulis:</b> SteVenJr | <b>Afiliasi:</b> Riset Sains Data & NLP SentimentGreen | <b>Tahun:</b> 2024", S["meta"]),
        Paragraph("<b>Kontak:</b> github.com/stevenjr-yt/sentimen-ekonomi-hijau | <b>Aplikasi Demo:</b> https://sentimentgreen.vercel.app", S["meta"]),
        Spacer(1, 0.3*cm),

        Paragraph("ABSTRAK", S["h2"]),
        Paragraph("""Transisi akseleratif menuju paradigma ekonomi hijau (green economy) menuntut dukungan sosio-politik yang kuat dari masyarakat luas. Media sosial mikroblog Twitter/X memegang peranan krusial sebagai barometer spontan dinamika diskursus publik mengenai kebijakan iklim, pajak karbon, dan elektrifikasi transportasi. Penelitian ini melakukan investigasi komparatif antara dua algoritma pembelajaran mesin terawasi klasik yang efisien dan interpretable—Multinomial Naive Bayes (MNB) dan Linear Support Vector Machine (Linear SVM)—dalam mengklasifikasikan sentimen tweet iklim berbahasa Inggris. Dataset yang dieksplorasi bersumber dari <i>Twitter Climate Change Sentiment Dataset</i> (Edward Qian, Kaggle) sejumlah 43.943 data mentah, yang setelah filtering kelas berita (news) dan deduplikasi menghasilkan korpus bersih sebanyak 31.907 sampel (20.580 positif, 7.478 netral, dan 3.849 negatif). Representasi teks dikonstruksi melalui Unigram-Bigram Term Frequency-Inverse Document Frequency (TF-IDF) dengan ruang fitur 15.000 kata ternormalisasi L2. Hasil evaluasi empiris pada 6.382 data uji menunjukkan bahwa Linear SVM secara konsisten mengungguli MNB dengan akurasi 74,07% berbanding 72,89%, serta F1-Score makro 65,81% berbanding 58,46%. Penanganan ketidakseimbangan kelas menggunakan pembobotan kelas seimbang (balanced class weighting) pada SVM berhasil mendongkrak recall kelas minoritas negatif hingga 60,13% (meningkat +25,32% dibandingkan MNB yang mengalami recall collapse di angka 34,81%). Model yang dioptimasi berhasil dikonversi ke dalam arsitektur inferensi sisi klien murni berbasis JavaScript tanpa ketergantungan server runtime.""", S["body"]),
        Paragraph("<b>Kata Kunci:</b> Analisis Sentimen, Ekonomi Hijau, Perubahan Iklim, TF-IDF, Naive Bayes, Support Vector Machine, Natural Language Processing, Twitter", S["body"]),
        Spacer(1, 0.2*cm),

        Paragraph("ABSTRACT", S["h2"]),
        Paragraph("""The accelerating transition toward a green economy paradigm necessitates robust socio-political public support. The microblogging platform Twitter/X serves as a vital real-time barometer for spontaneous public discourse on climate governance, carbon taxation, and energy electrification. This study conducts an empirical comparative investigation between two classical, interpretable machine learning algorithms—Multinomial Naive Bayes (MNB) and Linear Support Vector Machine (Linear SVM)—in classifying sentiment of climate-related English tweets. Sourced from the Twitter Climate Change Sentiment Dataset (Edward Qian, Kaggle) comprising 43,943 raw tweets, filtering out news items and deduplication yielded a clean corpus of 31,907 instances (20,580 positive, 7,478 neutral, and 3,849 negative). Text representations were engineered using Unigram-Bigram Term Frequency-Inverse Document Frequency (TF-IDF) across a 15,000-vocabulary vector space with L2 regularization. Empirical evaluation on 6,382 test samples demonstrates that Linear SVM consistently outperforms MNB, achieving an accuracy of 74.07% vs. 72.89% and a macro F1-Score of 65.81% vs. 58.46%. Incorporating balanced class weighting within SVM mitigated class imbalance, boosting minority negative-class recall to 60.13% (+25.32% improvement over MNB's 34.81% recall collapse). The optimal model was subsequently exported into a standalone JavaScript client-side inference engine, ensuring zero-latency, serverless accessibility.""", S["body"]),
        Paragraph("<b>Keywords:</b> Sentiment Analysis, Green Economy, Climate Change, TF-IDF, Naive Bayes, Support Vector Machine, NLP, Twitter", S["body"]),
        hr(),
    ]

    # 1. PENDAHULUAN
    story += [
        Paragraph("1. PENDAHULUAN", S["h1"]),
        Paragraph("""Urgensi penanganan perubahan iklim menuntut restrukturisasi menyeluruh tatanan ekonomi dunia. Laporan Intergovernmental Panel on Climate Change (IPCC, 2023) menegaskan bahwa batas pemanasan global 1,5°C mustahil dipertahankan tanpa dekarbonisasi mendalam pada sektor energi, industri, dan transportasi. Berbagai inisiatif transisi menuju ekonomi hijau (green economy)—mulai dari insentif kendaraan listrik hingga instrumen carbon pricing—telah digulirkan secara luas di berbagai belahan dunia (UNEP, 2011).""", S["body"]),
        Paragraph("""Namun, keberhasilan implementasi kebijakan iklim sangat rentan terhadap penolakan atau dukungan opini publik. Media sosial mikroblog Twitter/X memegang peranan krusial sebagai wadah artikulasi ekspresi publik yang masif dan spontan. Metode survei opini publik konvensional (seperti jajak pendapat tatap muka atau kuesioner daring) memiliki keterbatasan mendasar berupa tingginya biaya logistik, sampel terbatas, dan latensi waktu pemrosesan yang lambat. Penambangan opini berbasis Natural Language Processing (NLP) menawarkan alternatif komputasional berkecepatan tinggi yang dapat memantau pergeseran sentimen secara kontinu (Pak & Paroubek, 2010).""", S["body"]),
        Paragraph("""Penelitian ini bertujuan untuk: (1) Menyusun pipeline pemrosesan teks yang terstandarisasi untuk data tweet iklim, (2) Membandingkan formulasi matematis dan performa empiris Naive Bayes dan Linear SVM pada dataset imbalanced, serta (3) Menjawab persoalan penerapan model NLP pada lingkungan web tanpa latensi jaringan.""", S["body"]),

        # 2. METODE PENELITIAN
        Paragraph("2. METODE PENELITIAN", S["h1"]),
        Paragraph("2.1 Sumber dan Karakteristik Dataset", S["h2"]),
        Paragraph("""Penelitian ini menggunakan <i>Twitter Climate Change Sentiment Dataset</i> yang dipublikasikan oleh Edward Qian di repositori Kaggle (2022). Dataset asli memuat 43.943 tweet berlabel numerik: -1 (Anti/Skeptis), 0 (Netral), 1 (Pro-Aksi Iklim), dan 2 (Fakta Berita / News). Label kelas 2 (News) sejumlah 9.276 baris dieliminasi karena bersifat pemberitaan objektif media tanpa opini personal. Sebanyak 2.760 baris tweet duplikat dibersihkan sehingga menyisakan 31.907 data valid.""", S["body"]),
    ]

    tbl_paper_split = [
        ["Kategori Kelas Sentimen", "Label", "Jumlah Data", "Persentase", "Data Latih (80%)", "Data Uji (20%)"],
        ["Positif (Pro-Climate)", "+1", "20.580", "64,50%", "16.464", "4.116"],
        ["Netral (Neutral)", "0", "7.478", "23,44%", "5.982", "1.496"],
        ["Negatif (Anti-Climate)", "-1", "3.849", "12,06%", "3.079", "770"],
        ["Total Korpus Bersih", "-", "31.907", "100,00%", "25.525", "6.382"],
    ]
    story += [safe_table(tbl_paper_split, [4.5*cm, 1.5*cm, 2.5*cm, 2.5*cm, 3*cm, 3*cm], S, align_center_cols={1,2,3,4,5}), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("2.2 Formulasi Text Preprocessing dan Vektorisasi TF-IDF", S["h2"]),
        Paragraph("""Setiap tweet mentah diproses melalui tahapan: (1) Penghapusan URL, mention (@user), hashtag (#tag), tanda baca, dan angka; (2) Case folding ke huruf kecil; (3) Penghapusan stopword NLTK bahasa Inggris dengan mempertahankan kata negasi sentimen; serta (4) Porter Stemming (Porter, 1980).""", S["body"]),
        Paragraph("""Ekstraksi fitur menerapkan pembobotan TF-IDF Unigram dan Bigram (1,2) dengan batasan leksikon 15.000 fitur teratas dan normalisasi L2:""", S["body"]),
        Paragraph("TF-IDF(t, d) = [ f(t, d) / Σ f(t', d) ] * [ log( (1+N)/(1+df(t)) ) + 1 ]", S["formula"]),

        Paragraph("2.3 Model Multinomial Naive Bayes dan Linear SVM", S["h2"]),
        Paragraph("""• <b>Multinomial Naive Bayes:</b> Memprediksi probabilitas posterior kelas menggunakan Teorema Bayes dengan Laplace smoothing α = 0.3 untuk menghindari zero-frequency error:""", S["body"]),
        Paragraph("P(w_i | c) = [ N_{w_i, c} + 0.3 ] / [ N_c + 0.3 * |V| ]", S["formula"]),
        Paragraph("""• <b>Linear Support Vector Machine:</b> Membentuk hyperplane optimal dengan fungsi tujuan minimasi margin berpenalti reguler C=0.5 dan penyeimbang bobot kelas (class_weight='balanced'):""", S["body"]),
        Paragraph("min_{w,b,ξ} [ (1/2)*||w||^2 + 0.5 * Σ W_{y_i} * ξ_i ]   s.t.  y_i(w^T x_i + b) >= 1 - ξ_i", S["formula"]),

        # 3. HASIL DAN PEMBAHASAN
        PageBreak(),
        Paragraph("3. HASIL DAN PEMBAHASAN", S["h1"]),
        Paragraph("3.1 Hasil Evaluasi Kinerja Model", S["h2"]),
        Paragraph("""Tabel 1 menyajikan hasil perbandingan metrik evaluasi model pada 6.382 data uji independen:""", S["body"]),
    ]

    tbl_paper_res = [
        ["Model Pembelajaran", "Akurasi", "Precision (M)", "Recall (M)", "F1-Score (M)", "F1-Score (Weighted)"],
        ["Multinomial Naive Bayes", "72,89%", "71,63%", "54,38%", "58,46%", "69,71%"],
        ["Linear SVM (Optimal)", "74,07%", "65,75%", "65,91%", "65,81%", "73,96%"],
    ]
    story += [safe_table(tbl_paper_res, [4.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm], S, align_center_cols={1,2,3,4,5}), Spacer(1, 0.3*cm)]

    if (RESULTS / "cm_svm.png").exists():
        story += [
            RLImage(str(RESULTS / "cm_svm.png"), width=9*cm, height=6.5*cm),
            Paragraph("Gambar 1. Matriks Konfusi Model Linear SVM pada 6.382 Sampel Data Uji", S["caption"]),
            Spacer(1, 0.2*cm),
        ]

    story += [
        Paragraph("3.2 Analisis Kritis Ketidakseimbangan Kelas (Class Imbalance Analysis)", S["h2"]),
        Paragraph("""Meskipun Naive Bayes mencapai precision macro 71,63%, algoritma tersebut mengalami kegagalan signifikan (recall collapse) pada kelas minoritas negatif dengan nilai recall hanya 34,81%. Hal ini terjadi akibat asumsi independensi fitur Naive Bayes dan bias kuat frekuensi apriori terhadap kelas mayoritas positif (64,50%). Sebagian besar tweet negatif salah diklasifikasikan ke dalam kelas positif.""", S["body"]),
        Paragraph("""Sebaliknya, Linear SVM dengan penyeimbang bobot kelas otomatis memberikan penalti lebih besar pada kekeliruan sampel minoritas, mendongkrak recall kelas negatif menjadi 60,13% (+25,32% peningkatan mutlak) dan menghasilkan F1-Score makro 65,81% (+7,35% di atas Naive Bayes). Hal ini membuktikan ketahanan Linear SVM dalam memisahkan ruang fitur berdimensi tinggi pada dataset yang imbalanced.""", S["body"]),

        # 4. KESIMPULAN
        Paragraph("4. KESIMPULAN", S["h1"]),
        Paragraph("""Penelitian ini berhasil menunjukkan bahwa Linear Support Vector Machine mengungguli Multinomial Naive Bayes dalam analisis sentimen isu ekonomi hijau pada platform Twitter. Linear SVM mencapai akurasi 74,07% dan F1-Score makro 65,81%, serta menunjukkan ketahanan superior terhadap ketidakseimbangan kelas data. Model yang dihasilkan telah berhasil dikonversi ke format bobot JSON mandiri dan diintegrasikan ke platform peramban web tanpa memerlukan server backend aktif.""", S["body"]),

        Paragraph("DAFTAR PUSTAKA", S["h1"]),
        Paragraph("[1] Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273-297.", S["body"]),
        Paragraph("[2] IPCC. (2023). Climate Change 2023: Synthesis Report. Contribution of Working Groups I, II and III to AR6.", S["body"]),
        Paragraph("[3] Joachims, T. (1998). Text categorization with Support Vector Machines. European Conference on Machine Learning, 137-142.", S["body"]),
        Paragraph("[4] McCallum, A., & Nigam, K. (1998). A comparison of event models for Naive Bayes text classification. AAAI-98 Workshop, 41-48.", S["body"]),
        Paragraph("[5] Pak, A., & Paroubek, P. (2010). Twitter as a corpus for sentiment analysis and opinion mining. LREC 2010, 1320-1326.", S["body"]),
        Paragraph("[6] Pedregosa, F., et al. (2011). Scikit-learn: Machine Learning in Python. JMLR, 12, 2825-2830.", S["body"]),
        Paragraph("[7] Porter, M. F. (1980). An algorithm for suffix stripping. Program, 14(3), 130-137.", S["body"]),
        Paragraph("[8] Qian, E. (2022). Twitter Climate Change Sentiment Dataset. Kaggle Dataset Repository.", S["body"]),
        Paragraph("[9] Salton, G., & Buckley, C. (1988). Term-weighting approaches in automatic text retrieval. IP&M, 24(5), 513-523.", S["body"]),
        Paragraph("[10] UNEP. (2011). Towards a Green Economy: Pathways to Sustainable Development and Poverty Eradication.", S["body"]),
        hr(),
        Paragraph("Publikasi Paper Ilmiah Resmi - SentimentGreen | https://sentimentgreen.vercel.app", S["center"]),
    ]

    doc.build(story)
    size = (DL / "Paper_Jurnal.pdf").stat().st_size
    (DOCS_PDF / "Paper_Jurnal.pdf").write_bytes((DL / "Paper_Jurnal.pdf").read_bytes())
    print(f"✅ Paper_Jurnal.pdf ({size//1024} KB)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. STUDI LITERATUR LENGKAP (LITERATURE REVIEW)
# ─────────────────────────────────────────────────────────────────────────────
def build_literatur():
    doc = SimpleDocTemplate(str(DL / "Studi_Literatur.pdf"), pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    S = make_styles()
    story = []

    story += [
        Spacer(1, 0.4*cm),
        Paragraph("TINJAUAN STUDI LITERATUR (LITERATURE REVIEW)", S["caption"]),
        Paragraph("Analisis Sentimen Isu Lingkungan, Energi Hijau, dan Perubahan Iklim Menggunakan Machine Learning pada Media Sosial: Kajian Literatur dan Analisis Kesenjangan Riset 2024", S["title"]),
        hr(),
        Paragraph("<b>Penyusun:</b> SteVenJr | <b>Afiliasi:</b> Riset Sains Data SentimentGreen | <b>Tahun:</b> 2024", S["meta"]),
        Paragraph("<b>Publikasi Terbuka:</b> https://sentimentgreen.vercel.app | <b>Repository:</b> github.com/stevenjr-yt/sentimen-ekonomi-hijau", S["meta"]),
        Spacer(1, 0.3*cm),

        Paragraph("RINGKASAN EKSEKUTIF", S["h2"]),
        Paragraph("""Tinjauan literatur komprehensif ini mengkaji perkembangan riset terkini (khususnya publikasi tahun 2024) mengenai penerapan teknik Natural Language Processing (NLP) dan machine learning dalam menganalisis sentimen opini publik terhadap isu keberlanjutan, energi terbarukan, kendaraan listrik (electric vehicles), dan ekonomi hijau. Melalui sintesis sistematis terhadap artikel jurnal terindeks, studi ini memetakan lanskap metodologi dari algoritma klasik (Naive Bayes, Support Vector Machine, Random Forest) hingga model transfer learning modern (BERT, IndoBERT, FastText). Hasil sintesis menunjukkan bahwa Support Vector Machine secara konsisten mempertahankan akurasi dan generalisasi terbaik di antara metode tradisional, terutama pada data media sosial yang tidak seimbang. Studi ini juga mengidentifikasi 5 kesenjangan riset (research gaps) utama yang menjadi fondasi dan justifikasi teknis arsitektur proyek SentimentGreen.""", S["body"]),
        hr(),

        Paragraph("1. METODOLOGI PENELUSURAN LITERATUR", S["h1"]),
    ]

    tbl_lit_method = [
        ["Parameter Penelusuran", "Spesifikasi Metodologis"],
        ["Pangkalan Data Akademik", "Google Scholar, Semantic Scholar, ResearchGate, Garuda Kemdikbudristek, IEEE Xplore"],
        ["Rentang Periode Terbit", "Fokus utama: Tahun 2024 (dengan landasan teori 1980–2023)"],
        ["Kata Kunci Boolean", "('analisis sentimen' OR 'sentiment analysis') AND ('green economy' OR 'climate change' OR 'kendaraan listrik') AND ('Naive Bayes' OR 'SVM' OR 'BERT')"],
        ["Kriteria Inklusi (Diterima)", "Artikel peer-reviewed, fokus domain lingkungan/energi, menggunakan pemodelan machine learning atau deep learning teruji"],
        ["Kriteria Eksklusi (Ditolak)", "Artikel opini non-empiris, penelitian lexicon-only tanpa evaluasi statistik, publikasi di luar topik lingkungan"],
    ]
    story += [safe_table(tbl_lit_method, [4.5*cm, 12.5*cm], S), Spacer(1, 0.3*cm)]

    story += [
        Paragraph("2. MATRIKS PERBANDINGAN ARTIKEL TERPILIH (PUBLIKASI 2024)", S["h1"]),
        Paragraph("""Tabel berikut merangkum studi literatur empiris terkini yang relevan dengan metodologi proyek:""", S["body"]),
    ]

    tbl_lit_articles = [
        ["No", "Penulis & Sumber Jurnal", "Metode Algoritma", "Dataset & Objek", "Hasil Akurasi", "Temuan & Kesenjangan Riset"],
        ["1", "Merdiansah et al. (2024)\nJIKOMSI Vol.7(1)", "IndoBERT (Fine-Tuned IndoNLU)", "Tweet X/Twitter Indonesia topik Kendaraan Listrik", "Komparatif unggul", "IndoBERT fine-tuning unggul atas base model; gap: topik terbatas pada EV, belum ekonomi hijau holistik"],
        ["2", "Hendrawan & Kusmiyati (2024)\nCESS Vol.9(1)", "Multinomial NB vs Linear SVM", "Twitter topik EV Indonesia", "SVM unggul", "SVM konsisten mengungguli Naive Bayes pada data Twitter; memperkuat justifikasi model SentimentGreen"],
        ["3", "Prameswari et al. (2024)\nInnovative Vol.4(4)", "SVM, Naive Bayes, Random Forest", "Twitter EV & Transisi Energi", "SVM terbaik", "SVM dengan TF-IDF menghasilkan metrik generalisasi terbaik; belum mengeksplorasi browser offline deployment"],
        ["4", "Hidayatullah et al. (2024)\nJournalISI Vol.6(3)", "FastText + BERT Transformer", "119.000 Tweet Energi Bersih Indonesia", "82,50%", "58% sentimen publik positif terhadap EV; model BERT unggul namun menuntut infrastruktur komputasi GPU tinggi"],
        ["5", "Edward Qian (2022 / Benchmark)\nKaggle Dataset", "Kaggle Benchmark Dataset", "43.943 Tweet Iklim Global (2008–2019)", "Baseline", "Dataset acuan internasional utama yang digunakan dalam proyek SentimentGreen"],
    ]
    story += [safe_table(tbl_lit_articles, [0.8*cm, 4.8*cm, 3.8*cm, 3.8*cm, 1.8*cm, 2*cm], S, align_center_cols={0,4}), Spacer(1, 0.4*cm)]

    story += [
        PageBreak(),
        Paragraph("3. SINTESIS METODOLOGIS DAN ANALISIS KOMPARATIF", S["h1"]),
        Paragraph("3.1 Dominasi Konsisten Support Vector Machine atas Naive Bayes", S["h2"]),
        Paragraph("""Seluruh literatur yang membandingkan Naive Bayes dan SVM pada data media sosial secara konsisten mencatat keunggulan SVM. Naive Bayes mengasumsikan independensi kondisional antar fitur, suatu asumsi yang sering terlanggar pada teks bahasa alami yang sarat dengan kolokasi (seperti <i>climate change</i>, <i>global warming</i>). SVM memandang representasi TF-IDF sebagai vektor dalam ruang berdimensi tinggi ($R^{15.000}$) dan mencari margin maksimal, memberikan ketahanan superior terhadap fenomena overfitting pada dataset teks berdimensi tinggi.""", S["body"]),

        Paragraph("3.2 Perkembangan Transformer dan Trade-Off Komputasi", S["h2"]),
        Paragraph("""Meskipun model berbasis arsitektur transformer (seperti BERT, RoBERTa, dan IndoBERT) mampu mencapai akurasi lebih tinggi, model tersebut memiliki bobot parameter ratusan megabyte hingga gigabyte serta menuntut latensi inferensi yang signifikan. Untuk skenario aplikasi web terdistribusi yang ditargetkan dapat berjalan langsung di browser pengguna tanpa biaya infrastruktur cloud, kombinasi TF-IDF dan Linear SVM menawarkan *sweet spot* optimal antara akurasi yang kompetitif (74%+), ukuran model sangat ringan (<2 MB), dan kecepatan inferensi instan (<5 milidetik).""", S["body"]),

        Paragraph("4. IDENTIFIKASI KESENJANGAN RISET (RESEARCH GAPS)", S["h1"]),
        Paragraph("1. <b>Kesenjangan Topik (Thematic Gap):</b> Mayoritas penelitian tahun 2024 hanya berfokus pada topik parsial seperti kendaraan listrik (EV) atau pajak karbon secara terisolasi. Belum ada studi komprehensif yang memetakan spektrum ekonomi hijau secara holistik.", S["bullet"]),
        Paragraph("2. <b>Kesenjangan Bahasa & Skala (Language & Scale Gap):</b> Penelitian di Indonesia umumnya menggunakan sampel lokal berukuran kecil (<2.000 tweet), sedangkan dataset iklim global berskala besar berbahasa Inggris jarang diteliti dalam publikasi nasional.", S["bullet"]),
        Paragraph("3. <b>Kesenjangan Arsitektur Penerapan (Deployment Gap):</b> Seluruh literatur yang dikaji berhenti pada tahap eksperimen Google Colab/Jupyter Notebook tanpa menyediakan antarmuka web inferensi offline yang dapat diakses publik.", S["bullet"]),
        Paragraph("4. <b>Kesenjangan Penanganan Imbalance (Class Imbalance Gap):</b> Banyak studi mengabaikan metrik Macro F1-Score dan hanya melaporkan Accuracy, mengaburkan masalah recall collapse pada kelas minoritas.", S["bullet"]),
        Paragraph("5. <b>Kontribusi SentimentGreen:</b> Proyek ini mengisi seluruh kesenjangan di atas dengan menyajikan platform analisis sentimen holistik, berdataset 31.907 tweet, evaluasi makro transparan, dan sistem inferensi browser offline murni.", S["bullet"]),

        Paragraph("5. DAFTAR REFERENSI", S["h1"]),
        Paragraph("[1] Hendrawan, G. N., & Kusmiyati, H. (2024). Evaluasi Performa Naive Bayes dan SVM dalam Analisis Sentimen Kendaraan Listrik. CESS, 9(1), 299-313.", S["body"]),
        Paragraph("[2] Hidayatullah, S., et al. (2024). Sentiment Analysis of Indonesian Citizens on Electric Vehicle Using FastText and BERT. JournalISI, 6(3), 780-791.", S["body"]),
        Paragraph("[3] Merdiansah, R., et al. (2024). Analisis Sentimen Pengguna X Indonesia Terkait Kendaraan Listrik Menggunakan IndoBERT. JIKOMSI, 7(1), 221-228.", S["body"]),
        Paragraph("[4] Prameswari, G. A. S. A., et al. (2024). Sentiment Analysis of Electric Vehicles on Twitter Using Machine Learning. Innovative, 4(4), 837-845.", S["body"]),
        Paragraph("[5] Qian, E. (2022). Twitter Climate Change Sentiment Dataset. Kaggle Dataset Repository.", S["body"]),
        Paragraph("[6] UNEP. (2011). Towards a Green Economy: Pathways to Sustainable Development and Poverty Eradication.", S["body"]),
        hr(),
        Paragraph("Dokumen Studi Literatur Ilmiah Resmi - SentimentGreen | https://sentimentgreen.vercel.app", S["center"]),
    ]

    doc.build(story)
    size = (DL / "Studi_Literatur.pdf").stat().st_size
    (DOCS_PDF / "Studi_Literatur.pdf").write_bytes((DL / "Studi_Literatur.pdf").read_bytes())
    print(f"✅ Studi_Literatur.pdf ({size//1024} KB)")

if __name__ == "__main__":
    print("Membangun seluruh Dokumen PDF Lengkap & Komprehensif...")
    build_laporan()
    build_paper()
    build_literatur()
    print("Semua dokumen PDF berhasil digenerate sempurna di web/downloads/ dan docs/pdf/!")
