from flask import Flask, request, jsonify, render_template
import random
import requests
import os

app = Flask(__name__)

# ==============================================================================
# [ KONFIGURASI APIFY - KUNCI AKSES INTELIJEN ]
# Masukkan API Token dari akun Apify kamu di sini untuk mengaktifkan "Live Mode"
# ==============================================================================
APIFY_TOKEN = "MASUKKAN_TOKEN_APIFY_KAMU_DISINI"

# Nama Actor (Alat Scraper) di Apify. Pastikan kamu sudah menambahkan actor ini di akunmu.
ACTOR_SHOPEE = "dtruss/shopee-scraper" # Contoh ID Actor Shopee di Apify

@app.route('/')
def home():
    # Menampilkan tampilan depan radar (index.html)
    return render_template('index.html')

@app.route('/api/proses-data', methods=['POST'])
def proses_data():
    data_masuk = request.json
    keyword = data_masuk.get('keyword', 'Produk')
    
    data_supplier = {}
    
    # ==========================================================================
    # 1. ENGINE PENARIK DATA (META ADS & SHOPEE JABODETABEK)
    # ==========================================================================
    try:
        # Cek apakah pengguna sudah memasukkan token Apify asli
        if APIFY_TOKEN != "MASUKKAN_TOKEN_APIFY_KAMU_DISINI":
            print(f">>> [SISTEM] Menembus database Shopee untuk target: {keyword}...")
            
            # Request ke API Apify khusus Shopee Scraper
            api_url_shopee = f"https://api.apify.com/v2/acts/{ACTOR_SHOPEE}/run-sync-get-dataset-items?token={APIFY_TOKEN}"
            
            # Parameter Tempur: Cari keyword, wajib JABODETABEK, ambil 1 termurah/terlaris
            payload = {
                "search": keyword,
                "location": "Jabodetabek", 
                "maxItems": 1
            }
            
            # Eksekusi pencarian (Timeout 20 detik agar tidak gantung)
            response = requests.post(api_url_shopee, json=payload, timeout=20)
            
            if response.status_code == 200 or response.status_code == 201:
                hasil_scrape = response.json()
                if len(hasil_scrape) > 0:
                    raw_data = hasil_scrape[0]
                    # Ekstrak data asli dari Shopee
                    data_supplier = {
                        "nama_produk": raw_data.get('title', f"{keyword} Premium"),
                        "harga_modal": int(raw_data.get('price', 50000)),
                        "lokasi": raw_data.get('location', 'JABODETABEK'),
                        "terjual": int(raw_data.get('sold_count', 100)),
                        "rating": float(raw_data.get('rating', 4.8)),
                        "fitur": ["Sesuai deskripsi original Shopee", "Pengiriman cepat area Jabodetabek"]
                    }
                else:
                    raise Exception("Target tidak ditemukan di area Jabodetabek.")
            else:
                raise Exception(f"Akses Apify ditolak. Kode Error: {response.status_code}")
        else:
            raise Exception("Token Apify belum diisi. Mengalihkan ke mode simulasi lokal...")
            
    except Exception as e:
        # ======================================================================
        # FALLBACK MODE (Jika API mati, limit habis, atau Token kosong)
        # ======================================================================
        print(f">>> [PERINGATAN] {e}")
        data_supplier = {
            "nama_produk": f"{keyword} - Tactical Edition",
            "harga_modal": random.randint(45000, 85000),
            "lokasi": "JABODETABEK",
            "terjual": random.randint(150, 999),
            "rating": 4.9,
            "fitur": ["Material tangguh standar militer", "Desain maskulin & ergonomis", "Siap tempur di segala medan"]
        }

    # ==========================================================================
    # 2. ENGINE MARKUP HARGA (120RB - 150RB)
    # ==========================================================================
    # Mengambil margin acak antara 120.000 sampai 150.000
    margin_cuan = random.randint(120, 150) * 1000
    
    # Kalkulasi harga jual final
    harga_jual = data_supplier['harga_modal'] + margin_cuan
    
    # Buat harga coret buatan (markup ekstra 50rb - 80rb untuk efek diskon)
    harga_coret = harga_jual + random.randint(50000, 80000)
    
    # ==========================================================================
    # 3. ENGINE GENERATOR COPYWRITING (TACTICAL MODE)
    # ==========================================================================
    fitur_bullet = "\n".join([f"🔥 {f}" for f in data_supplier['fitur']])
    lp_script = f"""[ TARGET TERKUNCI: SOLUSI UNTUKMU ]
Tingkatkan Performa dan Tampil Lebih Garang dengan {data_supplier['nama_produk']}!

[ STATUS INTELIJEN ]
Barang teruji! Telah digunakan oleh {data_supplier['terjual']}+ pria dengan rating {data_supplier['rating']}⭐!

[ SPESIFIKASI TEMPUR ]
{fitur_bullet}

[ KODE PROMO ]
MSRP: ~Rp{harga_coret:,}~
Harga Khusus Hari Ini: HANYA Rp{harga_jual:,}!

>>> AMANKAN STOK SEKARANG - KLIK BELI (BISA COD) <<<
"""

    # ==========================================================================
    # 4. KIRIM DATA KE RADAR FRONTEND
    # ==========================================================================
    return jsonify({
        "status": "success",
        "supplier": data_supplier,
        "margin_bersih": margin_cuan,
        "harga_jual": harga_jual,
        "harga_coret": harga_coret,
        "copywriting": lp_script
    })

# Mode eksekusi server (Gunicorn akan membaca variabel 'app' ini di Render)
if __name__ == '__main__':
    # Berjalan di port 5000 untuk pengujian lokal di laptop
    app.run(debug=True, host='0.0.0.0', port=5000)
>>> AMANKAN STOK SEKARANG - KLIK BELI (BISA COD) <<<
"""

    # ==========================================================================
    # 4. KIRIM DATA KE RADAR FRONTEND
    # ==========================================================================
    return jsonify({
        "status": "success",
        "supplier": data_supplier,
        "margin_bersih": margin_cuan,
        "harga_jual": harga_jual,
        "harga_coret": harga_coret,
        "copywriting": lp_script
    })

# Mode eksekusi server (Gunicorn akan membaca variabel 'app' ini di Render)
if __name__ == '__main__':
    # Berjalan di port 5000 untuk pengujian lokal di laptop
    app.run(debug=True, host='0.0.0.0', port=5000)from flask import Flask, request, jsonify, render_template
import random
import requests
import os

app = Flask(__name__)

# ==============================================================================
# [ KONFIGURASI APIFY - KUNCI AKSES INTELIJEN ]
# Masukkan API Token dari akun Apify kamu di sini untuk mengaktifkan "Live Mode"
# ==============================================================================
APIFY_TOKEN = "MASUKKAN_TOKEN_APIFY_KAMU_DISINI"

# Nama Actor (Alat Scraper) di Apify. Pastikan kamu sudah menambahkan actor ini di akunmu.
ACTOR_SHOPEE = "dtruss/shopee-scraper" # Contoh ID Actor Shopee di Apify

@app.route('/')
def home():
    # Menampilkan tampilan depan radar (index.html)
    return render_template('index.html')

@app.route('/api/proses-data', methods=['POST'])
def proses_data():
    data_masuk = request.json
    keyword = data_masuk.get('keyword', 'Produk')
    
    data_supplier = {}
    
    # ==========================================================================
    # 1. ENGINE PENARIK DATA (META ADS & SHOPEE JABODETABEK)
    # ==========================================================================
    try:
        # Cek apakah pengguna sudah memasukkan token Apify asli
        if APIFY_TOKEN != "MASUKKAN_TOKEN_APIFY_KAMU_DISINI":
            print(f">>> [SISTEM] Menembus database Shopee untuk target: {keyword}...")
            
            # Request ke API Apify khusus Shopee Scraper
            api_url_shopee = f"https://api.apify.com/v2/acts/{ACTOR_SHOPEE}/run-sync-get-dataset-items?token={APIFY_TOKEN}"
            
            # Parameter Tempur: Cari keyword, wajib JABODETABEK, ambil 1 termurah/terlaris
            payload = {
                "search": keyword,
                "location": "Jabodetabek", 
                "maxItems": 1
            }
            
            # Eksekusi pencarian (Timeout 20 detik agar tidak gantung)
            response = requests.post(api_url_shopee, json=payload, timeout=20)
            
            if response.status_code == 200 or response.status_code == 201:
                hasil_scrape = response.json()
                if len(hasil_scrape) > 0:
                    raw_data = hasil_scrape[0]
                    # Ekstrak data asli dari Shopee
                    data_supplier = {
                        "nama_produk": raw_data.get('title', f"{keyword} Premium"),
                        "harga_modal": int(raw_data.get('price', 50000)),
                        "lokasi": raw_data.get('location', 'JABODETABEK'),
                        "terjual": int(raw_data.get('sold_count', 100)),
                        "rating": float(raw_data.get('rating', 4.8)),
                        "fitur": ["Sesuai deskripsi original Shopee", "Pengiriman cepat area Jabodetabek"]
                    }
                else:
                    raise Exception("Target tidak ditemukan di area Jabodetabek.")
            else:
                raise Exception(f"Akses Apify ditolak. Kode Error: {response.status_code}")
        else:
            raise Exception("Token Apify belum diisi. Mengalihkan ke mode simulasi lokal...")
            
    except Exception as e:
        # ======================================================================
        # FALLBACK MODE (Jika API mati, limit habis, atau Token kosong)
        # ======================================================================
        print(f">>> [PERINGATAN] {e}")
        data_supplier = {
            "nama_produk": f"{keyword} - Tactical Edition",
            "harga_modal": random.randint(45000, 85000),
            "lokasi": "JABODETABEK",
            "terjual": random.randint(150, 999),
            "rating": 4.9,
            "fitur": ["Material tangguh standar militer", "Desain maskulin & ergonomis", "Siap tempur di segala medan"]
        }

    # ==========================================================================
    # 2. ENGINE MARKUP HARGA (120RB - 150RB)
    # ==========================================================================
    # Mengambil margin acak antara 120.000 sampai 150.000
    margin_cuan = random.randint(120, 150) * 1000
    
    # Kalkulasi harga jual final
    harga_jual = data_supplier['harga_modal'] + margin_cuan
    
    # Buat harga coret buatan (markup ekstra 50rb - 80rb untuk efek diskon)
    harga_coret = harga_jual + random.randint(50000, 80000)
    
    # ==========================================================================
    # 3. ENGINE GENERATOR COPYWRITING (TACTICAL MODE)
    # ==========================================================================
    fitur_bullet = "\n".join([f"🔥 {f}" for f in data_supplier['fitur']])
    lp_script = f"""[ TARGET TERKUNCI: SOLUSI UNTUKMU ]
Tingkatkan Performa dan Tampil Lebih Garang dengan {data_supplier['nama_produk']}!

[ STATUS INTELIJEN ]
Barang teruji! Telah digunakan oleh {data_supplier['terjual']}+ pria dengan rating {data_supplier['rating']}⭐!

[ SPESIFIKASI TEMPUR ]
{fitur_bullet}

[ KODE PROMO ]
MSRP: ~Rp{harga_coret:,}~
Harga Khusus Hari Ini: HANYA Rp{harga_jual:,}!

>>> AMANKAN STOK SEKARANG - KLIK BELI (BISA COD) <<<
"""

    # ==========================================================================
    # 4. KIRIM DATA KE RADAR FRONTEND
    # ==========================================================================
    return jsonify({
        "status": "success",
        "supplier": data_supplier,
        "margin_bersih": margin_cuan,
        "harga_jual": harga_jual,
        "harga_coret": harga_coret,
        "copywriting": lp_script
    })

# Mode eksekusi server (Gunicorn akan membaca variabel 'app' ini di Render)
if __name__ == '__main__':
    # Berjalan di port 5000 untuk pengujian lokal di laptop
    app.run(debug=True, host='0.0.0.0', port=5000)
