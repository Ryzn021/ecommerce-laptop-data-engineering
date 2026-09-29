#!/usr/bin/env python
import pandas as pd
import re # Library Python resmi untuk menggunakan Regular Expression (Regex)

def bersihkan_data_laptop():
    # Jalur file input (data mentah hasil scraping kemarin)
    file_mentah = "../../data/laptop_mentah.csv"
    file_bersih = "../../data/laptop_bersih.csv"
    
    try:
        # Membaca file CSV mentah ke dalam tabel Pandas DataFrame
        df = pd.read_csv(file_mentah)
        print(f"Membaca {len(df)} data laptop mentah...")
    except FileNotFoundError:
        print("Eror: File data mentah tidak ditemukan! Jalankan scraper terlebih dahulu.")
        return

    # --- 1. FILTERING DATA SAMPAH ---
    # Buat daftar kata kunci hitam. Jika judul mengandung kata ini, buang produk tersebut.
    # Ini untuk membuang aksesoris seperti tas, mouse, charger, atau antigores yang menyelinap.
    kata_kunci_sampah = ['tas', 'mouse', 'charger', 'antigores', 'screen', 'keyboard', 'adapter', 'sleeve', 'casing', 'baut']
    pola_sampah = '|'.join(kata_kunci_sampah) # Menggabungkan kata dengan simbol OR (tas|mouse|charger)
    
    # Memfilter data: Hanya ambil produk yang judulnya TIDAK mengandung kata kunci sampah
    df = df[~df['name'].str.contains(pola_sampah, case=False, na=False)]
    print(f"Setelah membuang aksesoris/sampah, tersisa: {len(df)} produk laptop asli.")

    # --- 2. DATA EXTRACTION DENGAN REGEX (Fungsi Inti) ---
    
    # Fungsi pembantu untuk mendeteksi RAM (Mencari angka yang diikuti huruf GB/gb/Gb)
    def ekstrak_ram(judul):
        # Pola Regex: (\d+)\s*(?:GB|gb|Gb|Gb) -> Cari angka (\d+), abaikan spasi, cari teks GB
        pola_ram = r'(\d+)\s*(?:GB|gb|Gb)'
        hasil = re.search(pola_ram, judul)
        if hasil:
            return int(hasil.group(1)) # Ambil angkanya saja (misal: 8 atau 16)
        return None # Jika tidak tertulis di judul, beri nilai kosong dulu

    # Fungsi pembantu untuk mendeteksi Tipe Storage (SSD atau HDD)
    def ekstrak_storage_type(judul):
        if re.search(r'ssd|SSD', judul):
            return 'SSD'
        elif re.search(r'hdd|HDD', judul):
            return 'HDD'
        return 'Unknown'

    # Fungsi pembantu untuk mendeteksi Kapasitas Storage (Mencari angka 128, 256, 512, atau 1)
    def ekstrak_storage_capacity(judul):
        # Pola mencari angka kapasitas populer dalam GB atau TB
        pola_storage = r'(128|256|512|1|2)\s*(?:GB|TB|gb|tb)'
        hasil = re.search(pola_storage, judul)
        if hasil:
            angka = hasil.group(1)
            # Jika angkanya 1 atau 2, kemungkinan besar itu satuan Terabyte (TB), ubah ke GB (1000)
            if angka in ['1', '2'] and ('tb' in judul.lower() or 'tb' in judul.lower()):
                return int(angka) * 1000
            return int(angka)
        return None

    # Menerapkan rumus-rumus Regex di atas ke seluruh baris tabel secara otomatis lewat Pandas
    df['RAM_GB'] = df['name'].apply(ekstrak_ram)
    df['Storage_Type'] = df['name'].apply(ekstrak_storage_type)
    df['Storage_Capacity_GB'] = df['name'].apply(ekstrak_storage_capacity)

    # --- 3. CLEANING KOLOM HARGA ---
    # Harga dari Tokopedia terkadang bertipe teks karena ada karakter Rp atau titik.
    # Kita bersihkan agar murni menjadi angka (integer) agar bisa dihitung secara matematis.
    if df['price'].dtype == 'O': # Jika tipe datanya Object/Teks
        df['price'] = df['price'].str.replace('Rp', '').str.replace('.', '').str.strip().astype(int)

    # Menyimpan hasil data tabel yang sudah terstruktur rapi ke file baru
    df.to_csv(file_bersih, index=False)
    print(f"🎉 SUKSES! Data bersih berhasil diekstrak dan disimpan di: {file_bersih}")
    
    # Menampilkan 5 sampel data teratas di terminal untuk pembuktian hasil kerja
    print("\n--- Sampel Data Hasil Olahan Regex & Pandas ---")
    print(df[['name', 'price', 'RAM_GB', 'Storage_Type', 'Storage_Capacity_GB']].head())

if __name__ == "__main__":
    bersihkan_data_laptop()