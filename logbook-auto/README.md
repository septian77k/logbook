# Logbook Auto-Upload

## Setup (sekali aja)

```bash
cd logbook-auto
pip install playwright
playwright install chromium
```

## Cara Pakai

### 1. Siapkan data
Edit `data.json` sesuai logbook kamu. Taruh foto-foto di folder `photos/`.

### 2. Buka Chrome dengan remote debugging
```bash
python main.py --launch-browser
```
Chrome akan terbuka. Navigasi manual ke halaman input logbook sampai siap isi form.

### 3. Jalankan script
```bash
python main.py
```

Script akan otomatis isi tanggal, upload foto, isi keterangan, klik save, lalu klik tombol Tambah untuk entry berikutnya.

## Troubleshooting

Kalau script error karena selector tidak ketemu, buka `main.py` dan sesuaikan selector di fungsi:
- `pick_date()` — untuk field tanggal
- `attach_photo()` — untuk input file foto  
- `fill_keterangan()` — untuk field keterangan
- `click_save()` — untuk tombol save
- `click_tambah()` — untuk tombol tambah di halaman list

Cara cari selector yang tepat: klik kanan elemen di browser → Inspect → lihat atribut `id`, `name`, `class`, atau teks tombolnya.
