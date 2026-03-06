from vkbottle.bot import Bot
from bot.labeler_config import labeler, state_dispanser
from config import Config
from bot.uploaders import init_uploader  # импортируем функцию инициализации загрузчика

bot = Bot(token=Config.BOT_TOKEN, labeler=labeler, state_dispenser=state_dispanser)

init_uploader(bot.api)

from bot.handlers import (
    anketa0_labeler,
    anketa1_labeler,
    anketa2_labeler,
    anketa3_labeler,
    what_your_practice_anketa_labeler
)

labeler.load(anketa0_labeler)
labeler.load(anketa1_labeler)
labeler.load(anketa2_labeler)
labeler.load(anketa3_labeler)
labeler.load(what_your_practice_anketa_labeler)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.run_forever()