
# Panduan Instalasi dan Penggunaan Script Grow

## Persyaratan
Sebelum menjalankan script, pastikan Anda memiliki:

1. **Python 3.x** terinstal di sistem Anda. 
2. **Pustaka Python** berikut:
   - `aiohttp`
   - `colorama`
3. File `token.txt` yang berisi refresh token.

## Langkah-Langkah Instalasi

### 1. Clone Repositori
Clone repositori ini ke sistem Anda menggunakan Git:
```bash
git clone https://github.com/isorganic/neng-hana.git
```

Masuk ke dalam direktori yang baru saja di-clone:
```bash
cd neng-hana
```

### 2. Cek Instalasi Python
Pastikan Python sudah terinstal di sistem Anda:
```bash
python3 --version
pip --version
```
Jika belum, instal Python terlebih dahulu sesuai dengan sistem operasi Anda.

### 3. Instalasi Pustaka yang Diperlukan
Jalankan perintah berikut untuk menginstal pustaka yang diperlukan:
```bash
pip install aiohttp colorama
```
Jika Anda menggunakan Termux atau membutuhkan izin tambahan, tambahkan `--user`:
```bash
pip install aiohttp colorama --user
```

### 4. Siapkan File `token.txt`
Buat file bernama `token.txt` di folder yang sama dengan script. Isi file ini dengan daftar refresh token Anda, satu token per baris. Contoh:
```
AMf-vBzq8z1YhvQLFFItLwJU...
AMf-vDxq7YhvQLGGItMRoYU...
```

### 5. Jalankan Script
Setelah semua persiapan selesai, jalankan script dengan perintah:
```bash
python3 main.py
```

## Cara Kerja Script
1. Script akan membaca semua refresh token dari file `token.txt`.
2. Script akan melakukan proses `grow` setiap jam pada menit ke-5 (misalnya 12:05, 13:05, dst.).
3. Status akan ditampilkan di terminal:
   - **Hijau**: Menunggu waktu grow berikutnya.
   - **Kuning**: Grow berhasil.
   - **Merah**: Terjadi error.

## Troubleshooting
Jika terjadi error:
1. Pastikan Python dan pustaka telah terinstal dengan benar.
2. Cek apakah `token.txt` berada di folder yang sama dengan script dan berisi token yang valid.
3. Jika ada kendala lain, silakan hubungi pengembang script.

## Catatan Tambahan
kalo ga work, dimohon untuk mandi dulu.
