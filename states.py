from aiogram.fsm.state import State,StatesGroup



class Product(StatesGroup):
    prod_name = State(),
    quantity = State()
    description = State()
    price = State()
    quantity = State()
