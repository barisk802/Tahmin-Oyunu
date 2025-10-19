import streamlit as st
import random

st.title("🎯 Sayıyı Tahmin Et")

if "sayi" not in st.session_state:
    st.session_state.sayi = random.randint(1, 101)

tahmin = st.number_input("Tahmininizi giriniz (1-100):", min_value=1, max_value=101, step=1)

if st.button("Tahmin Et"):
    if tahmin < st.session_state.sayi:
        st.info("Tahminini Yükselt ⬆️")
    elif tahmin > st.session_state.sayi:
        st.warning("Tahminini Küçült ⬇️")
    else:
        st.success("🎉 Doğru Tahmin!")
        st.balloons()

        st.session_state.sayi = random.randint(1, 101)
        st.info("Yeni sayı seçildi! Devam edebilirsin 👇")
