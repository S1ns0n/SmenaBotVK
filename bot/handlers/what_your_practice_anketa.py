from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message, BotLabeler
from vkbottle import BaseStateGroup
from bot.keyboards.what_your_practice_anketa_kb import practice_kb
from bot.keyboards import empty_kb
from database import db_manager


what_your_practice_anketa_labeler = BotLabeler()

class PracticeAnketaState(BaseStateGroup):
    PRACTICE = "practice"

@what_your_practice_anketa_labeler.message(text="тренинг")
async def practice_anketa_start(message: Message):
    await message.answer("Привет! Ты недавно прошёл тренинги на программе, укажи какую имено ты прошёл!", keyboard=practice_kb)
    await state_dispanser.set(message.peer_id, PracticeAnketaState.PRACTICE)

@what_your_practice_anketa_labeler.message(state=PracticeAnketaState.PRACTICE)
async def what_practice_process(message: Message):
    await message.answer("Тут анкета для тренингов", keyboard=empty_kb)


