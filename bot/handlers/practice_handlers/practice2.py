from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.practice1_kb import create_scale_keyboard
from bot.keyboards.anketa3_kb import create_numbered_keyboard
from database import db_manager


practice2_labeler = BotLabeler()


class Practice2State(BaseStateGroup):
    DREAM_DEFINED = "dream_defined"
    FUTURE_VISION = "future_vision"
    FORMULA_IMPL = "formula_impl"
    WORLDVIEW_CHANGED = "worldview_changed"
    KNOWLEDGE_SHARE = "knowledge_share"
    CLARITY = "clarity"
    USEFULNESS = "usefulness"
    INTEREST = "interest"
    DEPTH = "depth"
    TRAINER = "trainer"
    MISSING = "missing"


QUESTIONS_PRACTICE2 = {
    Practice2State.DREAM_DEFINED: "Определил ли ты в процессе тренинга свою мечту?\n1) да\n2) у меня была мечта, но я ее детальнее проработал\n3) нет\n4) затрудняюсь ответить",
    Practice2State.FUTURE_VISION: "Обрел ли ты четкий образ желаемого будущего состояния счастья или сильное чувство направления, куда хочешь двигаться?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice2State.FORMULA_IMPL: "Запомнил и внедрил ли ты в свою жизнь все 4 основы и 7 ключей Формулы?\n1) да\n2) заполнил, но не внедрил\n3) нет\n4) затрудняюсь ответить",
    Practice2State.WORLDVIEW_CHANGED: "Изменились ли некоторые твои взгляды на мир и на себя самого?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice2State.KNOWLEDGE_SHARE: "Обрел ли ты важное знание, которым хочешь поделиться с друзьями и близкими?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice2State.CLARITY: "Оцени понятность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice2State.USEFULNESS: "Оцени полезность тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice2State.INTEREST: "Оцени интересность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice2State.DEPTH: "Оцени глубину задач и практик тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice2State.TRAINER: "Оцени насколько убедительными и помогающими в тренинге были тренер и вдохновители по 10-балльной шкале, где 10 – самый высокий балл",
    Practice2State.MISSING: "Чего тебе не хватило в тренинге? (Если все было ок, поставь -)",
}


async def practice2_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="practice2"):
        await message.answer("Вы уже прошли эту анкету")
        return

    await message.answer("Тренинг «Формула мечты»", keyboard=empty_kb)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.DREAM_DEFINED], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, Practice2State.DREAM_DEFINED)


@practice2_labeler.message(state=Practice2State.DREAM_DEFINED)
async def q1_process(message: Message):
    # Валидация выбора 1-4
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 4):
        await message.answer("Пожалуйста, выбери номер от 1 до 4", keyboard=await create_numbered_keyboard(4))
        return
    ctx_storage.set(Practice2State.DREAM_DEFINED, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.FUTURE_VISION], keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice2State.FUTURE_VISION)


@practice2_labeler.message(state=Practice2State.FUTURE_VISION)
async def q2_process(message: Message):
    # Валидация выбора 1-3
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3", keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice2State.FUTURE_VISION, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.FORMULA_IMPL], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, Practice2State.FORMULA_IMPL)


@practice2_labeler.message(state=Practice2State.FORMULA_IMPL)
async def q3_process(message: Message):
    # Валидация выбора 1-4
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 4):
        await message.answer("Пожалуйста, выбери номер от 1 до 4", keyboard=await create_numbered_keyboard(4))
        return
    ctx_storage.set(Practice2State.FORMULA_IMPL, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.WORLDVIEW_CHANGED], keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice2State.WORLDVIEW_CHANGED)


@practice2_labeler.message(state=Practice2State.WORLDVIEW_CHANGED)
async def q4_process(message: Message):
    # Валидация выбора 1-3
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3", keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice2State.WORLDVIEW_CHANGED, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.KNOWLEDGE_SHARE], keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice2State.KNOWLEDGE_SHARE)


@practice2_labeler.message(state=Practice2State.KNOWLEDGE_SHARE)
async def q5_process(message: Message):
    # Валидация выбора 1-3
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3", keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice2State.KNOWLEDGE_SHARE, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.CLARITY], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice2State.CLARITY)


@practice2_labeler.message(state=Practice2State.CLARITY)
async def q6_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice2State.CLARITY, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.USEFULNESS], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice2State.USEFULNESS)


@practice2_labeler.message(state=Practice2State.USEFULNESS)
async def q7_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice2State.USEFULNESS, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.INTEREST], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice2State.INTEREST)


@practice2_labeler.message(state=Practice2State.INTEREST)
async def q8_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice2State.INTEREST, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.DEPTH], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice2State.DEPTH)


@practice2_labeler.message(state=Practice2State.DEPTH)
async def q9_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice2State.DEPTH, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.TRAINER], keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice2State.TRAINER)


@practice2_labeler.message(state=Practice2State.TRAINER)
async def q10_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10", keyboard=await create_scale_keyboard())
        return

    ctx_storage.set(Practice2State.TRAINER, text)
    await message.answer(QUESTIONS_PRACTICE2[Practice2State.MISSING], keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice2State.MISSING)


@practice2_labeler.message(state=Practice2State.MISSING)
async def q11_process(message: Message):
    ctx_storage.set(Practice2State.MISSING, message.text.strip())

    answers_data = {
        QUESTIONS_PRACTICE2[Practice2State.DREAM_DEFINED]: ctx_storage.get(Practice2State.DREAM_DEFINED),
        QUESTIONS_PRACTICE2[Practice2State.FUTURE_VISION]: ctx_storage.get(Practice2State.FUTURE_VISION),
        QUESTIONS_PRACTICE2[Practice2State.FORMULA_IMPL]: ctx_storage.get(Practice2State.FORMULA_IMPL),
        QUESTIONS_PRACTICE2[Practice2State.WORLDVIEW_CHANGED]: ctx_storage.get(Practice2State.WORLDVIEW_CHANGED),
        QUESTIONS_PRACTICE2[Practice2State.KNOWLEDGE_SHARE]: ctx_storage.get(Practice2State.KNOWLEDGE_SHARE),
        QUESTIONS_PRACTICE2[Practice2State.CLARITY]: ctx_storage.get(Practice2State.CLARITY),
        QUESTIONS_PRACTICE2[Practice2State.USEFULNESS]: ctx_storage.get(Practice2State.USEFULNESS),
        QUESTIONS_PRACTICE2[Practice2State.INTEREST]: ctx_storage.get(Practice2State.INTEREST),
        QUESTIONS_PRACTICE2[Practice2State.DEPTH]: ctx_storage.get(Practice2State.DEPTH),
        QUESTIONS_PRACTICE2[Practice2State.TRAINER]: ctx_storage.get(Practice2State.TRAINER),
        QUESTIONS_PRACTICE2[Practice2State.MISSING]: ctx_storage.get(Practice2State.MISSING),
    }

    await db_manager.save_anketa(
        peer_id=message.peer_id,
        anketa_type="practice2",
        data=answers_data
    )

    await message.answer("Спасибо!", keyboard=empty_kb)
    await state_dispanser.delete(peer_id=message.peer_id)
