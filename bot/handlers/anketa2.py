from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa2_kb import goal1_kb, goal2_kb, future_kb, yesno_kb, mentor_kb
from database import db_manager

class SecondAnketaState(BaseStateGroup):
    GOAL = "goal"
    GOAL_DREAM = "goal_dream"
    FUTURE = "future"
    ERRORS = "errors"
    RESPONSIBILITY = "responsibility"
    BALANCE = "balance"
    MENTOR = "mentor"

anketa2_labeler = BotLabeler()


@anketa2_labeler.message(text="анкета2")
async def anketa2_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa2"):
        await message.answer("Вы уже прошли анкету")
        return


    await message.answer("Раздел 3. Мечта и путь к ней", keyboard=empty_kb)
    await message.answer("1. Есть ли у тебя высшая цель – то, ради чего ты хочешь жить и трудиться?", keyboard=goal1_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.GOAL)


@anketa2_labeler.message(state=SecondAnketaState.GOAL)
async def goal_process(message: Message):
    ctx_storage.set("goal", message.text.strip())
    await message.answer("2. Что важнее: цель или мечта?", keyboard=goal2_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.GOAL_DREAM)


@anketa2_labeler.message(state=SecondAnketaState.GOAL_DREAM)
async def goal_dream_process(message: Message):
    ctx_storage.set("goal_dream", message.text.strip())
    await message.answer("3. Твое отношение к будущему:", keyboard=future_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.FUTURE)


@anketa2_labeler.message(state=SecondAnketaState.FUTURE)
async def future_process(message: Message):
    ctx_storage.set("future", message.text.strip())
    await message.answer("4. Помогают ли человеку ошибки двигаться к цели?", keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.ERRORS)


@anketa2_labeler.message(state=SecondAnketaState.ERRORS)
async def errors_process(message: Message):
    ctx_storage.set("errors", message.text.strip())
    await message.answer("5. Согласен ли ты, что человек сам несет 100%-ную ответственность за свое счастье?",
                         keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.RESPONSIBILITY)


@anketa2_labeler.message(state=SecondAnketaState.RESPONSIBILITY)
async def responsibility_process(message: Message):
    ctx_storage.set("responsibility", message.text.strip())
    await message.answer(
        "6. Чтобы быть счастливым, человеку нужно создать баланс и уделять одинаковое внимание разным сферам своей жизни?",
        keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.BALANCE)


@anketa2_labeler.message(state=SecondAnketaState.BALANCE)
async def balance_process(message: Message):
    ctx_storage.set("balance", message.text.strip())
    await message.answer("7. Есть ли на свете тот, кто достиг уже твоей мечты, и может тебе помочь?",
                         keyboard=mentor_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.MENTOR)


@anketa2_labeler.message(state=SecondAnketaState.MENTOR)
async def mentor_process(message: Message):
    mentor = message.text.strip()
    ctx_storage.set("mentor", mentor)

    anketa_data = {
        "goal": ctx_storage.get("goal"),
        "goal_dream": ctx_storage.get("goal_dream"),
        "future": ctx_storage.get("future"),
        "errors": ctx_storage.get("errors"),
        "responsibility": ctx_storage.get("responsibility"),
        "balance": ctx_storage.get("balance"),
        "mentor": mentor
    }

    await db_manager.save_anketa(
        peer_id=message.peer_id,
        anketa_type="anketa2",
        data=anketa_data
    )

    user_anketa = await db_manager.get_anketa_data(
        peer_id=message.peer_id,
        anketa_type="anketa2"
    )

    result = f"""✓ Анкета успешно заполнена!

    Раздел 3. Мечта и путь к ней:
    • Высшая цель: {user_anketa['goal']}
    • Цель/мечта: {user_anketa['goal_dream']}
    • Отношение к будущему: {user_anketa['future']}
    • Ошибки: {user_anketa['errors']}
    • Ответственность: {user_anketa['responsibility']}
    • Баланс: {user_anketa['balance']}
    • Ментор: {user_anketa['mentor']}"""

    await message.answer(result, keyboard=empty_kb)
    await state_dispanser.delete(message.peer_id)

