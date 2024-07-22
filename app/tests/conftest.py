import pytest
from fastapi.testclient import TestClient
from fastapi.security import OAuth2PasswordRequestForm
from api import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base
from database.database import get_db
from sqlalchemy.pool import StaticPool
from auth.authenticate import authenticate
from database.config import DB_Settings

from auth.jwt_handler import create_access_token
from models.users import UserTable


url = DB_Settings.DATABASE_URL
engine = create_engine(url, poolclass=StaticPool)
Session = sessionmaker(autoflush=False, bind=engine)


@pytest.fixture(name="session")
def session_fixture():
    Base.metadata.create_all(bind=engine)
    with Session() as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_db] = get_session_override
    app.dependency_overrides[OAuth2PasswordRequestForm] = (
        lambda: OAuth2PasswordRequestForm(username="test_3@mail.ru", password="123")
    )
    app.dependency_overrides[authenticate] = lambda: "test_3@mail.ru"

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="token")
def user_token(session: Session):

    test_user = (
        session.query(UserTable).filter(UserTable.email == "test_3@mail.ru").first()
    )
    token = create_access_token({"sub": test_user.email})
    return token
