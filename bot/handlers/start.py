import asyncio
from bot.labeler_config import labeler
from vkbottle.bot import Message
from database import db_manager
from ai import analyzer
from bot.handlers.anketa0 import anketa0_start
from bot.handlers.anketa1 import anketa1_start
from bot.handlers.anketa2 import anketa2_start
from bot.handlers.anketa3 import anketa3_start
from bot.utils import get_random_text
from bot.texts import greetings, yout_anketas_done, reminder
from config import Config
from bot.uploaders import photo_uploader



anketa_handlers = {
    "anketa0": anketa0_start,
    "anketa1": anketa1_start,
    "anketa2": anketa2_start,
    "anketa3": anketa3_start
}

@labeler.message(text=["/start", "Начать"])
async def start_anketas(message: Message):
    all_user_anketas = await db_manager.get_user_anketa_types(message.peer_id)
    print(all_user_anketas)

    for anketa_name, handler in anketa_handlers.items():
        if anketa_name not in all_user_anketas:
            photo = await photo_uploader.upload(
                file_source=str(Config.START_IMAGE),
                peer_id=message.peer_id,
            )
            await message.answer(get_random_text(greetings), attachment=photo)
            await handler(message)
            return

    await message.answer(get_random_text(yout_anketas_done))


@labeler.message(text="очистка")
async def clear_all_anktets(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass
    await db_manager.delete_user_anketas(peer_id=message.peer_id)
    await message.answer("Очищено!")
@labeler.message(text="анализ")
async def analyze(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass
    await message.answer("Анализирую ваши анкеты...")
    result = await analyzer.analyze_peer_anketas(message.peer_id)
    await db_manager.save_ai_answer(peer_id=message.peer_id, ai_answer_type="first_anketas", ai_answer=result)
    await message.answer(result)

@labeler.message(text="анализ прошедших")
async def analyze_all(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass
    checked = 0

    users = await db_manager.get_users_with_specific_anketas({"anketa0", "anketa1", "anketa2", "anketa3"})
    mes = await message.answer(f"Начал анализ прошедних...\nУже проверил: {checked} из {len(users)}")
    for user in users:

        result = await analyzer.analyze_peer_anketas(user)
        await db_manager.save_ai_answer(peer_id=user, ai_answer_type="first_anketas", ai_answer=result)
        checked = checked+1
        await message.ctx_api.messages.edit(
            peer_id=message.peer_id,
            message_id=mes.message_id,
            message=f"Начал анализ прошедних...\n уже проверил: {checked} из {len(users)}"
        )

    await message.answer("Проверка окончена!")


@labeler.message(text="прошедшие")
async def get_all_users_with_all_anketas(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass

    users = await db_manager.get_users_with_specific_anketas({"anketa0", "anketa1", "anketa2", "anketa3"})
    await message.answer(users)
    await message.answer(len(users))

@labeler.message(text="рассылка прошедшим")
async def send_ai_answers_all_users(message: Message):
    if message.peer_id != Config.ADMIN_PEER_ID:
        pass

    users = await db_manager.get_users_with_specific_anketas({"first_anketas"})
    success = 0

    for user_id in users:
        try:
            await message.ctx_api.messages.send(
                peer_id=user_id,
                message=await db_manager.get_anketa_data(peer_id=user_id, anketa_type="first_anketas"),
                random_id=0
            )
            success += 1
            await asyncio.sleep(0.3)
        except Exception as e:
            print(f"Ошибка для {user_id}: {e}")

    await message.answer(f"Ответы разосланы {success} пользователям!")

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
