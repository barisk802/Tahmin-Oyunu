import streamlit as st
import random
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

st.title("🎯 Sayıyı Tahmin Et - Google Sheets Skor Kaydı")

# Secrets üzerinden JSON alıyoruz
json_creds = st.secrets["gcp_service_account"]["key"]
creds_dict = json.loads(json_creds)

# Google Sheets bağlantısı
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(credentials)

# Google Sheet açma
sheet = client.open("sayi_tahmin_skorlar").sheet1  # Sheet adı tam olarak eşleşmeli

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
