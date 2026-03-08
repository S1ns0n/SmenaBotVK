from vkbottle import Keyboard, KeyboardButtonColor, Text

async def create_scale_keyboard():
    kb = Keyboard(inline=False, one_time=True)
    for i in range(1, 6):
        kb.add(Text(str(i)), color=KeyboardButtonColor.SECONDARY)
    kb.row()
    for i in range(6, 11):
        kb.add(Text(str(i)), color=KeyboardButtonColor.SECONDARY)
    return kb.get_json()