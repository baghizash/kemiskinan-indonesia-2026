# Measure DAX — Kemiskinan & Ketimpangan Indonesia 2026

Model bintang: `fact_kemiskinan_nasional`, `fact_kemiskinan_kota_desa`,
`fact_gini`, `fact_kemiskinan_provinsi` → `dim_periode` (lewat `periode_id`)
dan `fact_kemiskinan_provinsi` → `dim_provinsi` (lewat `provinsi`).
Semua nama measure polos (tanpa tanda "=" di dalam nama). Periode dikunci
lewat filter `dim_periode[periode]` agar slicer di halaman lain tetap bisa
memakai measure rata-rata biasa.

## Measure utama

```dax
Rata Rata Persen Miskin =
AVERAGE ( fact_kemiskinan_nasional[persen_miskin] )
```

```dax
Persen Miskin Mar 2026 =
CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Mar 2026" )
```

```dax
Persen Miskin Mar 2019 =
CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Mar 2019" )
```

```dax
Perubahan Persen Miskin 2019 ke 2026 =
[Persen Miskin Mar 2026] - [Persen Miskin Mar 2019]
```

```dax
Jumlah Miskin Mar 2026 Juta =
CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[jumlah_miskin_juta] ),
    dim_periode[periode] = "Mar 2026" )
```

```dax
Persen Miskin Puncak Pandemi Sep 2020 =
CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Sep 2020" )
```

```dax
Garis Kemiskinan Mar 2026 =
CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[garis_kemiskinan_rp] ),
    dim_periode[periode] = "Mar 2026" )
```

```dax
P1 Mar 2026 =
CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[p1] ),
    dim_periode[periode] = "Mar 2026" )
```

```dax
P2 Mar 2026 =
CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[p2] ),
    dim_periode[periode] = "Mar 2026" )
```

```dax
Gini Ratio =
AVERAGE ( fact_gini[gini_ratio] )
```

```dax
Gini Mar 2026 =
CALCULATE ( [Gini Ratio], fact_gini[daerah] = "Total",
    dim_periode[periode] = "Mar 2026" )
```

```dax
Gini Kota Mar 2026 =
CALCULATE ( AVERAGE ( fact_gini[gini_ratio] ),
    fact_gini[daerah] = "Perkotaan", dim_periode[periode] = "Mar 2026" )
```

```dax
Gini Desa Mar 2026 =
CALCULATE ( AVERAGE ( fact_gini[gini_ratio] ),
    fact_gini[daerah] = "Perdesaan", dim_periode[periode] = "Mar 2026" )
```

```dax
Persen Miskin Provinsi =
AVERAGE ( fact_kemiskinan_provinsi[persen_miskin] )
```

```dax
Jumlah Miskin Provinsi Ribu =
SUM ( fact_kemiskinan_provinsi[jumlah_miskin_ribu] )
```

```dax
Provinsi Di Atas Nasional Mar 2026 =
CALCULATE ( COUNTROWS ( fact_kemiskinan_provinsi ),
    dim_periode[periode] = "Mar 2026",
    FILTER ( fact_kemiskinan_provinsi,
        fact_kemiskinan_provinsi[persen_miskin] > [Persen Miskin Mar 2026] ) )
```

```dax
Persen Miskin Kota Desa =
AVERAGE ( fact_kemiskinan_kota_desa[persen_miskin] )
```

## Tabel verifikasi (dihitung dari CSV kit yang sama)

| Measure | Nilai yang harus tampil |
|---|---|
| Persen Miskin Mar 2026 | 8.07 |
| Persen Miskin Mar 2019 | 9.41 |
| Perubahan Persen Miskin 2019 ke 2026 | -1.34 |
| Jumlah Miskin Mar 2026 Juta | 22.93 |
| Persen Miskin Puncak Pandemi Sep 2020 | 10.19 |
| Garis Kemiskinan Mar 2026 | 669,235 |
| P1 Mar 2026 | 1.268 |
| P2 Mar 2026 | 0.291 |
| Gini Mar 2026 | 0.368 |
| Gini Kota Mar 2026 | 0.387 |
| Gini Desa Mar 2026 | 0.296 |
| Provinsi Di Atas Nasional Mar 2026 | 20 |
| Jumlah Miskin Provinsi Ribu (filter Mar 2026) | 22,929.69 |

Catatan: jumlah provinsi Maret 2026 jika dijumlah = 22.929,74 ribu ≈ total
nasional 22,93 juta (selisih pembulatan BPS). Nilai P1/P2 untuk Mar & Sep 2019
kosong (tidak terverifikasi), jadi garis tren P1/P2 mulai Mar 2020.
