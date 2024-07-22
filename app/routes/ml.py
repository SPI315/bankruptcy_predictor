from fastapi import APIRouter, Depends

from services.data import OperData
from services.transaction import Transaction
from services.users import User
from database.database import get_db
import json
from rmworker.send_message import RpcClient
from auth.authenticate import authenticate

from models.schemas import InputData

ml_router = APIRouter(tags=["ML"])


@ml_router.post("/pred/{id}")
async def pred(
    id: int, data: InputData, session=Depends(get_db), user: str = Depends(authenticate)
):
    oper_data = OperData(
        user_id=id,
    )
    user = User()
    transaction = Transaction()

    if user.check_balance(session, user_id=id) < 30:
        return "Требуется пополнить баланс"

    data_id = oper_data.save_input_data(input_data=data, session=session)

    to_send = json.dumps({id: data.model_dump()})

    response = RpcClient().send_message(message=to_send)
    result = json.loads(response)
    oper_data.save_output_data(session, result, data_id)
    transaction.write_off(session, user_id=id, value=30)
    return result
