from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from States.games import GameStates
from config import MIN_PLAYERS

router = Router()

async def chat_type(message : Message) -> bool:
    return message.chat.type in ["group" , "supergroup"]


@router.message(Command("start_mafia") , chat_type)
async def cmd_start_mafia(message: Message, state: FSMContext):
    print(f"Processing /start_mafia from chat {message.chat.id} by user {message.from_user.id}")
    print(f"Chat type: {message.chat.type}")  # Добавляем тип чата для отладки
    if message.from_user.id not in [admin.user.id for admin in await message.chat.get_administrators()]:
        await message.reply("Только администратор группы может начать игру!")
        return

    await state.set_state(GameStates.WAITING_FOR_PLAYERS)
    await state.update_data(chat_id=message.chat.id)
    await message.reply(
        "Игра в Мафию началась! Напишите боту в личку /start, чтобы присоединиться."
    )

@router.message(Command("begin_mafia"))
async def cmd_begin_mafia(message: Message, state: FSMContext):
    print(f"Processing /begin_mafia from chat {message.chat.id} by user {message.from_user.id}")
    print(f"Chat type: {message.chat.type}")
    if message.from_user.id not in [admin.user.id for admin in await message.chat.get_administrators()]:
        await message.reply("Только администратор группы может запустить игру!")
        return

    data = await state.get_data()
    chat_id = data.get("chat_id")

    if chat_id != message.chat.id:
        await message.reply("Сессия не найдена или создана в другой группе!")
        return

    player_count = 7
    if player_count < MIN_PLAYERS:
        await message.reply(f"Недостаточно игроков! Требуется минимум {MIN_PLAYERS}.")
        return

    await state.set_state(GameStates.NIGHT_ACTION)
    await message.reply("Игра началась! Роли распределены, ночь наступила.")