import os
import pandas as pd

def build_recommendation_model(movie_title, min_reviews=50):
    # 1. Temizlenmiş verileri yükle
    processed_dir = os.path.join("data", "processed")
    ratings_df = pd.read_csv(os.path.join(processed_dir, "ratings.csv"))
    movies_df = pd.read_csv(os.path.join(processed_dir, "movies.csv"))

    # 2. Matrisi Oluştur
    df = pd.merge(ratings_df, movies_df, on="item_id")
    user_movie_matrix = df.pivot_table(index="user_id", columns="title", values="rating")

    if movie_title not in user_movie_matrix.columns:
        return None

    # 3. Benzerlikleri Hesapla
    movie_user_ratings = user_movie_matrix[movie_title]
    similar_movies = user_movie_matrix.corrwith(movie_user_ratings)

    corr_df = pd.DataFrame(similar_movies, columns=["Correlation"])
    corr_df.dropna(inplace=True)

    # 4. Filtreleme ve Sıralama
    ratings_count = pd.DataFrame(df.groupby('title')['rating'].count())
    corr_df = corr_df.join(ratings_count['rating'])
    corr_df.rename(columns={'rating': 'Rating_Count'}, inplace=True)
    
    recommendations = corr_df[corr_df['Rating_Count'] > min_reviews].sort_values(by='Correlation', ascending=False)

    # Veriyi ekrana yazdırmak yerine arayüz için döndürüyoruz
    return recommendations.head(6)[1:]

if __name__ == "__main__":
    sonuc = build_recommendation_model("Star Wars (1977)")
    print(sonuc)