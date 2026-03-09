from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.practice1_kb import create_scale_keyboard
from bot.keyboards.anketa3_kb import create_numbered_keyboard
from bot.keyboards.practice3_theme_kb import theme_kb
from database import db_manager

practice3_labeler = BotLabeler()


class Practice3State(BaseStateGroup):
    # Выбор темы
    DREAM_THEME = "dream_theme"

    # 3.1 «На волнах мечты»
    DREAM_DEFINED = "dream_defined"
    FUTURE_VISION = "future_vision"
    WAVES_LISTENING = "waves_listening"
    WORLDVIEW_CHANGED = "worldview_changed"
    KNOWLEDGE_SHARE = "knowledge_share"
    CLARITY_DREAM = "clarity_dream"
    USEFULNESS_DREAM = "usefulness_dream"
    INTEREST_DREAM = "interest_dream"
    DEPTH_DREAM = "depth_dream"
    TRAINER_DREAM = "trainer_dream"
    MISSING_DREAM = "missing_dream"

    # 3.2 «Качества и ценности»
    VALUES_UNDERSTANDING = "values_understanding"
    NEW_QUALITIES = "new_qualities"
    PEERS_EXPANDED = "peers_expanded"
    IMPLEMENTATION_PLAN = "implementation_plan"
    WORLDVIEW_CHANGED_VALUES = "worldview_changed_values"
    KNOWLEDGE_SHARE_VALUES = "knowledge_share_values"
    CLARITY_VALUES = "clarity_values"
    USEFULNESS_VALUES = "usefulness_values"
    INTEREST_VALUES = "interest_values"
    DEPTH_VALUES = "depth_values"
    TRAINER_VALUES = "trainer_values"
    MISSING_VALUES = "missing_values"


# Вопросы 3.1 «На волнах мечты»
QUESTIONS_PRACTICE3_1 = {
    Practice3State.DREAM_DEFINED: "3.1. «На волнах мечты»\n\nОпределил ли ты в процессе тренинга свою мечту?\n1) да\n2) у меня была мечта, но я ее детальнее проработал\n3) нет\n4) затрудняюсь ответить",
    Practice3State.FUTURE_VISION: "Обрел ли ты четкий образ желаемого будущего состояния счастья или сильное чувство направления, куда хочешь двигаться?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice3State.WAVES_LISTENING: "Научился ли ты слушать «волны»?",
    Practice3State.WORLDVIEW_CHANGED: "Изменились ли некоторые твои взгляды на мир и на себя самого?",
    Practice3State.KNOWLEDGE_SHARE: "Обрел ли ты важное знание, которым хочешь поделиться с друзьями и близкими?",
    Practice3State.CLARITY_DREAM: "Оцени понятность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.USEFULNESS_DREAM: "Оцени полезность тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.INTEREST_DREAM: "Оцени интересность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.DEPTH_DREAM: "Оцени глубину задач и практик тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.TRAINER_DREAM: "Оцени насколько убедительными и помогающими в тренинге были тренер и вдохновители по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.MISSING_DREAM: "Чего тебе не хватило в тренинге? (Если все было ок, поставь -)",
}

# Вопросы 3.2 «Качества и ценности»
QUESTIONS_PRACTICE3_2 = {
    Practice3State.VALUES_UNDERSTANDING: "3.2. «Качества и ценности»\n\nИзменилось ли твое понимание своих ценностей и их значимости?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice3State.NEW_QUALITIES: "Открыл ли ты для себя новые личные качества, которых раньше в себе не замечал?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice3State.PEERS_EXPANDED: "Расширился ли твой круг единомышленников?\n1) да\n2) нет\n3) затрудняюсь ответить",
    Practice3State.IMPLEMENTATION_PLAN: "Получил ли ты четкий понятный план и навыки для реализации своих желаний?",
    Practice3State.WORLDVIEW_CHANGED_VALUES: "Изменились ли некоторые твои взгляды на мир и на себя самого?",
    Practice3State.KNOWLEDGE_SHARE_VALUES: "Обрел ли ты важное знание, которым хочешь поделиться с друзьями и близкими?",
    Practice3State.CLARITY_VALUES: "Оцени понятность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.USEFULNESS_VALUES: "Оцени полезность тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.INTEREST_VALUES: "Оцени интересность тренинга для тебя по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.DEPTH_VALUES: "Оцени глубину задач и практик тренинга по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.TRAINER_VALUES: "Оцени насколько убедительными и помогающими в тренинге были тренер и вдохновители по 10-балльной шкале, где 10 – самый высокий балл",
    Practice3State.MISSING_VALUES: "Чего тебе не хватило в тренинге? (Если все было ок, поставь -)",
}


async def practice3_start(message: Message):
    await message.answer(
        "Над какой темой ты работал на тренинге?",
        keyboard=theme_kb
    )
    await state_dispanser.set(message.peer_id, Practice3State.DREAM_THEME)


# Выбор темы
@practice3_labeler.message(state=Practice3State.DREAM_THEME)
async def theme_process(message: Message):
    text = message.text.strip()

    if text == "Мечта":
        await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.DREAM_DEFINED],
                             keyboard=await create_numbered_keyboard(4))
        await state_dispanser.set(message.peer_id, Practice3State.DREAM_DEFINED)
    elif text == "Качества и ценности":
        await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.VALUES_UNDERSTANDING],
                             keyboard=await create_numbered_keyboard(3))
        await state_dispanser.set(message.peer_id, Practice3State.VALUES_UNDERSTANDING)


# === 3.1 «На волнах мечты» ===
@practice3_labeler.message(state=Practice3State.DREAM_DEFINED)
async def q1_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 4):
        await message.answer("Пожалуйста, выбери номер от 1 до 4",
                             keyboard=await create_numbered_keyboard(4))
        return
    ctx_storage.set(Practice3State.DREAM_DEFINED, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.FUTURE_VISION],
                         keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice3State.FUTURE_VISION)


@practice3_labeler.message(state=Practice3State.FUTURE_VISION)
async def q2_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3",
                             keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice3State.FUTURE_VISION, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.WAVES_LISTENING],
                         keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.WAVES_LISTENING)


@practice3_labeler.message(state=Practice3State.WAVES_LISTENING)
async def q3_dream_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.WAVES_LISTENING, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.WORLDVIEW_CHANGED],
                         keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.WORLDVIEW_CHANGED)


@practice3_labeler.message(state=Practice3State.WORLDVIEW_CHANGED)
async def q4_dream_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.WORLDVIEW_CHANGED, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.KNOWLEDGE_SHARE],
                         keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.KNOWLEDGE_SHARE)


@practice3_labeler.message(state=Practice3State.KNOWLEDGE_SHARE)
async def q5_dream_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.KNOWLEDGE_SHARE, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.CLARITY_DREAM],
                         keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.CLARITY_DREAM)


# Оценки 3.1 (6-10)
@practice3_labeler.message(state=Practice3State.CLARITY_DREAM)
async def q6_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                             keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.CLARITY_DREAM, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.USEFULNESS_DREAM],
                         keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.USEFULNESS_DREAM)


@practice3_labeler.message(state=Practice3State.USEFULNESS_DREAM)
async def q7_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                             keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.USEFULNESS_DREAM, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.INTEREST_DREAM],
                         keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.INTEREST_DREAM)


@practice3_labeler.message(state=Practice3State.INTEREST_DREAM)
async def q8_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                             keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.INTEREST_DREAM, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.DEPTH_DREAM],
                         keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.DEPTH_DREAM)


@practice3_labeler.message(state=Practice3State.DEPTH_DREAM)
async def q9_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                             keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.DEPTH_DREAM, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.TRAINER_DREAM],
                         keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.TRAINER_DREAM)


@practice3_labeler.message(state=Practice3State.TRAINER_DREAM)
async def q10_dream_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.TRAINER_DREAM, text)
    await message.answer(QUESTIONS_PRACTICE3_1[Practice3State.MISSING_DREAM],
                        keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.MISSING_DREAM)


@practice3_labeler.message(state=Practice3State.MISSING_DREAM)
async def q11_dream_process(message: Message):
    ctx_storage.set(Practice3State.MISSING_DREAM, message.text.strip())

    answers_data = {
        "theme": "3.1. «На волнах мечты»",
        QUESTIONS_PRACTICE3_1[Practice3State.DREAM_DEFINED]: ctx_storage.get(Practice3State.DREAM_DEFINED),
        QUESTIONS_PRACTICE3_1[Practice3State.FUTURE_VISION]: ctx_storage.get(Practice3State.FUTURE_VISION),
        QUESTIONS_PRACTICE3_1[Practice3State.WAVES_LISTENING]: ctx_storage.get(Practice3State.WAVES_LISTENING),
        QUESTIONS_PRACTICE3_1[Practice3State.WORLDVIEW_CHANGED]: ctx_storage.get(Practice3State.WORLDVIEW_CHANGED),
        QUESTIONS_PRACTICE3_1[Practice3State.KNOWLEDGE_SHARE]: ctx_storage.get(Practice3State.KNOWLEDGE_SHARE),
        QUESTIONS_PRACTICE3_1[Practice3State.CLARITY_DREAM]: ctx_storage.get(Practice3State.CLARITY_DREAM),
        QUESTIONS_PRACTICE3_1[Practice3State.USEFULNESS_DREAM]: ctx_storage.get(Practice3State.USEFULNESS_DREAM),
        QUESTIONS_PRACTICE3_1[Practice3State.INTEREST_DREAM]: ctx_storage.get(Practice3State.INTEREST_DREAM),
        QUESTIONS_PRACTICE3_1[Practice3State.DEPTH_DREAM]: ctx_storage.get(Practice3State.DEPTH_DREAM),
        QUESTIONS_PRACTICE3_1[Practice3State.TRAINER_DREAM]: ctx_storage.get(Practice3State.TRAINER_DREAM),
        QUESTIONS_PRACTICE3_1[Practice3State.MISSING_DREAM]: ctx_storage.get(Practice3State.MISSING_DREAM),
    }

    await db_manager.save_anketa(
        peer_id=message.peer_id,
        anketa_type="practice3_1",
        data=answers_data
    )

    await message.answer("Спасибо!", keyboard=empty_kb)
    await state_dispanser.delete(peer_id=message.peer_id)


# === 3.2 «Качества и ценности» ===
@practice3_labeler.message(state=Practice3State.VALUES_UNDERSTANDING)
async def q1_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3",
                           keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice3State.VALUES_UNDERSTANDING, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.NEW_QUALITIES],
                        keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice3State.NEW_QUALITIES)


@practice3_labeler.message(state=Practice3State.NEW_QUALITIES)
async def q2_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3",
                           keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice3State.NEW_QUALITIES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.PEERS_EXPANDED],
                        keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, Practice3State.PEERS_EXPANDED)


@practice3_labeler.message(state=Practice3State.PEERS_EXPANDED)
async def q3_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 3):
        await message.answer("Пожалуйста, выбери номер от 1 до 3",
                           keyboard=await create_numbered_keyboard(3))
        return
    ctx_storage.set(Practice3State.PEERS_EXPANDED, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.IMPLEMENTATION_PLAN],
                        keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.IMPLEMENTATION_PLAN)


@practice3_labeler.message(state=Practice3State.IMPLEMENTATION_PLAN)
async def q4_values_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.IMPLEMENTATION_PLAN, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.WORLDVIEW_CHANGED_VALUES],
                        keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.WORLDVIEW_CHANGED_VALUES)


@practice3_labeler.message(state=Practice3State.WORLDVIEW_CHANGED_VALUES)
async def q5_values_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.WORLDVIEW_CHANGED_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.KNOWLEDGE_SHARE_VALUES],
                        keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.KNOWLEDGE_SHARE_VALUES)


@practice3_labeler.message(state=Practice3State.KNOWLEDGE_SHARE_VALUES)
async def q6_values_process(message: Message):
    text = message.text.strip()
    ctx_storage.set(Practice3State.KNOWLEDGE_SHARE_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.CLARITY_VALUES],
                        keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.CLARITY_VALUES)


# Оценки 3.2 (7-11)
@practice3_labeler.message(state=Practice3State.CLARITY_VALUES)
async def q7_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.CLARITY_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.USEFULNESS_VALUES],
                        keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.USEFULNESS_VALUES)


@practice3_labeler.message(state=Practice3State.USEFULNESS_VALUES)
async def q8_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.USEFULNESS_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.INTEREST_VALUES],
                        keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.INTEREST_VALUES)


@practice3_labeler.message(state=Practice3State.INTEREST_VALUES)
async def q9_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.INTEREST_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.DEPTH_VALUES],
                        keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.DEPTH_VALUES)


@practice3_labeler.message(state=Practice3State.DEPTH_VALUES)
async def q10_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.DEPTH_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.TRAINER_VALUES],
                        keyboard=await create_scale_keyboard())
    await state_dispanser.set(message.peer_id, Practice3State.TRAINER_VALUES)


@practice3_labeler.message(state=Practice3State.TRAINER_VALUES)
async def q11_values_process(message: Message):
    text = message.text.strip()
    if not text.isdigit() or not (1 <= int(text) <= 10):
        await message.answer("Пожалуйста, введи число от 1 до 10",
                           keyboard=await create_scale_keyboard())
        return
    ctx_storage.set(Practice3State.TRAINER_VALUES, text)
    await message.answer(QUESTIONS_PRACTICE3_2[Practice3State.MISSING_VALUES],
                        keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, Practice3State.MISSING_VALUES)


@practice3_labeler.message(state=Practice3State.MISSING_VALUES)
async def q12_values_process(message: Message):
    ctx_storage.set(Practice3State.MISSING_VALUES, message.text.strip())

    answers_data = {
        "theme": "3.2. «Качества и ценности»",
        QUESTIONS_PRACTICE3_2[Practice3State.VALUES_UNDERSTANDING]: ctx_storage.get(Practice3State.VALUES_UNDERSTANDING),
        QUESTIONS_PRACTICE3_2[Practice3State.NEW_QUALITIES]: ctx_storage.get(Practice3State.NEW_QUALITIES),
        QUESTIONS_PRACTICE3_2[Practice3State.PEERS_EXPANDED]: ctx_storage.get(Practice3State.PEERS_EXPANDED),
        QUESTIONS_PRACTICE3_2[Practice3State.IMPLEMENTATION_PLAN]: ctx_storage.get(Practice3State.IMPLEMENTATION_PLAN),
        QUESTIONS_PRACTICE3_2[Practice3State.WORLDVIEW_CHANGED_VALUES]: ctx_storage.get(Practice3State.WORLDVIEW_CHANGED_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.KNOWLEDGE_SHARE_VALUES]: ctx_storage.get(Practice3State.KNOWLEDGE_SHARE_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.CLARITY_VALUES]: ctx_storage.get(Practice3State.CLARITY_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.USEFULNESS_VALUES]: ctx_storage.get(Practice3State.USEFULNESS_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.INTEREST_VALUES]: ctx_storage.get(Practice3State.INTEREST_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.DEPTH_VALUES]: ctx_storage.get(Practice3State.DEPTH_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.TRAINER_VALUES]: ctx_storage.get(Practice3State.TRAINER_VALUES),
        QUESTIONS_PRACTICE3_2[Practice3State.MISSING_VALUES]: ctx_storage.get(Practice3State.MISSING_VALUES),
    }

    await db_manager.save_anketa(
        peer_id=message.peer_id,
        anketa_type="practice3_2",
        data=answers_data
    )

    await message.answer("Спасибо!", keyboard=empty_kb)
    await state_dispanser.delete(peer_id=message.peer_id)
