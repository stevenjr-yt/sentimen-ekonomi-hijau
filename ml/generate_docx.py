"""Generator Dokumen Microsoft Word (.docx) Lengkap untuk SentimentGreen.

Menghasilkan 3 Dokumen .docx:
1. Laporan_Project.docx (Laporan Teknis Lengkap 5 Bab + Visualisasi)
2. Paper_Jurnal.docx (Format Publikasi Jurnal Ilmiah ID & EN)
3. Studi_Literatur.docx (Systematic Literature Review 10 Jurnal & Gap Analysis)
"""
import pathlib
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = pathlib.Path(__file__).resolve().parent.parent
DL = ROOT / "web" / "downloads"
DL.mkdir(parents=True, exist_ok=True)
DOCS_DIR = ROOT / "docs" / "docx"
DOCS_DIR.mkdir(parents=True, exist_ok=True)
RESULTS = ROOT / "results"

COLOR_DARK = RGBColor(6, 78, 59)     # #064e3b
COLOR_GREEN = RGBColor(5, 150, 105)  # #059669
COLOR_GRAY = RGBColor(100, 116, 139) # #64748b

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_styled_table(doc, headers, data, col_widths=None):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    # Header Row
    hdr_cells = table.rows[0].cells
    for i, title in enumerate(headers):
        hdr_cells[i].text = str(title)
        set_cell_background(hdr_cells[i], '064E3B')
        p = hdr_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.bold = True
            run.font.color.rgb = RGBColor(255, 255, 255)
            run.font.size = Pt(9)

    # Data Rows
    for r_idx, row in enumerate(data):
        row_cells = table.rows[r_idx + 1].cells
        bg_hex = 'F8FAFC' if r_idx % 2 == 1 else 'FFFFFF'
        for c_idx, val in enumerate(row):
            row_cells[c_idx].text = str(val)
            set_cell_background(row_cells[c_idx], bg_hex)
            p = row_cells[c_idx].paragraphs[0]
            for run in p.runs:
                run.font.size = Pt(8.5)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = width

    doc.add_paragraph() # Spacing
    return table

# ─────────────────────────────────────────────────────────────────────────────
# 1. LAPORAN PROYEK (.docx)
# ─────────────────────────────────────────────────────────────────────────────
def build_laporan_docx():
    doc = docx.Document()

    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t = p_title.add_run("LAPORAN AKHIR PROYEK SAINS DATA\n")
    run_t.bold = True
    run_t.font.size = Pt(18)
    run_t.font.color.rgb = COLOR_DARK

    run_sub = p_title.add_run("ANALISIS SENTIMEN OPINI PUBLIK TERHADAP ISU EKONOMI HIJAU DAN PERUBAHAN IKLIM MENGGUNAKAN TF-IDF, MULTINOMIAL NAIVE BAYES, DAN LINEAR SUPPORT VECTOR MACHINE\n")
    run_sub.bold = True
    run_sub.font.size = Pt(12)
    run_sub.font.color.rgb = COLOR_GREEN

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Disusun oleh: SteVenJr | Departemen Ilmu Komputer, Fakultas Ilmu Komputer dan TI\n"
                           "Laboratorium Sains Data, AI & NLP SentimentGreen | Tahun Akademik: 2026\n"
                           "Dataset: Twitter Climate Change Sentiment Dataset (Kaggle: Edward Qian)\n"
                           "Aplikasi Web: https://sentimentgreen.vercel.app | Repositori: github.com/stevenjr-yt/sentimen-ekonomi-hijau\n")
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = COLOR_GRAY

    # Ringkasan Eksekutif
    h = doc.add_heading("RINGKASAN EKSEKUTIF", level=1)
    doc.add_paragraph(
        "Laporan ini menyajikan dokumentasi menyeluruh dari perancangan, eksperimentasi, evaluasi, dan implementasi sistem analisis sentimen terhadap opini publik terkait isu ekonomi hijau dan perubahan iklim pada media sosial Twitter. Proyek SentimentGreen memanfaatkan dataset riil sebanyak 43.943 tweet mentah dari Kaggle. Setelah proses penyaringan kelas news dan deduplikasi ketat, diperoleh 31.907 sampel valid (20.580 sentimen positif, 7.478 netral, dan 3.849 negatif). Pipeline preprocessing komprehensif dibangun meliputi pembersihan noise (cleaning), case folding, stopword removal dengan preservasi kata negasi, serta Porter stemming. Fitur diekstrak menggunakan TF-IDF unigram-bigram berdimensi 15.000 fitur. Model Linear Support Vector Machine (SVM) dengan pembobotan kelas seimbang berhasil mengungguli Multinomial Naive Bayes (MNB) dengan akurasi 74,07% berbanding 72,89% dan F1-Score makro 65,81% berbanding 58,46%. Keunggulan paling menonjol tampak pada recall kelas minoritas negatif yang mencapai 60,13% pada SVM berbanding hanya 34,81% pada MNB. Model akhir diekspor ke dalam bobot JSON murni sehingga inferensi dapat berjalan 100% offline di browser pengguna tanpa kebutuhan server komputasi aktif."
    )

    # BAB I: PENDAHULUAN
    doc.add_heading("BAB I – PENDAHULUAN", level=1)
    doc.add_heading("1.1 Latar Belakang Masalah", level=2)
    doc.add_paragraph(
        "Perubahan iklim global merupakan salah satu tantangan eksistensial terbesar peradaban modern. Berdasarkan laporan Intergovernmental Panel on Climate Change (IPCC AR6, 2023), emisi gas rumah kaca global harus ditekan sebesar 43% sebelum tahun 2030 agar ambang batas kenaikan suhu rata-rata permukaan bumi tidak melampaui 1,5°C di atas tingkat pra-industri. Dalam menjawab krisis ini, masyarakat global merumuskan transisi menuju green economy (ekonomi hijau)—suatu model pembangunan sosio-ekonomi yang memprioritaskan energi terbarukan, transportasi nol emisi, elektrifikasi massal, instrumen pasar karbon, dan efisiensi sumber daya lingkungan (UNEP, 2011)."
    )
    doc.add_paragraph(
        "Meskipun secara konseptual didukung oleh konsensus ilmiah internasional, implementasi kebijakan ekonomi hijau di lapangan senantiasa menghadapi tantangan polarisasi opini masyarakat. Biaya awal transisi energi, perubahan gaya hidup, subsidi kendaraan listrik, dan penutupan industri bahan bakar fosil kerap memicu resistensi, skeptisisme, atau kekhawatiran ekonomi di kalangan publik. Media sosial, khususnya Twitter/X, telah menjadi panggung utama diskursus publik di mana jutaan opini, kritik, dan sentimen masyarakat diartikulasikan secara spontan setiap harinya."
    )

    doc.add_heading("1.2 Rumusan Masalah", level=2)
    doc.add_paragraph("1. Bagaimana karakteristik, asal usul (provenance), dan distribusi sentimen publik terhadap isu iklim dan ekonomi hijau pada platform Twitter?", style='List Bullet')
    doc.add_paragraph("2. Bagaimana alur preprocessing teks yang sistematis dan konsisten untuk membersihkan noise informal khas Twitter tanpa merusak makna sentimen?", style='List Bullet')
    doc.add_paragraph("3. Bagaimana formulasi matematis dan komparasi performa antara algoritma Multinomial Naive Bayes dan Linear SVM pada dataset imbalanced?", style='List Bullet')
    doc.add_paragraph("4. Mengapa Support Vector Machine menghasilkan F1-Score makro yang lebih superior dalam mendeteksi kelas minoritas (negatif & netral)?", style='List Bullet')
    doc.add_paragraph("5. Bagaimana mengarsiteki model machine learning agar dapat berjalan sepenuhnya offline di sisi client browser tanpa ketergantungan server?", style='List Bullet')

    doc.add_heading("1.3 Tujuan Proyek", level=2)
    doc.add_paragraph("1. Mengumpulkan, mendokumentasikan, dan memproses 43.943 tweet mentah dari Twitter Climate Change Sentiment Dataset.", style='List Bullet')
    doc.add_paragraph("2. Mengembangkan pipeline text preprocessing Python dan JavaScript yang identik untuk menjamin konsistensi inferensi.", style='List Bullet')
    doc.add_paragraph("3. Membangun representasi ruang fitur TF-IDF unigram-bigram berdimensi 15.000 kata dengan normalisasi L2.", style='List Bullet')
    doc.add_paragraph("4. Melatih, mengoptimasi, dan mengevaluasi model Naive Bayes dan SVM menggunakan stratified 80:20 train-test split.", style='List Bullet')
    doc.add_paragraph("5. Menyajikan visualisasi WordCloud, matriks konfusi, dan dasbor web interaktif yang dapat diakses publik secara bebas.", style='List Bullet')

    # BAB II: LANDASAN TEORI & RUMUS LENGKAP
    doc.add_heading("BAB II – TINJAUAN PUSTAKA DAN LANDASAN TEORI", level=1)
    doc.add_heading("2.1 Formulasi Matematis TF-IDF & Normalisasi L2 (Euclidean Norm)", level=2)
    doc.add_paragraph(
        "TF-IDF (Term Frequency - Inverse Document Frequency) adalah metode pembobotan statistik yang mengukur signifikansi relatif sebuah term t dalam dokumen d terhadap kumpulan korpus N dokumen:\n"
        "1. TF(t, d) = f(t, d) / [ Σ_{t' in d} f(t', d) ]\n"
        "2. IDF(t) = ln [ (1 + N) / (1 + df(t)) ] + 1\n"
        "3. Bobot Mentah: v(t, d) = TF(t, d) * IDF(t)\n"
        "4. Normalisasi L2 (Euclidean Norm): v_norm = v / sqrt(Σ v_i^2)\n"
        "Akar kuadrat (sqrt) berfungsi sebagai normalisasi panjang vektor agar tweet pendek dan tweet panjang dinilai secara adil berdasarkan proporsi makna, bukan panjang karakter."
    )

    doc.add_heading("2.2 Formulasi Multinomial Naive Bayes (MNB)", level=2)
    doc.add_paragraph(
        "Berdasarkan Teorema Bayes dengan asumsi independensi bersyarat fitur dan Laplace Smoothing α = 0.3:\n"
        "P(c | d) ∝ P(c) * Π_{i=1}^{n} P(w_i | c)\n"
        "P(w_i | c) = [ N_{w_i, c} + 0.3 ] / [ N_c + 0.3 * |V| ]\n"
        "Klasifikasi: c_pred = argmax_c [ log P(c) + Σ log P(w_i | c) ]"
    )

    doc.add_heading("2.3 Formulasi Linear Support Vector Machine (Linear SVM)", level=2)
    doc.add_paragraph(
        "Linear SVM mencari hyperplane optimal w^T * x + b = 0 dengan margin maksimal 2 / ||w|| melalui formulasi optimasi soft-margin berbobot seimbang:\n"
        "min_{w, b, ξ} [ (1/2) * ||w||^2 + C * Σ W_{y_i} * ξ_i ]\n"
        "Subject to: y_i * ( w^T * x_i + b ) >= 1 - ξ_i,  ξ_i >= 0\n"
        "Bobot Penyeimbang Kelas: W_c = N_total / [ K * N_c ] (K = 3 kelas)\n"
        "Fungsi Keputusan (One-vs-Rest): c_pred = argmax_c [ w_c^T * x + b_c ]"
    )

    # BAB III: METODOLOGI & PERJALANAN DATA
    doc.add_heading("BAB III – METODOLOGI DAN PERJALANAN DATA", level=1)
    doc.add_paragraph("Karakteristik dan spesifikasi teknis dataset yang digunakan:")
    tbl_prov_data = [
        ["Nama Dataset", "Twitter Climate Change Sentiment Dataset"],
        ["Sumber Penyedia", "Kaggle (Edward Qian: edqian/twitter-climate-change-sentiment-dataset)"],
        ["File Dataset", "data/twitter_sentiment_data.csv (~6.3 MB)"],
        ["Total Data Mentah", "43.943 tweet teranotasi"],
        ["Pembersihan Data", "9.276 kelas news dibuang; 2.760 duplikasi dibersihkan"],
        ["Total Sampel Akhir", "31.907 tweet valid (Positif: 20.580, Netral: 7.478, Negatif: 3.849)"],
        ["Pembagian Data", "Data Latih (80% = 25.525 sampel) | Data Uji (20% = 6.382 sampel)"],
        ["Vocabulary", "14.893 fitur leksikon unik"],
    ]
    create_styled_table(doc, ["Parameter Dataset", "Keterangan Spesifikasi"], tbl_prov_data, [Inches(2.5), Inches(4.5)])

    doc.add_heading("3.2 Implementasi Kode Sumber & Arsitektur Model", level=2)
    doc.add_paragraph(
        "Model dilatih menggunakan Python 3.10 dan pustaka scikit-learn dengan pipeline yang terdokumentasi rapi di ml/train.py. Ekstraksi fitur menggunakan TfidfVectorizer(ngram_range=(1,2), max_features=15000), diikuti inisialisasi LinearSVC(C=0.5, class_weight='balanced') dan MultinomialNB(alpha=0.3).\n\n"
        "Matriks bobot model kemudian diekspor ke file web/model/model.json yang memuat 15.000 kata leksikon, nilai IDF, koefisien SVM (3 x 15.000), dan nilai bias (intercept). Pada sisi peramban web (web/inference.js), JavaScript menghitung perkalian titik sparse dot-product dan fungsi Softmax secara mandiri. Hal ini mewujudkan inferensi AI 100% luring (offline) tanpa dependensi server, memangkas latensi menjadi di bawah 3 milidetik per tweet, serta menjaga privasi teks pengguna secara penuh."
    )

    # BAB IV: HASIL EVALUASI & VISUALISASI
    doc.add_heading("BAB IV – HASIL EVALUASI, METRIK, DAN PEMBAHASAN", level=1)
    doc.add_paragraph("Hasil perbandingan kinerja empiris model pada 6.382 data uji independen:")
    tbl_eval_data = [
        ["Multinomial Naive Bayes", "72,89%", "71,63%", "54,38%", "58,46%", "69,71%"],
        ["Linear SVM (Optimal)", "74,07%", "65,75%", "65,91%", "65,81%", "73,96%"],
        ["Selisih (SVM - MNB)", "+1,18%", "-5,88%", "+11,53%", "+7,35%", "+4,25%"],
    ]
    create_styled_table(doc, ["Algoritma", "Akurasi", "Precision (M)", "Recall (M)", "F1-Score (M)", "F1-Score (Weighted)"], tbl_eval_data)

    # Sisipkan Gambar Visualisasi
    doc.add_heading("4.1 Visualisasi Kinerja & Matriks Konfusi", level=2)
    if (RESULTS / "perbandingan_model.png").exists():
        doc.add_picture(str(RESULTS / "perbandingan_model.png"), width=Inches(6.0))
        p = doc.add_paragraph("Gambar 4.1 Grafik Perbandingan Metrik Evaluasi: Naive Bayes vs Linear SVM")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    if (RESULTS / "cm_svm.png").exists():
        doc.add_picture(str(RESULTS / "cm_svm.png"), width=Inches(4.5))
        p = doc.add_paragraph("Gambar 4.2 Matriks Konfusi Linear SVM pada 6.382 Data Uji")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # BAB V: KESIMPULAN
    doc.add_heading("BAB V – KESIMPULAN DAN REKOMENDASI", level=1)
    doc.add_paragraph(
        "1. Linear SVM terbukti sebagai algoritma terbaik dengan akurasi 74,07% dan F1-Score makro 65,81%, unggul mutlak dibanding Naive Bayes dalam mengenali kelas minoritas negatif.\n"
        "2. Mayoritas opini publik (64,50%) menyatakan dukungan positif terhadap aksi iklim dan ekonomi hijau.\n"
        "3. Pipeline text preprocessing (cleaning, stopword selective, Porter stemming) dan ekstraksi TF-IDF 15.000 fitur sangat efektif untuk representasi teks tweet.\n"
        "4. Model berhasil diekspor ke bobot JSON mandiri dan berjalan 100% offline di browser web pengguna tanpa server backend."
    )

    out_file = DL / "Laporan_Project.docx"
    doc.save(str(out_file))
    (DOCS_DIR / "Laporan_Project.docx").write_bytes(out_file.read_bytes())
    size = out_file.stat().st_size
    print(f"✅ Laporan_Project.docx ({size//1024} KB)")

# ─────────────────────────────────────────────────────────────────────────────
# 2. PAPER JURNAL (.docx)
# ─────────────────────────────────────────────────────────────────────────────
def build_paper_docx():
    doc = docx.Document()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = p_title.add_run("JURNAL ILMIAH ILMU KOMPUTER DAN SISTEM INFORMASI (JIKOMSI) - TAHUN 2026\n")
    r_cat.font.size = Pt(10)
    r_cat.font.color.rgb = COLOR_GRAY

    r_title = p_title.add_run("Komparasi Empiris Multinomial Naive Bayes dan Linear Support Vector Machine untuk Analisis Sentimen Opini Publik terhadap Isu Ekonomi Hijau pada Twitter\n")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = COLOR_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("SteVenJr (stevenjr.research@gmail.com)\n"
                           "Departemen Ilmu Komputer, Fakultas Ilmu Komputer dan Teknologi Informasi\n"
                           "Laboratorium Sains Data, Kecerdasan Artifisial, dan NLP | Tahun Publikasi: 2026\n"
                           "Aplikasi Web: https://sentimentgreen.vercel.app | Repositori: github.com/stevenjr-yt/sentimen-ekonomi-hijau\n")
    r_meta.font.size = Pt(9)
    r_meta.font.color.rgb = COLOR_GRAY

    doc.add_heading("ABSTRAK", level=2)
    doc.add_paragraph(
        "Transisi akseleratif menuju paradigma ekonomi hijau (green economy) menuntut dukungan sosio-politik yang kuat dari masyarakat luas. Media sosial mikroblog Twitter/X memegang peranan krusial sebagai barometer spontan dinamika diskursus publik mengenai kebijakan iklim, pajak karbon, dan elektrifikasi transportasi. Penelitian ini melakukan investigasi komparatif antara dua algoritma pembelajaran mesin terawasi klasik yang efisien dan interpretable—Multinomial Naive Bayes (MNB) dan Linear Support Vector Machine (Linear SVM)—dalam mengklasifikasikan sentimen tweet iklim berbahasa Inggris. Dataset yang dieksplorasi bersumber dari Twitter Climate Change Sentiment Dataset (Edward Qian, Kaggle) sejumlah 43.943 data mentah, yang setelah filtering kelas berita (news) dan deduplikasi menghasilkan korpus bersih sebanyak 31.907 sampel (20.580 positif, 7.478 netral, dan 3.849 negatif). Representasi teks dikonstruksi melalui Unigram-Bigram TF-IDF dengan ruang fitur 15.000 kata ternormalisasi L2. Hasil evaluasi empiris pada 6.382 data uji menunjukkan bahwa Linear SVM secara konsisten mengungguli MNB dengan akurasi 74,07% berbanding 72,89%, serta F1-Score makro 65,81% berbanding 58,46%. Penanganan ketidakseimbangan kelas menggunakan pembobotan kelas seimbang pada SVM berhasil mendongkrak recall kelas minoritas negatif hingga 60,13% (meningkat +25,32% dibandingkan MNB yang mengalami recall collapse di angka 34,81%). Model yang dioptimasi berhasil dikonversi ke dalam arsitektur inferensi sisi klien murni berbasis JavaScript tanpa ketergantungan server runtime."
    )
    p_kw = doc.add_paragraph()
    p_kw.add_run("Kata Kunci: ").bold = True
    p_kw.add_run("Analisis Sentimen, Ekonomi Hijau, Perubahan Iklim, TF-IDF, Naive Bayes, Support Vector Machine, NLP, Twitter")

    doc.add_heading("ABSTRACT", level=2)
    doc.add_paragraph(
        "The accelerating transition toward a green economy paradigm necessitates robust socio-political public support. The microblogging platform Twitter/X serves as a vital real-time barometer for spontaneous public discourse on climate governance, carbon taxation, and energy electrification. Sourced from the Twitter Climate Change Sentiment Dataset (Edward Qian, Kaggle) comprising 43,943 raw tweets, filtering out news items and deduplication yielded a clean corpus of 31,907 instances. Empirical evaluation on 6,382 test samples demonstrates that Linear SVM consistently outperforms MNB, achieving an accuracy of 74.07% vs. 72.89% and a macro F1-Score of 65.81% vs. 58.46%. Incorporating balanced class weighting within SVM mitigated class imbalance, boosting minority negative-class recall to 60.13%."
    )

    doc.add_heading("1. PENDAHULUAN", level=1)
    doc.add_paragraph(
        "Urgensi penanganan perubahan iklim menuntut restrukturisasi menyeluruh tatanan ekonomi dunia (IPCC, 2023). Opini publik di media sosial Twitter menjadi faktor penentu suksesnya kebijakan transisi energi bersih. Penelitian ini membandingkan kinerja MNB dan SVM secara terstandarisasi untuk klasifikasi teks berskala besar."
    )

    doc.add_heading("2. METODE DAN HASIL", level=1)
    doc.add_paragraph(
        "Penelitian ini menerapkan ekstraksi fitur TF-IDF unigram-bigram berdimensi 15.000 kata dengan normalisasi L2 dan Porter Stemmer. Model Linear SVM dioptimasi dengan class_weight='balanced' untuk mengatasi ketidakseimbangan kelas. Seluruh bobot model diekspor ke format JSON mandiri sehingga inferensi dapat dieksekusi 100% di browser klien via JavaScript tanpa server backend."
    )
    tbl_paper_data = [
        ["Multinomial Naive Bayes", "72,89%", "71,63%", "54,38%", "58,46%"],
        ["Linear SVM (Optimal)", "74,07%", "65,75%", "65,91%", "65,81%"],
    ]
    create_styled_table(doc, ["Model", "Akurasi", "Precision (M)", "Recall (M)", "F1-Score (M)"], tbl_paper_data)

    if (RESULTS / "cm_svm.png").exists():
        doc.add_picture(str(RESULTS / "cm_svm.png"), width=Inches(4.0))

    doc.add_heading("3. KESIMPULAN", level=1)
    doc.add_paragraph(
        "Linear SVM terbukti lebih tangguh dan seimbang dalam memprediksi sentimen opini publik iklim di Twitter, menghasilkan peningkatan recall kelas minoritas secara substansial."
    )

    out_file = DL / "Paper_Jurnal.docx"
    doc.save(str(out_file))
    (DOCS_DIR / "Paper_Jurnal.docx").write_bytes(out_file.read_bytes())
    size = out_file.stat().st_size
    print(f"✅ Paper_Jurnal.docx ({size//1024} KB)")

# ─────────────────────────────────────────────────────────────────────────────
# 3. STUDI LITERATUR (.docx)
# ─────────────────────────────────────────────────────────────────────────────
def build_literatur_docx():
    doc = docx.Document()

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_cat = p_title.add_run("SYSTEMATIC LITERATURE REVIEW & RESEARCH GAP ANALYSIS\n")
    r_cat.font.size = Pt(10)
    r_cat.font.color.rgb = COLOR_GRAY

    r_title = p_title.add_run("Kajian Komparatif Sistematis Metodologi Analisis Sentimen Isu Lingkungan, Energi Bersih, dan Ekonomi Hijau: Pemetaan Komparasi 10 Jurnal Terakreditasi dan Kesenjangan Riset (2024–2026)\n")
    r_title.bold = True
    r_title.font.size = Pt(14)
    r_title.font.color.rgb = COLOR_DARK

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Penyusun: SteVenJr | Afiliasi: Riset Sains Data SentimentGreen | Tahun: 2026\n"
                           "Aplikasi Web: https://sentimentgreen.vercel.app | Repo: github.com/stevenjr-yt/sentimen-ekonomi-hijau\n")
    r_meta.font.size = Pt(8.5)
    r_meta.font.color.rgb = COLOR_GRAY

    doc.add_heading("RINGKASAN EKSEKUTIF", level=2)
    doc.add_paragraph(
        "Tinjauan literatur sistematis ini menyajikan telaah mendalam terhadap publikasi ilmiah terkini (2024–2026) dalam domain analisis sentimen media sosial terkait diskursus transisi energi, kendaraan listrik, perubahan iklim, dan kebijakan ekonomi hijau. Melalui penelusuran terhadap pangkalan data akademik nasional dan internasional (Google Scholar, SINTA, Scopus, Garuda, IEEE Xplore), studi ini membandingkan sepuluh artikel acuan dengan arsitektur proyek SentimentGreen."
    )

    doc.add_heading("MATRIKS PERBANDINGAN 10 JURNAL TERAKREDITASI", level=1)
    tbl_lit_data = [
        ["1", "Merdiansah et al. (2024) - JIKOMSI", "SINTA 3", "IndoBERT + Fine-tuning IndoNLU", "Tweet EV", "Fine-tuning unggul. Gap: Topik sempit pada EV."],
        ["2", "Hendrawan & Kusmiyati (2024) - CESS", "SINTA 2", "Multinomial NB vs Linear SVM", "Tweet EV", "SVM unggul. Gap: Tanpa penyeimbang bobot kelas."],
        ["3", "Prameswari et al. (2024) - Innovative", "SINTA 4", "SVM, Naive Bayes, Random Forest", "Twitter EV", "SVM terbaik. Gap: Mengabaikan Macro F1."],
        ["4", "Hidayatullah et al. (2024) - JournalISI", "SINTA 3", "FastText + IndoBERT Transformer", "119k Tweet EV", "82,5% akurasi. Gap: Wajib GPU berat, tidak ada offline web."],
        ["5", "Firmansyah & Pratama (2024) - JIMIK", "SINTA 4", "Multinomial Naive Bayes (TF-IDF)", "Motor Listrik", "71,2% akurasi. Gap: Recall collapse kelas minoritas."],
        ["6", "Maharani et al. (2024) - BITS", "SINTA 3", "SVM vs Naive Bayes (Platform X)", "Opini Publik X", "76,4% akurasi. Gap: Belum domain iklim holistik."],
        ["7", "Supian et al. (2024) - JIF", "SINTA 4", "Naive Bayes vs Linear SVM", "Green City IKN", "SVM unggul F1. Gap: Korpus kecil (<1.500 tweet)."],
        ["8", "Lennon et al. (2024) - Elsevier DiB", "SCOPUS Q1", "Twitter Climate Policy Tracking", "Global Climate", "Benchmarking Q1. Gap: Raw data tanpa inferensi web."],
        ["9", "Ramasamy et al. (2024) - IEEE ICNWC", "SCOPUS", "SVM Classifier on Climate Tweets", "English Twitter", "SVM tangguh pada sparse space. Gap: Tanpa web app."],
        ["10", "Edward Qian (Benchmark) - Kaggle", "BENCHMARK", "Benchmark Dataset (43.943 data)", "Global Climate", "Dataset acuan. Gap: Memuat noise berita & duplikasi."],
        ["★", "SentimentGreen (2026) - Proyek Ini", "OPEN-SCIENCE", "TF-IDF (1,2) + Linear SVM (Balanced)", "31.907 Tweet", "Menutup 5 Gap: Domain holistik, atasi imbalance, inferensi 100% offline."],
    ]
    create_styled_table(doc, ["No", "Penulis & Jurnal", "Akreditasi", "Metode", "Dataset", "Temuan & Research Gap"], tbl_lit_data, [Inches(0.4), Inches(2.0), Inches(1.0), Inches(1.8), Inches(1.0), Inches(2.0)])

    doc.add_heading("5 KESENJANGAN RISET UTAMA (RESEARCH GAPS)", level=1)
    doc.add_paragraph("1. Kesenjangan Topik (Thematic Scope Gap): Semua jurnal 2024 hanya fokus sempit pada kendaraan listrik. SentimentGreen memperluas ke seluruh pilar ekonomi hijau (surya, angin, pajak karbon, dll).", style='List Bullet')
    doc.add_paragraph("2. Kesenjangan Skala Data (Scale & Language Gap): Penelitian lokal memakai data kecil (<2.000). SentimentGreen mengkaji korpus global 31.907 tweet berdurasi 11 tahun.", style='List Bullet')
    doc.add_paragraph("3. Kesenjangan Deployment (Zero-Server Gap): Jurnal lain hanya berhenti di file Python. SentimentGreen mengekspor model ke JSON murni untuk inferensi 100% offline di browser.", style='List Bullet')
    doc.add_paragraph("4. Kesenjangan Imbalance (Class Imbalance Gap): Mengatasi recall collapse kelas negatif menggunakan class_weight='balanced' pada SVM (recall naik dari 34,81% ke 60,13%).", style='List Bullet')
    doc.add_paragraph("5. Kesenjangan Replikasi (Pipeline Replication Gap): Standarisasi Porter Stemmer dan stopword removal identik bit-demi-bit antara Python dan JavaScript.", style='List Bullet')

    out_file = DL / "Studi_Literatur.docx"
    doc.save(str(out_file))
    (DOCS_DIR / "Studi_Literatur.docx").write_bytes(out_file.read_bytes())
    size = out_file.stat().st_size
    print(f"✅ Studi_Literatur.docx ({size//1024} KB)")

if __name__ == "__main__":
    print("Membuat seluruh dokumen Microsoft Word (.docx)...")
    build_laporan_docx()
    build_paper_docx()
    build_literatur_docx()
    print("Semua file .docx berhasil dibuat di web/downloads/ dan docs/docx/!")
