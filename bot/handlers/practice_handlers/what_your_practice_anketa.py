from unittest import case

from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message, BotLabeler
from vkbottle import BaseStateGroup
from bot.keyboards.what_your_practice_anketa_kb import practice_kb
from bot.keyboards import empty_kb
from database import db_manager
from bot.handlers.practice_handlers.practice1 import practice1_start
from bot.handlers.practice_handlers.practice2 import practice2_start
from bot.handlers.practice_handlers.practice3 import practice3_start


what_your_practice_anketa_labeler = BotLabeler()
class PracticeAnketaState(BaseStateGroup):
    PRACTICE = "practice"

@what_your_practice_anketa_labeler.message(text="тренинг")
async def practice_anketa_start(message: Message):
    await message.answer("Привет, друг!\nКак прошли твои дни? Надеюсь, ты все еще полон сил, а теперь еще и насытился полезными ответами, мудрыми вопросами и значимыми открытиями. Давай исследуем твой рост в процессе тренинга.\nВыбери тренинг, который ты прошел:\n\n1) Путь к самореализации\n\n2) Формула мечты\n\n3) Тренинг по модели героя-созидателя", keyboard=practice_kb)
    await state_dispanser.set(message.peer_id, PracticeAnketaState.PRACTICE)

@what_your_practice_anketa_labeler.message(state=PracticeAnketaState.PRACTICE)
async def what_practice_process(message: Message):
    answer = message.text
    match answer:
        case "1":
            await practice1_start(message)
        case "2":
            await practice2_start(message)
        case "3":
            await practice3_start(message)
        case _:
            await message.answer("Выбери цифру)")




