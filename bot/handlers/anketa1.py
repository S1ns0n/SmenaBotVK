from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa1_kb import choice_kb, projects_kb, parent_kb
from database import db_manager
from bot.handlers.anketa2 import anketa2_start
from bot.utils import remove_brackets_text

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
    FirstAnketaState.INTERESTS: "Твои интересы (3 направления) [максимум 3 балла за 3 направления. 2 – за 2,1 – за 1, 0 – если пропуск]",
    FirstAnketaState.PROFESSION: "Знаешь ли ты, какое дело жизни/профессию выбрать? Почему именно это дело? [Развернутый ответ (3 предложения и более) – 3 балла, 0- пропуск, 1 – одно предложение.]",
    FirstAnketaState.PARENTS: "Поддерживают ли тебя родители в выборе? [3 балла – да или нет, затрудняюсь – 1 балл]",
    FirstAnketaState.FRUITS: "Какие плоды (продукты своей деятельности. Пример: картины, игры, мероприятия) ты создаешь уже сегодня)? Перечисли не менее 3 [максимум 3 балла за более 3 плодов. 2 – за 2-3 плода, 1 – за 1, 0 – если пропуск]",
    FirstAnketaState.EFFECTS: "Какие эффекты (последствия, количественные и качественные результаты, впечатления у других людей. Пример: больше подростков интересуются БПЛА, родители испытывают гордость и радость) есть от создаваемых тобой плодов? [максимум 3 балла за более 3 эффектов. 2 – за 2-3 эффекта, 1 – за 1, 0 – если пропуск]",
    FirstAnketaState.GROUPS: "Перечисли 5-7 групп людей или живых существ, для пользы которых тебе интересно трудиться/которым интересно помогать? Пример: родители/врачи/молодые предприниматели/бездомные собаки [максимум 3 балла за более 5-7 групп. 2 – за 3-5 групп, 1 – за 1-3 группы, 0 – если пропуск]",
    FirstAnketaState.ACTIVITIES: "Расставь дела в порядке ОТ МЕНЕЕ интересного и увлекательного К БОЛЕЕ интересному и увлекательному:\n1) Физическая активность\n2) Общение\n3) Уход за животными и растениями\n4) Решение логических задач и планирование\n5) Выступление на публике\n6) Размышление о том, как устроен мир\n7) Рефлексия (исследование собственных чувств и мыслей)\n8) Наблюдение за красотой мира и создание творческих результатов [3 – за выполненное задание 0- если задание не выполнено, или цифры идут в последовательном порядке]",
    FirstAnketaState.FACTORS: "Расставь факторы, которые влияют на успех в карьере, ОТ МЕНЕЕ значимого К БОЛЕЕ значимому:\n1) Связи\n2) Удача\n3) Сочетание твердых знаний, железной воли и верности своим ценностям\n4) Диплом престижного вуза — это главный пропуск в жизнь\n5) Деньги\n6) Гибкость, умение подстроиться под систему\n7) Усердный труд\n8) Лидерские качества [3 – за выполненное задание 0- если задание не выполнено, или цифры идут в последовательном порядке]",
    FirstAnketaState.CHOICE: "Когда ты думаешь о своей будущей профессии, для тебя важнее всего:\n\nА. найти стабильное место («функцию»), где будут понятные правила и гарантированный доход\n\nБ. найти сферу, где я смогу реализовать свою «Суперсилу» и влиять на развитие своей страны\n\nВ. пока не думаю об этом, надеюсь, что обстоятельства сами выведут меня в нужное место. [А-3 балла, Б-5 баллов, В-1 балл]",
    FirstAnketaState.PROJECTS: "Являешься ли ты активным участником программ и проектов для молодежи? [3 балла да, 1 балл нет, затрудняюсь – 0 баллов]"
}



async def anketa1_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa1"):
        await message.answer("Вы уже прошли анкету")
        return

    await message.answer("Раздел 2. Профессиональное самоопределение", keyboard=empty_kb)
    await message.answer("1. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.INTERESTS]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.INTERESTS)


@anketa1_labeler.message(state=FirstAnketaState.INTERESTS)
async def interests_process(message: Message):
    ctx_storage.set(FirstAnketaState.INTERESTS, message.text.strip())
    await message.answer("2. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.PROFESSION]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.PROFESSION)


@anketa1_labeler.message(state=FirstAnketaState.PROFESSION)
async def profession_process(message: Message):
    ctx_storage.set(FirstAnketaState.PROFESSION, message.text.strip())
    await message.answer("3. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.PARENTS]), keyboard=parent_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.PARENTS)


@anketa1_labeler.message(state=FirstAnketaState.PARENTS)
async def parents_process(message: Message):
    ctx_storage.set(FirstAnketaState.PARENTS, message.text.strip())
    await message.answer("4. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.FRUITS]), keyboard=empty_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.FRUITS)


@anketa1_labeler.message(state=FirstAnketaState.FRUITS)
async def fruits_process(message: Message):
    ctx_storage.set(FirstAnketaState.FRUITS, message.text.strip())
    await message.answer("5. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.EFFECTS]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.EFFECTS)


@anketa1_labeler.message(state=FirstAnketaState.EFFECTS)
async def effects_process(message: Message):
    ctx_storage.set(FirstAnketaState.EFFECTS, message.text.strip())
    await message.answer("6. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.GROUPS]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.GROUPS)


@anketa1_labeler.message(state=FirstAnketaState.GROUPS)
async def groups_process(message: Message):
    ctx_storage.set(FirstAnketaState.GROUPS, message.text.strip())
    await message.answer("7. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.ACTIVITIES]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.ACTIVITIES)


@anketa1_labeler.message(state=FirstAnketaState.ACTIVITIES)
async def activities_process(message: Message):
    ctx_storage.set(FirstAnketaState.ACTIVITIES, message.text.strip())
    await message.answer("8. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.FACTORS]))
    await state_dispanser.set(message.peer_id, FirstAnketaState.FACTORS)


@anketa1_labeler.message(state=FirstAnketaState.FACTORS)
async def factors_process(message: Message):
    ctx_storage.set(FirstAnketaState.FACTORS, message.text.strip())
    await message.answer("9. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.CHOICE]), keyboard=choice_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.CHOICE)


@anketa1_labeler.message(state=FirstAnketaState.CHOICE)
async def choice_process(message: Message):
    ctx_storage.set(FirstAnketaState.CHOICE, message.text.strip())
    await message.answer("10. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.PROJECTS]), keyboard=projects_kb)
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




