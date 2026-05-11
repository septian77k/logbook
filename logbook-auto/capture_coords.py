"""
Jalankan sekali untuk rekam koordinat elemen SIPINTAR.
Pastikan modal 'Tambah Log Book' sudah terbuka di Chrome.

Cara pakai:
  python capture_coords.py
"""

import json
import time
import pyautogui

ELEMENTS = [
    ("btn_tambah",    "Arahkan mouse ke tombol HIJAU '+ Tambah' (halaman list, TUTUP modal dulu)"),
    ("field_nama",    "Buka modal, arahkan ke field 'Nama Kegiatan'"),
    ("field_tanggal", "Arahkan ke field 'Tanggal Kegiatan'"),
    ("field_waktu",   "Arahkan ke field 'Waktu Kegiatan (Satuan Menit)'"),
    ("field_uraian",  "Arahkan ke textarea 'Uraian Kegiatan'"),
    ("btn_choosefile","Arahkan ke tombol 'Choose File'"),
    ("btn_simpan",    "Arahkan ke tombol 'Simpan'"),
]

coords = {}

print("🎯 Capture Koordinat SIPINTAR")
print("Buka Chrome ke halaman logbook SIPINTAR sekarang.\n")

for name, instruction in ELEMENTS:
    print(f"{'─'*50}")
    print(f"📍 {name}")
    print(f"   {instruction}")
    input("   Tekan ENTER, lalu arahkan mouse ke elemen dalam 4 detik...")

    for i in range(4, 0, -1):
        print(f"   {i}...", end="\r")
        time.sleep(1)

    x, y = pyautogui.position()
    coords[name] = {"x": x, "y": y}
    print(f"   ✅ Tersimpan: ({x}, {y})          ")

with open("coords.json", "w") as f:
    json.dump(coords, f, indent=2)

print("\n✅ Koordinat disimpan ke coords.json")
print("Sekarang jalankan: python main.py")
