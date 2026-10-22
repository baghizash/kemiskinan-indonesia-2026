# -*- coding: utf-8 -*-
"""
Analisis Kemiskinan & Ketimpangan Indonesia 2026 — membaca CSV kompilasi
BPS di data/, menghitung findings.json (dengan verifikasi silang) dan
membuat 12 chart PNG berlabel Bahasa Indonesia.
Jalankan: ~/workspace/mienv/bin/python scripts/analysis.py
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
DATA = os.path.join(ROOT, "data")
CHARTS = os.path.join(ROOT, "charts")
os.makedirs(CHARTS, exist_ok=True)

# Palet (kombinasi favorit user #4: muted red + oat + pumpkin)
RED = "#A63D40"; DEEP = "#5E262B"; PUMPKIN = "#E07B39"; OAT = "#FAF6EF"
SLATE = "#2E2A26"; GREY = "#8A7F76"; TAUPE = "#C08552"; GOLD = "#D9A441"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "text.color": SLATE, "axes.edgecolor": "#D8CFC4",
    "axes.labelcolor": SLATE, "xtick.color": SLATE, "ytick.color": SLATE,
    "figure.facecolor": "white", "axes.facecolor": "white",
    "axes.grid": True, "grid.color": "#EFE7DB", "grid.linewidth": 0.7,
    "font.size": 10,
})

LBL_SHORT = {"Mar 2019": "Mar 19", "Sep 2019": "Sep 19", "Mar 2020": "Mar 20",
             "Sep 2020": "Sep 20", "Mar 2021": "Mar 21", "Sep 2021": "Sep 21",
             "Mar 2022": "Mar 22", "Sep 2022": "Sep 22", "Mar 2023": "Mar 23",
             "Mar 2024": "Mar 24", "Sep 2024": "Sep 24", "Mar 2025": "Mar 25",
             "Sep 2025": "Sep 25", "Mar 2026": "Mar 26"}


def rp(x):
    return "Rp" + f"{int(round(x)):,}".replace(",", ".")


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, name), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("chart:", name)


# ------------------------------------------------------------------ muat data
nas = pd.read_csv(os.path.join(DATA, "kemiskinan_nasional.csv"))
kd = pd.read_csv(os.path.join(DATA, "kemiskinan_kota_desa.csv"))
gini = pd.read_csv(os.path.join(DATA, "gini_nasional.csv"))
prov = pd.read_csv(os.path.join(DATA, "kemiskinan_provinsi.csv"))
URUT = {p: i for i, p in enumerate(nas.periode)}
nas["u"] = nas.periode.map(URUT)
kd["u"] = kd.periode.map(URUT)
gini["u"] = gini.periode.map(URUT)

N = nas.set_index("periode")
K = kd[kd.daerah == "Perkotaan"].set_index("periode")
D = kd[kd.daerah == "Perdesaan"].set_index("periode")
G = gini.pivot(index="periode", columns="daerah", values="gini_ratio")

# ------------------------------------------------------------- verifikasi dasar
# kota + desa (juta) harus sama dengan total nasional (toleransi pembulatan)
for p in nas.periode:
    s = K.loc[p, "jumlah_miskin_juta"] + D.loc[p, "jumlah_miskin_juta"]
    assert abs(s - N.loc[p, "jumlah_miskin_juta"]) <= 0.02, (p, s)
# jumlah provinsi Mar 2026 (ribu) ~ total nasional x1000
s26 = prov[prov.periode == "Mar 2026"].jumlah_miskin_ribu.sum()
assert abs(s26 - N.loc["Mar 2026", "jumlah_miskin_juta"] * 1000) < 5, s26
s25 = prov[prov.periode == "Mar 2025"].jumlah_miskin_ribu.sum()
assert abs(s25 - N.loc["Mar 2025", "jumlah_miskin_juta"] * 1000) < 5, s25
# GKM + GKBM = GK
assert ((nas.gkm_rp + nas.gkbm_rp) - nas.garis_kemiskinan_rp).abs().max() == 0
print("verifikasi dasar: LOLOS (kota+desa=total, provinsi=nasional, GKM+GKBM=GK)")

F = {}
# ------------------------------------------------------------- nasional
F["terbaru"] = {"periode": "Mar 2026",
                "persen": float(N.loc["Mar 2026", "persen_miskin"]),
                "jumlah_juta": float(N.loc["Mar 2026", "jumlah_miskin_juta"]),
                "garis_kemiskinan_rp": int(N.loc["Mar 2026", "garis_kemiskinan_rp"])}
F["mar2019"] = {"persen": float(N.loc["Mar 2019", "persen_miskin"]),
                "jumlah_juta": float(N.loc["Mar 2019", "jumlah_miskin_juta"]),
                "garis_kemiskinan_rp": int(N.loc["Mar 2019", "garis_kemiskinan_rp"])}
F["delta_2019_2026_pp"] = round(F["terbaru"]["persen"] - F["mar2019"]["persen"], 2)
F["delta_2019_2026_juta"] = round(F["terbaru"]["jumlah_juta"] - F["mar2019"]["jumlah_juta"], 2)
puncak = nas.loc[nas.persen_miskin.idxmax()]
F["puncak_pandemi"] = {"periode": puncak.periode, "persen": float(puncak.persen_miskin),
                       "jumlah_juta": float(puncak.jumlah_miskin_juta)}
F["lonjakan_pandemi_pp"] = round(F["puncak_pandemi"]["persen"] - F["mar2019"]["persen"], 2)
# periode pertama setelah Sep 2019 yang kembali di bawah level Mar 2019
sesudah = nas[nas.u > URUT["Sep 2019"]]
kembali = sesudah[sesudah.persen_miskin < F["mar2019"]["persen"]].iloc[0]
F["kembali_di_bawah_prapandemi"] = {"periode": kembali.periode,
                                    "persen": float(kembali.persen_miskin)}
gk19, gk26 = F["mar2019"]["garis_kemiskinan_rp"], F["terbaru"]["garis_kemiskinan_rp"]
F["gk_tumbuh_persen_2019_2026"] = round((gk26 / gk19 - 1) * 100, 1)
F["gk_cagr_persen"] = round(((gk26 / gk19) ** (1 / 7) - 1) * 100, 2)
F["pangsa_makanan_mar2026_persen"] = round(
    N.loc["Mar 2026", "gkm_rp"] / gk26 * 100, 2)
F["pangsa_makanan_mar2019_persen"] = round(
    N.loc["Mar 2019", "gkm_rp"] / gk19 * 100, 2)

# ------------------------------------------------------------- kota vs desa
F["gap_kota_desa_pp"] = {
    p: round(float(D.loc[p, "persen_miskin"] - K.loc[p, "persen_miskin"]), 2)
    for p in ["Mar 2019", "Sep 2020", "Mar 2026"]}
F["rasio_desa_kota_mar2026"] = round(
    float(D.loc["Mar 2026", "persen_miskin"] / K.loc["Mar 2026", "persen_miskin"]), 2)
F["kota_mar2026"] = {"persen": float(K.loc["Mar 2026", "persen_miskin"]),
                     "jumlah_juta": float(K.loc["Mar 2026", "jumlah_miskin_juta"])}
F["desa_mar2026"] = {"persen": float(D.loc["Mar 2026", "persen_miskin"]),
                     "jumlah_juta": float(D.loc["Mar 2026", "jumlah_miskin_juta"])}

# ------------------------------------------------------------- gini
F["gini"] = {
    "mar2019": float(G.loc["Mar 2019", "Total"]),
    "puncak": {"periode": str(G.Total.idxmax()), "nilai": float(G.Total.max())},
    "terendah": {"periode": str(G.Total.idxmin()), "nilai": float(G.Total.min())},
    "mar2026": float(G.loc["Mar 2026", "Total"]),
    "kota_mar2026": float(G.loc["Mar 2026", "Perkotaan"]),
    "desa_mar2026": float(G.loc["Mar 2026", "Perdesaan"]),
    "perubahan_sep2025_mar2026": round(
        float(G.loc["Mar 2026", "Total"] - G.loc["Sep 2025", "Total"]), 3),
}
F["pangsa_40_terbawah_mar2026_persen"] = float(
    gini[(gini.periode == "Mar 2026") & (gini.daerah == "Total")]
    .pangsa_40_terbawah_persen.iloc[0])

# ------------------------------------------------------------- P1 / P2
F["p1p2"] = {
    "p1_sep2020": float(N.loc["Sep 2020", "p1"]), "p2_sep2020": float(N.loc["Sep 2020", "p2"]),
    "p1_mar2026": float(N.loc["Mar 2026", "p1"]), "p2_mar2026": float(N.loc["Mar 2026", "p2"]),
    "p1_kota_mar2026": float(K.loc["Mar 2026", "p1"]), "p1_desa_mar2026": float(D.loc["Mar 2026", "p1"]),
    "p2_kota_mar2026": float(K.loc["Mar 2026", "p2"]), "p2_desa_mar2026": float(D.loc["Mar 2026", "p2"]),
    "p1_desa_sep2025": float(D.loc["Sep 2025", "p1"]),
    "p1_kota_sep2025": float(K.loc["Sep 2025", "p1"]),
}
F["p1p2"]["p1_turun_persen_dari_puncak"] = round(
    (F["p1p2"]["p1_mar2026"] / F["p1p2"]["p1_sep2020"] - 1) * 100, 1)

# ------------------------------------------------------------- provinsi
p26 = prov[prov.periode == "Mar 2026"].copy()
p19 = prov[prov.periode == "Mar 2019"].copy()
F["provinsi_mar2026"] = {
    "tertinggi": {"provinsi": p26.loc[p26.persen_miskin.idxmax(), "provinsi"],
                  "persen": float(p26.persen_miskin.max())},
    "terendah": {"provinsi": p26.loc[p26.persen_miskin.idxmin(), "provinsi"],
                 "persen": float(p26.persen_miskin.min())},
}
F["provinsi_mar2026"]["gap_pp"] = round(
    F["provinsi_mar2026"]["tertinggi"]["persen"] - F["provinsi_mar2026"]["terendah"]["persen"], 2)
F["provinsi_mar2026"]["rasio"] = round(
    F["provinsi_mar2026"]["tertinggi"]["persen"] / F["provinsi_mar2026"]["terendah"]["persen"], 2)
F["provinsi_di_atas_nasional_mar2026"] = int((p26.persen_miskin > F["terbaru"]["persen"]).sum())
jawa26 = p26[p26.pulau == "Jawa"].jumlah_miskin_ribu.sum()
F["pangsa_jawa_mar2026_persen"] = round(jawa26 / (F["terbaru"]["jumlah_juta"] * 1000) * 100, 2)
pulau26 = p26.groupby("pulau").jumlah_miskin_ribu.sum().sort_values(ascending=False)
F["jumlah_per_pulau_mar2026_juta"] = {k: round(v / 1000, 2) for k, v in pulau26.items()}

gab = p19.set_index("provinsi").persen_miskin.rename("p19").to_frame()
gab["p26"] = p26.set_index("provinsi").persen_miskin
gab = gab.drop(index=["Papua", "Papua Barat"])  # wilayah 2019 tidak sebanding (pemekaran 2022)
gab["delta_pp"] = (gab.p26 - gab.p19).round(2)
F["perubahan_2019_2026_32provinsi"] = {
    "membaik_terbesar": [
        {"provinsi": k, "delta_pp": float(v)}
        for k, v in gab.delta_pp.nsmallest(5).items()],
    "memburuk": [
        {"provinsi": k, "delta_pp": float(v)}
        for k, v in gab[ gab.delta_pp > 0].delta_pp.sort_values(ascending=False).items()],
    "jumlah_membaik": int((gab.delta_pp < 0).sum()),
    "jumlah_total": int(len(gab)),
}
gk26p = prov[(prov.periode == "Mar 2026") & (prov.garis_kemiskinan_rp.notna())]
F["gk_provinsi_mar2026"] = {
    "tertinggi": {"provinsi": gk26p.loc[gk26p.garis_kemiskinan_rp.idxmax(), "provinsi"],
                  "rp": int(gk26p.garis_kemiskinan_rp.max())},
    "terendah": {"provinsi": gk26p.loc[gk26p.garis_kemiskinan_rp.idxmin(), "provinsi"],
                 "rp": int(gk26p.garis_kemiskinan_rp.min())},
}
top_jml = p26.nlargest(3, "jumlah_miskin_ribu")
F["jumlah_terbesar_mar2026"] = [
    {"provinsi": r.provinsi, "ribu": float(r.jumlah_miskin_ribu)} for r in top_jml.itertuples()]

with open(os.path.join(ROOT, "findings.json"), "w") as f:
    json.dump(F, f, indent=2, ensure_ascii=False)
print("findings.json tertulis")
print(json.dumps({k: F[k] for k in ["delta_2019_2026_pp", "puncak_pandemi",
                                    "kembali_di_bawah_prapandemi", "gk_tumbuh_persen_2019_2026",
                                    "provinsi_di_atas_nasional_mar2026",
                                    "pangsa_jawa_mar2026_persen"]}, indent=1))

x = np.arange(len(nas))
xs = [LBL_SHORT[p] for p in nas.periode]

# ============================================================ 01 tren nasional
fig, ax1 = plt.subplots(figsize=(9.6, 4.6))
ax1.plot(x, nas.persen_miskin, color=RED, lw=2.6, marker="o", ms=4.5, label="Persentase (%)")
ax1.fill_between(x, nas.persen_miskin, 7.6, color=RED, alpha=0.07)
ax1.set_ylabel("Persentase penduduk miskin (%)")
ax1.set_ylim(7.6, 10.8); ax1.set_xticks(x); ax1.set_xticklabels(xs, rotation=35, ha="left")
ax2 = ax1.twinx(); ax2.grid(False)
ax2.bar(x, nas.jumlah_miskin_juta, color=TAUPE, alpha=0.45, width=0.62, label="Jumlah (juta)")
ax2.set_ylabel("Jumlah penduduk miskin (juta)"); ax2.set_ylim(20, 30)
for xi, v in zip(x, nas.persen_miskin):
    ax1.annotate(f"{v:.2f}".replace(".", ","), (xi, v), textcoords="offset points",
                 xytext=(0, 7), ha="center", fontsize=8.3, color=DEEP, fontweight="bold")
ax1.set_title("Kemiskinan Nasional 2019–2026: Puncak Pandemi Sep 2020 (10,19%), Kini 8,07%",
              fontsize=12, fontweight="bold", color=DEEP)
h1, l1 = ax1.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper right", frameon=False, fontsize=9)
save(fig, "01_tren_nasional.png")

# ============================================================ 02 lonjakan & pemulihan
fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.plot(x, nas.persen_miskin, color=RED, lw=2.6, marker="o", ms=4.5)
ax.axhline(9.41, color=GREY, ls="--", lw=1.2)
ax.annotate("Level prapandemi Mar 2019: 9,41%", (0.2, 9.52), fontsize=9.5, color=GREY)
ax.annotate("Puncak pandemi\nSep 2020: 10,19%", (3, 10.19), textcoords="offset points",
            xytext=(-6, 12), fontsize=10, color=DEEP, fontweight="bold")
xi23 = URUT["Mar 2023"]
ax.annotate("Mar 2023: 9,36%\npertama di bawah prapandemi", (xi23, 9.36),
            textcoords="offset points", xytext=(-16, -38), fontsize=10,
            color=DEEP, fontweight="bold")
ax.annotate("Mar 2026: 8,07%\nterendah dalam seri", (13, 8.07), textcoords="offset points",
            xytext=(-58, 16), fontsize=10, color=PUMPKIN, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left"); ax.set_ylim(7.7, 10.7)
ax.set_ylabel("Persentase penduduk miskin (%)")
ax.set_title("Lonjakan Pandemi dan Jalan Pemulihannya", fontsize=12, fontweight="bold", color=DEEP)
save(fig, "02_pandemi_pemulihan.png")

# ============================================================ 03 garis kemiskinan
fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.fill_between(x, nas.gkm_rp / 1000, color=PUMPKIN, alpha=0.85, label="Makanan (GKM)")
ax.fill_between(x, nas.gkm_rp / 1000, nas.garis_kemiskinan_rp / 1000, color=TAUPE,
                alpha=0.75, label="Bukan makanan (GKBM)")
ax.plot(x, nas.garis_kemiskinan_rp / 1000, color=DEEP, lw=2.2)
for xi, v in [(0, 425.25), (13, 669.235)]:
    ax.annotate(rp(v * 1000), (xi, v), textcoords="offset points",
                xytext=(0, 8), ha="center", fontsize=10, fontweight="bold", color=DEEP)
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left")
ax.set_ylabel("Rp ribu/kapita/bulan")
ax.set_title("Garis Kemiskinan Naik 57,4% dalam 7 Tahun — 74,7% di Antaranya Makanan (Mar 2026)",
             fontsize=11.5, fontweight="bold", color=DEEP)
ax.legend(frameon=False, fontsize=9, loc="upper left")
save(fig, "03_garis_kemiskinan.png")

# ============================================================ 04 kota vs desa
fig, ax = plt.subplots(figsize=(9.6, 4.4))
kk = kd[kd.daerah == "Perkotaan"].sort_values("u")
dd = kd[kd.daerah == "Perdesaan"].sort_values("u")
ax.plot(x, dd.persen_miskin, color=RED, lw=2.6, marker="o", ms=4.5, label="Perdesaan")
ax.plot(x, kk.persen_miskin, color=PUMPKIN, lw=2.6, marker="o", ms=4.5, label="Perkotaan")
ax.fill_between(x, kk.persen_miskin, dd.persen_miskin, color=RED, alpha=0.08)
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left"); ax.set_ylim(5.8, 14)
ax.set_ylabel("Persentase penduduk miskin (%)")
ax.set_title("Kemiskinan Desa Selalu ±2 Kali Kota — Keduanya Turun ke Titik Terendah di Mar 2026",
             fontsize=11.5, fontweight="bold", color=DEEP)
ax.legend(frameon=False, fontsize=10)
save(fig, "04_kota_desa.png")

# ============================================================ 05 gap kota-desa
gap = (D.persen_miskin - K.persen_miskin).reindex(nas.periode)
fig, ax = plt.subplots(figsize=(9.6, 4.2))
ax.bar(x, gap, color=TAUPE, width=0.62)
ax.plot(x, gap, color=DEEP, lw=1.6)
for xi, v in zip(x, gap):
    ax.annotate(f"{v:.2f}".replace(".", ","), (xi, v), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=8.3, color=DEEP)
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left"); ax.set_ylim(0, 7)
ax.set_ylabel("Selisih desa − kota (poin persen)")
ax.set_title("Kesenjangan Kota–Desa Menyempit: 6,16 Poin (Mar 2019) → 4,33 Poin (Mar 2026)",
             fontsize=11.5, fontweight="bold", color=DEEP)
save(fig, "05_gap_kota_desa.png")

# ============================================================ 06 gini
fig, ax = plt.subplots(figsize=(9.6, 4.4))
gt = gini[gini.daerah == "Total"].sort_values("u")
gk_ = gini[gini.daerah == "Perkotaan"].sort_values("u")
gd = gini[gini.daerah == "Perdesaan"].sort_values("u")
ax.plot(x, gt.gini_ratio, color=DEEP, lw=2.8, marker="o", ms=5, label="Total")
ax.plot(x, gk_.gini_ratio, color=RED, lw=2.0, marker="s", ms=4, label="Perkotaan")
ax.plot(x, gd.gini_ratio, color=PUMPKIN, lw=2.0, marker="^", ms=4.5, label="Perdesaan")
ax.annotate("Puncak Mar 2023: 0,388", (URUT["Mar 2023"], 0.388), textcoords="offset points",
            xytext=(-30, 10), fontsize=10, fontweight="bold", color=DEEP)
ax.annotate("Sep 2025: 0,363\n(terendah) lalu naik\nke 0,368 (Mar 2026)", (12.4, 0.362),
            textcoords="offset points", xytext=(-118, -6), fontsize=9.5, color=PUMPKIN,
            fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left"); ax.set_ylim(0.28, 0.42)
ax.set_ylabel("Gini Ratio")
ax.set_title("Ketimpangan: Gini Menyempit Perlahan, tetapi Kota Jauh Lebih Timpang dari Desa",
             fontsize=11.5, fontweight="bold", color=DEEP)
ax.legend(frameon=False, fontsize=10, loc="lower left")
save(fig, "06_gini.png")

# ============================================================ 07 provinsi Mar 2026
p26s = p26.sort_values("persen_miskin")
fig, ax = plt.subplots(figsize=(7.6, 9.2))
colors = [RED if v > 8.07 else TAUPE for v in p26s.persen_miskin]
ax.barh(p26s.provinsi, p26s.persen_miskin, color=colors)
ax.axvline(8.07, color=DEEP, ls="--", lw=1.3)
ax.annotate("Nasional 8,07%", (8.3, 1.2), fontsize=9.5, color=DEEP, fontweight="bold")
for v, p in zip(p26s.persen_miskin, p26s.provinsi):
    ax.annotate(f"{v:.2f}".replace(".", ","), (v, p), textcoords="offset points",
                xytext=(4, -3), fontsize=8.3, color=SLATE)
ax.set_xlim(0, 34); ax.set_xlabel("Persentase penduduk miskin Mar 2026 (%)")
ax.set_title("Kemiskinan per Provinsi, Maret 2026\nPapua Tengah 30,41% — Bali 3,44%",
             fontsize=12, fontweight="bold", color=DEEP)
save(fig, "07_provinsi_mar2026.png")

# ============================================================ 08 perubahan 2019-2026
gabs = gab.sort_values("delta_pp")
fig, ax = plt.subplots(figsize=(7.6, 8.6))
cols = [RED if v > 0 else "#5B7553" for v in gabs.delta_pp]
ax.barh(gabs.index, gabs.delta_pp, color=cols)
ax.axvline(0, color=DEEP, lw=1.2)
for v, p in zip(gabs.delta_pp, gabs.index):
    ax.annotate(f"{v:+.2f}".replace(".", ","), (v, p), textcoords="offset points",
                xytext=(4 if v >= 0 else -34, -3), fontsize=8.3, color=SLATE)
ax.set_xlim(-4.4, 1.2); ax.set_xlabel("Perubahan poin persen, Mar 2019 → Mar 2026")
ax.set_title("Perubahan Kemiskinan Provinsi 2019 → 2026 (32 provinsi sebanding)\nHampir Semua Membaik; NTT Membaik Paling Besar",
             fontsize=11.5, fontweight="bold", color=DEEP)
save(fig, "08_perubahan_provinsi.png")

# ============================================================ 09 jumlah per pulau
fig, ax = plt.subplots(figsize=(9.2, 4.4))
pl = pulau26 / 1000
ax.bar(pl.index, pl.values, color=[RED if k == "Jawa" else TAUPE for k in pl.index])
for k, v in pl.items():
    ax.annotate(f"{v:.2f}".replace(".", ",") + " jt", (k, v), textcoords="offset points",
                xytext=(0, 6), ha="center", fontsize=10, fontweight="bold", color=DEEP)
ax.set_ylabel("Jumlah penduduk miskin (juta)")
ax.set_title("52,4% Penduduk Miskin Indonesia Tinggal di Pulau Jawa (Mar 2026)",
             fontsize=12, fontweight="bold", color=DEEP)
plt.setp(ax.get_xticklabels(), rotation=12, ha="right")
save(fig, "09_jumlah_pulau.png")

# ============================================================ 10 P1 P2
sub = nas[nas.p1.notna()]
fig, ax = plt.subplots(figsize=(9.6, 4.4))
ax.plot(sub.u, sub.p1, color=RED, lw=2.6, marker="o", ms=4.5, label="Indeks Kedalaman (P1)")
ax.plot(sub.u, sub.p2, color=PUMPKIN, lw=2.6, marker="s", ms=4.5, label="Indeks Keparahan (P2)")
ax.annotate("P1 puncak pandemi\nSep 2020: 1,75", (URUT["Sep 2020"], 1.75),
            textcoords="offset points", xytext=(8, 4), fontsize=10,
            fontweight="bold", color=DEEP)
ax.annotate("Mar 2026: P1 1,268 • P2 0,291\n(terendah dalam seri)", (13, 1.268),
            textcoords="offset points", xytext=(-150, 26), fontsize=10,
            fontweight="bold", color=PUMPKIN)
ax.set_xticks(x); ax.set_xticklabels(xs, rotation=35, ha="left"); ax.set_ylim(0, 2.0)
ax.set_ylabel("Nilai indeks")
ax.set_title("Kemiskinan Makin Dangkal: P1 Turun 27,5% dari Puncak Pandemi",
             fontsize=12, fontweight="bold", color=DEEP)
ax.legend(frameon=False, fontsize=10)
save(fig, "10_p1_p2.png")

# ============================================================ 11 P1 kota vs desa
fig, ax = plt.subplots(figsize=(9.2, 4.4))
labels = ["P1 Kota", "P1 Desa", "P2 Kota", "P2 Desa"]
v20 = [K.loc["Sep 2020", "p1"], D.loc["Sep 2020", "p1"],
       K.loc["Sep 2020", "p2"], D.loc["Sep 2020", "p2"]]
v26 = [K.loc["Mar 2026", "p1"], D.loc["Mar 2026", "p1"],
       K.loc["Mar 2026", "p2"], D.loc["Mar 2026", "p2"]]
xx = np.arange(4); wdt = 0.38
ax.bar(xx - wdt / 2, v20, wdt, color=TAUPE, label="Sep 2020 (puncak pandemi)")
ax.bar(xx + wdt / 2, v26, wdt, color=RED, label="Mar 2026")
for xi, v in list(zip(xx - wdt / 2, v20)) + list(zip(xx + wdt / 2, v26)):
    ax.annotate(f"{v:.3f}".replace(".", ","), (xi, v), textcoords="offset points",
                xytext=(0, 5), ha="center", fontsize=9, color=DEEP, fontweight="bold")
ax.set_xticks(xx); ax.set_xticklabels(labels); ax.set_ylim(0, 2.7)
ax.set_ylabel("Nilai indeks")
ax.set_title("Kedalaman Desa 1,8× Kota — dan P1 Desa Justru Naik di Semester Terakhir",
             fontsize=11.5, fontweight="bold", color=DEEP)
ax.legend(frameon=False, fontsize=9.5)
save(fig, "11_p1_kota_desa.png")

# ============================================================ 12 GK provinsi Mar 2026
gks = gk26p.sort_values("garis_kemiskinan_rp")
fig, ax = plt.subplots(figsize=(7.6, 9.2))
ax.barh(gks.provinsi, gks.garis_kemiskinan_rp / 1000, color=TAUPE)
ax.axvline(669.235, color=RED, ls="--", lw=1.3)
ax.annotate("Nasional Rp669 rb", (676, 1.2), fontsize=9.5, color=RED, fontweight="bold")
for v, p in zip(gks.garis_kemiskinan_rp, gks.provinsi):
    ax.annotate(rp(v), (v / 1000, p), textcoords="offset points",
                xytext=(4, -3), fontsize=8.0, color=SLATE)
ax.set_xlim(0, 1450); ax.set_xlabel("Garis kemiskinan Mar 2026 (Rp ribu/kapita/bulan)")
ax.set_title("Garis Kemiskinan per Provinsi, Maret 2026\nPapua Pegunungan Rp1,28 Jt — Sulawesi Barat Rp519 Rb",
             fontsize=11.5, fontweight="bold", color=DEEP)
save(fig, "12_gk_provinsi.png")

print("SELESAI: findings + 12 chart")
