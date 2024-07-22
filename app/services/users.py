from models.users import UserTable
from models.schemas import UserRegister
from loguru import logger


class User:
    def __init__(self) -> None:
        pass
    def user_add(self, session, user_data: UserRegister):
        user_add = UserTable(
            email=user_data.email,
            phone=user_data.phone,
            name=user_data.name,
            surname=user_data.surname,
            user_password=user_data.user_password,
            company_name=user_data.company_name,
            balance=user_data.balance,
        )
        session.add(user_add)
        session.commit()

    def get_user_by_email(self, session, email):
        user = session.query(UserTable).filter(UserTable.email == email).first()
        if user:
            return user
        else:
            return None

    def user_del(self, session, user_id):
        user = session.query(UserTable).filter(UserTable.id == user_id).first()
        session.delete(user)
        session.commit()
        logger.info(f"Пользователь с id{self.user_id} удален из базы")

    def check_balance(self, session, user_id):
        user = session.query(UserTable).filter(UserTable.id == user_id).first()
        return user.balance
