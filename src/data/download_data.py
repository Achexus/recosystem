import os
import zipfile
import requests

def download_and_extract_data():
    # Dosya yolları ve URL tanımlamaları
    url = "https://files.grouplens.org/datasets/movielens/ml-100k.zip"
    raw_dir = os.path.join("data", "raw")
    zip_path = os.path.join(raw_dir, "ml-100k.zip")
    
    # data/raw klasörü yoksa oluştur
    os.makedirs(raw_dir, exist_ok=True)
    
    # 1. Zip dosyasını indir [cite: 20]
    if not os.path.exists(zip_path):
        print("MovieLens 100k veri seti indiriliyor...")
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(zip_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
            print("İndirme tamamlandı!")
        else:
            print(f"Hata: Veri seti indirilemedi. Durum kodu: {response.status_code}")
            return
    else:
        print("Zip dosyası zaten mevcut, indirme adımı atlanıyor.")

    # 2. Zip dosyasını ayıkla [cite: 21]
    print("Zip dosyası data/raw dizinine ayıklanıyor...")
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        # Doğrudan data/raw klasörünün içine ayıkla [cite: 21]
        zip_ref.extractall(raw_dir)
    print("Ayıklama işlemi başarıyla tamamlandı!")

if __name__ == "__main__":
    download_and_extract_data()