import streamlit as st
import requests
from menu import menu
from params import FASTAPI_URL

menu()


st.title("Для регистрации введи свои данные:")

with st.form("signup", border=False):
    email = st.text_input("Почта")
    password = st.text_input("Пароль", type="password")
    name = st.text_input("Имя")
    surname = st.text_input("Фамилия")
    phone = st.text_input("Номер телефона")
    company_name = st.text_input("Наименование компании")

    if st.form_submit_button("Отправить"):
        data = {
            "email": email,
            "phone": phone,
            "name": name,
            "surname": surname,
            "user_password": password,
            "company_name": company_name,
            "balance": 0,
        }
        response = requests.post(f"{FASTAPI_URL}/user/signup/", json=data)
        if response.status_code == 200:
            st.markdown(response.json())
            st.markdown("А теперь войди на сайт")
        else:
            st.error("some error")
