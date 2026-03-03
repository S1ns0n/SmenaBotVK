from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa2_kb import goal1_kb, goal2_kb, future_kb, yesno_kb, mentor_kb
from database import db_manager
from bot.handlers.anketa3 import anketa3_start
from bot.utils import remove_brackets_text


anketa2_labeler = BotLabeler()
class SecondAnketaState(BaseStateGroup):
    GOAL = "goal"
    GOAL_DREAM = "goal_dream"
    FUTURE = "future"
    ERRORS = "errors"
    RESPONSIBILITY = "responsibility"
    BALANCE = "balance"
    MENTOR = "mentor"


QUESTIONS_SECTION2 = {
    SecondAnketaState.GOAL: "Есть ли у тебя высшая цель – то, ради чего ты хочешь жить и трудиться? [да 3 балла, нет 0 баллов, затрудняюсь ответить 1 балл]",
    SecondAnketaState.GOAL_DREAM: "Что важнее: цель или мечта? [цель 2 балла, мечта 3 балла, затрудняюсь ответить 1 балл, это одно и то же 0 баллов]",
    SecondAnketaState.FUTURE: "Твое отношение к будущему: [надеюсь, что все как-нибудь само собой устроится 1 балл, я немного боюсь неизвестности и предпочитаю, чтобы все шло предсказуемо 2 балла, я вижу будущее как поле для возможностей, где я сам могу создавать свою реальность 5 баллов]",
    SecondAnketaState.ERRORS: "Помогают ли человеку ошибки двигаться к цели? [да 3 балла, нет 0 баллов, затрудняюсь ответить 1 балл]",
    SecondAnketaState.RESPONSIBILITY: "Согласен ли ты, что человек сам несет 100%-ную ответственность за свое счастье? [да 3 балла, нет 1 балл, затрудняюсь ответить 0 баллов]",
    SecondAnketaState.BALANCE: "Чтобы быть счастливым, человеку нужно создать баланс и уделять одинаковое внимание разным сферам своей жизни? [да 3 балла, нет 1 балл, затрудняюсь ответить 0 баллов]",
    SecondAnketaState.MENTOR: "Есть ли на свете тот, кто достиг уже твоей мечты, и может тебе помочь? [да, я уже у него учусь 3 балла, да, но он не может мне помочь 0 баллов, нет 1 балл]"
}


@anketa2_labeler.message(text="анкета2")
async def anketa2_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa2"):
        await message.answer("Вы уже прошли анкету")
        return

    await message.answer("Раздел 3. Мечта и путь к ней", keyboard=empty_kb)
    await message.answer("1. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.GOAL]), keyboard=goal1_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.GOAL)


@anketa2_labeler.message(state=SecondAnketaState.GOAL)
async def goal_process(message: Message):
    ctx_storage.set(SecondAnketaState.GOAL, message.text.strip())
    await message.answer("2. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.GOAL_DREAM]), keyboard=goal2_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.GOAL_DREAM)


@anketa2_labeler.message(state=SecondAnketaState.GOAL_DREAM)
async def goal_dream_process(message: Message):
    ctx_storage.set(SecondAnketaState.GOAL_DREAM, message.text.strip())
    await message.answer("3. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.FUTURE]), keyboard=future_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.FUTURE)


@anketa2_labeler.message(state=SecondAnketaState.FUTURE)
async def future_process(message: Message):
    ctx_storage.set(SecondAnketaState.FUTURE, message.text.strip())
    await message.answer("4. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.ERRORS]), keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.ERRORS)


@anketa2_labeler.message(state=SecondAnketaState.ERRORS)
async def errors_process(message: Message):
    ctx_storage.set(SecondAnketaState.ERRORS, message.text.strip())
    await message.answer("5. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.RESPONSIBILITY]), keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.RESPONSIBILITY)


@anketa2_labeler.message(state=SecondAnketaState.RESPONSIBILITY)
async def responsibility_process(message: Message):
    ctx_storage.set(SecondAnketaState.RESPONSIBILITY, message.text.strip())
    await message.answer("6. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.BALANCE]), keyboard=yesno_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.BALANCE)


@anketa2_labeler.message(state=SecondAnketaState.BALANCE)
async def balance_process(message: Message):
    ctx_storage.set(SecondAnketaState.BALANCE, message.text.strip())
    await message.answer("7. " + remove_brackets_text(QUESTIONS_SECTION2[SecondAnketaState.MENTOR]), keyboard=mentor_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.MENTOR)


@anketa2_labeler.message(state=SecondAnketaState.MENTOR)
async def mentor_process(message: Message):
    mentor = message.text.strip()
    ctx_storage.set(SecondAnketaState.MENTOR, mentor)

    anketa_data = {
        QUESTIONS_SECTION2[SecondAnketaState.GOAL]: ctx_storage.get(SecondAnketaState.GOAL),
        QUESTIONS_SECTION2[SecondAnketaState.GOAL_DREAM]: ctx_storage.get(SecondAnketaState.GOAL_DREAM),
        QUESTIONS_SECTION2[SecondAnketaState.FUTURE]: ctx_storage.get(SecondAnketaState.FUTURE),
        QUESTIONS_SECTION2[SecondAnketaState.ERRORS]: ctx_storage.get(SecondAnketaState.ERRORS),
        QUESTIONS_SECTION2[SecondAnketaState.RESPONSIBILITY]: ctx_storage.get(SecondAnketaState.RESPONSIBILITY),
        QUESTIONS_SECTION2[SecondAnketaState.BALANCE]: ctx_storage.get(SecondAnketaState.BALANCE),
        QUESTIONS_SECTION2[SecondAnketaState.MENTOR]: mentor
    }

    await db_manager.save_anketa(peer_id=message.peer_id, anketa_type="anketa2", data=anketa_data)
    await state_dispanser.delete(message.peer_id)
    await anketa3_start(message=message)

