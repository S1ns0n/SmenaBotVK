from bot.labeler_config import labeler, state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards.anketa0_kb import sex_kb
from bot.keyboards import empty_kb


class FirstAnketaState(BaseStateGroup):
    FIO = "fio"
    SEX = "sex"
    AGE = "age"
    SCHOOL = "school"


@labeler.message(text="анкета0")
async def start_handler(message: Message):
    await message.answer("Привет! Давай заполним анкету.\n\nРаздел 1. Персональные данные", keyboard=empty_kb)
    await message.answer("1. Укажите ваше полное ФИО")
    await state_dispanser.set(message.peer_id, FirstAnketaState.FIO)
    # проверка, проходил ли тип уже анкету и очистка state на всякий случай


@labeler.message(state=FirstAnketaState.FIO)
async def fio_process(message: Message):
    fio = message.text.strip()
    ctx_storage.set("fio", fio)
    await message.answer("2. Укажите ваш пол", keyboard=sex_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.SEX)


@labeler.message(state=FirstAnketaState.SEX)
async def sex_process(message: Message):
    sex = message.text.strip().lower()
    ctx_storage.set("sex", sex)
    await message.answer("3. Укажите ваш возраст", keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.AGE)


@labeler.message(state=FirstAnketaState.AGE)
async def age_process(message: Message):
    age = message.text.strip()
    ctx_storage.set("age", age)
    await message.answer("4. Укажите вашу школу, колледж или лицей")
    await state_dispanser.set(message.peer_id, FirstAnketaState.SCHOOL)


@labeler.message(state=FirstAnketaState.SCHOOL)
async def school_process(message: Message):
    school = message.text.strip()
    ctx_storage.set("school", school)

    # Собираем все данные анкеты
    anketa_data = {
        "fio": ctx_storage.get("fio"),
        "sex": ctx_storage.get("sex"),
        "age": ctx_storage.get("age"),
        "school": school
    }

    # Показываем итоговую анкету
    result = f"""✓ Анкета успешно заполнена!

Раздел 1. Персональные данные:
• ФИО: {anketa_data['fio']}
• Пол: {anketa_data['sex'].capitalize()}
• Возраст: {anketa_data['age']} лет  
• Образование: {anketa_data['school']}"""

    await message.answer(result)

    # Сбрасываем состояние и данные
    await state_dispanser.delete(message.peer_id)
