import streamlit as st
import pandas as pd
import os
from src.models.recommend import build_recommendation_model

# Sayfa ayarları
st.set_page_config(page_title="Film Tavsiye Motoru", page_icon="🍿")

st.title("🎬 Akıllı Film Tavsiye Motoru")
st.markdown("İzlediğiniz ve beğendiğiniz bir filmi seçin, yapay zeka size benzer zevklere sahip kullanıcıların izlediği diğer filmleri önersin!")

# Filmleri açılır liste (dropdown) için yükle
@st.cache_data
def load_movies():
    movies_path = os.path.join("data", "processed", "movies.csv")
    if os.path.exists(movies_path):
        return pd.read_csv(movies_path)
    return pd.DataFrame()

movies_df = load_movies()

if not movies_df.empty:
    movie_list = sorted(movies_df['title'].dropna().unique().tolist())
    
    # Kutunun boş gelmesi için index=None ve şık bir görünüm için placeholder ekliyoruz
    selected_movie = st.selectbox(
        "Bir film seçin (Yazarak arayabilirsiniz):", 
        movie_list,
        index=None,
        placeholder="Aramak için buraya tıklayın veya yazın..."
    )

    # Butona basıldığında çalışacak kısım
    if st.button("Bana Film Öner 🚀"):
        # Eğer kutu boşken butona basılırsa uyarı ver
        if selected_movie is None:
            st.warning("Lütfen film önerebilmem için kutudan bir film seçin veya arayın.")
        else:
            with st.spinner('Matrisler hesaplanıyor, algoritma çalışıyor...'):
                recommendations = build_recommendation_model(selected_movie)
                
                if recommendations is not None and not recommendations.empty:
                    st.success(f"**{selected_movie}** sevenler bunları da sevdi:")
                    st.table(recommendations[['Correlation', 'Rating_Count']])
                else:
                    st.error("Bu film için yeterli veri bulunamadı.")
else:
    st.error("Veri seti bulunamadı. Lütfen önce veri ön işleme adımlarını tamamlayın.")