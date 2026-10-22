# -*- coding: utf-8 -*-
"""
Modul pembelajaran Analisis Kemiskinan & Ketimpangan Indonesia 2026 —
landscape A4, gaya pro pemula, Bahasa Indonesia sederhana, banyak visual.
Angka dibaca dari findings.json. Output: Modul-Analisis-Kemiskinan.pdf
"""
import json
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
F = json.load(open(os.path.join(ROOT, "findings.json")))

RED = colors.HexColor("#A63D40"); DEEP = colors.HexColor("#5E262B")
PUMPKIN = colors.HexColor("#E07B39"); OAT = colors.HexColor("#FAF6EF")
SLATE = colors.HexColor("#2E2A26"); GREY = colors.HexColor("#6E6258")
LIGHT = colors.HexColor("#F3EADB"); TAUPE = colors.HexColor("#C08552")
WHITE = colors.white

W, H = landscape(A4)  # 29.7 x 21 cm

H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=25, leading=31,
                    textColor=DEEP, spaceAfter=6)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=16.5, leading=21,
                    textColor=DEEP, spaceBefore=4, spaceAfter=5)
BODY = ParagraphStyle("BODY", fontName="Helvetica", fontSize=11.5, leading=16,
                      textColor=SLATE, spaceAfter=6)
SMALL = ParagraphStyle("SMALL", fontName="Helvetica", fontSize=9.5, leading=13,
                       textColor=GREY)
CALLOUT = ParagraphStyle("CALLOUT", fontName="Helvetica", fontSize=11.5,
                         leading=16, textColor=SLATE)
BOLD = ParagraphStyle("BOLD", parent=BODY, fontName="Helvetica-Bold")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DEEP)
    canvas.rect(0, 0, W, 0.85 * cm, stroke=0, fill=1)
    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawString(1.4 * cm, 0.32 * cm,
                      "Modul Analisis Kemiskinan & Ketimpangan Indonesia 2026 — Data: BPS (BRS Profil Kemiskinan & Gini)")
    canvas.drawRightString(W - 1.4 * cm, 0.32 * cm, f"Halaman {doc.page}")
    canvas.restoreState()


def img(name, w):
    from PIL import Image as PILImage
    p = os.path.join(CH, name)
    iw, ih = PILImage.open(p).size
    return Image(p, width=w, height=w * ih / iw)


def callout(text, bg=LIGHT, bar=RED):
    t = Table([[Paragraph(text, CALLOUT)]], colWidths=[W - 3.4 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("LINEBEFORE", (0, 0), (0, -1), 3.5, bar),
        ("LEFTPADDING", (0, 0), (-1, -1), 12), ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def kpi_table():
    data = [[Paragraph("<b>Persen Miskin<br/>Mar 2026</b>", SMALL),
             Paragraph("<b>Jumlah Miskin<br/>Mar 2026</b>", SMALL),
             Paragraph("<b>Garis Kemiskinan<br/>Mar 2026</b>", SMALL),
             Paragraph("<b>Gini Ratio<br/>Mar 2026</b>", SMALL)],
            [Paragraph("<b><font size=17 color='#A63D40'>8,07%</font></b>", BODY),
             Paragraph("<b><font size=17 color='#A63D40'>22,93 jt</font></b>", BODY),
             Paragraph("<b><font size=17 color='#A63D40'>Rp669.235</font></b>", BODY),
             Paragraph("<b><font size=17 color='#A63D40'>0,368</font></b>", BODY)],
            [Paragraph("Mar 2019: 9,41%", SMALL),
             Paragraph("Mar 2019: 25,14 jt", SMALL),
             Paragraph("Mar 2019: Rp425.250", SMALL),
             Paragraph("Mar 2019: 0,382", SMALL)]]
    t = Table(data, colWidths=[(W - 2.8 * cm) / 4] * 4)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#E3D5C3")),
        ("LINEABOVE", (0, 0), (-1, 0), 3, RED),
        ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    return t


story = []

# ---------------------------------------------------------------- sampul isi
story.append(Spacer(1, 1.1 * cm))
story.append(Paragraph("Memahami Kemiskinan &amp; Ketimpangan Indonesia", H1))
story.append(Paragraph(
    "Modul belajar analisis data untuk pemula: membaca angka kemiskinan resmi "
    "BPS dari 2019 sampai 2026, memahami arti garis kemiskinan, indeks "
    "kedalaman, dan Gini Ratio — lalu merakitnya menjadi dashboard Power BI.", BODY))
story.append(kpi_table())
story.append(Spacer(1, 0.5 * cm))
story.append(callout(
    "<b>Gambaran besarnya:</b> pada Maret 2026, 8,07% penduduk Indonesia "
    "(22,93 juta jiwa) hidup di bawah garis kemiskinan. Ini angka terendah "
    "dalam tujuh tahun. Tetapi cerita lengkapnya tidak sesederhana itu — "
    "modul ini membedahnya satu per satu."))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    "<b>Cara memakai modul ini:</b> baca berurutan. Setiap bab punya satu "
    "grafik utama, penjelasan dengan bahasa sehari-hari, dan kotak "
    "<i>Analogi</i> atau <i>Catatan Analis</i>. Di akhir ada bab praktik "
    "Power BI dan glosarium istilah.", BODY))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 1
story.append(Paragraph("Bab 1 — Apa Itu Kemiskinan Menurut BPS?", H2))
story.append(Paragraph(
    "BPS mengukur kemiskinan dari sisi <b>pengeluaran</b>. Seseorang disebut "
    "miskin bila rata-rata pengeluaran per kapita per bulannya berada di "
    "bawah <b>Garis Kemiskinan (GK)</b>. GK sendiri adalah jumlah dari dua "
    "bagian: Garis Kemiskinan Makanan (GKM) — biaya kebutuhan makanan setara "
    "2.100 kkal per hari — dan Garis Kemiskinan Bukan Makanan (GKBM) — biaya "
    "perumahan, pakaian, pendidikan, kesehatan, dan kebutuhan dasar lain.", BODY))
story.append(img("03_garis_kemiskinan.png", 19.5 * cm))
story.append(callout(
    "<b>Analogi:</b> garis kemiskinan itu seperti garis finis limbo — "
    "batangnya naik terus (Rp425 ribu di Mar 2019 menjadi Rp669 ribu di "
    "Mar 2026) karena harga kebutuhan pokok naik. Kabar baiknya: makin "
    "banyak orang yang berhasil melewati batang yang makin tinggi itu.",
    bar=PUMPKIN))
story.append(Paragraph(
    "Pada Maret 2026, 74,70% dari garis kemiskinan adalah makanan. Artinya "
    "kemiskinan di Indonesia masih sangat ditentukan oleh harga pangan — "
    "penyumbang terbesarnya adalah beras, disusul rokok kretek filter. "
    "Inilah mengapa proyek portofolio Harga Pangan dan proyek ini saling "
    "berkaitan.", BODY))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 2
story.append(Paragraph("Bab 2 — Tujuh Tahun: Pandemi, Puncak, dan Pemulihan", H2))
story.append(img("01_tren_nasional.png", 20.5 * cm))
story.append(Paragraph(
    "BPS merilis angka kemiskinan dua kali setahun, untuk kondisi <b>Maret</b> "
    "dan <b>September</b>. Dari 2019 sampai 2026 ada 14 periode (September "
    "2023 tidak diterbitkan BPS). Garis merah menunjukkan persentase "
    "penduduk miskin (P0), batang menunjukkan jumlahnya dalam juta jiwa.", BODY))
story.append(callout(
    "<b>Tiga babak cerita:</b> (1) sebelum pandemi kemiskinan turun perlahan "
    "ke 9,22% (Sep 2019); (2) pandemi mendorongnya ke puncak 10,19% atau "
    "27,55 juta jiwa pada Sep 2020; (3) setelah itu turun nyaris tanpa jeda "
    "hingga 8,07% pada Mar 2026. Persentase pertama kali kembali di bawah "
    "level prapandemi pada Mar 2023 (9,36%)."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 3
story.append(Paragraph("Bab 3 — Kota vs Desa: Dua Wajah Kemiskinan", H2))
story.append(img("04_kota_desa.png", 20 * cm))
story.append(Paragraph(
    "Persentase kemiskinan perdesaan (10,67% pada Mar 2026) selalu jauh di "
    "atas perkotaan (6,34%). Tetapi jangan tertipu persen: karena penduduk "
    "kota sangat banyak, jumlah penduduk miskinnya terbagi nyaris rata — "
    "12,10 juta di desa dan 10,83 juta di kota.", BODY))
story.append(img("05_gap_kota_desa.png", 19 * cm))
story.append(callout(
    "<b>Catatan Analis:</b> selisih (gap) desa-kota menyempit dari 6,16 poin "
    "persen (Mar 2019) ke 4,33 poin (Mar 2026). Menyempitnya gap adalah kabar "
    "baik ganda: kemiskinan turun <i>dan</i> distribusinya antarwilayah "
    "makin merata."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 4
story.append(Paragraph("Bab 4 — Ketimpangan: Mengenal Gini Ratio", H2))
story.append(img("06_gini.png", 20 * cm))
story.append(Paragraph(
    "<b>Gini Ratio</b> mengukur ketimpangan pengeluaran: 0 berarti semua "
    "orang pengeluarannya sama persis, 1 berarti satu orang menguasai semua "
    "pengeluaran. Indonesia berada di 0,368 pada Mar 2026 — kategori "
    "ketimpangan sedang. Gini perkotaan (0,387) selalu lebih tinggi daripada "
    "perdesaan (0,296): di desa pengeluaran warga lebih seragam.", BODY))
story.append(callout(
    "<b>Pelajaran penting:</b> kemiskinan dan ketimpangan bisa bergerak "
    "berlawanan. Semester Sep 2025 ke Mar 2026 kemiskinan turun ke rekor "
    "terendah, tetapi Gini naik dari 0,363 ke 0,368. Artinya perbaikan "
    "semester itu lebih banyak dinikmati kelompok pengeluaran atas. "
    "Indikator pendampingnya: pangsa pengeluaran 40% penduduk terbawah "
    "sebesar 19,22% pada Mar 2026 (kota hanya 18,31%, desa 22,24%).",
    bar=PUMPKIN))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 5
story.append(Paragraph("Bab 5 — Seberapa Dalam Kemiskinannya? (P1 &amp; P2)", H2))
story.append(Paragraph(
    "Persentase (P0) hanya menghitung <i>berapa banyak</i> orang miskin. "
    "Dua indeks lain mengukur kualitasnya: <b>Indeks Kedalaman (P1)</b> — "
    "rata-rata jarak pengeluaran penduduk miskin dari garis kemiskinan; "
    "makin kecil makin dangkal. <b>Indeks Keparahan (P2)</b> — ketimpangan "
    "pengeluaran di antara sesama penduduk miskin; makin kecil makin merata.", BODY))
story.append(img("10_p1_p2.png", 20 * cm))
story.append(img("11_p1_kota_desa.png", 18.5 * cm))
story.append(callout(
    "<b>Sinyal yang mudah terlewat:</b> P1 turun 27,5% dari puncak pandemi "
    "(1,75 menjadi 1,268). Tetapi di semester terakhir, P1 perdesaan justru "
    "naik dari 1,661 ke 1,744 saat kota membaik. Jumlah orang miskin desa "
    "berkurang, tetapi yang tersisa makin jauh di bawah garis — kelompok "
    "inilah yang paling sulit dijangkau program bantuan biasa."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 6
story.append(Paragraph("Bab 6 — Peta Provinsi: Jurang di Satu Negara", H2))
story.append(img("07_provinsi_mar2026.png", 13.2 * cm))
story.append(Paragraph(
    "Pada Maret 2026 provinsi dengan kemiskinan tertinggi adalah Papua "
    "Tengah (30,41%) dan terendah Bali (3,44%) — jurang 26,97 poin persen "
    "atau 8,8 kali lipat. Sebanyak 20 dari 38 provinsi masih berada di atas "
    "rata-rata nasional 8,07%.", BODY))
story.append(PageBreak())
story.append(Paragraph("Bab 6 (lanjutan) — Siapa Membaik, Siapa Tertinggal?", H2))
story.append(img("08_perubahan_provinsi.png", 13.2 * cm))
story.append(Paragraph(
    "Membandingkan Maret 2019 dengan Maret 2026 untuk 32 provinsi yang "
    "wilayahnya tidak berubah (Papua dikecualikan karena pemekaran 2022): "
    "28 provinsi membaik. Perbaikan terbesar di NTT (turun 3,57 poin). "
    "Empat provinsi justru naik: DKI Jakarta (+0,49), Banten (+0,29), "
    "Kepulauan Bangka Belitung (+0,13), dan Kalimantan Tengah (+0,11). "
    "DKI Jakarta menarik: pada 2019 ia yang terendah (3,47%), lalu posisinya "
    "digeser Bali.", BODY))
story.append(img("09_jumlah_pulau.png", 19 * cm))
story.append(callout(
    "<b>Persentase vs jumlah:</b> provinsi berpersentase rendah bisa "
    "menyumbang jumlah terbesar. Jawa Timur (9,06%) memiliki 3,71 juta "
    "penduduk miskin — terbanyak se-Indonesia. Total 52,4% penduduk miskin "
    "Indonesia tinggal di Pulau Jawa."))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 7
story.append(Paragraph("Bab 7 — Praktik: Merakit Dashboard Power BI", H2))
story.append(Paragraph(
    "Folder <b>powerbi/</b> pada proyek ini berisi kit siap rakit menjadi "
    "file <b>Kemiskinan-Indonesia-2026.pbix</b>. Modelnya berbentuk bintang "
    "(star schema): empat tabel fakta dengan grain terpisah — nasional per "
    "periode, kota/desa per periode, Gini per periode, provinsi per periode — "
    "dihubungkan ke dimensi periode dan dimensi provinsi.", BODY))
story.append(img("../powerbi/dashboard_preview_halaman1.png", 21 * cm) if False else
             Image(os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"),
                   width=21 * cm, height=21 * cm * 0.5625))
story.append(Paragraph(
    "<b>Langkah singkat:</b> (1) muat 6 CSV dari folder powerbi; (2) buat 5 "
    "relasi sesuai build_guide.md; (3) urutkan kolom periode menurut kolom "
    "urutan agar Maret selalu sebelum September; (4) buat 17 measure dari "
    "measures_dax.md dan cocokkan dengan tabel verifikasinya; (5) susun 4 "
    "halaman mengikuti dashboard_layout.md.", BODY))
story.append(callout(
    "<b>Tiga jebakan pemula:</b> jangan menjumlahkan kolom persen (selalu "
    "rata-rata); selalu filter periode sebelum membaca peringkat provinsi "
    "(satu tabel berisi 5 periode); dan jangan mencampur satuan ribu "
    "(provinsi) dengan juta (nasional) dalam satu visual.",
    bar=PUMPKIN))
story.append(PageBreak())

# ---------------------------------------------------------------- bab 8
story.append(Paragraph("Bab 8 — SQL &amp; Notebook: Mengolahnya Sendiri", H2))
story.append(Paragraph(
    "File <b>sql/queries.sql</b> berisi kueri analitis atas CSV kompilasi: "
    "tren nasional, gap kota-desa per periode, peringkat provinsi terbaru, "
    "perubahan 2019 ke 2026, dan provinsi di atas rata-rata nasional. "
    "Notebook <b>analysis.ipynb</b> mereproduksi seluruh angka temuan dari "
    "CSV yang sama, sehingga semua klaim di modul ini bisa kamu periksa "
    "ulang baris demi baris.", BODY))
story.append(Paragraph("<b>Latihan untukmu:</b>", BOLD))
story.append(Paragraph(
    "1. Dengan SQL, temukan periode ketika jumlah penduduk miskin kota "
    "pertama kali turun di bawah 11 juta setelah pandemi.<br/>"
    "2. Hitung berapa poin Gini kota berubah dari Mar 2019 ke Mar 2026, dan "
    "bandingkan dengan perubahan Gini desa.<br/>"
    "3. Provinsi mana yang garis kemiskinannya tertinggi pada Mar 2026, dan "
    "berapa kali lipat garis kemiskinan provinsi terendah?<br/>"
    "4. Jelaskan dengan bahasamu sendiri: mengapa P1 desa bisa naik saat "
    "persentase kemiskinan desa turun?", BODY))
story.append(callout(
    "<b>Kunci singkat:</b> (1) Maret 2026 (10,83 juta) — pada semua periode "
    "setelah pandemi sebelumnya jumlah kota masih di atas 11 juta (terendah "
    "Sep 2024: 11,05 juta). (2) Kota 0,392 ke "
    "0,387 (turun 0,005); desa 0,317 ke 0,296 (turun 0,021) — desa membaik "
    "lebih cepat. (3) Papua Pegunungan Rp1.275.343, sekitar 2,5 kali "
    "Sulawesi Barat Rp519.404. (4) Karena yang berhasil keluar dari "
    "kemiskinan biasanya yang paling dekat ke garis; yang tersisa rata-rata "
    "lebih jauh di bawah garis.", bg=colors.HexColor("#FDF6EC")))
story.append(PageBreak())

# ---------------------------------------------------------------- glosarium
story.append(Paragraph("Glosarium &amp; Sumber", H2))
story.append(Paragraph(
    "<b>P0</b> — persentase penduduk miskin (headcount ratio). "
    "<b>P1</b> — indeks kedalaman kemiskinan. <b>P2</b> — indeks keparahan "
    "kemiskinan. <b>Garis Kemiskinan (GK)</b> — pengeluaran minimum per "
    "kapita per bulan agar tidak disebut miskin. <b>GKM/GKBM</b> — komponen "
    "makanan dan bukan makanan dari GK. <b>Gini Ratio</b> — ukuran "
    "ketimpangan pengeluaran 0 sampai 1. <b>Poin persen (pp)</b> — selisih "
    "aritmetika dua persentase. <b>Susenas</b> — Survei Sosial Ekonomi "
    "Nasional, sumber data BPS untuk kemiskinan dan Gini. <b>BRS</b> — "
    "Berita Resmi Statistik, format rilis resmi BPS.", BODY))
story.append(Paragraph(
    "<b>Sumber data:</b> seluruh angka dikompilasi dari BRS BPS Profil "
    "Kemiskinan di Indonesia (edisi Maret 2020, 2021, 2022, 2023, 2025, dan "
    "2026; No. 80/08/Th. XXIX untuk edisi terbaru), BRS Tingkat Ketimpangan "
    "Pengeluaran Penduduk Indonesia (termasuk No. 20/02/Th. XXIX, 5 Februari "
    "2026), dan publikasi BPS Penghitungan dan Analisis Kemiskinan Makro "
    "Indonesia 2019. Rincian per angka ada di data/SOURCES.md pada repo. "
    "Catatan cakupan: P1/P2 tahun 2019 tidak terverifikasi sehingga seri "
    "indeks mulai Maret 2020; jumlah penduduk miskin provinsi Maret 2019 "
    "lengkap hanya untuk 18 provinsi; perbandingan provinsi 2019 ke 2026 "
    "dibatasi 32 provinsi yang wilayahnya sebanding.", BODY))
story.append(Spacer(1, 0.5 * cm))
story.append(callout(
    "<b>Penutup:</b> angka kemiskinan bukan sekadar statistik — ia adalah "
    "ringkasan jutaan keputusan rumah tangga. Tugas analis adalah membacanya "
    "dengan jujur: merayakan penurunan 8,07% sambil tetap menunjuk klaster "
    "Papua, kedalaman desa, dan Gini yang berbalik arah. Selamat — kamu "
    "baru saja membaca satu laporan kemiskinan utuh seperti analis "
    "sungguhan.",
    bar=PUMPKIN))
story.append(Spacer(1, 0.4 * cm))
story.append(Paragraph(
    "Disusun oleh BAGHIZ ASSHIDDIQIE ARASYA — Data Analyst. "
    "Repo: github.com/baghizash/kemiskinan-indonesia-2026", SMALL))

doc = SimpleDocTemplate(os.path.join(ROOT, "Modul-Analisis-Kemiskinan.pdf"),
                        pagesize=landscape(A4), leftMargin=1.4 * cm,
                        rightMargin=1.4 * cm, topMargin=1.2 * cm,
                        bottomMargin=1.3 * cm,
                        title="Modul Analisis Kemiskinan & Ketimpangan Indonesia 2026",
                        author="Baghiz Asshiddiqie Arasya")
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print("PDF modul tertulis")
