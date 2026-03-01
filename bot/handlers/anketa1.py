from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa1_kb import choice_kb, projects_kb

anketa1_labeler = BotLabeler()


class SecondAnketaState(BaseStateGroup):
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


@anketa1_labeler.message(text="анкета1")
async def anketa2_start(message: Message):
    await message.answer("Раздел 2. Профессиональное самоопределение", keyboard=empty_kb)
    await message.answer("1. Твои интересы (3 направления)")
    await state_dispanser.set(message.peer_id, SecondAnketaState.INTERESTS)


@anketa1_labeler.message(state=SecondAnketaState.INTERESTS)
async def interests_process(message: Message):
    ctx_storage.set("interests", message.text.strip())
    await message.answer("2. Знаешь ли ты, какое дело жизни/профессию выбрать? Почему именно это дело?")
    await state_dispanser.set(message.peer_id, SecondAnketaState.PROFESSION)


@anketa1_labeler.message(state=SecondAnketaState.PROFESSION)
async def profession_process(message: Message):
    ctx_storage.set("profession", message.text.strip())
    await message.answer("3. Поддерживают ли тебя родители в выборе?")
    await state_dispanser.set(message.peer_id, SecondAnketaState.PARENTS)


@anketa1_labeler.message(state=SecondAnketaState.PARENTS)
async def parents_process(message: Message):
    ctx_storage.set("parents", message.text.strip())
    await message.answer("4. Какие плоды (продукты своей деятельности. Пример: картины, игры, мероприятия) ты создаешь уже сегодня)? Перечисли не менее 3")
    await state_dispanser.set(message.peer_id, SecondAnketaState.FRUITS)


@anketa1_labeler.message(state=SecondAnketaState.FRUITS)
async def fruits_process(message: Message):
    ctx_storage.set("fruits", message.text.strip())
    await message.answer("5. Какие эффекты (последствия, количественные и качественные результаты, впечатления у других людей. Пример: больше подростков интересуются БПЛА, родители испытывают гордость и радость) есть от создаваемых тобой плодов? ")
    await state_dispanser.set(message.peer_id, SecondAnketaState.EFFECTS)


@anketa1_labeler.message(state=SecondAnketaState.EFFECTS)
async def effects_process(message: Message):
    ctx_storage.set("effects", message.text.strip())
    await message.answer("6. Перечисли 5-7 групп людей или живых существ, для пользы которых тебе интересно трудиться/которым интересно помогать? Пример: родители/врачи/молодые предприниматели/бездомные собаки")
    await state_dispanser.set(message.peer_id, SecondAnketaState.GROUPS)


@anketa1_labeler.message(state=SecondAnketaState.GROUPS)
async def groups_process(message: Message):
    ctx_storage.set("groups", message.text.strip())
    await message.answer(
        "7. Расставь дела в порядке ОТ МЕНЕЕ интересного и увлекательного К БОЛЕЕ интересному и увлекательному:\n-Физическая активность\n-Общение\n-Уход за животными и растениями\n-Решение логических задач и планирование\n-Выступление на публике\n-Размышление о том, как устроен мир\n-Рефлексия\n-Наблюдение за красотой мира и создание творческих результатов")
    await state_dispanser.set(message.peer_id, SecondAnketaState.ACTIVITIES)


@anketa1_labeler.message(state=SecondAnketaState.ACTIVITIES)
async def activities_process(message: Message):
    ctx_storage.set("activities", message.text.strip())
    await message.answer(
        "8. Расставь факторы, которые влияют на успех в карьере, ОТ МЕНЕЕ значимого К БОЛЕЕ значимому:\nсвязи\n-удача\n-сочетание твердых знаний/железной воли/верности ценностям\n-диплом престижного вуза\n-деньги\n-гибкость\n-усердный труд\n-лидерские качества")
    await state_dispanser.set(message.peer_id, SecondAnketaState.FACTORS)


@anketa1_labeler.message(state=SecondAnketaState.FACTORS)
async def factors_process(message: Message):
    ctx_storage.set("factors", message.text.strip())
    await message.answer(
        "9. Когда ты думаешь о своей будущей профессии, для тебя важнее всего:\n\nА. найти стабильное место («функцию»), где будут понятные правила и гарантированный доход\n\nБ. найти сферу, где я смогу реализовать свою «Суперсилу» и влиять на развитие своей страны\n\nВ. пока не думаю об этом, надеюсь, что обстоятельства сами выведут меня в нужное место.",
        keyboard=choice_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.CHOICE)


@anketa1_labeler.message(state=SecondAnketaState.CHOICE)
async def choice_process(message: Message):
    ctx_storage.set("choice", message.text.strip())
    await message.answer("10. Являешься ли ты активным участником программ и проектов для молодежи?",
                         keyboard=projects_kb)
    await state_dispanser.set(message.peer_id, SecondAnketaState.PROJECTS)


@anketa1_labeler.message(state=SecondAnketaState.PROJECTS)
async def projects_process(message: Message):
    ctx_storage.set("projects", message.text.strip())

    # Итоговая анкета
    result = """✓ Раздел 2 заполнен!

Раздел 2. Профессиональное самоопределение:
• Интересы: """ + ctx_storage.get("interests") + """
• Профессия: """ + ctx_storage.get("profession") + """
• Родители: """ + ctx_storage.get("parents") + """
• Плоды: """ + ctx_storage.get("fruits") + """
• Эффекты: """ + ctx_storage.get("effects") + """
• Группы: """ + ctx_storage.get("groups") + """
• Активности: """ + ctx_storage.get("activities") + """
• Факторы: """ + ctx_storage.get("factors") + """
• Выбор: """ + ctx_storage.get("choice") + """
• Проекты: """ + ctx_storage.get("projects")

    await message.answer(result, keyboard=empty_kb)
    await state_dispanser.delete(message.peer_id)
