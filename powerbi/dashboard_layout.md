# Layout Dashboard Power BI — Kemiskinan & Ketimpangan Indonesia 2026

File: `Kemiskinan-Indonesia-2026.pbix` · Tema: latar oat `#FAF6EF`, aksen
muted red `#A63D40`, pumpkin `#E07B39`, teks slate `#2E2A26`.
Judul tiap halaman memakai periode eksplisit (Mar/Sep + tahun).

## Halaman 1 — Ringkasan Nasional
- 4 kartu KPI: Persen Miskin Mar 2026 (8,07%), Jumlah Miskin Mar 2026
  (22,93 jt), Garis Kemiskinan Mar 2026 (Rp669.235), Gini Mar 2026 (0,368).
- Line chart: persen_miskin per periode (sumbu urutan dim_periode).
- Column chart: jumlah_miskin_juta per periode.
- Slicer periode (dim_periode[periode], urut menurut kolom urutan).
- Textbox metodologi: data BPS (BRS Profil Kemiskinan & Gini), seri
  Mar 2019–Mar 2026; tidak ada periode Sep 2023.

## Halaman 2 — Kota vs Desa
- Line chart ganda: persen_miskin kota vs desa per periode (legenda daerah).
- Bar chart: P1 & P2 kota vs desa pada Mar 2026 (filter periode).
- Kartu: selisih desa−kota Mar 2026 (4,33 poin) & rasio (1,68×).
- Area/catatan: P1 desa naik Sep 2025 → Mar 2026 saat kota membaik.

## Halaman 3 — Provinsi
- Bar terurut menurun: persen_miskin per provinsi, filter Mar 2026
  (Papua Tengah di puncak 30,41%).
- Bar: jumlah_miskin_ribu per provinsi Mar 2026 (Jawa Timur terbesar).
- Tabel rinci: provinsi, persen, jumlah (ribu), garis kemiskinan (Mar 2026).
- Slicer periode (Mar 2019, Sep 2024, Mar 2025, Sep 2025, Mar 2026).
- Catatan: perbandingan 2019→2026 hanya untuk 32 provinsi sebanding
  (Papua & Papua Barat 2019 mencakup wilayah pemekaran 2022).

## Halaman 4 — Ketimpangan & Kedalaman
- Line chart: Gini total/kota/desa per periode.
- Line chart: P1 & P2 nasional per periode (Mar 2019–Mar 2026).
- Kartu: Gini Mar 2026 (0,368), pangsa pengeluaran 40% terbawah Mar 2026
  (19,22%), P1 Mar 2026 (1,268), P2 Mar 2026 (0,291).
- Textbox: Gini naik dari titik terendah Sep 2025 (0,363) saat kemiskinan
  turun — ketimpangan dan kemiskinan bisa bergerak berlawanan arah.
