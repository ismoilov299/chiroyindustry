from aiogram import types
from aiogram.dispatcher import FSMContext

from data import texts
from loader import dp, db
from states.order_form import UserStates


@dp.message_handler(lambda message: message.text in [texts.BTN_LANG_UZ, texts.BTN_LANG_RU], state=UserStates.IN_LANG)
async def process_language(message: types.Message, state: FSMContext):
    user_language = message.text

    # Map language to numeric value
    language_id = 1 if user_language == texts.BTN_LANG_UZ else 2

    # Save the user's language in the state
    await state.update_data(language=language_id)

    # Save the user's language in the database
    user_id = message.from_user.id
    db.update_user_field(user_id, "lang_id", language_id)

    # Transition to the next state (IN_MENU)
    await UserStates.IN_MENU.set()

    keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Add the first button separately
    keyboard_menu.add(texts.BTN_ORDER[language_id])

    # Add the remaining buttons in pairs
    buttons_menu_row1 = [texts.BTN_MY_ORDERS[language_id],texts.BTN_ABOUT_US[language_id]]
    buttons_menu_row2 = [texts.BTN_SETTINGS[language_id],texts.CONTENT[language_id]]

    keyboard_menu.add(*buttons_menu_row1)
    keyboard_menu.add(*buttons_menu_row2)

    # Check if the user is an admin (you need to implement this check)

    await message.answer(text=texts.TEXT_MAIN_MENU[language_id], reply_markup=keyboard_menu)
    await state.finish()