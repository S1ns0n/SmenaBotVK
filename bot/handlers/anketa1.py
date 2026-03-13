from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa1_kb import choice_kb, projects_kb, parent_kb
from database import db_manager
from ai import analyzer
from bot.utils import remove_brackets_text
from bot.uploaders import photo_uploader
from config import Config

anketa1_labeler = BotLabeler()


class FirstAnketaState(BaseStateGroup):
    INTERESTS = "interests"
    PROFESSION = "profession"
    PARENTS = "parents"
    CHOICE = "choice"
    PROJECTS = "projects"

QUESTIONS_SECTION1 = {
    FirstAnketaState.INTERESTS: "Твои интересы (3 направления) [максимум 3 балла за 3 направления. 2 – за 2,1 – за 1, 0 – если пропуск]",
    FirstAnketaState.PROFESSION: "Знаешь ли ты, какое дело жизни/профессию выбрать? Почему именно это дело? [Развернутый ответ (3 предложения и более) – 3 балла, 0- пропуск, 1 – одно предложение.]",
    FirstAnketaState.PARENTS: "Поддерживают ли тебя родители в выборе? [3 балла – да или нет, затрудняюсь – 1 балл]",
    FirstAnketaState.CHOICE: "Когда ты думаешь о своей будущей профессии, для тебя важнее всего:\n\nА. найти стабильное место («функцию»), где будут понятные правила и гарантированный доход\n\nБ. найти сферу, где я смогу реализовать свою «Суперсилу» и влиять на развитие своей страны\n\nВ. пока не думаю об этом, надеюсь, что обстоятельства сами выведут меня в нужное место. [А-3 балла, Б-5 баллов, В-1 балл]",
    FirstAnketaState.PROJECTS: "Являешься ли ты активным участником программ и проектов для молодежи? [3 балла да, 1 балл нет, затрудняюсь – 0 баллов]"
}



async def anketa1_start(message: Message):
    if await db_manager.has_user_anketa(peer_id=message.peer_id, anketa_type="anketa1"):
        await message.answer("Вы уже прошли анкету")
        return

    await message.answer("Профессиональное самоопределение", keyboard=empty_kb)
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
    await message.answer("4. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.CHOICE]), keyboard=choice_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.CHOICE)

@anketa1_labeler.message(state=FirstAnketaState.CHOICE)
async def choice_process(message: Message):
    ctx_storage.set(FirstAnketaState.CHOICE, message.text.strip())
    await message.answer("5. " + remove_brackets_text(QUESTIONS_SECTION1[FirstAnketaState.PROJECTS]), keyboard=projects_kb)
    await state_dispanser.set(message.peer_id, FirstAnketaState.PROJECTS)


@anketa1_labeler.message(state=FirstAnketaState.PROJECTS)
async def projects_process(message: Message):
    projects = message.text.strip()
    ctx_storage.set(FirstAnketaState.PROJECTS, projects)

    anketa_data = {
        QUESTIONS_SECTION1[FirstAnketaState.INTERESTS]: ctx_storage.get(FirstAnketaState.INTERESTS),
        QUESTIONS_SECTION1[FirstAnketaState.PROFESSION]: ctx_storage.get(FirstAnketaState.PROFESSION),
        QUESTIONS_SECTION1[FirstAnketaState.PARENTS]: ctx_storage.get(FirstAnketaState.PARENTS),
        QUESTIONS_SECTION1[FirstAnketaState.CHOICE]: ctx_storage.get(FirstAnketaState.CHOICE),
        QUESTIONS_SECTION1[FirstAnketaState.PROJECTS]: projects
    }

    await state_dispanser.delete(message.peer_id)
    mes = await message.answer("думаю...", keyboard=empty_kb)
    answer = await analyzer.analyze_peer_anketas(message.peer_id, anketa_data=anketa_data)

    await message.ctx_api.messages.delete(
        peer_id=message.peer_id,
        message_ids=[mes.message_id]
    )

    photo = await photo_uploader.upload(
        file_source=str(Config.AI_IMAGE),
        peer_id=message.peer_id,
    )
    await message.answer(answer, attachment=photo)



