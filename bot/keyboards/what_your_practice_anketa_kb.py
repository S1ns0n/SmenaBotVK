from vkbottle import Keyboard, KeyboardButtonColor, Text

practice_kb = Keyboard(inline=False)
practice_kb.add(Text("тренинг по модели героя-созидателя"), color=KeyboardButtonColor.PRIMARY)
practice_kb.row()
practice_kb.add(Text("тренинг «Путь к самореализации»"), color=KeyboardButtonColor.PRIMARY)
practice_kb.row()
practice_kb.add(Text("тренинг «Формула мечты»"), color=KeyboardButtonColor.PRIMARY)