from aiogram.fsm.state import State , StatesGroup

class GameStates(StatesGroup):
    # Ожидание игроков(в группе когда ждут присоедениеия)
    WAITING_FOR_PLAYERS = State()

    # Ночь
    Night = State()

    # День
    Day_Vote = State()

    # Завершение игры
    Game_Over = State()

    # Раздача ролей
    Role = State()

