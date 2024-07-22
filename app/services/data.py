from models.data import DataTable
from models.schemas import InputData
import datetime


# класс для данных
class OperData:
    def __init__(
        self,
        user_id: int = 0,
    ) -> None:
        self.user_id = user_id

    # метод для загрузки истории запросов пользователя
    def load_data(self, session, user_id):
        data = session.query(DataTable).filter(DataTable.user_id == user_id).all()
        if not data:
            return None

        return data

    # метод для удаления истории запросов пользователя
    def delete_data_history(self, session, user_id):
        session.query(DataTable).filter(DataTable.user_id == user_id).delete()
        session.commit()

    # метод для преобразования данных из БД в словарь
    def transform_data(self, data):
        transform_data = {}
        for obj in data:
            obj_data = {
                "Дата запроса": obj.request_date,
                "Активы, которые будут использованы в ближайший год": obj.current_assets,
                "Сумма, уплаченная за товары": obj.cost_of_goods_sold,
                "Износ и амортизация": obj.depreciation_and_amortization,
                "Предметы и сырье": obj.inventory,
                "Общая прибыльность": obj.net_income,
                "Средства, еще не оплаченные клиентами": obj.total_receivables,
                "Все активы": obj.total_assets,
                "Долгосрочные обязательства": obj.total_longterm_debt,
                "Прибыль до вычета процентов и налогов": obj.ebit,
                "Прибыль после вычета всех затрат на производство": obj.gross_profit,
                "Сумма кредиторской задолженности, начисленных обязательств и налогов": obj.total_current_liabilities,
                "Сумма прибыли, оставшаяся после уплаты всех прямых и косвенных затрат": obj.retained_earnings,
                "Совокупные долги и обязательства перед внешними сторонами": obj.total_liabilities,
                "Исходящие данные": obj.output_data,
            }
        transform_data[f"Данные ID{obj.id}"] = obj_data
        return transform_data

    # метод для сохранения входящих данных
    def save_input_data(self, input_data: InputData, session):
        data_add = DataTable(
            user_id=self.user_id,
            request_date=datetime.datetime.now().strftime("%Y.%m.%d %H:%M:%S"),
            current_assets=input_data.current_assets,
            cost_of_goods_sold=input_data.cost_of_goods_sold,
            depreciation_and_amortization=input_data.depreciation_and_amortization,
            inventory=input_data.inventory,
            net_income=input_data.net_income,
            total_receivables=input_data.total_receivables,
            total_assets=input_data.total_assets,
            total_longterm_debt=input_data.total_longterm_debt,
            ebit=input_data.ebit,
            gross_profit=input_data.gross_profit,
            total_current_liabilities=input_data.total_current_liabilities,
            retained_earnings=input_data.retained_earnings,
            total_liabilities=input_data.total_liabilities,
            output_data=None,
        )
        session.add(data_add)
        session.commit()
        return data_add.id

    # метод для сохранения исходящих данных
    def save_output_data(self, session, output_data, data_id):
        data = (
            session.query(DataTable)
            .filter(DataTable.user_id == self.user_id, DataTable.id == data_id)
            .first()
        )
        data.output_data = output_data
        session.commit()

    def check_output(self, session, data_id):

        if self.load_output_data(session, data_id) == None:
            return "no prediction("
        else:
            return "have prediction!"

    def load_output_data(self, session, data_id):
        output_data = (
            session.query(DataTable.output_data)
            .filter(DataTable.user_id == self.user_id, DataTable.id == data_id)
            .first()
        )
        if not output_data:
            return None
        
        return output_data[0]
