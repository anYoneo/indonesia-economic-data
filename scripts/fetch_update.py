#!/usr/bin/env python3
"""Perbarui dua CSV di data/ langsung dari sumber publiknya.

Hanya butuh `requests`. Sumbernya identik dengan yang dipakai layanan berbayar,
jadi angka di sini selalu bisa Anda segarkan sendiri kapan pun.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import requests

OUT = Path(__file__).resolve().parent.parent / "data"

# 13 indikator Indonesia yang ada di ekspor gratis ini.
INDIKATOR = {
    "FP.CPI.TOTL": "Indeks harga konsumen (CPI, 2010=100)",
    "FP.CPI.TOTL.ZG": "Inflasi harga konsumen (%)",
    "AG.PRD.FOOD.XD": "Indeks produksi pangan (2014-2016=100)",
    "NV.AGR.TOTL.ZS": "Nilai tambah pertanian (% dari PDB)",
    "NY.GDP.MKTP.CD": "PDB (harga berlaku, USD)",
    "NY.GDP.PCAP.CD": "PDB per kapita (USD)",
    "PA.NUS.FCRF": "Kurs resmi (IDR per USD)",
    "SL.UEM.TOTL.ZS": "Tingkat pengangguran (%)",
    "AG.CON.FERT.ZS": "Konsumsi pupuk (kg per hektar lahan garapan)",
    "SP.DYN.LE00.IN": "Angka harapan hidup (tahun)",
    "IT.NET.USER.ZS": "Pengguna internet (% populasi)",
    "BX.KLT.DINV.CD.WD": "Arus masuk investasi asing langsung (USD)",
    "SP.POP.TOTL": "Jumlah penduduk",
}

WB = "https://api.worldbank.org/v2/country/IDN/indicator/{kode}?format=json&per_page=20000"


def angka_ke_csv() -> int:
    baris = []
    for kode, nama in INDIKATOR.items():
        r = requests.get(WB.format(kode=kode), timeout=60)
        r.raise_for_status()
        payload = r.json()
        if len(payload) < 2 or not payload[1]:
            print(f"  lewati {kode}: sumber tidak mengembalikan data", file=sys.stderr)
            continue
        for d in payload[1]:
            if d.get("value") is None:
                continue
            baris.append({
                "series_id": f"wb:idn:{kode}",
                "nama": f"{nama} — Indonesia",
                "satuan": "",
                "periode": d["date"],
                "nilai": d["value"],
                "sumber": "worldbank",
                "lisensi": "World Bank Open Data — CC BY 4.0",
            })
        print(f"  {kode:18} {len(payload[1])} periode")
    baris.sort(key=lambda b: (b["series_id"], b["periode"]))
    p = OUT / "indonesia_annual.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["series_id", "nama", "satuan", "periode",
                                          "nilai", "sumber", "lisensi"])
        w.writeheader()
        w.writerows(baris)
    print(f"-> {p.name}: {len(baris)} baris")
    return len(baris)


def kurs_ke_csv(tahun: int = 5) -> int:
    mulai = f"{__import__('datetime').date.today().year - tahun}-01-01"
    r = requests.get(
        "https://api.frankfurter.app/" + mulai + "..",
        params={"from": "USD", "to": "IDR"},
        timeout=60,
    )
    r.raise_for_status()
    rates = r.json().get("rates", {})
    p = OUT / "usd_idr_daily.csv"
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["series_id", "nama", "satuan", "periode",
                                          "nilai", "sumber", "lisensi"])
        w.writeheader()
        for tgl in sorted(rates):
            w.writerow({
                "series_id": "fx:USDIDR",
                "nama": "Kurs USD/IDR",
                "satuan": "IDR",
                "periode": tgl,
                "nilai": rates[tgl]["IDR"],
                "sumber": "fx",
                "lisensi": "ECB reference rates (via frankfurter.app)",
            })
    print(f"-> {p.name}: {len(rates)} hari")
    return len(rates)


if __name__ == "__main__":
    print("Mengambil data World Bank...")
    angka_ke_csv()
    print("Mengambil kurs ECB...")
    kurs_ke_csv()
    print("Selesai.")
