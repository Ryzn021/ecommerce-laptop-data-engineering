#!/usr/bin/env python
import requests
import pandas as pd
import json
import urllib.parse # Library bawaan untuk mengubah spasi menjadi format URL (%20)

def ambil_data_tokopedia(keyword, jumlah_halaman=1):
    url = "https://gql.tokopedia.com/graphql/SearchProductQueryV4"
    
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Origin": "https://www.tokopedia.com",
        "Referer": f"https://tokopedia.com{urllib.parse.quote(keyword)}"
    }

    # --- PERBAIKAN STRUKTUR PAYLOAD (Mengikuti Aturan API Terbaru) ---
    # Kita menggabungkan semua variabel pencarian menjadi satu baris string query param
    string_param = f"device=desktop&navsource=&ob=23&page={jumlah_halaman}&q={urllib.parse.quote(keyword)}&related=true&rows=60&safe_search=false&scheme=https&source=search&st=product&start=0"

    payload = [{
        "operationName": "SearchProductQueryV4",
        "variables": {
            "params": string_param # Memasukkan string parameter tunggal
        },
        # Query GraphQL disesuaikan untuk menerima parameter tunggal ($params)
        "query": """query SearchProductQueryV4($params: String!) {
          ace_search_product_v4(params: $params) {
            data {
              products {
                id
                name
                price
                imageUrl
                rating
                countReview
                shop {
                  id
                  name
                  city
                }
              }
            }
          }
        }"""
    }]

    print(f"Sedang menarik data laptop dengan kata kunci: '{keyword}'...")
    response = requests.post(url, headers=headers, json=payload)
    
    print(f"Status HTTP Server: {response.status_code}")
    
    if response.status_code == 200:
        try:
            data_json = response.json()
            # API mengembalikan respons dalam format List di layer terluar, ambil indeks [0]
            daftar_produk = data_json[0]['data']['ace_search_product_v4']['data']['products']
            return daftar_produk
        except (json.decoder.JSONDecodeError, KeyError, IndexError) as e:
            print(f"\n⚠️ Gagal membaca struktur data JSON. Detail Eror: {e}")
            return []
    else:
        print(f"Koneksi ditolak oleh sistem keamanan Tokopedia.")
        return []

if __name__ == "__main__":
    print("Menghubungi server Tokopedia...")
    
    # Kata kunci pencarian gabungan Asus atau Lenovo yang sudah Anda perbaiki kemarin
    data_mentah = ambil_data_tokopedia("acer ryzen rtx 5060", jumlah_halaman=1)
    
    if data_mentah:
        # Mengubah data JSON mentah menjadi tabel Pandas DataFrame
        df = pd.DataFrame(data_mentah)
        
        # --- TAMBAHAN BARU: MEMBUAT KOLOM LINK PRODUK SECARA OTOMATIS ---
        # Kita menggabungkan URL dasar Tokopedia dengan kolom 'id' produk
        df['product_link'] = "https://tokopedia.com" + df['id'].astype(str)
        
        # Jalur tempat menyimpan file hasil buruan
        jalur_simpan = "../../data/laptop_mentah.csv"
        
        # Menyimpan tabel ke file .CSV fisik
        df.to_csv(jalur_simpan, index=False)
        print(f"🎉 SUKSES! Berhasil mengamankan {len(df)} data laptop mentah di: {jalur_simpan}")
        print("🔗 Kolom 'product_link' sudah berhasil disertakan di dalam file CSV!")
    else:
        print("\nPipeline Data Mandek: Dataset gagal dibuat.")
