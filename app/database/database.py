from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import Base
from models.users import UserTable
from models.data import DataTable
from models.transactions import TransactionsTable
from database.config import DB_Settings


url = DB_Settings.DATABASE_URL
engine = create_engine(url)
SessionLocal = sessionmaker(autoflush=False, bind=engine)

def get_db():
    with SessionLocal() as session:
        yield session

def db_init():
    Base.metadata.create_all(bind=engine)