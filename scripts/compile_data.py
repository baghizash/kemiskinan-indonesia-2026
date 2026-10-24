# -*- coding: utf-8 -*-
"""
Kompilasi data Kemiskinan & Ketimpangan Indonesia dari publikasi resmi BPS
(Berita Resmi Statistik Profil Kemiskinan & Tingkat Ketimpangan, berbagai
edisi 2019-2026). Semua angka di bawah ini disalin dari tabel BRS yang
tercantum di data/SOURCES.md — tidak ada angka karangan. Sel kosong berarti
angka tersebut tidak berhasil diverifikasi dari BRS dan sengaja dikosongkan.

Menghasilkan:
  data/kemiskinan_nasional.csv
  data/kemiskinan_kota_desa.csv
  data/gini_nasional.csv
  data/kemiskinan_provinsi.csv
  data/SOURCES.md
"""
import csv
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

# periode: (label, tahun, bulan_ke, urutan)
PERIODE = [
    ("Mar 2019", 2019, 3, 1), ("Sep 2019", 2019, 9, 2),
    ("Mar 2020", 2020, 3, 3), ("Sep 2020", 2020, 9, 4),
    ("Mar 2021", 2021, 3, 5), ("Sep 2021", 2021, 9, 6),
    ("Mar 2022", 2022, 3, 7), ("Sep 2022", 2022, 9, 8),
    ("Mar 2023", 2023, 3, 9), ("Mar 2024", 2024, 3, 10),
    ("Sep 2024", 2024, 9, 11), ("Mar 2025", 2025, 3, 12),
    ("Sep 2025", 2025, 9, 13), ("Mar 2026", 2026, 3, 14),
]
LBL = [p[0] for p in PERIODE]

# ------------------------------------------------------- seri nasional
# label: (persen, jumlah_juta, gk, gkm, gkbm, p1_total, p2_total)
NASIONAL = {
    "Mar 2019": (9.41, 25.14, 425250, 313232, 112018, 1.55, 0.37),
    "Sep 2019": (9.22, 24.78, 440538, 324911, 115627, 1.50, 0.36),
    "Mar 2020": (9.78, 26.42, 454652, 335793, 118859, 1.61, 0.38),
    "Sep 2020": (10.19, 27.55, 458947, 339004, 119943, 1.75, 0.47),
    "Mar 2021": (10.14, 27.54, 472525, 349474, 123051, 1.714, 0.424),
    "Sep 2021": (9.71, 26.50, 486168, 360007, 126161, 1.668, 0.418),
    "Mar 2022": (9.54, 26.16, 505469, 374455, 131014, 1.586, 0.395),
    "Sep 2022": (9.57, 26.36, 535547, 397125, 138422, 1.562, 0.379),
    "Mar 2023": (9.36, 25.90, 550458, 408522, 141936, 1.528, 0.377),
    "Mar 2024": (9.03, 25.22, 582932, 433906, 149026, 1.461, 0.347),
    "Sep 2024": (8.57, 24.06, 595242, 443433, 151809, 1.364, 0.322),
    "Mar 2025": (8.47, 23.85, 609160, 454299, 154861, 1.365, 0.319),
    "Sep 2025": (8.25, 23.36, 641443, 478955, 162488, 1.290, 0.303),
    "Mar 2026": (8.07, 22.93, 669235, 499886, 169349, 1.268, 0.291),
}

# ------------------------------------------------------- kota / desa
# label: (persen, jumlah_juta, p1, p2)
KOTA = {
    "Mar 2019": (6.69, 9.99, 1.05, 0.24), "Sep 2019": (6.56, 9.86, 1.02, 0.23),
    "Mar 2020": (7.38, 11.16, 1.13, 0.25), "Sep 2020": (7.88, 12.04, 1.26, 0.31),
    "Mar 2021": (7.89, 12.18, 1.294, 0.314), "Sep 2021": (7.60, 11.86, 1.229, 0.291),
    "Mar 2022": (7.50, 11.82, 1.187, 0.286), "Sep 2022": (7.53, 11.98, 1.158, 0.264),
    "Mar 2023": (7.29, 11.74, 1.163, 0.281), "Mar 2024": (7.09, 11.64, 1.095, 0.252),
    "Sep 2024": (6.66, 11.05, 0.981, 0.215), "Mar 2025": (6.73, 11.27, 1.061, 0.245),
    "Sep 2025": (6.60, 11.18, 1.040, 0.245), "Mar 2026": (6.34, 10.83, 0.951, 0.209),
}
DESA = {
    "Mar 2019": (12.85, 15.15, 2.18, 0.55), "Sep 2019": (12.60, 14.93, 2.11, 0.53),
    "Mar 2020": (12.82, 15.26, 2.21, 0.55), "Sep 2020": (13.20, 15.51, 2.39, 0.68),
    "Mar 2021": (13.10, 15.37, 2.266, 0.569), "Sep 2021": (12.53, 14.64, 2.253, 0.587),
    "Mar 2022": (12.29, 14.34, 2.125, 0.542), "Sep 2022": (12.36, 14.38, 2.115, 0.536),
    "Mar 2023": (12.22, 14.16, 2.035, 0.511), "Mar 2024": (11.79, 13.58, 1.983, 0.483),
    "Sep 2024": (11.34, 13.01, 1.918, 0.476), "Mar 2025": (11.03, 12.58, 1.811, 0.427),
    "Sep 2025": (10.72, 12.18, 1.661, 0.390), "Mar 2026": (10.67, 12.10, 1.744, 0.414),
}

# ------------------------------------------------------- gini
# label: (total, kota, desa, pangsa40_total_atau_None)
GINI = {
    "Mar 2019": (0.382, 0.392, 0.317, 17.71), "Sep 2019": (0.380, 0.391, 0.315, 17.71),
    "Mar 2020": (0.381, 0.393, 0.317, 17.73), "Sep 2020": (0.385, 0.399, 0.319, 17.93),
    "Mar 2021": (0.384, 0.401, 0.315, 17.76), "Sep 2021": (0.381, 0.398, 0.314, 17.97),
    "Mar 2022": (0.384, 0.403, 0.314, 18.06), "Sep 2022": (0.381, 0.402, 0.313, 18.24),
    "Mar 2023": (0.388, 0.409, 0.313, 18.04), "Mar 2024": (0.379, 0.399, 0.306, 18.40),
    "Sep 2024": (0.381, 0.402, 0.308, 18.41), "Mar 2025": (0.375, 0.395, 0.299, 18.65),
    "Sep 2025": (0.363, 0.383, 0.295, 19.28), "Mar 2026": (0.368, 0.387, 0.296, 19.22),
}

# ------------------------------------------------------- provinsi
PULAU = {}
for p in ["Aceh", "Sumatera Utara", "Sumatera Barat", "Riau", "Jambi",
          "Sumatera Selatan", "Bengkulu", "Lampung", "Kepulauan Bangka Belitung",
          "Kepulauan Riau"]:
    PULAU[p] = "Sumatera"
for p in ["DKI Jakarta", "Jawa Barat", "Jawa Tengah", "DI Yogyakarta",
          "Jawa Timur", "Banten"]:
    PULAU[p] = "Jawa"
for p in ["Bali", "Nusa Tenggara Barat", "Nusa Tenggara Timur"]:
    PULAU[p] = "Bali dan Nusa Tenggara"
for p in ["Kalimantan Barat", "Kalimantan Tengah", "Kalimantan Selatan",
          "Kalimantan Timur", "Kalimantan Utara"]:
    PULAU[p] = "Kalimantan"
for p in ["Sulawesi Utara", "Sulawesi Tengah", "Sulawesi Selatan",
          "Sulawesi Tenggara", "Gorontalo", "Sulawesi Barat"]:
    PULAU[p] = "Sulawesi"
for p in ["Maluku", "Maluku Utara", "Papua Barat", "Papua Barat Daya", "Papua",
          "Papua Selatan", "Papua Tengah", "Papua Pegunungan"]:
    PULAU[p] = "Maluku dan Papua"

# provinsi: (persen, jumlah_ribu) — Mar 2019 lengkap 34 provinsi (Penghitungan 2019, Tabel 2.5)
PROV_2019 = {
    "Aceh": (15.32, 819.44), "Sumatera Utara": (8.83, 1282.04),
    "Sumatera Barat": (6.42, 348.22), "Riau": (7.08, 490.72),
    "Jambi": (7.60, 274.32), "Sumatera Selatan": (12.71, 1073.74),
    "Bengkulu": (15.23, 302.30), "Lampung": (12.62, 1063.66),
    "Kepulauan Bangka Belitung": (4.62, 68.38), "Kepulauan Riau": (5.90, 128.46),
    "DKI Jakarta": (3.47, 365.55), "Jawa Barat": (6.91, 3399.16),
    "Jawa Tengah": (10.80, 3743.23), "DI Yogyakarta": (11.70, 448.47),
    "Jawa Timur": (10.37, 4112.25), "Banten": (5.09, 654.46),
    "Bali": (3.79, 163.85), "Nusa Tenggara Barat": (14.56, 735.96),
    "Nusa Tenggara Timur": (21.09, 1146.32), "Kalimantan Barat": (7.49, 378.41),
    "Kalimantan Tengah": (4.98, 134.59), "Kalimantan Selatan": (4.55, 192.48),
    "Kalimantan Timur": (5.94, 219.92), "Kalimantan Utara": (6.63, 48.78),
    "Sulawesi Utara": (7.66, 191.70), "Sulawesi Tengah": (13.48, 410.36),
    "Sulawesi Selatan": (8.69, 767.80), "Sulawesi Tenggara": (11.24, 302.58),
    "Gorontalo": (15.52, 186.03), "Sulawesi Barat": (11.02, 151.40),
    "Maluku": (17.69, 317.69), "Maluku Utara": (6.77, 84.60),
    "Papua Barat": (22.17, 211.50), "Papua": (27.53, 926.36),
}
PROV_SEP2024 = {
    "Aceh": (12.64, 718.96), "Sumatera Utara": (7.19, 1110.92),
    "Sumatera Barat": (5.42, 315.43), "Riau": (6.36, 473.04),
    "Jambi": (7.26, 272.70), "Sumatera Selatan": (10.51, 948.84),
    "Bengkulu": (12.52, 261.15), "Lampung": (10.62, 939.30),
    "Kepulauan Bangka Belitung": (5.08, 78.58), "Kepulauan Riau": (4.78, 124.96),
    "DKI Jakarta": (4.14, 449.07), "Jawa Barat": (7.08, 3668.35),
    "Jawa Tengah": (9.58, 3396.34), "DI Yogyakarta": (10.40, 430.47),
    "Jawa Timur": (9.56, 3893.82), "Banten": (5.70, 777.49),
    "Bali": (3.80, 176.21), "Nusa Tenggara Barat": (11.91, 658.60),
    "Nusa Tenggara Timur": (19.02, 1107.94), "Kalimantan Barat": (6.25, 333.99),
    "Kalimantan Tengah": (5.26, 149.24), "Kalimantan Selatan": (4.02, 180.20),
    "Kalimantan Timur": (5.51, 211.88), "Kalimantan Utara": (5.38, 41.11),
    "Sulawesi Utara": (6.70, 173.30), "Sulawesi Tengah": (11.04, 358.33),
    "Sulawesi Selatan": (7.77, 711.77), "Sulawesi Tenggara": (10.63, 305.27),
    "Gorontalo": (13.87, 170.03), "Sulawesi Barat": (10.71, 155.91),
    "Maluku": (15.78, 293.99), "Maluku Utara": (6.03, 79.69),
    "Papua Barat": (21.09, 108.28), "Papua Barat Daya": (16.95, 96.81),
    "Papua": (18.09, 161.07), "Papua Selatan": (19.35, 103.02),
    "Papua Tengah": (27.60, 287.54), "Papua Pegunungan": (29.66, 331.12),
}
PROV_MAR2025 = {
    "Aceh": (12.33, 704.69), "Sumatera Utara": (7.36, 1140.25),
    "Sumatera Barat": (5.35, 312.35), "Riau": (6.16, 460.96),
    "Jambi": (7.19, 270.94), "Sumatera Selatan": (10.15, 919.60),
    "Bengkulu": (12.08, 252.97), "Lampung": (10.00, 887.02),
    "Kepulauan Bangka Belitung": (5.00, 77.71), "Kepulauan Riau": (4.44, 117.28),
    "DKI Jakarta": (4.28, 464.87), "Jawa Barat": (7.02, 3654.74),
    "Jawa Tengah": (9.48, 3366.69), "DI Yogyakarta": (10.23, 425.82),
    "Jawa Timur": (9.50, 3875.88), "Banten": (5.63, 772.78),
    "Bali": (3.72, 173.24), "Nusa Tenggara Barat": (11.78, 654.57),
    "Nusa Tenggara Timur": (18.60, 1088.78), "Kalimantan Barat": (6.16, 330.95),
    "Kalimantan Tengah": (5.19, 147.80), "Kalimantan Selatan": (3.84, 172.72),
    "Kalimantan Timur": (5.17, 199.71), "Kalimantan Utara": (5.54, 42.57),
    "Sulawesi Utara": (6.71, 173.84), "Sulawesi Tengah": (10.92, 356.19),
    "Sulawesi Selatan": (7.60, 698.13), "Sulawesi Tenggara": (10.54, 304.43),
    "Gorontalo": (13.24, 162.74), "Sulawesi Barat": (10.41, 152.31),
    "Maluku": (15.38, 287.76), "Maluku Utara": (5.81, 77.27),
    "Papua Barat": (20.66, 106.90), "Papua Barat Daya": (17.95, 103.57),
    "Papua": (19.16, 171.38), "Papua Selatan": (19.71, 105.53),
    "Papua Tengah": (28.90, 302.31), "Papua Pegunungan": (30.03, 337.32),
}
PROV_SEP2025 = {
    "Aceh": (12.22, 703.33), "Sumatera Utara": (7.24, 1128.06),
    "Sumatera Barat": (5.31, 312.30), "Riau": (6.30, 475.57),
    "Jambi": (6.89, 261.25), "Sumatera Selatan": (9.85, 898.24),
    "Bengkulu": (11.88, 250.19), "Lampung": (9.66, 860.13),
    "Kepulauan Bangka Belitung": (4.77, 74.65), "Kepulauan Riau": (4.26, 114.55),
    "DKI Jakarta": (4.03, 439.12), "Jawa Barat": (6.78, 3550.71),
    "Jawa Tengah": (9.39, 3344.82), "DI Yogyakarta": (10.08, 422.79),
    "Jawa Timur": (9.30, 3804.29), "Banten": (5.51, 760.85),
    "Bali": (3.42, 160.09), "Nusa Tenggara Barat": (11.38, 637.18),
    "Nusa Tenggara Timur": (17.50, 1031.69), "Kalimantan Barat": (5.97, 322.54),
    "Kalimantan Tengah": (4.94, 141.75), "Kalimantan Selatan": (3.73, 168.81),
    "Kalimantan Timur": (5.19, 202.04), "Kalimantan Utara": (5.47, 42.45),
    "Sulawesi Utara": (6.62, 172.13), "Sulawesi Tengah": (10.52, 345.38),
    "Sulawesi Selatan": (7.43, 685.14), "Sulawesi Tenggara": (10.14, 295.31),
    "Gorontalo": (12.62, 155.76), "Sulawesi Barat": (10.18, 149.88),
    "Maluku": (15.25, 286.86), "Maluku Utara": (5.59, 74.81),
    "Papua Barat": (19.58, 102.40), "Papua Barat Daya": (17.50, 102.41),
    "Papua": (17.82, 160.25), "Papua Selatan": (19.26, 103.92),
    "Papua Tengah": (29.45, 309.86), "Papua Pegunungan": (27.21, 308.19),
}
PROV_MAR2026 = {
    "Aceh": (12.34, 713.78), "Sumatera Utara": (7.10, 1110.37),
    "Sumatera Barat": (5.27, 311.14), "Riau": (6.19, 470.80),
    "Jambi": (6.67, 253.73), "Sumatera Selatan": (9.50, 869.97),
    "Bengkulu": (11.83, 250.11), "Lampung": (9.31, 831.89),
    "Kepulauan Bangka Belitung": (4.75, 74.61), "Kepulauan Riau": (4.09, 111.22),
    "DKI Jakarta": (3.96, 432.62), "Jawa Barat": (6.54, 3436.48),
    "Jawa Tengah": (9.21, 3285.43), "DI Yogyakarta": (9.70, 408.87),
    "Jawa Timur": (9.06, 3712.23), "Banten": (5.38, 746.73),
    "Bali": (3.44, 162.01), "Nusa Tenggara Barat": (11.17, 628.50),
    "Nusa Tenggara Timur": (17.52, 1037.64), "Kalimantan Barat": (5.78, 313.37),
    "Kalimantan Tengah": (5.09, 146.71), "Kalimantan Selatan": (3.63, 165.41),
    "Kalimantan Timur": (5.14, 200.64), "Kalimantan Utara": (5.18, 40.54),
    "Sulawesi Utara": (6.32, 164.78), "Sulawesi Tengah": (10.46, 345.06),
    "Sulawesi Selatan": (7.24, 669.63), "Sulawesi Tenggara": (10.02, 293.47),
    "Gorontalo": (12.16, 150.60), "Sulawesi Barat": (10.00, 148.06),
    "Maluku": (14.91, 281.54), "Maluku Utara": (5.79, 77.85),
    "Papua Barat": (18.68, 98.46), "Papua Barat Daya": (16.49, 97.51),
    "Papua": (18.39, 165.98), "Papua Selatan": (18.54, 100.61),
    "Papua Tengah": (30.41, 321.28), "Papua Pegunungan": (26.34, 300.06),
}
# Garis kemiskinan provinsi (Rp/kapita/bulan) — terverifikasi untuk Mar 2019,
# Sep 2024, Mar 2025, Sep 2025, Mar 2026 (lihat GK_PROV di bawah)
GK_PROV_MAR2026 = {
    "Aceh": 742464, "Sumatera Utara": 743301, "Sumatera Barat": 808511,
    "Riau": 758447, "Jambi": 744065, "Sumatera Selatan": 628228,
    "Bengkulu": 735745, "Lampung": 657467, "Kepulauan Bangka Belitung": 1012331,
    "Kepulauan Riau": 891524, "DKI Jakarta": 925525, "Jawa Barat": 609790,
    "Jawa Tengah": 596676, "DI Yogyakarta": 672756, "Jawa Timur": 609732,
    "Banten": 753492, "Bali": 675354, "Nusa Tenggara Barat": 606951,
    "Nusa Tenggara Timur": 584252, "Kalimantan Barat": 675653,
    "Kalimantan Tengah": 723149, "Kalimantan Selatan": 714032,
    "Kalimantan Timur": 935662, "Kalimantan Utara": 948355,
    "Sulawesi Utara": 578499, "Sulawesi Tengah": 685244, "Sulawesi Selatan": 542095,
    "Sulawesi Tenggara": 536562, "Gorontalo": 535255, "Sulawesi Barat": 519404,
    "Maluku": 825638, "Maluku Utara": 724488, "Papua Barat": 909502,
    "Papua Barat Daya": 871495, "Papua": 773455, "Papua Selatan": 615015,
    "Papua Tengah": 905417, "Papua Pegunungan": 1275343,
}
# GK provinsi Mar 2019 — Penghitungan dan Analisis Kemiskinan Makro 2019, Tabel 2.2 (total K+D)
GK_PROV_MAR2019 = {
    "Aceh": 486935, "Sumatera Utara": 466122, "Sumatera Barat": 503652,
    "Riau": 500612, "Jambi": 448509, "Sumatera Selatan": 410532,
    "Bengkulu": 499660, "Lampung": 418309, "Kepulauan Bangka Belitung": 677716,
    "Kepulauan Riau": 594059, "DKI Jakarta": 637260, "Jawa Barat": 386198,
    "Jawa Tengah": 369385, "DI Yogyakarta": 432026, "Jawa Timur": 397687,
    "Banten": 462726, "Bali": 400624, "Nusa Tenggara Barat": 384880,
    "Nusa Tenggara Timur": 373922, "Kalimantan Barat": 438555,
    "Kalimantan Tengah": 438248, "Kalimantan Selatan": 457222,
    "Kalimantan Timur": 609155, "Kalimantan Utara": 651416,
    "Sulawesi Utara": 371283, "Sulawesi Tengah": 441036, "Sulawesi Selatan": 329880,
    "Sulawesi Tenggara": 327402, "Gorontalo": 333070, "Sulawesi Barat": 328144,
    "Maluku": 508777, "Maluku Utara": 444650, "Papua Barat": 573313,
    "Papua": 540099,
}
# GK provinsi Sep 2024 & Mar 2025 — BRS Profil Kemiskinan Mar 2025, Tabel 9 (total K+D)
GK_PROV_SEP2024 = {
    "Aceh": 665855, "Sumatera Utara": 648336, "Sumatera Barat": 714991,
    "Riau": 702620, "Jambi": 658100, "Sumatera Selatan": 564462,
    "Bengkulu": 672816, "Lampung": 599018, "Kepulauan Bangka Belitung": 917673,
    "Kepulauan Riau": 807602, "DKI Jakarta": 846085, "Jawa Barat": 535509,
    "Jawa Tengah": 521093, "DI Yogyakarta": 613370, "Jawa Timur": 547751,
    "Banten": 667403, "Bali": 580306, "Nusa Tenggara Barat": 540339,
    "Nusa Tenggara Timur": 533944, "Kalimantan Barat": 611320,
    "Kalimantan Tengah": 641524, "Kalimantan Selatan": 644107,
    "Kalimantan Timur": 853997, "Kalimantan Utara": 876375,
    "Sulawesi Utara": 511710, "Sulawesi Tengah": 608687, "Sulawesi Selatan": 467991,
    "Sulawesi Tenggara": 473343, "Gorontalo": 487578, "Sulawesi Barat": 460283,
    "Maluku": 739818, "Maluku Utara": 639337, "Papua Barat": 816613,
    "Papua Barat Daya": 791570, "Papua": 708811, "Papua Selatan": 548646,
    "Papua Tengah": 798333, "Papua Pegunungan": 1079160,
}
GK_PROV_MAR2025 = {
    "Aceh": 676247, "Sumatera Utara": 666546, "Sumatera Barat": 729806,
    "Riau": 713117, "Jambi": 664127, "Sumatera Selatan": 581702,
    "Bengkulu": 683820, "Lampung": 612451, "Kepulauan Bangka Belitung": 956833,
    "Kepulauan Riau": 832410, "DKI Jakarta": 852768, "Jawa Barat": 547752,
    "Jawa Tengah": 537812, "DI Yogyakarta": 626363, "Jawa Timur": 558029,
    "Banten": 684232, "Bali": 607847, "Nusa Tenggara Barat": 556846,
    "Nusa Tenggara Timur": 549607, "Kalimantan Barat": 622882,
    "Kalimantan Tengah": 654066, "Kalimantan Selatan": 650675,
    "Kalimantan Timur": 866193, "Kalimantan Utara": 884970,
    "Sulawesi Utara": 530304, "Sulawesi Tengah": 624854, "Sulawesi Selatan": 477966,
    "Sulawesi Tenggara": 488171, "Gorontalo": 495576, "Sulawesi Barat": 475488,
    "Maluku": 757600, "Maluku Utara": 662397, "Papua Barat": 831001,
    "Papua Barat Daya": 812630, "Papua": 714365, "Papua Selatan": 566052,
    "Papua Tengah": 817834, "Papua Pegunungan": 1132178,
}
# GK provinsi Sep 2025 — BRS Profil Kemiskinan Sep 2025, Tabel 8 (total K+D)
GK_PROV_SEP2025 = {
    "Aceh": 715103, "Sumatera Utara": 718220, "Sumatera Barat": 776517,
    "Riau": 747345, "Jambi": 713849, "Sumatera Selatan": 609044,
    "Bengkulu": 712003, "Lampung": 634062, "Kepulauan Bangka Belitung": 992426,
    "Kepulauan Riau": 870738, "DKI Jakarta": 897768, "Jawa Barat": 575499,
    "Jawa Tengah": 570870, "DI Yogyakarta": 649331, "Jawa Timur": 585020,
    "Banten": 715288, "Bali": 642986, "Nusa Tenggara Barat": 575856,
    "Nusa Tenggara Timur": 563052, "Kalimantan Barat": 652220,
    "Kalimantan Tengah": 683664, "Kalimantan Selatan": 684567,
    "Kalimantan Timur": 897759, "Kalimantan Utara": 933675,
    "Sulawesi Utara": 557310, "Sulawesi Tengah": 664691, "Sulawesi Selatan": 514958,
    "Sulawesi Tenggara": 519411, "Gorontalo": 519640, "Sulawesi Barat": 510846,
    "Maluku": 797060, "Maluku Utara": 692592, "Papua Barat": 868631,
    "Papua Barat Daya": 855657, "Papua": 736720, "Papua Selatan": 587264,
    "Papua Tengah": 873843, "Papua Pegunungan": 1235328,
}
GK_PROV = {
    "Mar 2019": GK_PROV_MAR2019, "Sep 2024": GK_PROV_SEP2024,
    "Mar 2025": GK_PROV_MAR2025, "Sep 2025": GK_PROV_SEP2025,
    "Mar 2026": GK_PROV_MAR2026,
}

PERIOD_ID = {p[0]: p[1] * 100 + p[2] for p in PERIODE}
URUT = {p[0]: p[3] for p in PERIODE}


def num(x):
    return "" if x is None else x


# ------------------------------------------------------------------ tulis CSV
with open(os.path.join(DATA, "kemiskinan_nasional.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["periode", "tahun", "bulan", "persen_miskin", "jumlah_miskin_juta",
                "garis_kemiskinan_rp", "gkm_rp", "gkbm_rp", "p1", "p2"])
    for lbl, th, bln, _ in PERIODE:
        ps, jm, gk, gkm, gkbm, p1, p2 = NASIONAL[lbl]
        w.writerow([lbl, th, "Maret" if bln == 3 else "September", ps, jm,
                    gk, gkm, gkbm, num(p1), num(p2)])

with open(os.path.join(DATA, "kemiskinan_kota_desa.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["periode", "daerah", "persen_miskin", "jumlah_miskin_juta", "p1", "p2"])
    for lbl in LBL:
        for daerah, src in (("Perkotaan", KOTA), ("Perdesaan", DESA)):
            ps, jm, p1, p2 = src[lbl]
            w.writerow([lbl, daerah, ps, jm, num(p1), num(p2)])

with open(os.path.join(DATA, "gini_nasional.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["periode", "daerah", "gini_ratio", "pangsa_40_terbawah_persen"])
    for lbl in LBL:
        tot, kot, des, p40 = GINI[lbl]
        w.writerow([lbl, "Total", tot, num(p40)])
        w.writerow([lbl, "Perkotaan", kot, ""])
        w.writerow([lbl, "Perdesaan", des, ""])

with open(os.path.join(DATA, "kemiskinan_provinsi.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["periode", "provinsi", "pulau", "persen_miskin",
                "jumlah_miskin_ribu", "garis_kemiskinan_rp"])
    for lbl, src in (("Mar 2019", PROV_2019), ("Sep 2024", PROV_SEP2024),
                     ("Mar 2025", PROV_MAR2025), ("Sep 2025", PROV_SEP2025),
                     ("Mar 2026", PROV_MAR2026)):
        for prov, (ps, jm) in src.items():
            gk = GK_PROV.get(lbl, {}).get(prov, "")
            w.writerow([lbl, prov, PULAU[prov], ps, num(jm), gk])

print("CSV kompilasi tertulis: nasional(14), kota_desa(28), gini(42), provinsi(186)")

# ------------------------------------------------------------------ SOURCES.md
SOURCES = """# Sumber Data — Kemiskinan & Ketimpangan Indonesia 2026

Semua angka dalam proyek ini **dikompilasi manual dari publikasi resmi Badan
Pusat Statistik (BPS)**: Berita Resmi Statistik (BRS) *Profil Kemiskinan di
Indonesia* dan *Tingkat Ketimpangan Pengeluaran Penduduk Indonesia* (Gini
Ratio), ditambah publikasi BPS *Penghitungan dan Analisis Kemiskinan Makro
Indonesia*. Tidak ada API tunggal; setiap seri dirangkai dari tabel BRS
berbagai edisi (tiap edisi Maret memuat 3 periode: Maret tahun sebelumnya,
September, dan Maret tahun berjalan — begitu pula rantai Tabel 1, 3, dan 6).
Data mentah Susenas tidak dibagikan ulang; yang dibagikan adalah angka
agregat resmi yang diterbitkan BPS.

## Dokumen sumber utama (bps.go.id / web-api.bps.go.id)

| Dokumen | Nomor & tanggal rilis | Dipakai untuk |
|---|---|---|
| Profil Kemiskinan di Indonesia Maret 2026 | No. 80/08/Th. XXIX, 5 Agustus 2026 | Seri nasional Gambar 1 (Mar 2019–Mar 2026), Tabel 1 kota/desa, Tabel 2 pulau, Tabel 3 GK, Tabel 6 P1/P2, Tabel 7/8 provinsi Sep 2025 & Mar 2026, Tabel 9 GK provinsi Mar 2026 |
| Profil Kemiskinan di Indonesia September 2025 | No. 19/02/Th. XXIX, 5 Februari 2026 | Tabel 7/8 provinsi Mar 2025 & Sep 2025 (cek silang); Tabel 8 GK provinsi Sep 2025 (lengkap 38 provinsi) |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia September 2025 | No. 20/02/Th. XXIX, 5 Februari 2026 | Gambar 1 seri Gini Sep 2019–Sep 2025 (total, kota, desa); pangsa 40% terbawah Sep 2025 = 19,28% |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia Maret 2026 | BRS Gini Maret 2026 (rilis Agustus 2026) | Gini Mar 2026: total 0,368; kota 0,387; desa 0,296; pangsa 40% terbawah 19,22% |
| Profil Kemiskinan di Indonesia Maret 2025 | No. 63/07/Th. XXVIII, 25 Juli 2025 | Tabel 1, 3, 6 (Mar 2024–Mar 2025); Tabel 7/8 provinsi Sep 2024 & Mar 2025; Tabel 9 GK provinsi Sep 2024 & Mar 2025 (lengkap 38 provinsi); kemiskinan ekstrem Mar 2025 0,85% |
| Profil Kemiskinan di Indonesia Maret 2023 | No. 47/07/Th. XXVI, 17 Juli 2023 | Tabel 1, 3, 6 (Mar 2022–Mar 2023) |
| Profil Kemiskinan di Indonesia Maret 2022 | No. 51/07/Th. XXV, 15 Juli 2022 | Tabel 1, 3, 6 (Mar 2021–Mar 2022), termasuk P1/P2 Sep 2021 |
| Profil Kemiskinan di Indonesia Maret 2021 | No. 53/07/Th. XXIV, 15 Juli 2021 | Tabel 1, 3, 6 (Mar 2020–Mar 2021) |
| Profil Kemiskinan di Indonesia September 2020 | BRS 15 Februari 2021 | Tabel 3 GK (Sep 2019–Sep 2020) |
| Profil Kemiskinan di Indonesia September 2019 | BRS 15 Januari 2020 | Tabel 3 GK: Sep 2019 = Rp440.538 (GKM 324.911, GKBM 115.627); Tabel 6 P1/P2 Mar & Sep 2019 (total, kota, desa); abstraksi bps.go.id |
| Persentase Penduduk Miskin Maret 2020 Naik Menjadi 9,78 Persen | Rilis bps.go.id, 15 Juli 2020 | Kota/desa Sep 2019 (kota 6,56%/9,86 jt; desa 12,60%/14,93 jt); GK Mar 2020 |
| Persentase Penduduk Miskin Maret 2019 Sebesar 9,41 Persen | Rilis bps.go.id, 15 Juli 2019 | Mar 2019: kota 6,69%/9,99 jt; desa 12,85%/15,15 jt; GK Rp425.250 |
| Gini Ratio Maret 2019 Tercatat Sebesar 0,382 | Rilis bps.go.id, 15 Juli 2019 | Gini Mar 2019: total 0,382; kota 0,392; desa 0,317; pangsa 40% terbawah 17,71% |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia September 2019 | No. 09/01/Th. XXIII, 15 Januari 2020 | Gini Sep 2019: 0,380; kota 0,391; desa 0,315 |
| Gini Ratio Maret 2020 Tercatat Sebesar 0,381 | Rilis bps.go.id, 15 Juli 2020 | Gini Mar 2020: 0,381; kota 0,393; desa 0,317; pangsa 40% terbawah 17,73% |
| Penghitungan dan Analisis Kemiskinan Makro Indonesia 2019 (Katalog 3205022) + Indikator Kemiskinan Menurut Provinsi Mar & Sep 2019 | Publikasi BPS | Provinsi Mar 2019: persentase + jumlah (ribu) lengkap 34 provinsi (Tabel 2.5); GK provinsi Mar 2019 (Tabel 2.2, total kota+desa) |
| BRS Gini Ratio berbagai edisi (Sep 2020, Mar 2021, Sep 2021, Mar 2022, Sep 2024) + BRS Gini Maret 2024 (No. 51/07/Th. XXVII, 1 Juli 2024, Tabel 1) + Penghitungan dan Analisis Kemiskinan Makro Indonesia 2025 (Katalog 3205022, Gambar 3.7) | Rilis BPS 2021–2026 | Pangsa pengeluaran 40% terbawah (total): Sep 2020 17,93%; Mar 2021 17,76%; Sep 2021 17,97%; Mar 2022 18,06%; Sep 2022 18,24%; Mar 2023 18,04%; Mar 2024 18,40%; Sep 2024 18,41%; Mar 2025 18,65%; Sep 2025 19,28% — seri pangsa kini lengkap 14 periode |

## Catatan cakupan & keputusan data

- **Tidak ada periode September 2023.** BPS tidak menerbitkan Susenas
  September 2023 untuk kemiskinan (peralihan metodologi/pendataan), sehingga
  seri melompat dari Mar 2023 ke Mar 2024. Ini disengaja, bukan data hilang.
- **P1/P2 lengkap Mar 2019–Mar 2026 (14 periode).** Nilai Mar & Sep 2019
  diisi dari Tabel 6 BRS Profil Kemiskinan September 2019 (dicek silang
  identik pada Tabel 6 BRS September 2020): Mar 2019 P1 1,55 / P2 0,37;
  Sep 2019 P1 1,50 / P2 0,36, termasuk rincian kota/desa.
- **Jumlah penduduk miskin provinsi Maret 2019 lengkap 34 dari 34 provinsi**
  (Tabel 2.5 Penghitungan dan Analisis Kemiskinan Makro Indonesia 2019);
  persentase Mar 2019 juga lengkap 34 provinsi.
- **Garis kemiskinan provinsi** diisi untuk 5 periode: Mar 2019 (34 provinsi,
  Tabel 2.2 publikasi Penghitungan 2019), Sep 2024 & Mar 2025 (38 provinsi,
  Tabel 9 BRS Mar 2025), Sep 2025 (38 provinsi, Tabel 8 BRS Sep 2025), dan
  Mar 2026 (38 provinsi, Tabel 9 BRS Mar 2026). Semua nilai adalah total
  kota+desa per provinsi.
- **Pangsa pengeluaran 40% terbawah (total) lengkap 14 periode** dari BRS
  Gini Ratio berbagai edisi (lihat tabel sumber); nilai kota/desa tidak
  dikompilasi, hanya baris Total yang diisi.
- **Gini kota/desa Sep 2020** (kota 0,399; desa 0,319) dibaca dari Gambar 1
  BRS Gini Sep 2025 dan dicek silang dengan tabel Gini BPS per provinsi
  (baris Indonesia). Nilai total & desa cocok di semua titik cek.
- **Jumlah nasional Sep 2019 = 24,78 juta** mengikuti seri Gambar 1 BRS
  Mar 2025/Mar 2026 (abstraksi BRS Sep 2019 menulis 24,79 karena pembulatan
  komponen kota 9,86 + desa 14,93).
- **Perubahan provinsi 2019 → 2026** dihitung untuk 32 provinsi yang
  wilayahnya stabil. Papua dan Papua Barat dikecualikan dari peringkat
  perubahan karena wilayah 2019-nya mencakup provinsi hasil pemekaran 2022
  (Papua Selatan, Papua Tengah, Papua Pegunungan, Papua Barat Daya), sehingga
  tidak sebanding (not like-for-like).
- Satuan: persentase dalam persen (%), jumlah nasional dalam juta orang,
  jumlah provinsi dalam ribu orang, garis kemiskinan dalam Rp/kapita/bulan.
"""
with open(os.path.join(DATA, "SOURCES.md"), "w") as f:
    f.write(SOURCES)
print("SOURCES.md tertulis")
