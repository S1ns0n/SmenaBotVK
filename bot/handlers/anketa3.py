from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa3_kb import create_numbered_keyboard
from database import db_manager


anketa3_labeler = BotLabeler()

class ThirdAnketaState(BaseStateGroup):
    PERSONAL_QUALITIES = "personal_qualities"
    CONNECTION_WITH_HOMELAND = "connection_with_homeland"
    IDEAS = "ideas"
    LIFE_WORK = "life_work"
    DIFFICULTIES = "difficulties"
    LEADERSHIP = "leadership"
    FUTURE_VISION = "future_vision"
    SUPPORT = "support"
    KNOWLEDGE = "knowledge"
    REFLECTION = "reflection"
    VALUES = "values"


QUESTIONS_SECTION3 = {
    ThirdAnketaState.PERSONAL_QUALITIES: "1. Определи, насколько для тебя важны те или иные качества, и расставь их ОТ МЕНЕЕ значимого К БОЛЕЕ значимому:\n-Личные качества\n-Любовь к родине\n-Мечта\n-Опыт\n-Ценности\n-Наставничество\n-Единомышленники\n-Навыки и знания)",
    ThirdAnketaState.CONNECTION_WITH_HOMELAND: "2. Какая она – твоя связь с Родиной?\n1) Я активно участвую в проектах по развитию России/моей малой родины\n2) Для меня эта связь – в культуре. В музыке, в языке, в искусстве, в общей исторической памяти\n3) Я привязан к своему городу/области; люблю гулять по родному краю, по знакомым улицам или лесам, мне нравятся люди, мне нравится наша жизнь, наши увлечения; я вижу свой город и знаю, что хотел бы сделать лучше\n4) Мне трудно ответить на этот вопрос: у меня нет особой связи.",
    ThirdAnketaState.IDEAS: "3. Как ты поступаешь со своими идеями?\n1) Мне нравится окружать себя единомышленниками и вместе создавать, находиться в творческом процессе. У нас не всегда получается, но сам процесс создания очень вдохновляет, кажется, что вместе мы свернем горы\n2) Я постоянно генерирую новые идеи, вижу себя реализатором, представляю значимые последствия моих действий\n3) Иногда мне приходят новые идеи, но я редко их развиваю или делюсь ими\n4) Я предпочитаю работать по проверенным методам и не стремлюсь к созданию чего-то принципиально нового.",
    ThirdAnketaState.LIFE_WORK: "4. Что такое для тебя дело жизни?\n1) Это моя страсть, дело, которым я горю. Возможно, у меня не все получается, но сам процесс погружения, изучения и творения делает меня наполненным и помогает развиваться\n2) Это то, что у меня хорошо получается и с чем я хочу связать свою жизнь\n3) Это дело, которое приносит мне доход и позволяет жить свободно и радостно\n4) Это моя работа, которую я делаю/буду делать, чтобы обеспечивать себя необходимым",
    ThirdAnketaState.DIFFICULTIES: "5. Как ты реагируешь на трудности, неудачи и препятствия на пути к своим целям?\n1) Препятствия меня не останавливают, я всегда ищу способы их преодолеть и продолжаю двигаться к цели с удвоенной силой\n2) Я стараюсь быть упорным(ой), но иногда трудности сильно демотивируют, и мне требуется время, чтобы восстановиться. Я обдумываю свои ошибки и делаю выводы\n3) При столкновении с серьезными трудностями я часто сомневаюсь в своих силах и могу отступить\n4) Я легко сдаюсь при первых же сложностях и предпочитаю избегать ситуаций, требующих большого упорства",
    ThirdAnketaState.LEADERSHIP: "6. Чувствуешь ли ты себя комфортно в роли лидера, когда нужно вести за собой или объединять людей?\n1) Я легко нахожу общий язык с людьми, умею вдохновлять их и объединять для достижения общих целей; я стремлюсь занять роль лидера\n2) Я не стремлюсь быть лидером, просто хорошо делаю то, что умею и то, что мне нравится. И часто так выходит, что вокруг меня собираются такие же увлеченные люди, и мы вместе начинаем создавать\n3) Мне бывает сложно налаживать контакты и работать в команде\n4) Я предпочитаю работать в одиночку и не стремлюсь к взаимодействию с большим количеством людей",
    ThirdAnketaState.FUTURE_VISION: "7. Есть ли у тебя четкий образ желаемого будущего состояния счастья или сильное внутреннее чувство направления, куда ты хочешь двигаться, чтобы создать что-то значимое?\n1) У меня есть четкий и вдохновляющий образ будущего, к которому я стремлюсь, этот образ меня зажигает\n2) Я чувствую, куда хочу двигаться, но мой образ будущего пока не очень конкретен или постоянно меняется\n3) У меня есть цели и планы, но мечты или вектора движения - нет\n4) Я живу сегодняшним днем, чувствую себя хорошо прямо сейчас, я уверен(а), что все сложится идеально для меня",
    ThirdAnketaState.SUPPORT: "8. Ощущаешь ли ты поддержку со стороны семьи, друзей или сообщества в своих начинаниях? Ищешь ли единомышленников для совместного развития, обмена идеями и реализации?\n1) Я ценю поддержку семьи, друзей и сообщества, и сам(а) стремлюсь быть опорой для единомышленников\n2) У меня есть близкие люди, которые меня поддерживают, и мне этого достаточно\n3) Я предпочитаю полагаться только на себя и редко обращаюсь за помощью",
    ThirdAnketaState.KNOWLEDGE: "9. Стремишься ли ты постоянно приобретать новые знания и навыки? Кто тебе в этом помогает?\n1) Я постоянно учусь новому. В этом мне помогают мои школьные учителя и педагоги на кружках и секциях\n2) Самые полезные знания и навыки я получаю не в учебе, а через жизненный опыт и общение с новыми людьми. Стараюсь находить тех, кто близок мне по ценностям и целям\n3) Серфинг в интернете, обучающие ролики, книги – мои лучшие учителя\n4) Я считаю, что уже достаточно знаю, и не вижу необходимости в постоянном обучении или наставничестве",
    ThirdAnketaState.REFLECTION: "10. Свойственно ли тебе размышлять в одиночестве о том, что с тобой произошло?\n1) Не люблю быть один. Это удручает. Лучше с кем-нибудь поболтать\n2) Иногда мне нравится поразмышлять в одиночестве. Например, на прогулке\n3) Люблю посидеть с дневником и записать свои мысли. Мне нравится, что я могу вернуться к ним, перечитать, вспомнить, проанализировать прошлый опыт\n4) Я кайфую, когда могу остаться в одиночестве и поразмышлять, записать свои мысли. Из этих мыслей я собираю личный блог. Мне нравится делиться своими выводами и получать обратную связь",
    ThirdAnketaState.VALUES: "11. Зачем по-твоему человеку выявлять, знать и развивать свои ценности?\n1) Ценности – это жизненные ориентиры человека, то, что для него важно, чем он руководствуется в жизни. Если человек знает свои ценности, он понимает себя и причины своих поступков\n2) Я знаю свои ценности, но мне это никак не помогает\n3) Не понимаю, о каких ценностях речь\n4) Думаю, навыки и знания гораздо важнее ценностей. Именно они определяют, кто мы такие. Поэтому не вижу большого смысла в исследовании ценностей"
}


@anketa3_labeler.message(text="анкета3")
async def anketa3_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa3"):
        await message.answer("Вы уже прошли эту анкету")
        return

    await message.answer("Раздел 4: Модель героя-созидателя", keyboard=empty_kb)
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.PERSONAL_QUALITIES])
    await state_dispanser.set(message.peer_id, ThirdAnketaState.PERSONAL_QUALITIES)


@anketa3_labeler.message(state=ThirdAnketaState.PERSONAL_QUALITIES)
async def q1_process(message: Message):
    ctx_storage.set(ThirdAnketaState.PERSONAL_QUALITIES, message.text.strip())
    await message.answer("Прочитай каждое утверждение и выберите вариант ответа, который наиболее точно описывает тебя:", keyboard=empty_kb)
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.CONNECTION_WITH_HOMELAND], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.CONNECTION_WITH_HOMELAND)


@anketa3_labeler.message(state=ThirdAnketaState.CONNECTION_WITH_HOMELAND)
async def q2_process(message: Message):
    ctx_storage.set(ThirdAnketaState.CONNECTION_WITH_HOMELAND, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.IDEAS], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.IDEAS)


@anketa3_labeler.message(state=ThirdAnketaState.IDEAS)
async def q3_process(message: Message):
    ctx_storage.set(ThirdAnketaState.IDEAS, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.LIFE_WORK], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.LIFE_WORK)


@anketa3_labeler.message(state=ThirdAnketaState.LIFE_WORK)
async def q4_process(message: Message):
    ctx_storage.set(ThirdAnketaState.LIFE_WORK, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.DIFFICULTIES], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.DIFFICULTIES)


@anketa3_labeler.message(state=ThirdAnketaState.DIFFICULTIES)
async def q5_process(message: Message):
    ctx_storage.set(ThirdAnketaState.DIFFICULTIES, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.LEADERSHIP], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.LEADERSHIP)


@anketa3_labeler.message(state=ThirdAnketaState.LEADERSHIP)
async def q6_process(message: Message):
    ctx_storage.set(ThirdAnketaState.LEADERSHIP, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.FUTURE_VISION], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.FUTURE_VISION)


@anketa3_labeler.message(state=ThirdAnketaState.FUTURE_VISION)
async def q7_process(message: Message):
    ctx_storage.set(ThirdAnketaState.FUTURE_VISION, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.SUPPORT], keyboard=await create_numbered_keyboard(3))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.SUPPORT)


@anketa3_labeler.message(state=ThirdAnketaState.SUPPORT)
async def q8_process(message: Message):
    ctx_storage.set(ThirdAnketaState.SUPPORT, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.KNOWLEDGE], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.KNOWLEDGE)


@anketa3_labeler.message(state=ThirdAnketaState.KNOWLEDGE)
async def q9_process(message: Message):
    ctx_storage.set(ThirdAnketaState.KNOWLEDGE, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.REFLECTION], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.REFLECTION)


@anketa3_labeler.message(state=ThirdAnketaState.REFLECTION)
async def q10_process(message: Message):
    ctx_storage.set(ThirdAnketaState.REFLECTION, message.text.strip())
    await message.answer(QUESTIONS_SECTION3[ThirdAnketaState.VALUES], keyboard=await create_numbered_keyboard(4))
    await state_dispanser.set(message.peer_id, ThirdAnketaState.VALUES)


@anketa3_labeler.message(state=ThirdAnketaState.VALUES)
async def q11_process(message: Message):
    q11_answer = message.text.strip()
    ctx_storage.set(ThirdAnketaState.VALUES, q11_answer)

    anketa_data = {
        QUESTIONS_SECTION3[ThirdAnketaState.PERSONAL_QUALITIES]: ctx_storage.get(ThirdAnketaState.PERSONAL_QUALITIES),
        QUESTIONS_SECTION3[ThirdAnketaState.CONNECTION_WITH_HOMELAND]: ctx_storage.get(ThirdAnketaState.CONNECTION_WITH_HOMELAND),
        QUESTIONS_SECTION3[ThirdAnketaState.IDEAS]: ctx_storage.get(ThirdAnketaState.IDEAS),
        QUESTIONS_SECTION3[ThirdAnketaState.LIFE_WORK]: ctx_storage.get(ThirdAnketaState.LIFE_WORK),
        QUESTIONS_SECTION3[ThirdAnketaState.DIFFICULTIES]: ctx_storage.get(ThirdAnketaState.DIFFICULTIES),
        QUESTIONS_SECTION3[ThirdAnketaState.LEADERSHIP]: ctx_storage.get(ThirdAnketaState.LEADERSHIP),
        QUESTIONS_SECTION3[ThirdAnketaState.FUTURE_VISION]: ctx_storage.get(ThirdAnketaState.FUTURE_VISION),
        QUESTIONS_SECTION3[ThirdAnketaState.SUPPORT]: ctx_storage.get(ThirdAnketaState.SUPPORT),
        QUESTIONS_SECTION3[ThirdAnketaState.KNOWLEDGE]: ctx_storage.get(ThirdAnketaState.KNOWLEDGE),
        QUESTIONS_SECTION3[ThirdAnketaState.REFLECTION]: ctx_storage.get(ThirdAnketaState.REFLECTION),
        QUESTIONS_SECTION3[ThirdAnketaState.VALUES]: q11_answer
    }

    await db_manager.save_anketa(peer_id=message.peer_id, anketa_type="anketa3", data=anketa_data)

    user_anketa = await db_manager.get_anketa_data(peer_id=message.peer_id, anketa_type="anketa3")

    result = f"""✓ Анкета успешно заполнена!

Раздел 4. Модель героя-созидателя:
"""
    for question, answer in user_anketa.items():
        short_question = question[:50] + "..." if len(question) > 50 else question
        result += f"• {short_question}: {answer}\n"

    await message.answer(result, keyboard=empty_kb)
    await state_dispanser.delete(message.peer_id)