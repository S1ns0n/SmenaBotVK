from vkbottle import Keyboard, KeyboardButtonColor, Text

projects_kb = Keyboard(inline=False)
projects_kb.add(Text("Да"), color=KeyboardButtonColor.PRIMARY)
projects_kb.row()
projects_kb.add(Text("Нет"), color=KeyboardButtonColor.PRIMARY)
projects_kb.row()
projects_kb.add(Text("Не уверен(а)"), color=KeyboardButtonColor.PRIMARY)

choice_kb = Keyboard(inline=False)
choice_kb.add(Text("А"), color=KeyboardButtonColor.PRIMARY)
choice_kb.add(Text("Б"), color=KeyboardButtonColor.PRIMARY)
choice_kb.add(Text("В"), color=KeyboardButtonColor.PRIMARY)

parent_kb = Keyboard(inline=False)
parent_kb.add(Text("Да"), color=KeyboardButtonColor.PRIMARY)
parent_kb.row()
parent_kb.add(Text("Нет"), color=KeyboardButtonColor.PRIMARY)
parent_kb.row()
parent_kb.add(Text("Затрудняюсь ответить"), color=KeyboardButtonColor.PRIMARY)