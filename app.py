import streamlit as st

# ─── Konfigurasi halaman ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistem Pakar Rekomendasi Kacamata",
    layout="centered",
)

# ─── CSS Kustom ───────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Warna dasar halaman ── */
[data-testid="stAppViewContainer"] { background-color: #0d1117; color: #e6edf3; }
[data-testid="stHeader"]           { background: transparent; }
[data-testid="block-container"]    { padding-top: 2rem; padding-bottom: 2rem; max-width: 1100px; }

/* ── Judul ── */
.main-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

/* ── Banner info ── */
.info-banner {
    background-color: #161b22;
    border: 1px solid #1f6feb;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #58a6ff;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

/* ── Divider ── */
.divider { border: none; border-top: 1px solid #30363d; margin: 1rem 0; }

/* ── CARD: styling pada container Streamlit native ──
   Streamlit merender st.container() sebagai div[data-testid="stVerticalBlock"].
   Kita pakai trick: beri tiap kartu sebuah class unik via markdown kosong,
   lalu target container induknya dengan CSS sibling/parent selector.
   Cara paling andal: gunakan st.container(border=True) yang tersedia
   sejak Streamlit 1.30, lalu override warnanya. */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 12px !important;
    padding: 0.2rem 0.5rem !important;
}

/* ── Judul kartu ── */
.card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
}

/* ── Label pertanyaan ── */
.qlabel {
    font-weight: 700;
    color: #e6edf3;
    font-size: 0.97rem;
    margin-bottom: 0.2rem;
}

/* ── Radio button ── */
div[data-testid="stRadio"] label        { color: #ffffff !important; font-size: 0.94rem; }
div[data-testid="stRadio"] > div        { gap: 0.3rem; }

/* Lingkaran radio yang belum dipilih */
div[data-testid="stRadio"] input[type="radio"] { accent-color: #1f6feb; }

/* ── Tombol Analisis ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(90deg, #1f6feb, #388bfd);
    color: #ffffff;
    font-size: 1.05rem;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2rem;
    width: 100%;
    cursor: pointer;
    transition: opacity 0.2s;
    letter-spacing: 0.03em;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85; }

/* ── Kotak hasil ── */
.result-box {
    background-color: #0d2137;
    border: 1px solid #1f6feb;
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-top: 1rem;
}
.result-title  { font-size: 1.2rem; font-weight: 800; color: #58a6ff; margin-bottom: 0.4rem; }
.face-shape    { font-size: 1.6rem; font-weight: 800; color: #ffffff;  margin-bottom: 0.6rem; }
.rec-label     { font-size: 0.85rem; color: #8b949e; font-weight: 600;
                 text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.4rem; }
.rec-item {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    margin-bottom: 0.4rem;
    color: #e6edf3;
    font-size: 0.93rem;
}
</style>
""",
    unsafe_allow_html=True,
)


# ─── Logika sistem pakar ──────────────────────────────────────────────────────
def analisis_wajah(
    bagian_lebar, bentuk_dagu, bentuk_rahang, panjang_wajah, menyempit_dagu
):
    # Aturan inferensi
    if (
        bagian_lebar == "Pipi"
        and bentuk_dagu == "Membulat"
        and bentuk_rahang == "Membulat"
    ):
        bentuk = "Bulat"
    elif bagian_lebar == "Dahi" and menyempit_dagu == "Ya" and bentuk_dagu == "Runcing":
        bentuk = "Hati / Heart"
    elif (
        bagian_lebar == "Rahang"
        and bentuk_rahang == "Tegas"
        and panjang_wajah == "Panjang dan lebar hampir sama"
    ):
        bentuk = "Persegi / Square"
    elif (
        bagian_lebar == "Dahi"
        and bentuk_rahang == "Tegas"
        and panjang_wajah == "Lebih panjang dari lebar wajah"
    ):
        bentuk = "Berlian / Diamond"
    elif (
        panjang_wajah == "Lebih panjang dari lebar wajah" and menyempit_dagu == "Tidak"
    ):
        bentuk = "Oval"
    elif bagian_lebar == "Pipi" and bentuk_rahang == "Tegas":
        bentuk = "Segitiga / Triangle"
    elif bentuk_rahang == "Tegas" and panjang_wajah == "Lebih panjang dari lebar wajah":
        bentuk = "Persegi Panjang / Oblong"
    else:
        bentuk = "Oval"

    rekomendasi = {
        "Oval": {
            "emoji": "😊",
            "desc": "Wajah oval sangat fleksibel — hampir semua model kacamata cocok.",
            "model": ["Wayfarer", "Aviator", "Round / Bulat", "Cat-Eye", "Geometric"],
        },
        "Bulat": {
            "emoji": "🔵",
            "desc": "Wajah bulat cocok dengan frame yang memberikan kesan memanjang.",
            "model": ["Rectangular / Kotak", "Wayfarer", "Geometric", "Browline"],
        },
        "Persegi / Square": {
            "emoji": "🟫",
            "desc": "Wajah persegi cocok dengan frame melengkung untuk memperlunak rahang.",
            "model": ["Round / Bulat", "Oval", "Aviator", "Cat-Eye"],
        },
        "Hati / Heart": {
            "emoji": "🩷",
            "desc": "Wajah hati cocok dengan frame yang lebih lebar di bagian bawah.",
            "model": [
                "Aviator",
                "Round / Bulat",
                "Rimless / Tanpa Bingkai",
                "Low-Bridge Fit",
            ],
        },
        "Berlian / Diamond": {
            "emoji": "💎",
            "desc": "Wajah berlian cocok dengan frame yang menonjolkan tulang pipi.",
            "model": ["Cat-Eye", "Oval", "Rimless / Tanpa Bingkai", "Browline"],
        },
        "Segitiga / Triangle": {
            "emoji": "🔺",
            "desc": "Wajah segitiga cocok dengan frame yang lebih tebal/lebar di bagian atas.",
            "model": ["Browline", "Cat-Eye", "Wayfarer", "Semi-Rimless"],
        },
        "Persegi Panjang / Oblong": {
            "emoji": "▬",
            "desc": "Wajah panjang cocok dengan frame besar yang memberi kesan lebih lebar.",
            "model": ["Oversized", "Round / Bulat", "Aviator besar", "Geometric lebar"],
        },
    }
    return bentuk, rekomendasi.get(bentuk, rekomendasi["Oval"])


# ─── UI utama ─────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="main-title">Sistem Pakar Rekomendasi Kacamata</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="info-banner">
    ℹ️ &nbsp; Jawab pertanyaan berikut untuk mengetahui bentuk wajah dan rekomendasi model kacamata yang sesuai.
</div>
""",
    unsafe_allow_html=True,
)

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Dua kolom ──
col1, col2 = st.columns(2, gap="medium")

# ── Kolom 1: Karakteristik Wajah ──
with col1:
    with st.container(border=True):  # border=True → card native Streamlit ≥1.30
        st.markdown(
            '<div class="card-title">Karakteristik Wajah</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="qlabel">1. Bagian wajah paling lebar</div>',
            unsafe_allow_html=True,
        )
        bagian_lebar = st.radio(
            "bagian_lebar",
            ["Dahi", "Pipi", "Rahang"],
            index=None,
            label_visibility="collapsed",
            key="q1",
        )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        st.markdown('<div class="qlabel">2. Bentuk dagu</div>', unsafe_allow_html=True)
        bentuk_dagu = st.radio(
            "bentuk_dagu",
            ["Runcing", "Membulat"],
            index=None,
            label_visibility="collapsed",
            key="q2",
        )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        st.markdown(
            '<div class="qlabel">3. Bentuk rahang</div>', unsafe_allow_html=True
        )
        bentuk_rahang = st.radio(
            "bentuk_rahang",
            ["Tegas", "Membulat"],
            index=None,
            label_visibility="collapsed",
            key="q3",
        )

# ── Kolom 2: Proporsi Wajah ──
with col2:
    with st.container(border=True):
        st.markdown(
            '<div class="card-title">Proporsi Wajah</div>', unsafe_allow_html=True
        )

        st.markdown(
            '<div class="qlabel">4. Panjang wajah</div>', unsafe_allow_html=True
        )
        panjang_wajah = st.radio(
            "panjang_wajah",
            ["Lebih panjang dari lebar wajah", "Panjang dan lebar hampir sama"],
            index=None,
            label_visibility="collapsed",
            key="q4",
        )

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)

        st.markdown(
            '<div class="qlabel">5. Apakah wajah menyempit ke arah dagu?</div>',
            unsafe_allow_html=True,
        )
        menyempit_dagu = st.radio(
            "menyempit_dagu",
            ["Ya", "Tidak"],
            index=None,
            label_visibility="collapsed",
            key="q5",
        )

st.markdown("<hr class='divider'>", unsafe_allow_html=True)

# ── Tombol & hasil ──
if st.button("🔍  Analisis", use_container_width=True):
    bentuk, info = analisis_wajah(
        bagian_lebar, bentuk_dagu, bentuk_rahang, panjang_wajah, menyempit_dagu
    )

    items_html = "".join(f'<div class="rec-item">✅ {m}</div>' for m in info["model"])
    st.markdown(
        f"""
    <div class="result-box">
        <div class="result-title">Hasil Analisis</div>
        <div class="face-shape">{info['emoji']} Bentuk Wajah: {bentuk}</div>
        <p style="color:#8b949e;font-size:.93rem;margin-bottom:1rem;">{info['desc']}</p>
        <div class="rec-label">Rekomendasi Model Kacamata</div>
        {items_html}
    </div>
    """,
        unsafe_allow_html=True,
    )
