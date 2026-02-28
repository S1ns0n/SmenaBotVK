from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa2_kb import goal1_kb, goal2_kb, future_kb, yesno_kb, mentor_kb

class ThirdAnketaState(BaseStateGroup):
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
    await message.answer("Раздел 3. Мечта и путь к ней", keyboard=empty_kb)
    await message.answer("1. Есть ли у тебя высшая цель – то, ради чего ты хочешь жить и трудиться?", keyboard=goal1_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.GOAL)


@anketa2_labeler.message(state=ThirdAnketaState.GOAL)
async def goal_process(message: Message):
    ctx_storage.set("goal", message.text.strip())
    await message.answer("2. Что важнее: цель или мечта?", keyboard=goal2_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.GOAL_DREAM)


@anketa2_labeler.message(state=ThirdAnketaState.GOAL_DREAM)
async def goal_dream_process(message: Message):
    ctx_storage.set("goal_dream", message.text.strip())
    await message.answer("3. Твое отношение к будущему:", keyboard=future_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.FUTURE)


@anketa2_labeler.message(state=ThirdAnketaState.FUTURE)
async def future_process(message: Message):
    ctx_storage.set("future", message.text.strip())
    await message.answer("4. Помогают ли человеку ошибки двигаться к цели?", keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.ERRORS)


@anketa2_labeler.message(state=ThirdAnketaState.ERRORS)
async def errors_process(message: Message):
    ctx_storage.set("errors", message.text.strip())
    await message.answer("5. Согласен ли ты, что человек сам несет 100%-ную ответственность за свое счастье?",
                         keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.RESPONSIBILITY)


@anketa2_labeler.message(state=ThirdAnketaState.RESPONSIBILITY)
async def responsibility_process(message: Message):
    ctx_storage.set("responsibility", message.text.strip())
    await message.answer(
        "6. Чтобы быть счастливым, человеку нужно создать баланс и уделять одинаковое внимание разным сферам своей жизни?",
        keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.BALANCE)


@anketa2_labeler.message(state=ThirdAnketaState.BALANCE)
async def balance_process(message: Message):
    ctx_storage.set("balance", message.text.strip())
    await message.answer("7. Есть ли на свете тот, кто достиг уже твоей мечты, и может тебе помочь?",
                         keyboard=mentor_kb)
    await state_dispanser.set(message.peer_id, ThirdAnketaState.MENTOR)


@anketa2_labeler.message(state=ThirdAnketaState.MENTOR)
async def mentor_process(message: Message):
    ctx_storage.set("mentor", message.text.strip())

    # Итоговая анкета
    result = f"""✓ Раздел 3 заполнен!

Раздел 3. Мечта и путь к ней:
• Высшая цель: {ctx_storage.get("goal")}
• Цель/мечта: {ctx_storage.get("goal_dream")}
• Отношение к будущему: {ctx_storage.get("future")}
• Ошибки: {ctx_storage.get("errors")}
• Ответственность: {ctx_storage.get("responsibility")}
• Баланс: {ctx_storage.get("balance")}
• Ментор: {ctx_storage.get("mentor")}
"""

    await message.answer(result, keyboard=empty_kb)
    await state_dispanser.delete(message.peer_id)

