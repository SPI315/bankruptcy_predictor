import streamlit as st
import requests
from params import FASTAPI_URL

def set_role():
    st.session_state.role = st.session_state._role



def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/predictor.py", label="Оценошная")
    st.sidebar.page_link("pages/histories.py", label="Веселые истории")
    choice = st.sidebar.number_input("Пополнить баланс", step=100)
    if st.sidebar.button("Пополнить"):
        if choice == 0:
            st.sidebar.markdown("На 0 пополнить нельзя")
        else:
            response = requests.post(
                f"{FASTAPI_URL}/transaction/replanishment/{st.session_state.user_id}",
                params={"summ": choice},
                timeout=600,
            )
            st.sidebar.markdown(response.text)
            st.rerun()
    if st.sidebar.button("Выйти"):
        st.session_state._role = False
        set_role()
        st.rerun()


def unauthenticated_menu():
    st.sidebar.page_link("main.py", label="Войти")
    st.sidebar.page_link("pages/signup.py", label="Зарегистрироваться")


def menu():
    if "role" not in st.session_state or st.session_state.role == False:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    if "role" not in st.session_state or st.session_state.role == False:
        st.switch_page("main.py")
    menu()
