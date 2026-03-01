import asyncio

from bot.labeler_config import labeler, state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards.anketa0_kb import sex_kb
from bot.keyboards import empty_kb
from database import db_manager


class ZeroAnketaState(BaseStateGroup):
    FIO = "fio"
    SEX = "sex"
    AGE = "age"
    SCHOOL = "school"


QUESTIONS_SECTION0 = {
    ZeroAnketaState.FIO: "Укажите ваше полное ФИО",
    ZeroAnketaState.SEX: "Укажите ваш пол (мужской/женский)",
    ZeroAnketaState.AGE: "Укажите ваш возраст",
    ZeroAnketaState.SCHOOL: "Укажите вашу школу, колледж или лицей"
}


@labeler.message(text="анкета0")
async def start_handler(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa0"):
        await message.answer("Вы уже прошли анкету")
        return

    await message.answer("Привет! Давай заполним анкету.\n\nРаздел 1. Персональные данные", keyboard=empty_kb)
    await message.answer("1. " + QUESTIONS_SECTION0[ZeroAnketaState.FIO])
    await state_dispanser.set(message.peer_id, ZeroAnketaState.FIO)


@labeler.message(state=ZeroAnketaState.FIO)
async def fio_process(message: Message):
    fio = message.text.strip()
    ctx_storage.set(ZeroAnketaState.FIO, fio)  # ✅ Ключ = состояние
    await message.answer("2. " + QUESTIONS_SECTION0[ZeroAnketaState.SEX], keyboard=sex_kb)
    await state_dispanser.set(message.peer_id, ZeroAnketaState.SEX)


@labeler.message(state=ZeroAnketaState.SEX)
async def sex_process(message: Message):
    sex = message.text.strip().lower()
    ctx_storage.set(ZeroAnketaState.SEX, sex)
    await message.answer("3. " + QUESTIONS_SECTION0[ZeroAnketaState.AGE], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, ZeroAnketaState.AGE)


@labeler.message(state=ZeroAnketaState.AGE)
async def age_process(message: Message):
    age = message.text.strip()
    ctx_storage.set(ZeroAnketaState.AGE, age)
    await message.answer("4. " + QUESTIONS_SECTION0[ZeroAnketaState.SCHOOL])
    await state_dispanser.set(message.peer_id, ZeroAnketaState.SCHOOL)


@labeler.message(state=ZeroAnketaState.SCHOOL)
async def school_process(message: Message):
    school = message.text.strip()
    ctx_storage.set(ZeroAnketaState.SCHOOL, school)

    # ✅ Вопросы = ключи в БД!
    anketa_data = {
        QUESTIONS_SECTION0[ZeroAnketaState.FIO]: ctx_storage.get(ZeroAnketaState.FIO),
        QUESTIONS_SECTION0[ZeroAnketaState.SEX]: ctx_storage.get(ZeroAnketaState.SEX),
        QUESTIONS_SECTION0[ZeroAnketaState.AGE]: ctx_storage.get(ZeroAnketaState.AGE),
        QUESTIONS_SECTION0[ZeroAnketaState.SCHOOL]: school
    }

    await db_manager.save_anketa(peer_id=message.peer_id, anketa_type="anketa0", data=anketa_data)

    user_anketa = await db_manager.get_anketa_data(peer_id=message.peer_id, anketa_type="anketa0")

    # ✅ Показываем с вопросами
    result = f"""✓ Анкета успешно заполнена!

Раздел 1. Персональные данные:
"""
    for question, answer in user_anketa.items():
        result += f"• {question}: {answer}\n"
    await message.answer(result)
    await state_dispanser.delete(message.peer_id)
