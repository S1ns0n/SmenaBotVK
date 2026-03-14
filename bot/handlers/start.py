import asyncio
from bot.labeler_config import labeler
from vkbottle.bot import Message
from database import db_manager, exporter
from bot.handlers.anketa1 import anketa1_start
from bot.utils import get_random_text
from bot.texts import reminder, greetings
from bot.keyboards import empty_kb
from ai import analyzer
from bot.uploaders import photo_uploader
from config import Config




@labeler.message(text=["/start", "Начать"])
async def start_anketas(message: Message):
    photo = await photo_uploader.upload(
        file_source=str(Config.START_IMAGE),
        peer_id=message.peer_id,
    )
    await message.answer(get_random_text(greetings), attachment=photo)
    await anketa1_start(message=message)

@labeler.message(text="анализ")
async def analyze(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    anketa_data = await db_manager.get_anketa_data(message.peer_id, "anketa1")
    if anketa_data is None:
        await message.answer("Нет анкеты для анализа")
        return

    await message.answer("Анализирую ваши анкеты...")
    result = await analyzer.analyze_peer_anketas(message.peer_id, anketa_data)
    photo = await photo_uploader.upload(
        file_source=str(Config.AI_IMAGE),
        peer_id=message.peer_id,
    )

    await message.answer(result, attachment=photo)

@labeler.message(text="команды")
async def commands(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    mes = ("Начать - начать сценарий треннинга (команда для всех)\n"
           "проверка - получить список всех пользователей\n"
           "напомнить - начать рассылку тренингов\n"
           "экспорт - начать выгрузку в гугл таблицы")

    await message.answer(mes)

@labeler.message(text="экспорт")
async def export_users_data(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    detailed_url = await exporter.export_to_google_sheets(detailed=False)



    await message.answer(detailed_url)


