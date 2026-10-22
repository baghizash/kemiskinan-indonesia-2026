# -*- coding: utf-8 -*-
"""
Membangun PPT portofolio Kemiskinan & Ketimpangan Indonesia 2026 (10 slide,
16:9) — standar deck terbaru: panel angka hero di sampul, chip KPI, slide
temuan, slide 9 pratinjau Dashboard Power BI, slide 10 Designed Close.
Semua angka dibaca dari findings.json (hasil analysis.py).
"""
import json
import os

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Cm, Pt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
CH = os.path.join(ROOT, "charts")
F = json.load(open(os.path.join(ROOT, "findings.json")))

RED = RGBColor(0xA6, 0x3D, 0x40); DEEP = RGBColor(0x5E, 0x26, 0x2B)
PUMPKIN = RGBColor(0xE0, 0x7B, 0x39); OAT = RGBColor(0xFA, 0xF6, 0xEF)
WHITE = RGBColor(0xFF, 0xFF, 0xFF); SLATE = RGBColor(0x2E, 0x2A, 0x26)
GREY = RGBColor(0x6E, 0x62, 0x58); LIGHT = RGBColor(0xEF, 0xE4, 0xD8)

prs = Presentation()
prs.slide_width = Cm(33.867); prs.slide_height = Cm(19.05)
BLANK = prs.slide_layouts[6]


def slide(bg=OAT):
    s = prs.slides.add_slide(BLANK)
    r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
    r.fill.solid(); r.fill.fore_color.rgb = bg; r.line.fill.background()
    r.shadow.inherit = False
    return s


def box(s, x, y, w, h, fill=None, line=None):
    r = s.shapes.add_shape(1, Cm(x), Cm(y), Cm(w), Cm(h))
    if fill is None:
        r.fill.background()
    else:
        r.fill.solid(); r.fill.fore_color.rgb = fill
    if line is None:
        r.line.fill.background()
    else:
        r.line.color.rgb = line; r.line.width = Pt(1)
    r.shadow.inherit = False
    return r


def txt(s, x, y, w, h, text, size=14, bold=False, color=SLATE, align=PP_ALIGN.LEFT):
    tb = s.shapes.add_textbox(Cm(x), Cm(y), Cm(w), Cm(h))
    tf = tb.text_frame; tf.word_wrap = True
    lines = text.split("\n")
    tf.paragraphs[0].text = lines[0]; tf.paragraphs[0].alignment = align
    for ln in lines[1:]:
        p = tf.add_paragraph(); p.text = ln; p.alignment = align
    for p in tf.paragraphs:
        p.font.size = Pt(size); p.font.bold = bold; p.font.color.rgb = color
        p.font.name = "Calibri"
    return tb


def title_bar(s, title, sub=None):
    box(s, 0, 0, 33.87, 2.5, fill=DEEP)
    txt(s, 1.2, 0.42, 31.5, 1.1, title, size=25, bold=True, color=WHITE)
    if sub:
        txt(s, 1.2, 1.42, 31.5, 0.8, sub, size=13, color=RGBColor(0xEA, 0xD9, 0xC8))


def bullets(s, x, y, w, items, size=15, gap=0.35):
    cy = y
    for head, body in items:
        txt(s, x, cy, 0.5, 0.7, "▪", size=size, bold=True, color=RED)
        txt(s, x + 0.6, cy, w - 0.6, 1.6, head, size=size, bold=True, color=DEEP)
        cy += 0.78
        if body:
            txt(s, x + 0.6, cy, w - 0.6, 1.8, body, size=size - 1.5, color=SLATE)
            cy += 0.62 + 0.55 * (len(body) // 62)
        cy += gap
    return cy


def pic(s, path, x, y, w=None, h=None):
    kw = {}
    if w: kw["width"] = Cm(w)
    if h: kw["height"] = Cm(h)
    return s.shapes.add_picture(path, Cm(x), Cm(y), **kw)


def chip(s, x, y, w, label, value, sub):
    box(s, x, y, w, 3.1, fill=WHITE, line=LIGHT)
    box(s, x, y, w, 0.18, fill=RED)
    txt(s, x + 0.35, y + 0.32, w - 0.7, 0.6, label, size=11.5, bold=True, color=GREY)
    txt(s, x + 0.35, y + 0.95, w - 0.7, 1.0, value, size=25, bold=True, color=RED)
    txt(s, x + 0.35, y + 2.05, w - 0.7, 0.9, sub, size=11, color=SLATE)


def footer(s, n):
    txt(s, 29.9, 18.35, 3.4, 0.5, f"{n} / 10", size=10, color=GREY, align=PP_ALIGN.RIGHT)
    txt(s, 1.2, 18.35, 12, 0.5, "Kemiskinan & Ketimpangan Indonesia 2026 • Data BPS",
        size=10, color=GREY)


# ================================================================ 1 · sampul
s = slide(bg=DEEP)
box(s, 0, 0, 19.6, 19.05, fill=DEEP)
txt(s, 1.4, 2.2, 17.5, 1.0, "PORTOFOLIO ANALISIS DATA", size=15, bold=True, color=PUMPKIN)
txt(s, 1.4, 3.3, 17.8, 3.4, "Kemiskinan &\nKetimpangan\nIndonesia 2026", size=43,
    bold=True, color=WHITE)
txt(s, 1.4, 8.3, 17.2, 2.6,
    "Mengurai tujuh tahun perjalanan kemiskinan Indonesia — dari 9,41% sebelum "
    "pandemi, memuncak 10,19% di September 2020, hingga rekor terendah 8,07% "
    "pada Maret 2026 — lengkap dengan ketimpangan, kedalaman, dan peta provinsi.",
    size=15.5, color=RGBColor(0xEF, 0xE4, 0xD8))
box(s, 1.4, 12.2, 16.8, 0.06, fill=PUMPKIN)
txt(s, 1.4, 12.7, 17.5, 2.2,
    "Sumber: BPS — Berita Resmi Statistik Profil Kemiskinan & Gini Ratio\n"
    "Periode: Maret & September 2019 sampai Maret 2026 (14 periode)",
    size=13, color=RGBColor(0xD8, 0xC6, 0xB4))
box(s, 20.6, 0, 13.27, 19.05, fill=RED)
txt(s, 21.8, 2.3, 11, 1.0, "PENDUDUK MISKIN\nMARET 2026", size=14, bold=True,
    color=RGBColor(0xF6, 0xDD, 0xD5))
txt(s, 21.8, 4.6, 11.4, 2.2, "8,07%", size=60, bold=True, color=WHITE)
txt(s, 21.8, 7.1, 11, 1.0, "22,93 juta jiwa — terendah dalam seri 2019–2026",
    size=14, color=RGBColor(0xF6, 0xDD, 0xD5))
box(s, 21.8, 8.6, 10, 0.05, fill=RGBColor(0xD8, 0x8A, 0x8E))
txt(s, 21.8, 9.1, 11, 3.4,
    "Gini Ratio Maret 2026: 0,368\n"
    "Garis kemiskinan: Rp669.235/kapita/bln\n"
    "Provinsi tertinggi: Papua Tengah 30,41%\n"
    "Provinsi terendah: Bali 3,44%",
    size=14.5, color=WHITE)
txt(s, 21.8, 15.6, 11, 1.6, "BAGHIZ ASSHIDDIQIE ARASYA\nData Analyst",
    size=14, bold=True, color=WHITE)

# ================================================================ 2 · KPI
s = slide()
title_bar(s, "Potret Terbaru: Maret 2026",
          "Empat angka kunci dari BRS Profil Kemiskinan Maret 2026 (rilis 5 Agustus 2026)")
chip(s, 1.2, 3.4, 7.5, "PERSENTASE PENDUDUK MISKIN", "8,07%",
     "Turun 1,34 poin dari Mar 2019 (9,41%)")
chip(s, 9.3, 3.4, 7.5, "JUMLAH PENDUDUK MISKIN", "22,93 jt",
     "2,21 juta lebih sedikit dari Mar 2019")
chip(s, 17.4, 3.4, 7.5, "GARIS KEMISKINAN", "Rp669.235",
     "Per kapita/bulan; 74,7% makanan")
chip(s, 25.5, 3.4, 7.2, "GINI RATIO", "0,368",
     "Kota 0,387 • Desa 0,296")
bullets(s, 1.2, 7.6, 31.4, [
    ("Titik terendah dalam tujuh tahun",
     "Baik persentase (8,07%) maupun jumlah (22,93 juta) pada Maret 2026 adalah "
     "yang terendah di seluruh seri Maret & September 2019–2026."),
    ("Kemiskinan desa tetap hampir dua kali kota",
     "Perdesaan 10,67% berbanding perkotaan 6,34% pada Maret 2026, tetapi "
     "kesenjangannya menyempit dari 6,16 poin (Mar 2019) menjadi 4,33 poin."),
    ("Satu semester yang janggal untuk dibaca bersama",
     "Maret 2026 kemiskinan turun ke rekor terendah, tetapi Gini justru naik "
     "dari titik terendahnya di September 2025 (0,363 ke 0,368) dan indeks "
     "kedalaman perdesaan memburuk. Detailnya di slide 7 dan 8."),
], size=15.5)
footer(s, 2)

# ================================================================ 3 · tren & pandemi
s = slide()
title_bar(s, "Tujuh Tahun: Lonjakan Pandemi, Lalu Turun Konsisten",
          "Persentase dan jumlah penduduk miskin, Maret & September 2019–2026")
pic(s, os.path.join(CH, "01_tren_nasional.png"), 1.2, 3.1, w=19.6)
bullets(s, 21.6, 3.4, 11.0, [
    ("Puncak pandemi: Sep 2020, 10,19%",
     "27,55 juta penduduk miskin — bertambah 2,41 juta jiwa hanya dalam tujuh "
     "bulan pertama pandemi (Mar–Sep 2020)."),
    ("Kembali di bawah prapandemi: Mar 2023",
     "Butuh 2,5 tahun sejak puncak hingga persentase menembus ke bawah 9,41% "
     "(Mar 2019), yaitu 9,36% pada Maret 2023."),
    ("Setelah itu turun nyaris tanpa jeda",
     "Dari 9,36% (Mar 2023) ke 8,07% (Mar 2026). Catatan: tidak ada periode "
     "September 2023 karena BPS tidak menerbitkannya — bukan data hilang."),
], size=14.5)
footer(s, 3)

# ================================================================ 4 · garis kemiskinan
s = slide()
title_bar(s, "Garis Kemiskinan Naik 57,4% dalam 7 Tahun",
          "Ambang pengeluaran minimum ikut bergerak — dan makanan mendominasi")
pic(s, os.path.join(CH, "03_garis_kemiskinan.png"), 1.2, 3.1, w=19.6)
bullets(s, 21.6, 3.4, 11.0, [
    ("Rp425.250 menjadi Rp669.235",
     "Kenaikan 57,4% dari Mar 2019 ke Mar 2026, setara pertumbuhan majemuk "
     "sekitar 6,7% per tahun — garis kemiskinan pada dasarnya mengikuti "
     "harga kebutuhan pokok."),
    ("74,7% adalah makanan",
     "Pangsa komoditas makanan dalam garis kemiskinan Maret 2026 sebesar "
     "74,70%; penyumbang terbesarnya beras, disusul rokok kretek filter."),
    ("Artinya untuk membaca tren",
     "Penduduk miskin berkurang bukan karena ambangnya diturunkan — ambangnya "
     "justru naik tajam, sehingga penurunan ini mencerminkan pengeluaran "
     "nyata yang membaik, bukan definisi yang melonggar."),
], size=14.5)
footer(s, 4)

# ================================================================ 5 · kota desa
s = slide()
title_bar(s, "Kota vs Desa: Kesenjangan Menyempit, Belum Hilang",
          "Persentase penduduk miskin menurut daerah, 2019–2026")
pic(s, os.path.join(CH, "04_kota_desa.png"), 1.2, 3.1, w=19.6)
bullets(s, 21.6, 3.4, 11.0, [
    ("Desa selalu sekitar dua kali kota",
     "Rasio perdesaan terhadap perkotaan turun dari 1,92× (Mar 2019) menjadi "
     "1,68× (Mar 2026) — tetap besar, tetapi terus mengecil."),
    ("Namun jumlahnya terbagi nyaris rata",
     "Maret 2026: 12,10 juta penduduk miskin di desa dan 10,83 juta di kota. "
     "Kemiskinan kota bukan isu kecil — hanya persentasenya yang lebih rendah "
     "karena penduduk kota jauh lebih banyak."),
    ("Gap menyempit 1,83 poin",
     "Selisih desa minus kota menyusut dari 6,16 poin (Mar 2019) ke 4,33 poin "
     "(Mar 2026), penyempitan paling konsisten di seluruh seri."),
], size=14.5)
footer(s, 5)

# ================================================================ 6 · gini
s = slide()
title_bar(s, "Ketimpangan: Menyempit Perlahan, Sempat Berbalik Arah",
          "Gini Ratio pengeluaran, Maret & September 2019–2026")
pic(s, os.path.join(CH, "06_gini.png"), 1.2, 3.1, w=19.6)
bullets(s, 21.6, 3.4, 11.0, [
    ("0,382 menjadi 0,368",
     "Selama tujuh tahun Gini turun 0,014 poin — menyempit, tetapi sangat "
     "perlahan, dengan puncak ketimpangan di Maret 2023 (0,388)."),
    ("Kota jauh lebih timpang dari desa",
     "Maret 2026: Gini perkotaan 0,387 berbanding perdesaan 0,296. Kesenjangan "
     "pengeluaran adalah fenomena perkotaan."),
    ("Sinyal waspada Maret 2026",
     "Gini naik dari 0,363 (Sep 2025, terendah) ke 0,368 di saat kemiskinan "
     "mencapai rekor terendah — hasil pertumbuhan semester itu dinikmati lebih "
     "banyak oleh kelompok atas. Pangsa pengeluaran 40% terbawah: 19,22%."),
], size=14.5)
footer(s, 6)

# ================================================================ 7 · kedalaman
s = slide()
title_bar(s, "Bukan Hanya Lebih Sedikit — Kemiskinannya Juga Lebih Dangkal",
          "Indeks kedalaman (P1) dan keparahan (P2), Maret 2020–2026")
pic(s, os.path.join(CH, "10_p1_p2.png"), 1.2, 3.1, w=19.6)
bullets(s, 21.6, 3.4, 11.0, [
    ("P1 turun 27,5% dari puncak pandemi",
     "Indeks kedalaman turun dari 1,75 (Sep 2020) ke 1,268 (Mar 2026): "
     "rata-rata pengeluaran penduduk miskin makin dekat ke garis kemiskinan."),
    ("P2 juga membaik: 0,47 menjadi 0,291",
     "Ketimpangan di antara sesama penduduk miskin menyusut — kelompok paling "
     "miskin tidak tertinggal sejauh saat pandemi."),
    ("Tapi desa memberi sinyal berlawanan",
     "Semester terakhir (Sep 2025 ke Mar 2026) P1 perdesaan naik dari 1,661 ke "
     "1,744 saat P1 kota turun. Penduduk miskin desa yang tersisa justru makin "
     "jauh di bawah garis — sasaran bantuan perlu dibaca per wilayah."),
], size=14.5)
footer(s, 7)

# ================================================================ 8 · provinsi
s = slide()
title_bar(s, "Peta Provinsi: Jurang 27 Poin Persen di Satu Negara",
          "Persentase penduduk miskin per provinsi, Maret 2026")
pic(s, os.path.join(CH, "07_provinsi_mar2026.png"), 1.2, 2.9, h=15.6)
bullets(s, 14.6, 3.2, 18.0, [
    ("Papua Tengah tertinggi: 30,41%",
     "Disusul Papua Pegunungan 26,34%. Enam provinsi kawasan Papua semuanya di "
     "atas 16% — klaster kemiskinan tertinggi Indonesia ada di timur."),
    ("Bali terendah: 3,44%",
     "Jurang tertinggi–terendah mencapai 26,97 poin persen atau 8,8 kali lipat. "
     "Sebanyak 20 dari 38 provinsi masih di atas rata-rata nasional 8,07%."),
    ("Persentase kecil, jumlah raksasa",
     "Jawa Timur hanya 9,06% tetapi penduduk miskinnya terbanyak: 3,71 juta. "
     "Total 52,4% penduduk miskin Indonesia tinggal di Pulau Jawa — intervensi "
     "berskala nasional tidak bisa mengabaikan Jawa."),
    ("Perubahan 2019 ke 2026",
     "Dari 32 provinsi yang wilayahnya sebanding, 28 membaik. Perbaikan "
     "terbesar: NTT (turun 3,57 poin). Empat yang justru naik: DKI Jakarta "
     "(+0,49), Banten (+0,29), Kepulauan Bangka Belitung (+0,13), dan "
     "Kalimantan Tengah (+0,11)."),
], size=14.5)
footer(s, 8)

# ================================================================ 9 · dashboard
s = slide()
title_bar(s, "Dashboard Power BI — Kemiskinan-Indonesia-2026.pbix",
          "Kit siap rakit di folder powerbi/ — model bintang, 17 measure DAX, 4 halaman")
pic(s, os.path.join(ROOT, "powerbi", "dashboard_preview_halaman1.png"), 1.2, 3.0, w=19.4)
bullets(s, 21.4, 3.1, 11.2, [
    ("Halaman 1 — Ringkasan Nasional",
     "Empat kartu KPI Maret 2026, tren persentase & jumlah per periode, "
     "slicer periode."),
    ("Halaman 2 — Kota vs Desa",
     "Garis ganda kota/desa, P1 & P2 per daerah, kartu selisih 4,33 poin."),
    ("Halaman 3 — Provinsi",
     "Bar terurut 38 provinsi, jumlah per provinsi, tabel rinci termasuk "
     "garis kemiskinan provinsi Maret 2026."),
    ("Halaman 4 — Ketimpangan & Kedalaman",
     "Tren Gini total/kota/desa, tren P1/P2, kartu pangsa 40% terbawah."),
    ("Aman dari jebakan klasik",
     "Grain dipisah per tabel fakta, persen selalu dirata-rata (bukan "
     "dijumlah), dan setiap measure punya nilai verifikasi di measures_dax.md."),
], size=13)
footer(s, 9)

# ================================================================ 10 · penutup
s = slide(bg=DEEP)
txt(s, 1.4, 1.6, 31, 1.2, "Kesimpulan", size=30, bold=True, color=WHITE)
box(s, 1.4, 3.0, 16.8, 0.06, fill=PUMPKIN)
items = [
    ("Rekor terendah tujuh tahun",
     "Kemiskinan mencapai 8,07% (22,93 juta jiwa) pada Maret 2026 — pulih penuh "
     "dari lonjakan pandemi 10,19% dan terus menurun sejak Maret 2023."),
    ("Kualitas penurunan juga membaik",
     "Garis kemiskinan naik 57,4%, indeks kedalaman turun 27,5% dari puncak "
     "pandemi, dan kesenjangan kota–desa menyempit ke 4,33 poin."),
    ("Tiga pekerjaan rumah tersisa",
     "Klaster Papua (tertinggi Papua Tengah 30,41% vs Bali 3,44%), kedalaman "
     "desa yang memburuk di semester terakhir, dan Gini yang berbalik naik "
     "dari 0,363 ke 0,368."),
    ("Metode & keterbatasan",
     "Seluruh angka dikompilasi dari BRS BPS dan dapat ditelusur di "
     "data/SOURCES.md. P1/P2 2019 tidak terverifikasi sehingga seri indeks "
     "mulai Mar 2020; perubahan provinsi dibatasi 32 provinsi sebanding."),
]
cy = 3.7
for head, body in items:
    txt(s, 1.4, cy, 0.5, 0.7, "▪", size=16, bold=True, color=PUMPKIN)
    txt(s, 2.0, cy, 29.5, 0.8, head, size=16.5, bold=True, color=WHITE)
    cy += 0.85
    txt(s, 2.0, cy, 29.5, 1.6, body, size=13.5, color=RGBColor(0xEF, 0xE4, 0xD8))
    cy += 0.62 + 0.5 * (len(body) // 95) + 0.55
box(s, 1.4, 16.6, 31.0, 0.05, fill=PUMPKIN)
txt(s, 1.4, 17.0, 31.4, 1.2,
    "Terima kasih — BAGHIZ ASSHIDDIQIE ARASYA • Data Analyst\n"
    "Repo: github.com/baghizash/kemiskinan-indonesia-2026",
    size=14, bold=True, color=WHITE)

OUT = os.path.join(ROOT, "Portofolio-Analisis-Kemiskinan.pptx")
prs.save(OUT)
print("PPTX:", OUT)
