# Kemiskinan & Ketimpangan Indonesia 2026

Analisis portofolio atas **data resmi BPS**: kemiskinan (persentase, jumlah,
garis kemiskinan, indeks kedalaman P1 & keparahan P2) dan ketimpangan
(Gini Ratio) Indonesia untuk **14 periode Maret & September 2019 sampai
Maret 2026**, lengkap dengan rincian kota–desa dan 38 provinsi.

> **Headline Maret 2026:** persentase penduduk miskin **8,07%** (**22,93 juta
> jiwa**) — terendah dalam seri 2019–2026. Gini Ratio **0,368**. Garis
> kemiskinan **Rp669.235/kapita/bulan**. Provinsi tertinggi **Papua Tengah
> 30,41%**, terendah **Bali 3,44%**.

## Temuan utama

1. **Lonjakan pandemi dan pemulihannya.** Kemiskinan memuncak di
   **September 2020 (10,19%; 27,55 juta jiwa)**, lalu turun nyaris tanpa jeda.
   Persentase pertama kali kembali di bawah level prapandemi (Mar 2019:
   9,41%) pada **Maret 2023 (9,36%)**.
2. **Garis kemiskinan naik 57,4%** dalam tujuh tahun (Rp425.250 → Rp669.235,
   ±6,7% per tahun); **74,70%** di antaranya adalah makanan (Mar 2026).
   Penduduk miskin berkurang *meski* ambangnya naik tajam.
3. **Kota–desa:** perdesaan 10,67% vs perkotaan 6,34% (Mar 2026), tetapi
   kesenjangannya menyempit dari **6,16 poin (Mar 2019) menjadi 4,33 poin**.
4. **Ketimpangan menyempit perlahan** (Gini 0,382 → 0,368), kota jauh lebih
   timpang daripada desa (0,387 vs 0,296). Namun Gini **naik dari titik
   terendah Sep 2025 (0,363)** di saat kemiskinan mencapai rekor terendah —
   keduanya bisa bergerak berlawanan arah.
5. **Kemiskinan makin dangkal:** P1 turun 27,5% dari puncak pandemi
   (1,75 → 1,268). Pengecualian penting: **P1 perdesaan naik di semester
   terakhir** (1,661 → 1,744) saat kota membaik.
6. **Jurang provinsi 26,97 poin persen (8,8×):** Papua Tengah 30,41% vs Bali
   3,44%; 20 dari 38 provinsi di atas rata-rata nasional. Namun **52,4%
   penduduk miskin tinggal di Pulau Jawa** — Jawa Timur terbanyak (3,71 jt).
7. **Perubahan 2019 → 2026:** 28 dari 32 provinsi sebanding membaik
   (terbaik NTT, turun 3,57 poin); 4 naik: DKI Jakarta (+0,49), Banten
   (+0,29), Kepulauan Bangka Belitung (+0,13), Kalimantan Tengah (+0,11).

## Struktur repo

```
data/        CSV kompilasi BPS + SOURCES.md (ketertelusuran per angka)
charts/      12 grafik PNG berlabel Bahasa Indonesia
scripts/     compile_data.py, analysis.py, build_powerbi.py,
             build_ppt.py, build_module.py, build_pbip.py
sql/         queries.sql — kueri analitis atas CSV kompilasi
powerbi/     Kit Power BI: 6 CSV model bintang, measures_dax.md,
             dashboard_layout.md, build_guide.md, pratinjau dashboard
pbip/        Paket PBIP Kemiskinan2026 (Report + SemanticModel + data CSV)
analysis.ipynb               Notebook reproduksi temuan dari CSV
findings.json                Seluruh angka temuan (dihitung analysis.py)
Portofolio-Analisis-Kemiskinan.pptx   Deck portofolio 10 slide
Modul-Analisis-Kemiskinan.pdf         Modul belajar (landscape, pemula)
```

## Data & metode

Seluruh angka **dikompilasi manual dari Berita Resmi Statistik (BRS) BPS** —
tidak ada API tunggal. Setiap seri dirangkai dari Tabel 1, 3, 6, 7/8, dan 9
BRS Profil Kemiskinan berbagai edisi plus BRS Gini Ratio; ketertelusuran
lengkap (dokumen, nomor rilis, tanggal) ada di `data/SOURCES.md`.

Keputusan & keterbatasan data yang disengaja:

- **Tidak ada periode September 2023** — BPS tidak menerbitkannya.
- **P1/P2 lengkap Mar 2019–Mar 2026** (14 periode, termasuk rincian
  kota/desa) dari Tabel 6 BRS Profil Kemiskinan.
- **Jumlah provinsi Maret 2019 lengkap 34 dari 34 provinsi**
  (persentase dan jumlah sama-sama lengkap).
- **Garis kemiskinan provinsi** terisi untuk 5 periode: Mar 2019,
  Sep 2024, Mar 2025, Sep 2025, dan Mar 2026.
- **Pangsa pengeluaran 40% terbawah** (baris Total) lengkap 14 periode
  dari BRS Gini Ratio berbagai edisi.
- Perubahan provinsi dihitung untuk **32 provinsi sebanding**; Papua dan
  Papua Barat 2019 mencakup wilayah pemekaran 2022 sehingga tidak
  like-for-like.

## Dashboard Power BI

Kit di folder `powerbi/` merakit file **`Kemiskinan-Indonesia-2026.pbix`**:

- Model bintang dengan grain terpisah: `fact_kemiskinan_nasional`,
  `fact_kemiskinan_kota_desa`, `fact_gini`, `fact_kemiskinan_provinsi`,
  `dim_periode`, `dim_provinsi`.
- **17 measure DAX bernama polos** di `measures_dax.md`, lengkap dengan
  tabel verifikasi (mis. Persen Miskin Mar 2026 harus tampil **8.07**,
  Gini Mar 2026 **0.368**, provinsi di atas nasional **20**).
- 4 halaman: Ringkasan Nasional · Kota vs Desa · Provinsi · Ketimpangan
  & Kedalaman. Pratinjau halaman 1: `powerbi/dashboard_preview_halaman1.png`.
- Paket **PBIP** di `pbip/Kemiskinan2026/` memungkinkan membuka model +
  report tanpa merakit dari nol: ekstrak, buka `.pbip`, arahkan parameter
  `FolderData` ke folder `data/` paket, Refresh, lalu Save As `.pbix`.

## Reproduksi

```bash
python scripts/compile_data.py   # data BPS -> CSV rapi + SOURCES.md
python scripts/analysis.py       # findings.json + 12 chart (dengan verifikasi)
python scripts/build_powerbi.py  # kit Power BI + measures + pratinjau
python scripts/build_ppt.py      # deck PPTX 10 slide
python scripts/build_module.py   # modul PDF
python scripts/build_pbip.py     # paket PBIP (tervalidasi)
```

## Tentang

Disusun oleh **BAGHIZ ASSHIDDIQIE ARASYA** — Data Analyst.
Bagian dari seri portofolio data Indonesia 2026 (pengangguran, harga pangan,
harga cabai, ISPA, gempa bumi, pariwisata, dan lainnya).
