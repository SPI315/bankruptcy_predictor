from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from models.users import UserTable
from models.base import Base

user = UserTable()


class DataTable(Base):
    __tablename__ = "data_table"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user_table.id"))
    user = relationship(UserTable, primaryjoin=user_id == UserTable.id)
    request_date = Column(TIMESTAMP)
    current_assets = Column(Integer)
    cost_of_goods_sold = Column(Integer)
    depreciation_and_amortization = Column(Integer)
    inventory = Column(Integer)
    net_income = Column(Integer)
    total_receivables = Column(Integer)
    total_assets = Column(Integer)
    total_longterm_debt = Column(Integer)
    ebit = Column(Integer)
    gross_profit = Column(Integer)
    total_current_liabilities = Column(Integer)
    retained_earnings = Column(Integer)
    total_liabilities = Column(Integer)
    output_data = Column(String)
