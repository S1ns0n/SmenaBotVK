import asyncio
from bot.labeler_config import labeler
from vkbottle.bot import Message
from database import db_manager
from bot.handlers.anketa0 import anketa0_start
from bot.handlers.anketa1 import anketa1_start
from bot.handlers.anketa2 import anketa2_start
from bot.handlers.anketa3 import anketa3_start
from bot.utils import get_random_text
from bot.texts import reminder
from config import Config
from bot.handlers.practice_handlers.what_your_practice_anketa import practice_anketa_start, send_practice_anketa



anketa_handlers = {
    "anketa0": anketa0_start,
    "anketa1": anketa1_start,
    "anketa2": anketa2_start,
    "anketa3": anketa3_start
}

@labeler.message(text=["/start", "Начать"])
async def start_anketas(message: Message):
    anketas = await db_manager.has_any_anketa_from_list(peer_id=message.peer_id,anketa_types={"practice1", "practice2", "practice3_1", "practice3_2"})
    if anketas:
        await practice_anketa_start(message)
    else:
        await message.answer("Ты уже завершил анкету!")

@labeler.message(text="проверка")
async def check(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    all_users = await db_manager.get_all_users()

    await message.answer(all_users)

@labeler.message(text="напомнить")
async def send_all_message(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    all_users = await db_manager.get_all_users()
    success = 0
    errors = 0

    for user_id in all_users:
        try:
            await send_practice_anketa(message.ctx_api, user_id)
            success += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            errors += 1
            print(f"Ошибка для {user_id}: {e}")

    await message.answer(f"Анкеты разосланы: {success} успешно, {errors} ошибок")

