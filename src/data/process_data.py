import os
import pandas as pd

def preprocess_data():
    raw_dir = os.path.join("data", "raw", "ml-100k")
    processed_dir = os.path.join("data", "processed")
    
    # Hedef klasör yoksa oluştur
    os.makedirs(processed_dir, exist_ok=True)
    
    print("Veri ön işleme adımı başlıyor...")
    
    # 1. Kullanıcı etkileşim verilerini (ratings) yükle ve temizle
    # u.data dosyası tab (tabulator) ile ayrılmıştır (\t)
    ratings_path = os.path.join(raw_dir, "u.data")
    if os.path.exists(ratings_path):
        print("Kullanıcı değerlendirme verileri (u.data) okunuyor...")
        ratings_columns = ["user_id", "item_id", "rating", "timestamp"]
        ratings_df = pd.read_csv(ratings_path, sep="\t", names=ratings_columns, engine="python")
        
        # Gereksiz timestamp kolonunu düşürelim
        ratings_df = ratings_df.drop(columns=["timestamp"])
        
        # Temizlenmiş veriyi kaydet
        output_ratings_path = os.path.join(processed_dir, "ratings.csv")
        ratings_df.to_csv(output_ratings_path, index=False)
        print(f"Kullanıcı etkileşimleri başarıyla kaydedildi: {output_ratings_path}")
    else:
        print(f"Hata: Değerlendirme dosyası bulunamadı! Yol: {ratings_path}")
        return

    # 2. Film detay verilerini (movies) yükle ve temizle
    # u.item dosyası dikey çizgi (|) ile ayrılmıştır ve latin-1 encoding gerektirir
    movies_path = os.path.join(raw_dir, "u.item")
    if os.path.exists(movies_path):
        print("Film detay verileri (u.item) okunuyor...")
        
        # Dosyada çok fazla kolon var (türler vb.), biz şimdilik sadece ID ve Başlık alacağız
        movies_columns = ["item_id", "title", "release_date", "video_release_date", "IMDb_URL"] + [f"genre_{i}" for i in range(19)]
        movies_df = pd.read_csv(movies_path, sep="|", names=movies_columns, encoding="latin-1", engine="python")
        
        # Sadece bizim için gerekli olan film ID'si ve başlığını seçelim
        movies_df = movies_df[["item_id", "title"]]
        
        # Temizlenmiş film listesini kaydet
        output_movies_path = os.path.join(processed_dir, "movies.csv")
        movies_df.to_csv(output_movies_path, index=False)
        print(f"Film detayları başarıyla kaydedildi: {output_movies_path}")
    else:
        print(f"Hata: Film detay dosyası bulunamadı! Yol: {movies_path}")
        return

    print("Veri ön işleme başarıyla tamamlandı!")

if __name__ == "__main__":
    preprocess_data()