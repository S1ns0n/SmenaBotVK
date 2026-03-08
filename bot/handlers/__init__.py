from .start import labeler
from .anketa0 import anketa0_labeler
from .anketa1 import anketa1_labeler
from .anketa2 import anketa2_labeler
from .anketa3 import anketa3_labeler
from bot.handlers.practice_handlers.what_your_practice_anketa import what_your_practice_anketa_labeler
from bot.handlers.practice_handlers.practice1 import practice1_labeler
from bot.handlers.practice_handlers.practice2 import practice2_labeler
from bot.handlers.practice_handlers.practice3 import practice3_labeler
__all__ = ("labeler","anketa0_labeler", "anketa1_labeler", "anketa2_labeler", "anketa3_labeler", "what_your_practice_anketa_labeler", "practice1_labeler", "practice2_labeler", "practice3_labeler")