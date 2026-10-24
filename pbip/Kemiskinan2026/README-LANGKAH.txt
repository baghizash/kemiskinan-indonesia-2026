LANGKAH MEMBUKA PAKET PBIP — Kemiskinan & Ketimpangan Indonesia 2026
====================================================================

1. Ekstrak file ZIP ini ke folder lokal (mis. C:\PowerBI\Kemiskinan).
2. Buka file Kemiskinan2026.pbip dengan Power BI Desktop.
3. Saat diminta parameter, klik Edit Parameters / Transform Data >
   Edit Parameters, lalu arahkan FolderData ke folder "data" di dalam
   hasil ekstrak (folder berisi 6 file CSV kit).
4. Klik Refresh agar seluruh tabel termuat.
5. Cek cepat angka kunci (Halaman 1 — Ringkasan Nasional):
   - Kartu Persen Miskin Mar 2026 harus menunjukkan 8,07
   - Kartu Jumlah Miskin Mar 2026 harus menunjukkan 22,93 (juta)
   - Kartu Garis Kemiskinan Mar 2026 harus menunjukkan 669.235 (Rp)
   - Kartu Gini Mar 2026 harus menunjukkan 0,368
   - Halaman 3: provinsi teratas Papua Tengah 30,41%; di atas nasional = 20 provinsi
6. Jika semua cocok, Save As menjadi Kemiskinan-Indonesia-2026.pbix.

Catatan sentuhan pertama (wajar terjadi):
- Kolom "periode" pada dim_periode mungkin perlu diatur ulang urutannya:
  pilih kolom periode > Sort by Column > urutan, agar Maret selalu tampil
  sebelum September pada sumbu grafik.
- Slicer periode mungkin tampil sebagai daftar (list), bukan slider —
  itu normal untuk data kategori Mar/Sep.
- Visual peta tidak dipakai (diganti bar terurut) karena visual peta PBIR
  rawan error; peringkat provinsi tetap terbaca jelas dari bar.
- Nilai P1/P2 lengkap Mar 2019–Mar 2026 (14 periode) dari Tabel 6 BRS
  Profil Kemiskinan, jadi tren P1/P2 tampil utuh sejak Mar 2019.
