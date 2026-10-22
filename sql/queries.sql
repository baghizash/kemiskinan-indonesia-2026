-- ============================================================
-- Kueri analitis — Kemiskinan & Ketimpangan Indonesia 2026
-- Tabel = CSV di folder data/ (muat sebagai tabel dengan nama yang sama):
--   kemiskinan_nasional, kemiskinan_kota_desa, gini_nasional,
--   kemiskinan_provinsi
-- Dialek: SQL standar (jalan di SQLite/DuckDB/BigQuery dengan penyesuaian
-- kecil pada pemuatan CSV). Periode selalu eksplisit (Mar/Sep + tahun).
-- ============================================================

-- 1) Tren nasional lengkap: persen, jumlah, garis kemiskinan
SELECT periode, persen_miskin, jumlah_miskin_juta, garis_kemiskinan_rp
FROM kemiskinan_nasional
ORDER BY tahun, CASE bulan WHEN 'Maret' THEN 1 ELSE 2 END;

-- 2) Lonjakan pandemi: perubahan poin persen antarperiode (LAG)
SELECT periode, persen_miskin,
       ROUND(persen_miskin - LAG(persen_miskin) OVER (ORDER BY tahun,
             CASE bulan WHEN 'Maret' THEN 1 ELSE 2 END), 2) AS delta_pp
FROM kemiskinan_nasional;

-- 3) Kapan pertama kali kembali di bawah level prapandemi (Mar 2019 = 9,41%)?
SELECT MIN(periode) AS periode_pertama_di_bawah_prapandemi
FROM (
  SELECT periode, persen_miskin,
         ROW_NUMBER() OVER (ORDER BY tahun,
           CASE bulan WHEN 'Maret' THEN 1 ELSE 2 END) AS rn
  FROM kemiskinan_nasional
) t
WHERE rn > 2 AND persen_miskin < 9.41;
-- Hasil: Mar 2023 (9,36%)

-- 4) Gap kota-desa per periode (poin persen)
SELECT k.periode,
       k.persen_miskin AS kota,
       d.persen_miskin AS desa,
       ROUND(d.persen_miskin - k.persen_miskin, 2) AS gap_pp
FROM kemiskinan_kota_desa k
JOIN kemiskinan_kota_desa d
  ON d.periode = k.periode AND d.daerah = 'Perdesaan'
WHERE k.daerah = 'Perkotaan'
ORDER BY k.periode;
-- Gap menyempit: 6,16 (Mar 2019) -> 4,33 (Mar 2026)

-- 5) Peringkat provinsi terbaru (Mar 2026)
SELECT provinsi, persen_miskin, jumlah_miskin_ribu, garis_kemiskinan_rp
FROM kemiskinan_provinsi
WHERE periode = 'Mar 2026'
ORDER BY persen_miskin DESC;
-- Tertinggi: Papua Tengah 30,41% | Terendah: Bali 3,44%

-- 6) Provinsi di atas rata-rata nasional, Mar 2026
SELECT COUNT(*) AS jumlah_provinsi_di_atas_nasional
FROM kemiskinan_provinsi
WHERE periode = 'Mar 2026' AND persen_miskin > 8.07;
-- Hasil: 20 dari 38 provinsi

-- 7) Perubahan Mar 2019 -> Mar 2026 untuk 32 provinsi sebanding
--    (Papua & Papua Barat dikecualikan: wilayah 2019 mencakup pemekaran 2022)
SELECT a.provinsi,
       a.persen_miskin AS persen_2019,
       b.persen_miskin AS persen_2026,
       ROUND(b.persen_miskin - a.persen_miskin, 2) AS delta_pp
FROM kemiskinan_provinsi a
JOIN kemiskinan_provinsi b
  ON b.provinsi = a.provinsi AND b.periode = 'Mar 2026'
WHERE a.periode = 'Mar 2019'
  AND a.provinsi NOT IN ('Papua', 'Papua Barat')
ORDER BY delta_pp;
-- Membaik terbesar: NTT -3,57 | Memburuk: DKI Jakarta +0,49

-- 8) Kontribusi pulau terhadap total penduduk miskin, Mar 2026
SELECT pulau,
       ROUND(SUM(jumlah_miskin_ribu) / 1000.0, 2) AS jumlah_juta,
       ROUND(SUM(jumlah_miskin_ribu) /
             (SELECT SUM(jumlah_miskin_ribu) FROM kemiskinan_provinsi
              WHERE periode = 'Mar 2026') * 100, 1) AS pangsa_persen
FROM kemiskinan_provinsi
WHERE periode = 'Mar 2026'
GROUP BY pulau
ORDER BY jumlah_juta DESC;
-- Jawa 12,02 jt = 52,4%

-- 9) Tren Gini total, kota, desa
SELECT periode,
       MAX(CASE WHEN daerah = 'Total' THEN gini_ratio END) AS gini_total,
       MAX(CASE WHEN daerah = 'Perkotaan' THEN gini_ratio END) AS gini_kota,
       MAX(CASE WHEN daerah = 'Perdesaan' THEN gini_ratio END) AS gini_desa
FROM gini_nasional
GROUP BY periode
ORDER BY periode;

-- 10) Kedalaman & keparahan: dari puncak pandemi ke terbaru
SELECT periode, p1, p2
FROM kemiskinan_nasional
WHERE periode IN ('Sep 2020', 'Mar 2026');
-- P1: 1,75 -> 1,268 | P2: 0,47 -> 0,291
