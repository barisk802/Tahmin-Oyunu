import streamlit as st
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

st.title("🎯 Sayıyı Tahmin Et - Google Sheets Skor Kaydı")

# Google Sheets bağlantısı
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("streamlit-anahtar.json", scope)
client = gspread.authorize(credentials)

sheet = client.open("sayi_tahmin_skorlar").sheet1  # Google Sheet adınla aynı olmalı

# Oyun değişkenleri
if "sayi" not in st.session_state:
    st.session_state.sayi = random.randint(1, 100)
if "deneme" not in st.session_state:
    st.session_state.deneme = 0

isim = st.text_input("Adınızı Giriniz:")

tahmin = st.number_input("Tahmininizi giriniz (1-100):", min_value=1, max_value=100, step=1)

if st.button("Tahmin Et"):
    st.session_state.deneme += 1

    if tahmin < st.session_state.sayi:
        st.info("Tahminini Yükselt ⬆️")
    elif tahmin > st.session_state.sayi:
        st.warning("Tahminini Küçült ⬇️")
    else:
        st.success(f"{st.session_state.deneme} denemede doğru bildiniz 🎉")
        st.balloons()

        # Skoru Google Sheets'e kaydet
        if isim:
            tarih = datetime.now().strftime("%d.%m.%Y %H:%M")
            sheet.append_row([isim, st.session_state.deneme, tarih])
            st.info("Skorunuz kaydedildi ✅")

        # Yeni oyun
        st.session_state.sayi = random.randint(1, 100)
        st.session_state.deneme = 0

# Skor tablosunu göster
st.subheader("📊 Güncel Skor Tablosu")
data = sheet.get_all_records()
if data:
    for i, satir in enumerate(data, start=1):
        st.write(f"{i}. {satir['İsim']} - {satir['Deneme']} deneme ({satir['Tarih']})")
else:
    st.write("Henüz kayıt yok.")
