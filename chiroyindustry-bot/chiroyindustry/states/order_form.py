from aiogram.dispatcher.filters.state import StatesGroup, State


class Form(StatesGroup):
    market = State()
    name = State()
    phone = State()
    product = State()
    region = State()
    location = State()

class UserStates(StatesGroup):
    # Define states inside the UserStates class
    IN_START = State()
    IN_LANG = State()
    IN_NAME = State()
    IN_MENU = State()

class ChangeLang(StatesGroup):
    Lang = State()