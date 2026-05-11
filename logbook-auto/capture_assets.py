"""
Jalankan script ini untuk capture screenshot elemen-elemen SIPINTAR.
Pastikan halaman logbook SIPINTAR sudah terbuka di Chrome sebelum menjalankan ini.

Cara pakai:
  python capture_assets.py

Script akan minta kamu klik tiap elemen satu per satu, lalu crop dan simpan ke folder assets/.
"""

import pyautogui
import time
from PIL import ImageGrab

ELEMENTS = [
    ("btn_tambah",   "Klik tombol HIJAU '+ Tambah' di halaman list logbook"),
    ("btn_simpan",   "Buka modal dulu (klik Tambah), lalu klik tombol 'Simpan' di modal"),
    ("btn_choosefile", "Klik tombol 'Choose File' di modal"),
    ("field_nama",   "Klik field 'Nama Kegiatan' di modal"),
    ("field_tanggal","Klik field 'Tanggal Kegiatan' di modal"),
    ("field_waktu",  "Klik field 'Waktu Kegiatan' di modal"),
    ("field_uraian", "Klik di dalam textarea 'Uraian Kegiatan' di modal"),
]

CROP_SIZE = 120  # px radius sekitar titik klik

def capture_element(name, instruction):
    print(f"\n{'='*50}")
    print(f"📸 {name}")
    print(f"   {instruction}")
    print(f"   Kamu punya 5 detik untuk posisikan mouse, lalu JANGAN GERAK.")
    input("   Tekan ENTER saat siap...")

    print("   3...")
    time.sleep(1)
    print("   2...")
    time.sleep(1)
    print("   1...")
    time.sleep(1)

    x, y = pyautogui.position()
    print(f"   📍 Posisi: ({x}, {y})")

    # Crop area sekitar posisi mouse
    left   = max(0, x - CROP_SIZE)
    top    = max(0, y - CROP_SIZE)
    right  = x + CROP_SIZE
    bottom = y + CROP_SIZE

    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    path = f"assets/{name}.png"
    screenshot.save(path)
    print(f"   ✅ Disimpan ke {path}")

if __name__ == "__main__":
    print("🎯 Capture Assets SIPINTAR")
    print("Pastikan halaman logbook SIPINTAR sudah terbuka di Chrome.\n")

    for name, instruction in ELEMENTS:
        capture_element(name, instruction)

    print("\n✅ Semua asset berhasil di-capture!")
    print("Sekarang jalankan: python main.py")
