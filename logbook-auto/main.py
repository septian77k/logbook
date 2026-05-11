"""
Logbook Auto-Upload - SIPINTAR
Menggunakan pyautogui (koordinat dari coords.json)
Web UI: http://localhost:5000
"""

import json
import os
import time
import threading
import pyautogui
import pyperclip
from pathlib import Path
from flask import Flask, render_template, request, jsonify

# ── Config ────────────────────────────────────────────────────────────────────
DATA_FILE             = "data.json"
COORDS_FILE           = "coords.json"
DELAY_BETWEEN_ACTIONS = 1.5
DELAY_AFTER_SAVE      = 3.0
COUNTDOWN_SECONDS     = 10

pyautogui.FAILSAFE = True
pyautogui.PAUSE    = 0.2

# ── State ─────────────────────────────────────────────────────────────────────
app        = Flask(__name__)
stop_flag  = threading.Event()
status_log = []
is_running = False


def log(msg: str):
    print(msg)
    status_log.append(msg)
    if len(status_log) > 300:
        status_log.pop(0)


def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def load_coords():
    if not os.path.exists(COORDS_FILE):
        raise Exception("coords.json tidak ditemukan. Jalankan dulu: python capture_coords.py")
    with open(COORDS_FILE, "r") as f:
        return json.load(f)


# ── pyautogui helpers ─────────────────────────────────────────────────────────
def click_at(coords, name):
    x, y = coords[name]["x"], coords[name]["y"]
    pyautogui.click(x, y)
    time.sleep(0.3)


def clear_and_type(text: str):
    """Isi field via clipboard — aman untuk teks panjang dan karakter unicode."""
    pyperclip.copy(str(text))
    pyautogui.hotkey("ctrl", "a")
    time.sleep(0.1)
    pyautogui.hotkey("ctrl", "v")


# ── Automation core ───────────────────────────────────────────────────────────
def run_automation(start_date: str):
    global is_running
    is_running = True
    stop_flag.clear()
    status_log.clear()

    try:
        coords = load_coords()
    except Exception as e:
        log(f"❌ {e}")
        is_running = False
        return

    data = load_data()
    filtered = [e for e in data if e["tanggal"] >= start_date]
    if not filtered:
        log(f"❌ Tidak ada entry mulai tanggal {start_date}.")
        is_running = False
        return

    log(f"📋 Memproses {len(filtered)} entry mulai {start_date}")
    log(f"⚠️  Jangan sentuh mouse/keyboard selama otomasi!")
    log(f"⚠️  Darurat: geser mouse ke pojok kiri atas layar.\n")

    # Countdown — beri waktu user klik ke Chrome
    for i in range(COUNTDOWN_SECONDS, 0, -1):
        if stop_flag.is_set():
            log("⏹️  Dihentikan.")
            is_running = False
            return
        log(f"⏳ Mulai dalam {i} detik... (klik ke window Chrome sekarang!)")
        time.sleep(1)

    log("🚀 Mulai!\n")

    for i, entry in enumerate(filtered):
        if stop_flag.is_set():
            log("⏹️  Dihentikan oleh pengguna.")
            break

        tanggal = entry["tanggal"]
        nama    = entry["nama_kegiatan"]
        menit   = entry["waktu_menit"]
        uraian  = entry["uraian"]
        foto    = entry["foto"]

        log(f"[{i+1}/{len(filtered)}] {tanggal} — {nama}")

        try:
            # Klik tombol + Tambah
            log("  → Klik Tambah...")
            click_at(coords, "btn_tambah")
            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Nama Kegiatan
            log("  → Nama Kegiatan...")
            click_at(coords, "field_nama")
            clear_and_type(nama)
            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Tanggal — format MM/DD/YYYY untuk Windows date input
            log("  → Tanggal...")
            click_at(coords, "field_tanggal")
            y, m, d = tanggal.split("-")
            pyautogui.hotkey("ctrl", "a")
            pyautogui.typewrite(f"{m}{d}{y}", interval=0.05)
            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Waktu
            log("  → Waktu...")
            click_at(coords, "field_waktu")
            clear_and_type(menit)
            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Uraian
            log("  → Uraian...")
            click_at(coords, "field_uraian")
            clear_and_type(uraian)
            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Upload foto
            abs_foto = str(Path(foto).resolve())
            if os.path.exists(abs_foto):
                log("  → Upload foto...")
                click_at(coords, "btn_choosefile")
                time.sleep(2)  # tunggu dialog file explorer
                pyperclip.copy(abs_foto)
                pyautogui.hotkey("ctrl", "a")
                pyautogui.hotkey("ctrl", "v")
                time.sleep(0.5)
                pyautogui.press("enter")
                time.sleep(1.5)
            else:
                log(f"  ⚠️  Foto tidak ditemukan — dilewati")

            time.sleep(DELAY_BETWEEN_ACTIONS)

            # Simpan
            log("  → Simpan...")
            click_at(coords, "btn_simpan")
            log(f"  ✅ Berhasil!\n")
            time.sleep(DELAY_AFTER_SAVE)

        except pyautogui.FailSafeException:
            log("🛑 FAILSAFE aktif — otomasi dihentikan.")
            break
        except Exception as e:
            log(f"  ❌ Error: {e}")
            log("  ⏸️  Script berhenti.\n")
            break
    else:
        log("🎉 Semua entry selesai diupload!")

    is_running = False


# ── Flask routes ──────────────────────────────────────────────────────────────
@app.route("/")
def index():
    data = load_data()
    dates = [e["tanggal"] for e in data]
    coords_ready = os.path.exists(COORDS_FILE)
    coords = {}
    if coords_ready:
        with open(COORDS_FILE) as f:
            coords = json.load(f)
    return render_template("index.html", dates=dates, coords_ready=coords_ready, coords=coords)


@app.route("/mouse-pos")
def mouse_pos():
    x, y = pyautogui.position()
    return jsonify({"x": x, "y": y})


@app.route("/save-coords", methods=["POST"])
def save_coords():
    data = request.json
    with open(COORDS_FILE, "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"ok": True})


@app.route("/start", methods=["POST"])
def start():
    global is_running
    if is_running:
        return jsonify({"ok": False, "msg": "Otomasi sedang berjalan."})
    start_date = request.json.get("start_date")
    if not start_date:
        return jsonify({"ok": False, "msg": "Pilih tanggal mulai."})
    t = threading.Thread(target=run_automation, args=(start_date,), daemon=True)
    t.start()
    return jsonify({"ok": True, "msg": f"Otomasi dimulai. Klik ke window Chrome dalam {COUNTDOWN_SECONDS} detik!"})


@app.route("/stop", methods=["POST"])
def stop():
    stop_flag.set()
    return jsonify({"ok": True, "msg": "Sinyal stop dikirim."})


@app.route("/status")
def status():
    return jsonify({"running": is_running, "log": list(status_log)})


if __name__ == "__main__":
    print("🌐 Buka browser ke http://localhost:5000")
    app.run(debug=False, port=5000)
