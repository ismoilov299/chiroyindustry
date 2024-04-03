from aiogram import types
from aiogram.dispatcher import FSMContext

from data import texts
from loader import dp, db
from states.order_form import ChangeLang


@dp.message_handler(text=['⚙ Sozlamalar', '⚙ Настройки'])
async def setting(message: types.Message, state: FSMContext):
    # Get user information
    keyboard_lang = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lang_buttons = [texts.BTN_LANG_UZ, texts.BTN_LANG_RU]
    keyboard_lang.add(*lang_buttons)
    await message.answer(texts.TEXT_LANG_WARNING, reply_markup=keyboard_lang)
    await ChangeLang.Lang.set()


@dp.message_handler(lambda message: message.text in [texts.BTN_LANG_UZ, texts.BTN_LANG_RU],state=ChangeLang.Lang)
async def handle_language_selection(message: types.Message, state: FSMContext):
    user_language = message.text

    # Map language to numeric value
    language_id = 1 if user_language == texts.BTN_LANG_UZ else 2

    # Save the user's language in the state
    # await state.update_data(language=language_id)
    user_id = message.from_user.id
    db.update_user_field(user_id, "lang_id", language_id)
    keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard_menu.add(texts.BTN_ORDER[lang_id])

    buttons_menu_row1 = [texts.BTN_MY_ORDERS[lang_id], texts.BTN_ABOUT_US[lang_id]]
    buttons_menu_row2 = [texts.BTN_SETTINGS[lang_id], texts.CONTENT[lang_id]]

    keyboard_menu.add(*buttons_menu_row1)
    keyboard_menu.add(*buttons_menu_row2)

    if language_id == 1:
        await message.answer("Siz O'zbek tilini tanladingiz.",reply_markup=keyboard_menu)
    elif language_id == 2:
        await message.answer("Вы выбрали русский язык.",reply_markup=keyboard_menu)
    await state.finish()