from vkbottle.bot import BotLabeler
from bot.labeler_config import state_dispanser, ctx_storage
from vkbottle.bot import Message
from vkbottle import BaseStateGroup
from bot.keyboards import empty_kb
from bot.keyboards.anketa1_kb import choice_kb, projects_kb, parent_kb
from database import db_manager
from bot.handlers.anketa2 import anketa2_start
from bot.utils import remove_brackets_text

practice2_labeler = BotLabeler()

