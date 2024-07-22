import streamlit as st
from menu import menu_with_redirect
import requests
from params import FASTAPI_URL

menu_with_redirect()


def check_balance():
    check_balance = requests.get(
        f"{FASTAPI_URL}/user/balance/{st.session_state.user_id}",
        headers={"Authorization": f"Bearer {st.session_state.user_token}"},
        timeout=600,
    )
    balance = check_balance.text
    st.sidebar.markdown(
        f"""
                # Баланс:
                # :red[{balance} :money_with_wings:]"""
    )


st.title("Введи значения для оценки:")

current_assets = st.number_input(
    "Активы, которые будут использованы в ближайший год",
    min_value=-100,
    max_value=200000,
    help="Все активы компании, которые ожидается продать или использовать в результате стандартных бизнес-операций в течение следующего года",
)
cost_of_goods_sold = st.number_input(
    "Сумма, уплаченная за товары",
    min_value=-1000,
    max_value=400000,
    help="Общая сумма, которую компания заплатила за товары, непосредственно связанные с продажей продукции",
)
depreciation_and_amortization = st.number_input(
    "Износ и амортизация",
    min_value=0,
    max_value=50000,
    help="Амортизация относится к утрате стоимости материальных основных средств со временем (таких как имущество, оборудование, здания и заводы). Износ относится к утрате стоимости нематериальных активов со временем.",
)
inventory = st.number_input(
    "Предметы и сырье",
    min_value=0,
    max_value=100000,
    help="Учет предметов и сырья, которые компания либо использует в производстве, либо продает.",
)
net_income = st.number_input(
    "Общая прибыльность",
    min_value=-200000,
    max_value=200000,
    help="Общая прибыльность компании после вычета всех расходов и затрат из общей выручки.",
)
total_receivables = st.number_input(
    "Средства, еще не оплаченные клиентами",
    min_value=-10,
    max_value=200000,
    help="Остаток средств, причитающихся компании за поставленные товары или оказанные услуги, но еще не оплаченные клиентами.",
)
total_assets = st.number_input(
    "Все активы",
    min_value=0,
    max_value=800000,
    help="Все активы или ценные предметы, принадлежащие бизнесу.",
)
total_longterm_debt = st.number_input(
    "Долгосрочные обязательства",
    min_value=-10,
    max_value=200000,
    help="Займы и другие обязательства компании, которые не будут погашены в течение одного года с даты баланса.",
)
ebit = st.number_input(
    "Прибыль до вычета процентов и налогов",
    min_value=-200000,
    max_value=200000,
    help="Прибыль до вычета процентов и налогов.",
)
gross_profit = st.number_input(
    "Прибыль после вычета всех затрат на производство",
    min_value=-100000,
    max_value=200000,
    help="Прибыль компании после вычета всех затрат, связанных с производством и продажей ее продукции или услуг.",
)
total_current_liabilities = st.number_input(
    "Сумма кредиторской задолженности, начисленных обязательств и налогов",
    min_value=0,
    max_value=200000,
    help="Сумма кредиторской задолженности, начисленных обязательств и налогов, таких как задолженность по облигациям на конец года, заработные платы и оставшиеся комиссии.",
)
retained_earnings = st.number_input(
    "Сумма прибыли, оставшаяся после уплаты всех прямых и косвенных затрат",
    min_value=-200000,
    max_value=600000,
    help="Сумма прибыли, оставшаяся у компании после уплаты всех прямых и косвенных затрат, налогов на прибыль и дивидендов акционерам.",
)
total_liabilities = st.number_input(
    "Совокупные долги и обязательства перед внешними сторонами",
    min_value=-0,
    max_value=600000,
    help="Совокупные долги и обязательства компании перед внешними сторонами.",
)

if st.button("Оценить"):
    input_data = {
        "current_assets": current_assets,
        "cost_of_goods_sold": cost_of_goods_sold,
        "depreciation_and_amortization": depreciation_and_amortization,
        "inventory": inventory,
        "net_income": net_income,
        "total_receivables": total_receivables,
        "total_assets": total_assets,
        "total_longterm_debt": total_longterm_debt,
        "ebit": ebit,
        "gross_profit": gross_profit,
        "total_current_liabilities": total_current_liabilities,
        "retained_earnings": retained_earnings,
        "total_liabilities": total_liabilities,
    }
    response = requests.post(
        f"{FASTAPI_URL}/model/pred/{st.session_state.user_id}",
        headers={"Authorization": f"Bearer {st.session_state.user_token}"},
        json=input_data,
        timeout=600,
    )
    check_balance()
    if response.status_code == 200:
        prediction = int(response.json())
        if prediction <= 5:
            st.success(f"Вероятность банкротства компании: {prediction} %", icon="✅")
        elif prediction > 5 and prediction <= 50:
            st.warning(f"Вероятность банкротства компании: {prediction} %", icon="⚠️")
        else:
            st.error(f"Вероятность банкротства компании: {prediction} %", icon="🚨")

    else:
        st.error("Какая то ошибка")
