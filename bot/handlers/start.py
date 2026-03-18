import asyncio
from bot.labeler_config import labeler
from vkbottle.bot import Message
from database import db_manager, exporter
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
    users_with_practice1 = await db_manager.get_users_with_specific_anketas({"practice1"})
    users_with_practice2 = await db_manager.get_users_with_specific_anketas({"practice2"})
    users_with_practice3_1 = await db_manager.get_users_with_specific_anketas({"practice3_1"})
    users_with_practice3_2 = await db_manager.get_users_with_specific_anketas({"practice3_2"})
    await message.answer(f"Всего прошло анкету по тренингам: {len(users_with_practice1) + len(users_with_practice2) + len(users_with_practice3_1) + len(users_with_practice3_2)}")
    await message.answer(all_users)

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

@labeler.message(text="напомнить")
async def send_all_message(message: Message):
    if message.peer_id != int(Config.ADMIN_PEER_ID):
        return

    all_users = await db_manager.get_all_users()
    print(all_users)
    success = 0
    errors = 0

    for user_id in all_users:
        try:
            await message.ctx_api.messages.send(
                peer_id=user_id,
                message="""Друзья!

Мы знаем, что именно из ваших идей и смелых фантазий рождаются самые крутые проекты. Но чтобы наши общие мечты превращались в реальность, нам нужна ваша обратная связь!

Если вы еще не успели поделиться своими мыслями, сейчас самое время. Нам важно услышать голос каждого Мечтателя. Ваши ответы помогут нам понять, куда двигаться дальше и как сделать наше пространство еще лучше.

ссылка на выходную анкету:
https://forms.yandex.ru/cloud/69b8016695add5bd9218dcf5

Пройдите анкету, это займет всего 5-7 минут, но подарит нам бесценный материал для размышлений.""",
                random_id=0
            )
            success += 1
            await db_manager.select_status_for_user(user_id, "sended_practice")
            await asyncio.sleep(0.3)
        except Exception as e:
            errors += 1
            print(f"Ошибка для {user_id}: {e}")

    await message.answer(f"Анкеты разосланы: {success} успешно, {errors} ошибок")

