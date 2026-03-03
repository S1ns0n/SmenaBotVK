from bot.labeler_config import labeler
from vkbottle.bot import Message
from vkbottle.tools.formatting import Formatter
from database import db_manager
from ai import analyzer
from bot.handlers.anketa0 import anketa0_start
from bot.handlers.anketa1 import anketa1_start
from bot.handlers.anketa2 import anketa2_start
from bot.handlers.anketa3 import anketa3_start



anketa_handlers = {
    "anketa0": anketa0_start,
    "anketa1": anketa1_start,
    "anketa2": anketa2_start,
    "anketa3": anketa3_start
}

@labeler.message(text="/start")
async def start_anketas(message: Message):
    all_user_anketas = await db_manager.get_user_anketa_types(message.peer_id)
    print(all_user_anketas)

    for anketa_name, handler in anketa_handlers.items():
        if anketa_name not in all_user_anketas:
            await handler(message)
            return

    await message.answer("Вы прошли все анкеты!")


@labeler.message(text="анкета3")
async def special_start_anketa3(message:Message):
    await anketa3_start(message=message)

@labeler.message(text="очистка")
async def clear_all_anktets(message: Message):
    await db_manager.delete_user_anketas(peer_id=message.peer_id)
    await message.answer("Очищено!")
@labeler.message(text="анализ")
async def analyze(message: Message):
    await message.answer("Анализирую ваши анкеты...")
    result = await analyzer.analyze_peer_anketas(message.peer_id)
    await message.answer(result)