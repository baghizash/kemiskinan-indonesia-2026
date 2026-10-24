#!/usr/bin/env python3
"""Build the Kemiskinan2026 PBIP package (validated pattern, cf. Pariwisata2026).

Output: ~/workspace/pbip/Kemiskinan2026/ + copy at <project>/pbip/Kemiskinan2026/
Validate: python3 ~/workspace/pbip/validate_pbip.py ~/workspace/pbip/Kemiskinan2026
"""
import json, uuid, shutil
from pathlib import Path

NS = uuid.UUID('6f1c2a90-3b4d-4e5f-8a70-1b2c3d4e5f60')
def G(s): return str(uuid.uuid5(NS, s))

PROJ = 'Kemiskinan2026'
ROOT = Path.home() / 'workspace' / 'pbip' / PROJ
PROOT = Path(__file__).resolve().parent.parent
KIT = PROOT / 'powerbi'
REP = ROOT / f'{PROJ}.Report'
SEM = ROOT / f'{PROJ}.SemanticModel'
DEF_R = REP / 'definition'
DEF_S = SEM / 'definition'

VC = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.0.0/schema.json'
PG = 'https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json'

def W(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
def WJ(path, obj):
    W(path, json.dumps(obj, indent=2, ensure_ascii=False))

# ---------------------------------------------------------------- field refs
def col(e, p):  return {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def mea(e, p):  return {"Measure": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}
def agg(e, p, f=0): return {"Aggregation": {"Expression": {"SourceRef": {"Entity": e}}, "Function": f, "Property": p}}
def proj(field, e, p, native=None):
    return {"field": field, "queryRef": f"{e}.{p}", "nativeQueryRef": native or p}
def sortby(field, direction):
    return {"field": field, "direction": direction}

_fc = [0]
def catfilter(alias, e, p, values):
    _fc[0] += 1
    return {
        "name": f"flt{_fc[0]:014x}",
        "ordinal": _fc[0],
        "field": col(e, p),
        "type": "Categorical",
        "filter": {
            "Version": 2,
            "From": [{"Name": alias, "Entity": e, "Type": 0}],
            "Where": [{"Condition": {"In": {
                "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": alias}}, "Property": p}}],
                "Values": [[{"Literal": {"Value": f"'{v}'"}}] for v in values],
            }}}],
        },
        "isHiddenInViewMode": False,
        "isLockedInViewMode": False,
    }

def title_obj(text):
    return {"title": [{"properties": {
        "show": {"expr": {"Literal": {"Value": "true"}}},
        "text": {"expr": {"Literal": {"Value": f"'{text}'"}}},
        "bold": {"expr": {"Literal": {"Value": "true"}}},
    }}]}

def visual(name, x, y, w, h, vtype, qstate=None, title_text=None, filters=None,
           sorts=None, objects=None, z=0):
    v = {"$schema": VC, "name": name,
         "position": {"x": x, "y": y, "z": z, "height": h, "width": w, "tabOrder": z},
         "visual": {"visualType": vtype}}
    if qstate is not None:
        q = {"queryState": qstate}
        if sorts:
            q["sortDefinition"] = {"sort": sorts, "isDefaultSort": False}
        v["visual"]["query"] = q
    if objects is not None:
        v["visual"]["objects"] = objects
    if title_text:
        v["visual"]["visualContainerObjects"] = title_obj(title_text)
    if filters:
        v["filterConfig"] = {"filters": filters}
    return v

def textbox(name, x, y, w, h, text, size=14, bold=False, z=0):
    tr = {"value": text, "textStyle": {"fontFamily": "Segoe UI", "fontSize": size}}
    if bold:
        tr["textStyle"]["bold"] = True
    objects = {"general": [{"properties": {"paragraphs": [{
        "textRuns": [tr], "horizontalTextAlignment": "left"}]}}]}
    return visual(name, x, y, w, h, "textbox", objects=objects, z=z)

def slicer(name, x, y, w, h, e, p, z=0):
    return visual(name, x, y, w, h, "slicer",
                  qstate={"Values": {"projections": [proj(col(e, p), e, p)]}}, z=z)

# ------------------------------------------------------------------- TMDL
TABLES = {
    'dim_periode': [
        ('periode_id', 'int64', '0'), ('periode', 'string', None),
        ('tahun', 'int64', '0'), ('bulan', 'string', None), ('urutan', 'int64', '0')],
    'dim_provinsi': [
        ('provinsi', 'string', None), ('pulau', 'string', None)],
    'fact_kemiskinan_nasional': [
        ('periode_id', 'int64', '0'), ('periode', 'string', None),
        ('persen_miskin', 'double', '0.00'), ('jumlah_miskin_juta', 'double', '0.00'),
        ('garis_kemiskinan_rp', 'int64', '#,##0'), ('gkm_rp', 'int64', '#,##0'),
        ('gkbm_rp', 'int64', '#,##0'), ('p1', 'double', '0.000'), ('p2', 'double', '0.000')],
    'fact_kemiskinan_kota_desa': [
        ('periode_id', 'int64', '0'), ('periode', 'string', None),
        ('daerah', 'string', None), ('persen_miskin', 'double', '0.00'),
        ('jumlah_miskin_juta', 'double', '0.00'),
        ('p1', 'double', '0.000'), ('p2', 'double', '0.000')],
    'fact_gini': [
        ('periode_id', 'int64', '0'), ('periode', 'string', None),
        ('daerah', 'string', None), ('gini_ratio', 'double', '0.000'),
        ('pangsa_40_terbawah_persen', 'double', '0.00')],
    'fact_kemiskinan_provinsi': [
        ('periode_id', 'int64', '0'), ('periode', 'string', None),
        ('provinsi', 'string', None), ('persen_miskin', 'double', '0.00'),
        ('jumlah_miskin_ribu', 'double', '#,##0.00'),
        ('garis_kemiskinan_rp', 'int64', '#,##0')],
}
SORTBY = {('dim_periode', 'periode'): 'urutan'}
MTYPE = {'int64': 'Int64.Type', 'double': 'type number', 'string': 'type text', 'dateTime': 'type date'}

MEASURES = {
    'fact_kemiskinan_nasional': [
        ('Rata Rata Persen Miskin', 'AVERAGE ( fact_kemiskinan_nasional[persen_miskin] )', '0.00'),
        ('Persen Miskin Mar 2026', 'CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Mar 2026" )', '0.00'),
        ('Persen Miskin Mar 2019', 'CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Mar 2019" )', '0.00'),
        ('Perubahan Persen Miskin 2019 ke 2026', '[Persen Miskin Mar 2026] - [Persen Miskin Mar 2019]', '0.00'),
        ('Jumlah Miskin Mar 2026 Juta', 'CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[jumlah_miskin_juta] ), dim_periode[periode] = "Mar 2026" )', '0.00'),
        ('Persen Miskin Puncak Pandemi Sep 2020', 'CALCULATE ( [Rata Rata Persen Miskin], dim_periode[periode] = "Sep 2020" )', '0.00'),
        ('Garis Kemiskinan Mar 2026', 'CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[garis_kemiskinan_rp] ), dim_periode[periode] = "Mar 2026" )', '#,##0'),
        ('P1 Mar 2026', 'CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[p1] ), dim_periode[periode] = "Mar 2026" )', '0.000'),
        ('P2 Mar 2026', 'CALCULATE ( AVERAGE ( fact_kemiskinan_nasional[p2] ), dim_periode[periode] = "Mar 2026" )', '0.000'),
    ],
    'fact_gini': [
        ('Gini Ratio', 'AVERAGE ( fact_gini[gini_ratio] )', '0.000'),
        ('Gini Mar 2026', 'CALCULATE ( [Gini Ratio], fact_gini[daerah] = "Total", dim_periode[periode] = "Mar 2026" )', '0.000'),
        ('Gini Kota Mar 2026', 'CALCULATE ( AVERAGE ( fact_gini[gini_ratio] ), fact_gini[daerah] = "Perkotaan", dim_periode[periode] = "Mar 2026" )', '0.000'),
        ('Gini Desa Mar 2026', 'CALCULATE ( AVERAGE ( fact_gini[gini_ratio] ), fact_gini[daerah] = "Perdesaan", dim_periode[periode] = "Mar 2026" )', '0.000'),
    ],
    'fact_kemiskinan_provinsi': [
        ('Persen Miskin Provinsi', 'AVERAGE ( fact_kemiskinan_provinsi[persen_miskin] )', '0.00'),
        ('Jumlah Miskin Provinsi Ribu', 'SUM ( fact_kemiskinan_provinsi[jumlah_miskin_ribu] )', '#,##0.00'),
        ('Provinsi Di Atas Nasional Mar 2026', 'CALCULATE ( COUNTROWS ( fact_kemiskinan_provinsi ), dim_periode[periode] = "Mar 2026", FILTER ( fact_kemiskinan_provinsi, fact_kemiskinan_provinsi[persen_miskin] > [Persen Miskin Mar 2026] ) )', '0'),
    ],
    'fact_kemiskinan_kota_desa': [
        ('Persen Miskin Kota Desa', 'AVERAGE ( fact_kemiskinan_kota_desa[persen_miskin] )', '0.00'),
    ],
}

RELATIONSHIPS = [
    ('fact_kemiskinan_nasional', 'periode_id', 'dim_periode', 'periode_id'),
    ('fact_kemiskinan_kota_desa', 'periode_id', 'dim_periode', 'periode_id'),
    ('fact_gini', 'periode_id', 'dim_periode', 'periode_id'),
    ('fact_kemiskinan_provinsi', 'periode_id', 'dim_periode', 'periode_id'),
    ('fact_kemiskinan_provinsi', 'provinsi', 'dim_provinsi', 'provinsi'),
]

def table_tmdl(name):
    cols = TABLES[name]
    out = [f'table {name}', f'\tlineageTag: {G("tab-" + name)}', '']
    for mname, dax, fmt in MEASURES.get(name, []):
        if '\n' in dax:
            body = '\n'.join('\t\t\t' + ln for ln in dax.split('\n'))
            out.append(f"\tmeasure '{mname}' = ```")
            out.append(body)
            out.append('\t\t\t```')
        else:
            out.append(f"\tmeasure '{mname}' =")
            out.append(f'\t\t\t{dax}')
        out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("mea-" + name + "-" + mname)}')
        out.append('')
    for cname, dtype, fmt in cols:
        out.append(f'\tcolumn {cname}')
        out.append(f'\t\tdataType: {dtype}')
        if fmt:
            out.append(f'\t\tformatString: {fmt}')
        out.append(f'\t\tlineageTag: {G("col-" + name + "-" + cname)}')
        if (name, cname) in SORTBY:
            out.append(f'\t\tsortByColumn: {SORTBY[(name, cname)]}')
        out.append('\t\tsummarizeBy: none')
        out.append(f'\t\tsourceColumn: {cname}')
        out.append('')
    pairs = ', '.join(f'{{"{c}", {MTYPE[t]}}}' for c, t, _ in cols)
    out.append(f'\tpartition {name} = m')
    out.append('\t\tmode: import')
    out.append('\t\tsource = ```')
    out.append('\t\t\t\tlet')
    out.append(f'\t\t\t\t\tSource = Csv.Document(File.Contents(FolderData & "\\{name}.csv"), [Delimiter = ",", Columns = {len(cols)}, Encoding = 65001, QuoteStyle = QuoteStyle.None]),')
    out.append('\t\t\t\t\tPromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),')
    out.append(f'\t\t\t\t\tChangedType = Table.TransformColumnTypes(PromotedHeaders, {{{pairs}}})')
    out.append('\t\t\t\tin')
    out.append('\t\t\t\t\tChangedType')
    out.append('\t\t\t\t```')
    return '\n'.join(out) + '\n'

def build_model():
    WJ(SEM / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "SemanticModel", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-sem')}})
    WJ(SEM / 'definition.pbism', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/semanticModel/definitionProperties/2.0.0/schema.json",
        "version": "4.0", "settings": {}})
    W(DEF_S / 'database.tmdl', 'database\n\tcompatibilityLevel: 1600\n')
    refs = '\n'.join(f'ref table {t}' for t in TABLES)
    W(DEF_S / 'model.tmdl',
      f'model Model\n\tculture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n{refs}\n\nref expression FolderData\n')
    W(DEF_S / 'expressions.tmdl',
      'expression FolderData = ```\n'
      '\t\t"C:\\\\PowerBI\\\\Kemiskinan\\\\data" meta [IsParameterQuery = true, IsParameterQueryRequired = true, Type = "Text"]\n'
      '\t\t```\n'
      f'\tlineageTag: {G("expr-FolderData")}\n')
    rel = []
    for i, (ft, fc, tt, tc) in enumerate(RELATIONSHIPS):
        rel.append(f'relationship {G("rel-" + str(i))}')
        rel.append(f'\tfromColumn: {ft}.{fc}')
        rel.append(f'\ttoColumn: {tt}.{tc}')
        rel.append('\tcrossFilteringBehavior: oneDirection')
        rel.append('')
    W(DEF_S / 'relationships.tmdl', '\n'.join(rel))
    for t in TABLES:
        W(DEF_S / 'tables' / f'{t}.tmdl', table_tmdl(t))
    nodes = []
    for i, t in enumerate(TABLES):
        nodes.append({"location": {"x": (i % 3) * 300, "y": (i // 3) * 260},
                      "nodeIndex": t, "nodeLineageTag": G('tab-' + t),
                      "size": {"height": 200, "width": 234}, "zIndex": i})
    WJ(SEM / 'diagramLayout.json', {
        "version": "1.1.0",
        "diagrams": [{"ordinal": 0, "scrollPosition": {"x": 0, "y": 0}, "nodes": nodes,
                      "name": "All tables", "zoomValue": 100, "pinKeyFields": [],
                      "showExtraHeaderInfo": False, "hideKeyFieldsWhenCollapsed": False}],
        "selectedDiagram": "All tables", "defaultDiagram": "All tables"})

# ------------------------------------------------------------------ report
F_NAS = 'fact_kemiskinan_nasional'; F_KD = 'fact_kemiskinan_kota_desa'
F_GINI = 'fact_gini'; F_PROV = 'fact_kemiskinan_provinsi'
D_PER = 'dim_periode'; D_PROV = 'dim_provinsi'
MAR26 = lambda a='dp': catfilter(a, D_PER, 'periode', ['Mar 2026'])

def build_report():
    WJ(REP / '.platform', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/platform/platformProperties/1.0.0/schema.json",
        "metadata": {"type": "Report", "displayName": PROJ},
        "config": {"version": "2.0", "logicalId": G('platform-rep')}})
    WJ(REP / 'definition.pbir', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definitionProperties/2.0.0/schema.json",
        "version": "4.0",
        "datasetReference": {"byPath": {"path": f"../{PROJ}.SemanticModel"}}})
    WJ(DEF_R / 'version.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
        "version": "1.0.0"})
    WJ(DEF_R / 'report.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
        "themeCollection": {"baseTheme": {"name": "CY24SU10", "reportVersionAtImport": "5.60", "type": "SharedResources"}}})
    WJ(REP / 'StaticResources' / 'SharedResources' / 'BaseThemes' / 'CY24SU10.json', {
        "name": "CY24SU10",
        "dataColors": ["#A63D40", "#5E262B", "#E07B39", "#C08552", "#D9A441", "#8A7F76",
                       "#744EC2", "#D64550", "#197278", "#1AAB40", "#15C6F4", "#4092FF",
                       "#FF9B85", "#FFC36D", "#A0D8EF", "#5E4B8B"],
        "background": "#FAF6EF", "foreground": "#2E2A26", "tableAccent": "#A63D40"})

    pages = {}

    # ---- Page 1: Ringkasan Nasional
    p1 = []
    p1.append(textbox('v01Title', 0, 0, 900, 60, 'Kemiskinan & Ketimpangan Indonesia — Ringkasan Nasional', 20, bold=True, z=0))
    p1.append(slicer('v02SlicerPeriode', 930, 8, 330, 52, D_PER, 'periode', z=1))
    cards = [(F_NAS, 'Persen Miskin Mar 2026', 'Persen Miskin Mar 2026 (%)'),
             (F_NAS, 'Jumlah Miskin Mar 2026 Juta', 'Jumlah Miskin Mar 2026 (juta)'),
             (F_NAS, 'Garis Kemiskinan Mar 2026', 'Garis Kemiskinan Mar 2026 (Rp)'),
             (F_GINI, 'Gini Mar 2026', 'Gini Ratio Mar 2026')]
    for i, (ent, m, t) in enumerate(cards):
        p1.append(visual(f'v{3+i:02d}Card', i * 320, 76, 300, 110, 'card',
                         qstate={"Values": {"projections": [proj(mea(ent, m), ent, m)]}},
                         title_text=t, z=2 + i))
    p1.append(visual('v07LinePersen', 0, 200, 620, 250, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_PER, 'periode'), D_PER, 'periode')]},
                             "Y": {"projections": [proj(mea(F_NAS, 'Rata Rata Persen Miskin'), F_NAS, 'Rata Rata Persen Miskin')]}},
                     title_text='Persentase Penduduk Miskin per Periode (%)', z=6))
    p1.append(visual('v08ColJumlah', 640, 200, 620, 250, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(D_PER, 'periode'), D_PER, 'periode')]},
                             "Y": {"projections": [proj(agg(F_NAS, 'jumlah_miskin_juta', 0), F_NAS, 'jumlah_miskin_juta', 'Sum of jumlah_miskin_juta')]}},
                     title_text='Jumlah Penduduk Miskin per Periode (juta)', z=7))
    p1.append(textbox('v09Metode', 0, 466, 1260, 60,
                      'Sumber: BPS — BRS Profil Kemiskinan & Gini Ratio. Seri Maret & September 2019–2026 (tidak ada periode Sep 2023).', 12, z=8))
    pages['pg01Ringkasan'] = ('Ringkasan Nasional', p1)

    # ---- Page 2: Kota vs Desa
    p2 = []
    p2.append(textbox('v01Title', 0, 0, 900, 60, 'Kota vs Desa — Kesenjangan yang Menyempit', 20, bold=True, z=0))
    p2.append(slicer('v02SlicerPeriode', 930, 8, 330, 52, D_PER, 'periode', z=1))
    p2.append(visual('v03LineKD', 0, 76, 760, 300, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_PER, 'periode'), D_PER, 'periode')]},
                             "Y": {"projections": [proj(mea(F_KD, 'Persen Miskin Kota Desa'), F_KD, 'Persen Miskin Kota Desa')]},
                             "Series": {"projections": [proj(col(F_KD, 'daerah'), F_KD, 'daerah')]}},
                     title_text='Persen Miskin Kota vs Desa per Periode (%)', z=2))
    p2.append(visual('v04CardKota', 780, 76, 230, 140, 'card',
                     qstate={"Values": {"projections": [proj(mea(F_KD, 'Persen Miskin Kota Desa'), F_KD, 'Persen Miskin Kota Desa')]}},
                     title_text='Kota Mar 2026 (%)',
                     filters=[MAR26(), catfilter('fk', F_KD, 'daerah', ['Perkotaan'])], z=3))
    p2.append(visual('v05CardDesa', 1030, 76, 230, 140, 'card',
                     qstate={"Values": {"projections": [proj(mea(F_KD, 'Persen Miskin Kota Desa'), F_KD, 'Persen Miskin Kota Desa')]}},
                     title_text='Desa Mar 2026 (%)',
                     filters=[MAR26(), catfilter('fk', F_KD, 'daerah', ['Perdesaan'])], z=4))
    p2.append(visual('v06BarP1', 780, 232, 480, 144, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(F_KD, 'daerah'), F_KD, 'daerah')]},
                             "Y": {"projections": [proj(agg(F_KD, 'p1', 1), F_KD, 'p1', 'Average of p1')]}},
                     title_text='Indeks Kedalaman (P1) per Daerah — Mar 2026',
                     filters=[MAR26()], z=5))
    p2.append(visual('v07ColJumlahKD', 0, 392, 620, 268, 'clusteredColumnChart',
                     qstate={"Category": {"projections": [proj(col(F_KD, 'daerah'), F_KD, 'daerah')]},
                             "Y": {"projections": [proj(agg(F_KD, 'jumlah_miskin_juta', 0), F_KD, 'jumlah_miskin_juta', 'Sum of jumlah_miskin_juta')]}},
                     title_text='Jumlah Penduduk Miskin per Daerah — Mar 2026 (juta)',
                     filters=[MAR26('dp2')], z=6))
    p2.append(textbox('v08Catatan', 640, 392, 620, 268,
                      'Gap desa-kota menyempit dari 6,16 poin (Mar 2019) ke 4,33 poin (Mar 2026). Namun P1 perdesaan naik di semester terakhir (1,661 ke 1,744) saat kota membaik — penduduk miskin desa yang tersisa makin jauh di bawah garis kemiskinan.', 13, z=7))
    pages['pg02KotaDesa'] = ('Kota vs Desa', p2)

    # ---- Page 3: Provinsi
    p3 = []
    p3.append(textbox('v01Title', 0, 0, 900, 60, 'Provinsi — Jurang 27 Poin Persen di Satu Negara', 20, bold=True, z=0))
    p3.append(slicer('v02SlicerPeriode', 930, 8, 330, 52, D_PER, 'periode', z=1))
    p3.append(visual('v03BarPersenProv', 0, 76, 620, 584, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'Persen Miskin Provinsi'), F_PROV, 'Persen Miskin Provinsi')]}},
                     title_text='Persen Miskin per Provinsi — Mar 2026 (Papua Tengah 30,41%)',
                     filters=[MAR26()],
                     sorts=[sortby(mea(F_PROV, 'Persen Miskin Provinsi'), 'Descending')], z=2))
    p3.append(visual('v04BarJumlahProv', 640, 76, 620, 280, 'clusteredBarChart',
                     qstate={"Category": {"projections": [proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi')]},
                             "Y": {"projections": [proj(mea(F_PROV, 'Jumlah Miskin Provinsi Ribu'), F_PROV, 'Jumlah Miskin Provinsi Ribu')]}},
                     title_text='Jumlah Miskin per Provinsi — Mar 2026 (ribu)',
                     filters=[MAR26()],
                     sorts=[sortby(mea(F_PROV, 'Jumlah Miskin Provinsi Ribu'), 'Descending')], z=3))
    p3.append(visual('v05TableProv', 640, 372, 620, 288, 'tableEx',
                     qstate={"Values": {"projections": [
                         proj(col(D_PROV, 'provinsi'), D_PROV, 'provinsi'),
                         proj(mea(F_PROV, 'Persen Miskin Provinsi'), F_PROV, 'Persen Miskin Provinsi'),
                         proj(mea(F_PROV, 'Jumlah Miskin Provinsi Ribu'), F_PROV, 'Jumlah Miskin Provinsi Ribu'),
                         proj(agg(F_PROV, 'garis_kemiskinan_rp', 1), F_PROV, 'garis_kemiskinan_rp', 'Average of garis_kemiskinan_rp')]}},
                     title_text='Rincian Provinsi — Mar 2026',
                     filters=[MAR26()],
                     sorts=[sortby(mea(F_PROV, 'Persen Miskin Provinsi'), 'Descending')], z=4))
    pages['pg03Provinsi'] = ('Provinsi', p3)

    # ---- Page 4: Ketimpangan & Kedalaman
    p4 = []
    p4.append(textbox('v01Title', 0, 0, 900, 60, 'Ketimpangan & Kedalaman Kemiskinan', 20, bold=True, z=0))
    p4.append(slicer('v02SlicerPeriode', 930, 8, 330, 52, D_PER, 'periode', z=1))
    p4.append(visual('v03LineGini', 0, 76, 620, 280, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_PER, 'periode'), D_PER, 'periode')]},
                             "Y": {"projections": [proj(mea(F_GINI, 'Gini Ratio'), F_GINI, 'Gini Ratio')]},
                             "Series": {"projections": [proj(col(F_GINI, 'daerah'), F_GINI, 'daerah')]}},
                     title_text='Gini Ratio Total / Kota / Desa per Periode', z=2))
    p4.append(visual('v04LineP1P2', 640, 76, 620, 280, 'lineChart',
                     qstate={"Category": {"projections": [proj(col(D_PER, 'periode'), D_PER, 'periode')]},
                             "Y": {"projections": [
                                 proj(agg(F_NAS, 'p1', 1), F_NAS, 'p1', 'Average of p1'),
                                 proj(agg(F_NAS, 'p2', 1), F_NAS, 'p2', 'Average of p2')]}},
                     title_text='Indeks Kedalaman (P1) & Keparahan (P2) — mulai Mar 2020', z=3))
    cards4 = [(F_GINI, 'Gini Mar 2026', 'Gini Mar 2026'),
              (F_NAS, 'P1 Mar 2026', 'P1 Mar 2026'),
              (F_NAS, 'P2 Mar 2026', 'P2 Mar 2026')]
    for i, (ent, m, t) in enumerate(cards4):
        p4.append(visual(f'v{5+i:02d}Card', i * 320, 372, 300, 120, 'card',
                         qstate={"Values": {"projections": [proj(mea(ent, m), ent, m)]}},
                         title_text=t, z=4 + i))
    p4.append(visual('v08CardPangsa', 980, 372, 280, 120, 'card',
                     qstate={"Values": {"projections": [proj(agg(F_GINI, 'pangsa_40_terbawah_persen', 1), F_GINI, 'pangsa_40_terbawah_persen', 'Average of pangsa_40_terbawah_persen')]}},
                     title_text='Pangsa 40% Terbawah Mar 2026 (%)',
                     filters=[MAR26(), catfilter('fg', F_GINI, 'daerah', ['Total'])], z=7))
    p4.append(textbox('v09Catatan', 0, 508, 1260, 70,
                      'Gini naik dari titik terendah Sep 2025 (0,363) ke 0,368 (Mar 2026) saat kemiskinan mencapai rekor terendah — ketimpangan dan kemiskinan dapat bergerak berlawanan arah.', 13, z=8))
    pages['pg04Ketimpangan'] = ('Ketimpangan & Kedalaman', p4)

    order = list(pages)
    for pname, (disp, visuals) in pages.items():
        WJ(DEF_R / 'pages' / pname / 'page.json', {
            "$schema": PG, "name": pname, "displayName": disp,
            "displayOption": "FitToPage", "height": 720, "width": 1280})
        for v in visuals:
            WJ(DEF_R / 'pages' / pname / 'visuals' / v['name'] / 'visual.json', v)
    WJ(DEF_R / 'pages' / 'pages.json', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": order, "activePageName": order[0]})

README = """LANGKAH MEMBUKA PAKET PBIP — Kemiskinan & Ketimpangan Indonesia 2026
====================================================================

1. Ekstrak file ZIP ini ke folder lokal (mis. C:\\PowerBI\\Kemiskinan).
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
"""

# --------------------------------------------------------------------- main
def main():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    (ROOT / 'data').mkdir(parents=True)
    for f in sorted(KIT.glob('*.csv')):
        shutil.copy(f, ROOT / 'data' / f.name)
    WJ(ROOT / f'{PROJ}.pbip', {
        "$schema": "https://developer.microsoft.com/json-schemas/fabric/pbip/pbipProperties/1.0.0/schema.json",
        "version": "1.0",
        "artifacts": [{"report": {"path": f"{PROJ}.Report"}}],
        "settings": {"enableAutoRecovery": True}})
    W(ROOT / '.gitignore', '**/.pbi/localSettings.json\n**/.pbi/cache.abf\n')
    W(ROOT / 'README-LANGKAH.txt', README)
    build_model()
    build_report()
    dst = PROOT / 'pbip' / PROJ
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(ROOT, dst)
    print('built', ROOT, '+ copy at', dst)

if __name__ == '__main__':
    main()
