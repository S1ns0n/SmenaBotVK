from vkbottle import Keyboard, KeyboardButtonColor, Text

practice_kb = Keyboard(inline=False)
practice_kb.add(Text("1"), color=KeyboardButtonColor.PRIMARY)
practice_kb.row()
practice_kb.add(Text("2"), color=KeyboardButtonColor.PRIMARY)
practice_kb.row()
practice_kb.add(Text("3"), color=KeyboardButtonColor.PRIMARY)