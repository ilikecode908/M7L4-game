import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
from googletrans import Translator
import random
import os

duration = 3
sample_rate = 44100

seviyeye_gore_kelimeler = {
    "kolay": ["kedi", "köpek", "elma", "süt", "güneş", "ay"],
    "orta": ["muz", "okul", "arkadaş", "pencere", "sarı", "lamba"],
    "zor": ["teknoloji", "üniversite", "bilgi", "telaffuz", "hayal gücü"],
    "fazla zor": ["teğmen", "oran", "tebrikler", "aksesuar", "albay"]
}

print(" DOĞRU KONUŞ OYUNUNA HOŞ GELDİNİZ!")

while True:
    seviye = input("Hangi seviyeyi seçmek istersiniz? (kolay, orta, zor, fazla zor): ").lower()
    if seviye in seviyeye_gore_kelimeler:
        break
    print(" Geçersiz seviye, lütfen 'kolay', 'orta', 'zor' veya fazla zor yazın.")

translator = Translator()
recognizer = sr.Recognizer()

for i in range(3):
    print("\n" + "="*40)
    
    secilen_turkce_kelime = random.choice(seviyeye_gore_kelimeler[seviye])
    
    ceviri = translator.translate(secilen_turkce_kelime, src='tr', dest='en')
    hedef_ingilizce_kelime = ceviri.text.lower()

    print(f" Türkçe Kelime: ** {secilen_turkce_kelime.upper()} **")
    input(" İngilizcesini söylemek için ENTER'a basın ve konuşun...")

    print(" Dinleniyor... (3 saniyeniz var)")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")
    sd.wait()
    wav.write("output.wav", sample_rate, recording)
    print(" Kayıt tamamlandı, sesiniz analiz ediliyor...")

    with sr.AudioFile("output.wav") as source:
        audio = recognizer.record(source)
    try:
        soylenen_kelime = recognizer.recognize_google(audio, language="en-US").lower()
        print(f" Sizin söylediğiniz: {soylenen_kelime}")

        if soylenen_kelime == hedef_ingilizce_kelime:
            print(" DOĞRU! Harika telaffuz.")
        else:
            print(f" Maalesef eşleşmedi. Doğru cevap şuydu: '{hedef_ingilizce_kelime}'")

    except sr.UnknownValueError:
        print(" Sesiniz anlaşılamadı veya çok sessiz konuştunuz.")
    except sr.RequestError as e:
        print(f" İnternet bağlantısı veya hizmet hatası: {e}")

print("\n🏆 Oyun bitti!")

if os.path.exists("output.wav"):
    os.remove("output.wav")