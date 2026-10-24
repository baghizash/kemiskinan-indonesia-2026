# Panduan Merakit Dashboard — Kemiskinan & Ketimpangan Indonesia 2026

Hasil akhir: `Kemiskinan-Indonesia-2026.pbix`

1. Buka Power BI Desktop → Get Data → Text/CSV, muat 6 file di folder ini:
   `dim_periode.csv`, `dim_provinsi.csv`, `fact_kemiskinan_nasional.csv`,
   `fact_kemiskinan_kota_desa.csv`, `fact_gini.csv`,
   `fact_kemiskinan_provinsi.csv`.
2. Model view — buat relasi:
   - `fact_kemiskinan_nasional[periode_id]` → `dim_periode[periode_id]`
   - `fact_kemiskinan_kota_desa[periode_id]` → `dim_periode[periode_id]`
   - `fact_gini[periode_id]` → `dim_periode[periode_id]`
   - `fact_kemiskinan_provinsi[periode_id]` → `dim_periode[periode_id]`
   - `fact_kemiskinan_provinsi[provinsi]` → `dim_provinsi[provinsi]`
3. Tandai `dim_periode` sebagai date table tidak wajib; cukup urutkan kolom
   `periode` menurut kolom `urutan` (Sort by Column) agar sumbu waktu benar
   (Mar sebelum Sep, dan tidak ada Sep 2023).
4. Sembunyikan kolom `periode` pada tabel fakta (sudah ada di dim_periode)
   dan kolom kunci `periode_id` di semua tabel.
5. Buat semua measure dari `measures_dax.md` (nama persis seperti di file,
   tanpa tanda "=" di nama), lalu cocokkan hasilnya dengan **tabel
   verifikasi** di file yang sama sebelum lanjut ke visual.
6. Susun 4 halaman mengikuti `dashboard_layout.md` (tema oat/merah redup/
   pumpkin; judul halaman menyebut periode secara eksplisit).
7. Simpan sebagai `Kemiskinan-Indonesia-2026.pbix`.

Jebakan yang harus dihindari:
- Jangan menjumlahkan `persen_miskin` — selalu rata-rata (AVERAGE). Persen
  bukan nilai aditif.
- `fact_kemiskinan_provinsi` mencampur 5 periode; selalu filter periode
  (slicer/pin) sebelum membaca peringkat provinsi.
- Kolom `p1`/`p2` lengkap untuk semua periode Mar 2019–Mar 2026
  (termasuk rincian kota/desa dari Tabel 6 BRS).
- Jumlah provinsi dalam ribu, jumlah nasional dalam juta — jangan dicampur
  dalam satu visual tanpa konversi.
