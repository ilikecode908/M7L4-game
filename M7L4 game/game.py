# ---------------------------------------------------------
# 📦 KÜTÜPHANELER
# Ses kaydı, ses dosyası yazma, konuşma tanıma, çeviri, rastgele seçim, dosya
# ---------------------------------------------------------
import os
import random
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator

# ---------------------------------------------------------
# ⚙️ AYARLAR (Sabit değerler)
# Ses kaydı süresi, örnekleme hızı, maksimum hata, tur sayısı, kelime listeleri
# ---------------------------------------------------------
DURATION = 3
SAMPLE_RATE = 44100
MAX_HATA = 3
TUR_SAYISI = 3

KELIMELER = {
    "kolay": ["kedi", "köpek", "elma", "süt", "güneş", "ay"],
    "orta": ["muz", "okul", "arkadaş", "pencere", "sarı", "lamba"],
    "zor": ["teknoloji", "üniversite", "bilgi", "telaffuz", "hayal gücü"],
    "fazla zor": ["teğmen", "oran", "tebrikler", "aksesuar", "albay"]
}

# ---------------------------------------------------------
# 🎮 BAŞLANGIÇ EKRANI
# Oyuncuya hoş geldin mesajı gösterilir
# ---------------------------------------------------------
print("\n" + "=" * 50)
print("🎤 DOĞRU KONUŞ OYUNUNA HOŞ GELDİNİZ! 🎮")
print("=" * 50)

# ---------------------------------------------------------
# 🎚️ SEVİYE SEÇİMİ
# Oyuncu bir zorluk seviyesi seçer (kolay, orta, zor, fazla zor)
# Yanlış yazarsa tekrar istenir
# ---------------------------------------------------------
while True:
    seviye = input("\nSeviye seçin (kolay, orta, zor, fazla zor): ").lower()
    if seviye in KELIMELER:
        break
    print("❌ Geçersiz seviye, tekrar deneyin.")

# ---------------------------------------------------------
# 🧠 ÇEVİRİ VE SES TANIMA ARAÇLARININ HAZIRLANMASI
# Translator → Türkçe kelimeyi İngilizceye çevirir
# Recognizer → Ses dosyasını analiz eder
# ---------------------------------------------------------
translator = Translator()
recognizer = sr.Recognizer()

# ---------------------------------------------------------
# 🧮 SKOR VE HATA SAYACI
# Oyuncunun doğru ve yanlışlarını takip eder
# ---------------------------------------------------------
skor = 0
hatalar = 0

print("\n🔥 Oyun başlıyor! Toplam 3 kelime söyleyeceksiniz.")
print(f"❗ {MAX_HATA} hata yaparsanız oyun biter.\n")

# ---------------------------------------------------------
# 🔁 OYUN DÖNGÜSÜ (3 tur)
# Her turda:
# 1. Türkçe kelime seçilir
# 2. İngilizceye çevrilir
# 3. Oyuncu sesle cevap verir
# 4. Ses tanınır ve karşılaştırılır
# ---------------------------------------------------------
for tur in range(1, TUR_SAYISI + 1):
    print("\n" + "=" * 40)
    print(f"📌 TUR {tur}")

    # 🎯 Rastgele Türkçe kelime seçimi
    turkce_kelime = random.choice(KELIMELER[seviye])

    # 🌍 İngilizce çeviri
    ingilizce_kelime = translator.translate(turkce_kelime, src="tr", dest="en").text.lower()

    print(f"\nTürkçe Kelime: 🟦 {turkce_kelime.upper()} 🟦")
    input("🎙 İngilizcesini söylemek için ENTER'a basın...")

    # 🎧 Ses kaydı
    print("\n🎧 Dinleniyor... (3 saniyeniz var)")
    recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=1, dtype="int16")
    sd.wait()

    # 💾 Ses dosyasını kaydetme
    wav.write("output.wav", SAMPLE_RATE, recording)
    print("🔎 Ses analiz ediliyor...")

    # 🗣️ Ses tanıma
    try:
        with sr.AudioFile("output.wav") as source:
            audio = recognizer.record(source)
        soylenen = recognizer.recognize_google(audio, language="en-US").lower()

        print(f"🗣 Söylediğiniz: {soylenen}")

        # ✔ Doğru mu yanlış mı kontrolü
        if soylenen == ingilizce_kelime:
            print("✅ DOĞRU! Harika telaffuz.")
            skor += 1
        else:
            print(f"❌ Yanlış. Doğru cevap: '{ingilizce_kelime}'")
            hatalar += 1

    # ⚠️ Ses anlaşılmadı
    except sr.UnknownValueError:
        print("⚠️ Sesiniz anlaşılamadı.")
        hatalar += 1

    # 🌐 İnternet hatası
    except sr.RequestError:
        print("🌐 İnternet hatası.")
        hatalar += 1

    # 📊 Skor ekranı
    print(f"📊 Skor: {skor} | ❗ Hatalar: {hatalar}/{MAX_HATA}")

    # 💥 Hata limiti dolduysa oyun biter
    if hatalar >= MAX_HATA:
        print("\n💥 Çok fazla hata yaptınız, oyun sona erdi!")
        break

# ---------------------------------------------------------
# 🏁 OYUN BİTİŞ EKRANI
# Toplam skor gösterilir
# ---------------------------------------------------------
print("\n" + "=" * 50)
print("🏁 OYUN BİTTİ!")
print(f"🎯 Toplam Skorunuz: {skor}")
print("=" * 50)

# ---------------------------------------------------------
# 🗑️ GEÇİCİ SES DOSYASINI SİLME
# output.wav dosyası temizlenir
# ---------------------------------------------------------
if os.path.exists("output.wav"):
    os.remove("output.wav")
