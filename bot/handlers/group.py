from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from bot.states.game import GameStates
from bot.config import MIN_PLAYERS
from bot.utils.session_manager import add_active_session, remove_active_session

router = Router()

async def is_group_or_supergroup(message: Message) -> bool:
    return message.chat.type in ["group", "supergroup"]

@router.message(Command("start_mafia"), is_group_or_supergroup)
async def cmd_start_mafia(message: Message, state: FSMContext):
    print(f"Processing /start_mafia from chat {message.chat.id} by user {message.from_user.id}")
    print(f"Chat type: {message.chat.type}")
    if message.from_user.id not in [admin.user.id for admin in await message.chat.get_administrators()]:
        await message.reply("Только администратор группы может начать игру!")
        return

    storage = state.storage
    chat_id = message.chat.id
    group_state = FSMContext(storage=storage, key=(chat_id, chat_id))

    await group_state.set_state(GameStates.WAITING_FOR_PLAYERS)
    print(f"Set state to {await group_state.get_state()}")
    await group_state.update_data(chat_id=message.chat.id, players=[])
    saved_data = await group_state.get_data()
    print(f"Saved data after update: {saved_data}")

    add_active_session(message.chat.id)
    print(f"Added session {message.chat.id} to active sessions")

    await message.reply(
        "Игра в Мафию началась! Напишите боту в личку /start, чтобы присоединиться."
    )

@router.message(Command("begin_mafia"), is_group_or_supergroup)
async def cmd_begin_mafia(message: Message, state: FSMContext):
    print(f"Processing /begin_mafia from chat {message.chat.id} by user {message.from_user.id}")
    print(f"Chat type: {message.chat.type}")
    if message.from_user.id not in [admin.user.id for admin in await message.chat.get_administrators()]:
        await message.reply("Только администратор группы может запустить игру!")
        return

    storage = state.storage
    chat_id = message.chat.id
    group_state = FSMContext(storage=storage, key=(chat_id, chat_id))

    data = await group_state.get_data()
    chat_id_from_data = data.get("chat_id")
    print(f"Retrieved data: {data}, chat_id_from_data: {chat_id_from_data}")

    if chat_id_from_data != message.chat.id:
        await message.reply("Сессия не найдена или создана в другой группе!")
        return

    players = data.get("players", [])
    player_count = len(players)
    if player_count < MIN_PLAYERS:
        await message.reply(f"Недостаточно игроков! Требуется минимум {MIN_PLAYERS}. Сейчас подключено: {player_count}.")
        return

    remove_active_session(message.chat.id)
    print(f"Removed session {message.chat.id} from active sessions")

    await group_state.set_state(GameyStates.Role)
    await message.reply("Игра началась! Роли распределены, ночь наступила.")