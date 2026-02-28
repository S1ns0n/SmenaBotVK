from vkbottle import Keyboard, KeyboardButtonColor, Text

sex_kb = Keyboard(inline=False)
sex_kb.add(Text("Мужской"), color=KeyboardButtonColor.PRIMARY)
sex_kb.row()
sex_kb.add(Text("Женский"), color=KeyboardButtonColor.PRIMARY)