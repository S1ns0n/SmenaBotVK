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
from bot.handlers.practice_handlers.what_your_practice_anketa import practice_anketa_start



anketa_handlers = {
    "anketa0": anketa0_start,
    "anketa1": anketa1_start,
    "anketa2": anketa2_start,
    "anketa3": anketa3_start
}

@labeler.message(text=["/start", "Начать"])
async def start_anketas(message: Message):
    await practice_anketa_start(message)


@labeler.message(text="напомнить")
async def send_all_message(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass

    all_users = await db_manager.get_users_without_all_anketas({"anketa0", "anketa1", "anketa2", "anketa3"})
    success = 0

    for user_id in all_users:
        try:
            await message.ctx_api.messages.send(
                peer_id=user_id,
                message=get_random_text(reminder),
                random_id=0
            )
            success += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"Ошибка для {user_id}: {e}")

    await message.answer(f"Напоминания разосланы {success} пользователям!")
