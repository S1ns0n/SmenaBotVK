from vkbottle.bot import Bot
from bot.labeler_config import labeler, state_dispanser
from config import Config
from bot.handlers import anketa0_labeler, anketa1_labeler, anketa2_labeler, anketa3_labeler



bot = Bot(token=Config.BOT_TOKEN, labeler=labeler, state_dispenser=state_dispanser)
labeler.load(anketa0_labeler)
labeler.load(anketa1_labeler)
labeler.load(anketa2_labeler)
labeler.load(anketa3_labeler)



if __name__ == "__main__":
    print("Бот запущен...")
    bot.run_forever()
