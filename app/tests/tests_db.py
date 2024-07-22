from services.users import User
from tests.conftest import Session

from services.transaction import Transaction

test_transaction = Transaction()
user_for_tests = {
    "email": "test_3@mail.ru",
    "phone": "+7777777",
    "name": "test_3",
    "surname": "test_3",
    "user_password": "123",
    "company": "OOO",
    "balance": 0,
}


def test_create_user(session: Session):
    try:
        User().user_add(session, user_data=user_for_tests)
        assert True
    except Exception as e:
        assert False, e


def test_create_transaction(session: Session):
    try:
        test_user = User().get_user_by_email(session, email=user_for_tests["email"])
        test_transaction.replanishment(session, user_id=test_user.user_id, value=100)
        assert True
    except Exception as e:
        assert False, e


def test_delete_history(session: Session):
    try:
        test_user = User().get_user_by_email(session, email=user_for_tests["email"])
        test_transaction.del_history(session, user_id=test_user.user_id)
        assert True
    except Exception as e:
        assert False, e


def test_delete_user(session: Session):
    try:
        test_user = User().get_user_by_email(session, email=user_for_tests["email"])
        test_user.user_del(session, email=user_for_tests["email"])
        assert True
    except Exception as e:
        assert False, e
