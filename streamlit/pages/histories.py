import streamlit as st
import pandas as pd
from menu import menu_with_redirect
import requests
from params import FASTAPI_URL

menu_with_redirect()

st.title(
    f"Посмотри, что мы на тебя собрали, {st.session_state.user_name} :sleuth_or_spy:"
)

if st.button("Посмотреть историю транзакций"):
    response = requests.get(
        f"{FASTAPI_URL}/transaction/history/{st.session_state.user_id}",
        timeout=600,
    )
    if response.status_code == 200 or response.status_code == 404:
        history = pd.DataFrame(response.json())
        history = history.reindex(
            columns=["id", "user_id", "date", "replenishment", "write_off"]
        )
        history.columns = [
            "ID транзакции",
            "ID пользователя",
            "Дата",
            "Пополнение",
            "Списание",
        ]
        st.table(history)
    else:
        st.markdown("Извини, не могу говорить. Все, пока!")

if st.button("Посмотреть историю запросов"):
    response = requests.get(
        f"{FASTAPI_URL}/data/load_data_hist/{st.session_state.user_id}",
        timeout=600,
    )
    if response.status_code == 200 or response.status_code == 404:
        history = pd.DataFrame(response.json())
        history = history.reindex(
            columns=[
                "id",
                "user_id",
                "request_date",
                "current_assets",
                "cost_of_goods_sold",
                "depreciation_and_amortization",
                "inventory",
                "net_income",
                "total_receivables",
                "total_assets",
                "total_longterm_debt",
                "ebit",
                "gross_profit",
                "total_current_liabilities",
                "retained_earnings",
                "total_liabilities",
                "output_data",
            ]
        )
        history.columns = [
            "ID запроса",
            "ID пользователя",
            "Дата запроса",
            "Активы, которые будут использованы в ближайший год",
            "Сумма, уплаченная за товары",
            "Износ и амортизация",
            "Предметы и сырье",
            "Общая прибыльность",
            "Средства, еще не оплаченные клиентами",
            "Все активы",
            "Долгосрочные обязательства",
            "Прибыль до вычета процентов и налогов",
            "Прибыль после вычета всех затрат на производство",
            "Сумма кредиторской задолженности, начисленных обязательств и налогов",
            "Сумма прибыли, оставшаяся после уплаты всех прямых и косвенных затрат",
            "Совокупные долги и обязательства перед внешними сторонами",
            "Ответ сервиса",
        ]
        st.table(history)
    else:
        st.markdown("Извини, не могу говорить. Все, пока!")
