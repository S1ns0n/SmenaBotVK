from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.practice1_kb import create_scale_keyboard
from database import db_manager

practice1_labeler = BotLabeler()


class Practice1State(BaseStateGroup):
    DIRECTIONS = "directions"
    EFFECTS = "effects"
    GROUPS = "groups"
    RANKING = "ranking"
    CLARITY = "clarity"
    USEFULNESS = "usefulness"
    INTEREST = "interest"
    DEPTH = "depth"
    TRAINER = "trainer"
    MISSING = "missing"


QUESTIONS_PRACTICE1 = {
    Practice1State.DIRECTIONS: "1. Какие перспективные направления деятельности ты теперь видишь для себя? (перечисли не менее 3)",
    Practice1State.EFFECTS: "2. Какие эффекты (не менее 3) ты хочешь создавать своим трудом?",
    Practice1State.GROUPS: "3. На какие группы людей и живых существ тебе хотелось бы влиять теперь? (не менее 5)",
    Practice1State.RANKING: "4. Что теперь для тебя важно: расставь факторы, которые влияют на успех в карьере ОТ МЕНЕЕ значимого К БОЛЕЕ значимому:\n1) Связи\n2) Удача\n3) Сочетание твердых знаний, железной воли и верности своим ценностям\n4) Диплом престижного вуза\n5) Деньги\n6) Гибкость, умение подстроиться под систему\n7) Усердный труд\n8) Лидерские качества",
    Practice1State.CLARITY: "5. Оцени понятность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice1State.USEFULNESS: "6. Оцени полезность тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice1State.INTEREST: "7. Оцени интересность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice1State.DEPTH: "8. Оцени глубину задач и практик тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice1State.TRAINER: "9. Оцени насколько убедительными и помогающими в тренинге были тренер и вдохновители по 10-балльной шкале, где 10 – самый высокий балл",
    Practice1State.MISSING: "10. Чего тебе не хватило в тренинге? (Если все было ок, поставь -)",
}




async def practice1_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="practice1"):
        await message.answer("Вы уже прошли эту анкету")
        return

    await message.answer(QUESTIONS_PRACTICE1[Practice1State.DIRECTIONS], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice1State.DIRECTIONS)


@practice1_labeler.message(state=Practice1State.DIRECTIONS)
async def q1_process(message: Message):
    ctx_storage.set(Practice1State.DIRECTIONS, message.text.strip())
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.EFFECTS], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice1State.EFFECTS)


@practice1_labeler.message(state=Practice1State.EFFECTS)
async def q2_process(message: Message):
    ctx_storage.set(Practice1State.EFFECTS, message.text.strip())
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.GROUPS], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice1State.GROUPS)


@practice1_labeler.message(state=Practice1State.GROUPS)
async def q3_process(message: Message):
    ctx_storage.set(Practice1State.GROUPS, message.text.strip())
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.RANKING], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice1State.RANKING)


@practice1_labeler.message(state=Practice1State.RANKING)
async def q4_process(message: Message):
    ctx_storage.set(Practice1State.RANKING, message.text.strip())
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.CLARITY], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice1State.CLARITY)


@practice1_labeler.message(state=Practice1State.CLARITY)
async def q5_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice1State.CLARITY, text)
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.USEFULNESS], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice1State.USEFULNESS)


@practice1_labeler.message(state=Practice1State.USEFULNESS)
async def q6_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice1State.USEFULNESS, text)
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.INTEREST], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice1State.INTEREST)


@practice1_labeler.message(state=Practice1State.INTEREST)
async def q7_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice1State.INTEREST, text)
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.DEPTH], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice1State.DEPTH)


@practice1_labeler.message(state=Practice1State.DEPTH)
async def q8_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice1State.DEPTH, text)
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.TRAINER], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice1State.TRAINER)


@practice1_labeler.message(state=Practice1State.TRAINER)
async def q9_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice1State.TRAINER, text)
    await message.answer(QUESTIONS_PRACTICE1[Practice1State.MISSING], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice1State.MISSING)


@practice1_labeler.message(state=Practice1State.MISSING)
async def q10_process(message: Message):
    ctx_storage.set(Practice1State.MISSING, message.text.strip())

    answers_data = {
        QUESTIONS_PRACTICE1[Practice1State.DIRECTIONS]: ctx_storage.get(Practice1State.DIRECTIONS),
        QUESTIONS_PRACTICE1[Practice1State.EFFECTS]: ctx_storage.get(Practice1State.EFFECTS),
        QUESTIONS_PRACTICE1[Practice1State.GROUPS]: ctx_storage.get(Practice1State.GROUPS),
        QUESTIONS_PRACTICE1[Practice1State.RANKING]: ctx_storage.get(Practice1State.RANKING),
        QUESTIONS_PRACTICE1[Practice1State.CLARITY]: ctx_storage.get(Practice1State.CLARITY),
        QUESTIONS_PRACTICE1[Practice1State.USEFULNESS]: ctx_storage.get(Practice1State.USEFULNESS),
        QUESTIONS_PRACTICE1[Practice1State.INTEREST]: ctx_storage.get(Practice1State.INTEREST),
        QUESTIONS_PRACTICE1[Practice1State.DEPTH]: ctx_storage.get(Practice1State.DEPTH),
        QUESTIONS_PRACTICE1[Practice1State.TRAINER]: ctx_storage.get(Practice1State.TRAINER),
        QUESTIONS_PRACTICE1[Practice1State.MISSING]: ctx_storage.get(Practice1State.MISSING),
    }

    await db_manager.save_anketa(
        peer_id=message.peer_id,
        anketa_type="practice1",
        data=answers_data
    )

    await message.answer("Спасибо!", keyboard=empty_kb)
    await state_dispanser.delete(message.peer_id)