from pydantic import BaseModel


class UserRegister(BaseModel):
    email: str = "test@mail.ru"
    phone: str = "+777777777"
    name: str = "Ryan"
    surname: str = "Gosling"
    user_password: str = "123"
    company_name: str = "OOO"
    balance: int = 0


class InputData(BaseModel):
    current_assets: int = 0
    cost_of_goods_sold: int = 0
    depreciation_and_amortization: int = 0
    inventory: int = 0
    net_income: int = 0
    total_receivables: int = 0
    total_assets: int = 0
    total_longterm_debt: int = 0
    ebit: int = 0
    gross_profit: int = 0
    total_current_liabilities: int = 0
    retained_earnings: int = 0
    total_liabilities: int = 0
