import joblib


class OperModel:
    def __init__(
        self,
        model_path: str = "model/model.pkl",
    ):
        self.model = self.load_model(model_path)

    # метод для загрузки модели
    def load_model(self, model_path):
        try:
            model = joblib.load(model_path)
            return model
        except Exception as e:
            return f"Ошибка с загрузкой модели {e}"

    # метод для генерации ответа
    def response(self, data):
        response = self.model.predict_proba(data)[:, 0].tolist()
        print(response)
        response = response[0]*100
        return response
