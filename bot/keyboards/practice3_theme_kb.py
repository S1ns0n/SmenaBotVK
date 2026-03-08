from vkbottle import Keyboard, KeyboardButtonColor, Text


theme_kb = Keyboard(inline=False)
theme_kb.add(Text("Мечта"), color=KeyboardButtonColor.PRIMARY)
theme_kb.row()
theme_kb.add(Text("Качества и ценности"), color=KeyboardButtonColor.PRIMARY)
