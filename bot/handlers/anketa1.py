from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa1_kb import choice_kb, projects_kb
from database import db_manager
from bot.handlers.anketa2 import anketa2_start

anketa1_labeler = BotLabeler()


class FirstAnketaState(BaseStateGroup):
    INTERESTS = "interests"
    PROFESSION = "profession"
    PARENTS = "parents"
    FRUITS = "fruits"
    EFFECTS = "effects"
    GROUPS = "groups"
    ACTIVITIES = "activities"
    FACTORS = "factors"
    CHOICE = "choice"
    PROJECTS = "projects"

QUESTIONS_SECTION1 = {
    FirstAnketaState.INTERESTS: "Твои интересы (3 направления)",
    FirstAnketaState.PROFESSION: "Знаешь ли ты, какое дело жизни/профессию выбрать? Почему именно это дело?",
    FirstAnketaState.PARENTS: "Поддерживают ли тебя родители в выборе?",
    FirstAnketaState.FRUITS: "Какие плоды (продукты своей деятельности. Пример: картины, игры, мероприятия) ты создаешь уже сегодня)? Перечисли не менее 3",
    FirstAnketaState.EFFECTS: "Какие эффекты (последствия, количественные и качественные результаты, впечатления у других людей. Пример: больше подростков интересуются БПЛА, родители испытывают гордость и радость) есть от создаваемых тобой плодов?",
    FirstAnketaState.GROUPS: "Перечисли 5-7 групп людей или живых существ, для пользы которых тебе интересно трудиться/которым интересно помогать? Пример: родители/врачи/молодые предприниматели/бездомные собаки",
    FirstAnketaState.ACTIVITIES: "Расставь дела в порядке ОТ МЕНЕЕ интересного и увлекательного К БОЛЕЕ интересному и увлекательному:\n-Физическая активность\n-Общение\n-Уход за животными и растениями\n-Решение логических задач и планирование\n-Выступление на публике\n-Размышление о том, как устроен мир\n-Рефлексия (исследование собственных чувств и мыслей)\n-Наблюдение за красотой мира и создание творческих результатов",
    FirstAnketaState.FACTORS: "Расставь факторы, которые влияют на успех в карьере, ОТ МЕНЕЕ значимого К БОЛЕЕ значимому:\n-связи\n-удача\n-сочетание твердых знаний, железной воли и верности своим ценностям\n-диплом престижного вуза — это главный пропуск в жизнь\n-деньги\n-гибкость, умение подстроиться под систему\n-усердный труд\n-лидерские качества",
    FirstAnketaState.CHOICE: "Когда ты думаешь о своей будущей профессии, для тебя важнее всего:\n\nА. найти стабильное место («функцию»), где будут понятные правила и гарантированный доход\n\nБ. найти сферу, где я смогу реализовать свою «Суперсилу» и влиять на развитие своей страны\n\nВ. пока не думаю об этом, надеюсь, что обстоятельства сами выведут меня в нужное место.",
    FirstAnketaState.PROJECTS: "Являешься ли ты активным участником программ и проектов для молодежи?"
}


@anketa1_labeler.message(text="анкета1")
async def anketa1_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa1"):
        await message.answer("Вы уже прошли анкету")
        return

    await message.answer("Раздел 2. Профессиональное самоопределение", keyboard=empty_kb)
    await message.answer("1. " + QUESTIONS_SECTION1[FirstAnketaState.INTERESTS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.INTERESTS)


@anketa1_labeler.message(state=FirstAnketaState.INTERESTS)
async def interests_process(message: Message):
    ctx_storage.set(FirstAnketaState.INTERESTS, message.text.strip())
    await message.answer("2. " + QUESTIONS_SECTION1[FirstAnketaState.PROFESSION])
    await state_dispanser.set(message.peer_id, FirstAnketaState.PROFESSION)


@anketa1_labeler.message(state=FirstAnketaState.PROFESSION)
async def profession_process(message: Message):
    ctx_storage.set(FirstAnketaState.PROFESSION, message.text.strip())
    await message.answer("3. " + QUESTIONS_SECTION1[FirstAnketaState.PARENTS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.PARENTS)


@anketa1_labeler.message(state=FirstAnketaState.PARENTS)
async def parents_process(message: Message):
    ctx_storage.set(FirstAnketaState.PARENTS, message.text.strip())
    await message.answer("4. " + QUESTIONS_SECTION1[FirstAnketaState.FRUITS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.FRUITS)


@anketa1_labeler.message(state=FirstAnketaState.FRUITS)
async def fruits_process(message: Message):
    ctx_storage.set(FirstAnketaState.FRUITS, message.text.strip())
    await message.answer("5. " + QUESTIONS_SECTION1[FirstAnketaState.EFFECTS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.EFFECTS)


@anketa1_labeler.message(state=FirstAnketaState.EFFECTS)
async def effects_process(message: Message):
    ctx_storage.set(FirstAnketaState.EFFECTS, message.text.strip())
    await message.answer("6. " + QUESTIONS_SECTION1[FirstAnketaState.GROUPS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.GROUPS)


@anketa1_labeler.message(state=FirstAnketaState.GROUPS)
async def groups_process(message: Message):
    ctx_storage.set(FirstAnketaState.GROUPS, message.text.strip())
    await message.answer("7. " + QUESTIONS_SECTION1[FirstAnketaState.ACTIVITIES])
    await state_dispanser.set(message.peer_id, FirstAnketaState.ACTIVITIES)


@anketa1_labeler.message(state=FirstAnketaState.ACTIVITIES)
async def activities_process(message: Message):
    ctx_storage.set(FirstAnketaState.ACTIVITIES, message.text.strip())
    await message.answer("8. " + QUESTIONS_SECTION1[FirstAnketaState.FACTORS])
    await state_dispanser.set(message.peer_id, FirstAnketaState.FACTORS)


@anketa1_labeler.message(state=FirstAnketaState.FACTORS)
async def factors_process(message: Message):
    ctx_storage.set(FirstAnketaState.FACTORS, message.text.strip())
    await message.answer("9. " + QUESTIONS_SECTION1[FirstAnketaState.CHOICE], keyboard=choice_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.CHOICE)


@anketa1_labeler.message(state=FirstAnketaState.CHOICE)
async def choice_process(message: Message):
    ctx_storage.set(FirstAnketaState.CHOICE, message.text.strip())
    await message.answer("10. " + QUESTIONS_SECTION1[FirstAnketaState.PROJECTS], keyboard=projects_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.PROJECTS)


@anketa1_labeler.message(state=FirstAnketaState.PROJECTS)
async def projects_process(message: Message):
    projects = message.text.strip()
    ctx_storage.set(FirstAnketaState.PROJECTS, projects)

    anketa_data = {
        QUESTIONS_SECTION1[FirstAnketaState.INTERESTS]: ctx_storage.get(FirstAnketaState.INTERESTS),
        QUESTIONS_SECTION1[FirstAnketaState.PROFESSION]: ctx_storage.get(FirstAnketaState.PROFESSION),
        QUESTIONS_SECTION1[FirstAnketaState.PARENTS]: ctx_storage.get(FirstAnketaState.PARENTS),
        QUESTIONS_SECTION1[FirstAnketaState.FRUITS]: ctx_storage.get(FirstAnketaState.FRUITS),
        QUESTIONS_SECTION1[FirstAnketaState.EFFECTS]: ctx_storage.get(FirstAnketaState.EFFECTS),
        QUESTIONS_SECTION1[FirstAnketaState.GROUPS]: ctx_storage.get(FirstAnketaState.GROUPS),
        QUESTIONS_SECTION1[FirstAnketaState.ACTIVITIES]: ctx_storage.get(FirstAnketaState.ACTIVITIES),
        QUESTIONS_SECTION1[FirstAnketaState.FACTORS]: ctx_storage.get(FirstAnketaState.FACTORS),
        QUESTIONS_SECTION1[FirstAnketaState.CHOICE]: ctx_storage.get(FirstAnketaState.CHOICE),
        QUESTIONS_SECTION1[FirstAnketaState.PROJECTS]: projects
    }

    await db_manager.save_anketa(peer_id=message.peer_id, anketa_type="anketa1", data=anketa_data)
    await state_dispanser.delete(message.peer_id)
    await anketa2_start(message=message)




