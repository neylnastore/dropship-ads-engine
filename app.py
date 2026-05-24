import streamlit as st
import random

# Konfigurasi Halaman (Lebar)
st.set_page_config(page_title="Dropship Ads Engine", layout="wide")

# Judul Website
st.title("✨ Dropship Ads Engine")
st.markdown("Automasi Riset Produk, Markup Harga & Copywriting Landing Page")

# Fungsi Simulasi (Sama seperti sebelumnya)
def tarik_data_shopee(keyword):
    return {
        "nama_produk": f"{keyword} Premium",
        "harga_modal": 85000,
        "rating": 4.9,
        "terjual": 1500,
        "fitur_utama": ["Tahan air IP68", "Desain minimalis modern", "Material awet"]
    }

# Membagi layar jadi 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🛒 1. Product Discovery")
    keyword = st.text_input("Masukkan Kata Kunci Produk:", "Smartwatch Pria")
    cari_btn = st.button("Cari Produk")

with col2:
    st.subheader("💰 2. Pricing & Margin")
    margin_min = st.number_input("Margin Minimal (Rp)", value=120000)
    margin_max = st.number_input("Margin Maksimal (Rp)", value=150000)

if cari_btn:
    data = tarik_data_shopee(keyword)
    margin = random.randint(margin_min, margin_max)
    harga_jual = data['harga_modal'] + margin
    harga_coret = harga_jual + 75000
    
    with col1:
        st.success(f"Produk Ditemukan: {data['nama_produk']}")
        st.write(f"Harga Supplier: **Rp{data['harga_modal']:,}**")
        
    with col2:
        st.info("Kalkulasi Harga Jual")
        st.metric(label="Harga Final Landing Page", value=f"Rp{harga_jual:,}", delta=f"Profit: Rp{margin:,}")
        
    with col3:
        st.subheader("📝 3. Auto-Copywriting")
        fitur_bullet = "\n".join([f"✅ {fitur}" for fitur in data['fitur_utama']])
        
        lp_script = f"""
        **Headline:** Capek Beli Barang Mahal Tapi Cepat Rusak?
        Kenalkan, {data['nama_produk']} - Solusi Tampil Elegan!
        
        **Social Proof:** Terjual {data['terjual']}+ pcs (Rating {data['rating']}⭐)
        
        **Benefit:**
        {fitur_bullet}
        
        **Penawaran:**
        Harga Normal: ~Rp{harga_coret:,}~
        Promo Hari Ini: **HANYA Rp{harga_jual:,}!**
        """
        st.text_area("Script Landing Page & Meta Ads:", value=lp_script, height=300)
