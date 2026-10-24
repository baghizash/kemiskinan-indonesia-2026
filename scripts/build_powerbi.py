# -*- coding: utf-8 -*-
"""
Membangun kit Power BI untuk proyek Kemiskinan & Ketimpangan Indonesia 2026:
CSV model bintang (grain terpisah), measures_dax.md (nama measure polos +
tabel verifikasi yang dihitung dari data yang sama), dashboard_layout.md,
build_guide.md, dan dashboard_preview_halaman1.png.
Jalankan setelah analysis.py.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
PBI = os.path.join(ROOT, "powerbi")
CH = os.path.join(ROOT, "charts")
os.makedirs(PBI, exist_ok=True)

RED = "#A63D40"; DEEP = "#5E262B"; PUMPKIN = "#E07B39"; OAT = "#FAF6EF"
SLATE = "#2E2A26"; GREY = "#8A7F76"; TAUPE = "#C08552"; GOLD = "#D9A441"

nas = pd.read_csv(os.path.join(DATA, "kemiskinan_nasional.csv"))
kd = pd.read_csv(os.path.join(DATA, "kemiskinan_kota_desa.csv"))
gini = pd.read_csv(os.path.join(DATA, "gini_nasional.csv"))
prov = pd.read_csv(os.path.join(DATA, "kemiskinan_provinsi.csv"))
F = json.load(open(os.path.join(ROOT, "findings.json")))

URUT = {p: i + 1 for i, p in enumerate(nas.periode)}
PID = {p: int(str(nas.set_index("periode").loc[p, "tahun"]) +
              ("03" if nas.set_index("periode").loc[p, "bulan"] == "Maret" else "09"))
       for p in nas.periode}
nas_i = nas.set_index("periode")

# ------------------------------------------------------------------ dimensi
dim_periode = pd.DataFrame({
    "periode_id": [PID[p] for p in nas.periode],
    "periode": nas.periode,
    "tahun": nas.tahun,
    "bulan": nas.bulan,
    "urutan": [URUT[p] for p in nas.periode],
})
dim_periode.to_csv(os.path.join(PBI, "dim_periode.csv"), index=False)

dim_prov = (prov[["provinsi", "pulau"]].drop_duplicates()
            .sort_values("provinsi").reset_index(drop=True))
dim_prov.to_csv(os.path.join(PBI, "dim_provinsi.csv"), index=False)

# ------------------------------------------------------------------ fakta
fact_nas = nas.copy()
fact_nas["periode_id"] = fact_nas.periode.map(PID)
fact_nas = fact_nas[["periode_id", "periode", "persen_miskin", "jumlah_miskin_juta",
                     "garis_kemiskinan_rp", "gkm_rp", "gkbm_rp", "p1", "p2"]]
fact_nas.to_csv(os.path.join(PBI, "fact_kemiskinan_nasional.csv"), index=False)

fact_kd = kd.copy()
fact_kd["periode_id"] = fact_kd.periode.map(PID)
fact_kd = fact_kd[["periode_id", "periode", "daerah", "persen_miskin",
                   "jumlah_miskin_juta", "p1", "p2"]]
fact_kd.to_csv(os.path.join(PBI, "fact_kemiskinan_kota_desa.csv"), index=False)

fact_gini = gini.copy()
fact_gini["periode_id"] = fact_gini.periode.map(PID)
fact_gini = fact_gini[["periode_id", "periode", "daerah", "gini_ratio",
                        "pangsa_40_terbawah_persen"]]
fact_gini.to_csv(os.path.join(PBI, "fact_gini.csv"), index=False)

fact_prov = prov.copy()
fact_prov["periode_id"] = fact_prov.periode.map(PID)
fact_prov = fact_prov[["periode_id", "periode", "provinsi", "persen_miskin",
                       "jumlah_miskin_ribu", "garis_kemiskinan_rp"]]
fact_prov.to_csv(os.path.join(PBI, "fact_kemiskinan_provinsi.csv"), index=False)
print("kit CSV: dim_periode(14), dim_provinsi(38), fact_nasional(14),",
      "fact_kota_desa(28), fact_gini(42), fact_provinsi(186)")

# ------------------------------------------------------------------ DAX
t = F["terbaru"]; p26 = prov[prov.periode == "Mar 2026"]
MEASURES_MD = f"""# Measure DAX — Kemiskinan & Ketimpangan Indonesia 2026

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
| Persen Miskin Mar 2026 | {t['persen']:.2f} |
| Persen Miskin Mar 2019 | {F['mar2019']['persen']:.2f} |
| Perubahan Persen Miskin 2019 ke 2026 | {F['delta_2019_2026_pp']:.2f} |
| Jumlah Miskin Mar 2026 Juta | {t['jumlah_juta']:.2f} |
| Persen Miskin Puncak Pandemi Sep 2020 | {F['puncak_pandemi']['persen']:.2f} |
| Garis Kemiskinan Mar 2026 | {t['garis_kemiskinan_rp']:,} |
| P1 Mar 2026 | {F['p1p2']['p1_mar2026']:.3f} |
| P2 Mar 2026 | {F['p1p2']['p2_mar2026']:.3f} |
| Gini Mar 2026 | {F['gini']['mar2026']:.3f} |
| Gini Kota Mar 2026 | {F['gini']['kota_mar2026']:.3f} |
| Gini Desa Mar 2026 | {F['gini']['desa_mar2026']:.3f} |
| Provinsi Di Atas Nasional Mar 2026 | {F['provinsi_di_atas_nasional_mar2026']} |
| Jumlah Miskin Provinsi Ribu (filter Mar 2026) | {p26.jumlah_miskin_ribu.sum():,.2f} |

Catatan: jumlah provinsi Maret 2026 jika dijumlah = 22.929,74 ribu ≈ total
nasional 22,93 juta (selisih pembulatan BPS). Nilai P1/P2 kini lengkap
Mar 2019–Mar 2026 (14 periode, dari Tabel 6 BRS Profil Kemiskinan).
"""
with open(os.path.join(PBI, "measures_dax.md"), "w") as f:
    f.write(MEASURES_MD)

LAYOUT = """# Layout Dashboard Power BI — Kemiskinan & Ketimpangan Indonesia 2026

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
"""
with open(os.path.join(PBI, "dashboard_layout.md"), "w") as f:
    f.write(LAYOUT)

GUIDE = """# Panduan Merakit Dashboard — Kemiskinan & Ketimpangan Indonesia 2026

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
"""
with open(os.path.join(PBI, "build_guide.md"), "w") as f:
    f.write(GUIDE)

# ------------------------------------------------------------------ preview
fig = plt.figure(figsize=(12.8, 7.2))
fig.patch.set_facecolor(OAT)
axbg = fig.add_axes([0, 0, 1, 1]); axbg.axis("off")
axbg.add_patch(plt.Rectangle((0, 0.90), 1, 0.10, color=DEEP, transform=axbg.transAxes))
axbg.text(0.03, 0.965, "KEMISKINAN & KETIMPANGAN INDONESIA 2026 — RINGKASAN NASIONAL",
          transform=axbg.transAxes, color="white", fontsize=15, fontweight="bold", va="center")
axbg.text(0.03, 0.925, "Data BPS (BRS Profil Kemiskinan & Gini) • Seri Maret & September 2019–2026",
          transform=axbg.transAxes, color="#EAD9C8", fontsize=10, va="center")
kpis = [("Persen Miskin\nMar 2026", "8,07%", "dari 9,41% (Mar 2019)"),
        ("Jumlah Miskin\nMar 2026", "22,93 jt", "puncak pandemi 27,55 jt"),
        ("Garis Kemiskinan\nMar 2026", "Rp669.235", "/kapita/bulan"),
        ("Gini Ratio\nMar 2026", "0,368", "kota 0,387 • desa 0,296")]
for i, (lab, val, sub) in enumerate(kpis):
    xx = 0.03 + i * 0.243
    axbg.add_patch(plt.Rectangle((xx, 0.70), 0.225, 0.17, facecolor="white",
                                 edgecolor="#E3D5C3", transform=axbg.transAxes))
    axbg.text(xx + 0.012, 0.845, lab, transform=axbg.transAxes, fontsize=9.5, color=GREY, va="top")
    axbg.text(xx + 0.012, 0.775, val, transform=axbg.transAxes, fontsize=19,
              color=RED, fontweight="bold", va="center")
    axbg.text(xx + 0.012, 0.715, sub, transform=axbg.transAxes, fontsize=8.5, color=SLATE, va="center")
ax1 = fig.add_axes([0.045, 0.10, 0.56, 0.52]); ax1.set_facecolor("white")
ax1.plot(nas.periode, nas.persen_miskin, color=RED, lw=2.6, marker="o", ms=4)
ax1.fill_between(range(len(nas)), nas.persen_miskin, 7.4, color=RED, alpha=0.08)
ax1.set_ylim(7.4, 10.7); ax1.set_title("Persentase penduduk miskin per periode (%)",
                                       fontsize=11, color=DEEP, fontweight="bold")
plt.setp(ax1.get_xticklabels(), rotation=38, ha="left", fontsize=8)
ax2 = fig.add_axes([0.665, 0.10, 0.30, 0.52]); ax2.set_facecolor("white")
top = prov[prov.periode == "Mar 2026"].nlargest(6, "persen_miskin").iloc[::-1]
ax2.barh(top.provinsi, top.persen_miskin, color=RED)
ax2.set_title("Provinsi tertinggi, Mar 2026 (%)", fontsize=11, color=DEEP, fontweight="bold")
ax2.tick_params(labelsize=8.5)
fig.savefig(os.path.join(PBI, "dashboard_preview_halaman1.png"), dpi=170)
plt.close(fig)
print("measures_dax.md, dashboard_layout.md, build_guide.md, preview tertulis")
