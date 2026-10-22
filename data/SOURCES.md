# Sumber Data — Kemiskinan & Ketimpangan Indonesia 2026

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
| Profil Kemiskinan di Indonesia September 2025 | No. 19/02/Th. XXIX, 5 Februari 2026 | Tabel 7/8 provinsi Mar 2025 & Sep 2025 (cek silang) |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia September 2025 | No. 20/02/Th. XXIX, 5 Februari 2026 | Gambar 1 seri Gini Sep 2019–Sep 2025 (total, kota, desa) |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia Maret 2026 | BRS Gini Maret 2026 (rilis Agustus 2026) | Gini Mar 2026: total 0,368; kota 0,387; desa 0,296; pangsa 40% terbawah 19,22% |
| Profil Kemiskinan di Indonesia Maret 2025 | No. 63/07/Th. XXVIII, 25 Juli 2025 | Tabel 1, 3, 6 (Mar 2024–Mar 2025); Tabel 7/8 provinsi Sep 2024 & Mar 2025; kemiskinan ekstrem Mar 2025 0,85% |
| Profil Kemiskinan di Indonesia Maret 2023 | No. 47/07/Th. XXVI, 17 Juli 2023 | Tabel 1, 3, 6 (Mar 2022–Mar 2023) |
| Profil Kemiskinan di Indonesia Maret 2022 | No. 51/07/Th. XXV, 15 Juli 2022 | Tabel 1, 3, 6 (Mar 2021–Mar 2022), termasuk P1/P2 Sep 2021 |
| Profil Kemiskinan di Indonesia Maret 2021 | No. 53/07/Th. XXIV, 15 Juli 2021 | Tabel 1, 3, 6 (Mar 2020–Mar 2021) |
| Profil Kemiskinan di Indonesia September 2020 | BRS 15 Februari 2021 | Tabel 3 GK (Sep 2019–Sep 2020) |
| Profil Kemiskinan di Indonesia September 2019 | BRS 15 Januari 2020 | Tabel 3 GK: Sep 2019 = Rp440.538 (GKM 324.911, GKBM 115.627); abstraksi bps.go.id |
| Persentase Penduduk Miskin Maret 2020 Naik Menjadi 9,78 Persen | Rilis bps.go.id, 15 Juli 2020 | Kota/desa Sep 2019 (kota 6,56%/9,86 jt; desa 12,60%/14,93 jt); GK Mar 2020 |
| Persentase Penduduk Miskin Maret 2019 Sebesar 9,41 Persen | Rilis bps.go.id, 15 Juli 2019 | Mar 2019: kota 6,69%/9,99 jt; desa 12,85%/15,15 jt; GK Rp425.250 |
| Gini Ratio Maret 2019 Tercatat Sebesar 0,382 | Rilis bps.go.id, 15 Juli 2019 | Gini Mar 2019: total 0,382; kota 0,392; desa 0,317; pangsa 40% terbawah 17,71% |
| Tingkat Ketimpangan Pengeluaran Penduduk Indonesia September 2019 | No. 09/01/Th. XXIII, 15 Januari 2020 | Gini Sep 2019: 0,380; kota 0,391; desa 0,315 |
| Gini Ratio Maret 2020 Tercatat Sebesar 0,381 | Rilis bps.go.id, 15 Juli 2020 | Gini Mar 2020: 0,381; kota 0,393; desa 0,317; pangsa 40% terbawah 17,73% |
| Penghitungan dan Analisis Kemiskinan Makro Indonesia 2019 (Katalog 3205022) + Indikator Kemiskinan Menurut Provinsi Mar & Sep 2019 | Publikasi BPS | Provinsi Mar 2019: persentase 34 provinsi + jumlah (ribu) 18 provinsi |

## Catatan cakupan & keputusan data

- **Tidak ada periode September 2023.** BPS tidak menerbitkan Susenas
  September 2023 untuk kemiskinan (peralihan metodologi/pendataan), sehingga
  seri melompat dari Mar 2023 ke Mar 2024. Ini disengaja, bukan data hilang.
- **P1/P2 Maret & September 2019 dikosongkan.** Tabel 6 BRS September 2019
  tidak berhasil diambil utuh pada saat kompilasi; seri P1/P2 yang
  terverifikasi lengkap berjalan Mar 2020–Mar 2026 (12 periode, termasuk
  rincian kota/desa).
- **Jumlah penduduk miskin provinsi Maret 2019** hanya terverifikasi untuk
  18 dari 34 provinsi (sel kosong pada 16 provinsi); persentase Mar 2019
  lengkap untuk 34 provinsi.
- **Garis kemiskinan provinsi** hanya diisi untuk Mar 2026 (Tabel 9 BRS
  Mar 2026, lengkap 38 provinsi).
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
