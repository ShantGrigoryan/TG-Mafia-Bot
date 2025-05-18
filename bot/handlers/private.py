from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from bot.states.game import GameStates
from bot.utils.session_manager import get_active_sessions

router = Router()

async def is_private_chat(message: Message) -> bool:
    return message.chat.type == "private"

@router.message(CommandStart(), is_private_chat)
async def cmd_start_private(message: Message, state: FSMContext):
    print(f"Processing /start from user {message.from_user.id}")
    
    active_sessions = get_active_sessions()
    print(f"Active sessions (type: {type(active_sessions)}, value: {active_sessions})")

    if not active_sessions:
        print("No active sessions found")
        await message.answer("На данный момент нет активной игры. Ожидайте начала игры в группе!")
        return

    storage = state.storage
    active_session = None
    for chat_id in active_sessions:
        group_state = FSMContext(storage=storage, key=(chat_id, chat_id))
        current_state = await group_state.get_state()
        print(f"Checking chat {chat_id}, state: {current_state}")
        if current_state == GameStates.WAITING_FOR_PLAYERS.state:
            active_session = await group_state.get_data()
            active_session["chat_id"] = chat_id
            break

    if not active_session:
        print("No session in WAITING_FOR_PLAYERS state")
        await message.answer("На данный момент нет активной игры. Ожидайте начала игры в группе!")
        return

    chat_id = active_session["chat_id"]
    group_state = FSMContext(storage=storage, key=(chat_id, chat_id))
    data = await group_state.get_data()

    players = data.get("players", [])
    print(f"Current players: {players}")

    player_id = message.from_user.id
    if player_id in players:
        print(f"User {player_id} already joined")
        await message.answer("Вы уже подключились к игре!")
        return

    players.append(player_id)
    await group_state.update_data(players=players)
    updated_data = await group_state.get_data()
    print(f"Updated data after adding player: {updated_data}")

    await message.answer("Вы подключились к игре. Ожидайте старта.")