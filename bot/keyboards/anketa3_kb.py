from vkbottle import Keyboard, KeyboardButtonColor, Text
async def create_numbered_keyboard(count: int, color: KeyboardButtonColor = KeyboardButtonColor.PRIMARY) -> Keyboard:

    if count < 1 or count > 10:
        raise ValueError("Количество кнопок должно быть от 1 до 10")

    keyboard = Keyboard(inline=False)

    for i in range(1, count + 1):
        keyboard.add(Text(str(i)), color=color)
        if i < count:
            keyboard.row()

    return keyboard
