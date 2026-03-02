from bot.labeler_config import labeler
from vkbottle.bot import Message
from database import db_manager
from ai import analyzer


@labeler.message(text="очистка")
async def clear_all_anktets(message: Message):
    await db_manager.delete_user_anketas(peer_id=message.peer_id)
    await message.answer("Очищено!")
@labeler.message(text="анализ")
async def analyze(message: Message):
    await message.answer("Анализирую ваши анкеты...")

    result = await analyzer.analyze_peer_anketas(message.peer_id)
    await message.answer(result)