import os
import pandas as pd

def build_recommendation_model(movie_title, min_reviews=50):
    print("Veriler yükleniyor ve matris oluşturuluyor...")
    
    # 1. Temizlenmiş verileri yükle
    processed_dir = os.path.join("data", "processed")
    ratings_df = pd.read_csv(os.path.join(processed_dir, "ratings.csv"))
    movies_df = pd.read_csv(os.path.join(processed_dir, "movies.csv"))

    # 2. Puanlar ve Filmler tablosunu item_id üzerinden birleştir
    df = pd.merge(ratings_df, movies_df, on="item_id")

    # 3. Pivot Tablo (Kullanıcı-Film Matrisi) Oluştur
    # Satırlar: Kullanıcılar, Sütunlar: Filmler, Değerler: Puanlar
    user_movie_matrix = df.pivot_table(index="user_id", columns="title", values="rating")

    # Aranılan film veritabanında var mı kontrolü
    if movie_title not in user_movie_matrix.columns:
        print(f"Hata: '{movie_title}' isimli film veritabanında bulunamadı.")
        return

    # 4. Seçilen filmin (örneğin Star Wars) tüm kullanıcılar tarafından verilen puanlarını çek
    movie_user_ratings = user_movie_matrix[movie_title]

    # 5. Bu filmin puanları ile diğer tüm filmlerin puanları arasındaki Pearson Korelasyonunu hesapla
    print(f"'{movie_title}' için benzerlikler hesaplanıyor...")
    similar_movies = user_movie_matrix.corrwith(movie_user_ratings)

    # 6. Sonuçları daha düzgün görünmesi için bir DataFrame'e çevir ve boş (NaN) değerleri at
    corr_df = pd.DataFrame(similar_movies, columns=["Correlation"])
    corr_df.dropna(inplace=True)

    # 7. Sadece 1-2 kişinin izleyip 5 yıldız verdiği yanıltıcı filmleri elemek için puanlanma sayısını bul
    ratings_count = pd.DataFrame(df.groupby('title')['rating'].count())
    corr_df = corr_df.join(ratings_count['rating'])
    corr_df.rename(columns={'rating': 'Rating_Count'}, inplace=True)
    
    # 8. Belirli bir oy sayısını (min_reviews) geçen filmleri filtrele ve benzerlik oranına göre büyükten küçüğe sırala
    recommendations = corr_df[corr_df['Rating_Count'] > min_reviews].sort_values(by='Correlation', ascending=False)

    # 9. Sonuçları ekrana yazdır (İlk sırada filmin kendisi çıkacağı için [1:6] ile sonraki 5 filmi alıyoruz)
    print(f"\n--- '{movie_title}' SEVENLER BUNLARI DA SEVDİ ---")
    print(recommendations.head(6)[1:])

if __name__ == "__main__":
    # Algoritmayı test etmek için ikonik bir film seçelim
    build_recommendation_model("Star Wars (1977)")