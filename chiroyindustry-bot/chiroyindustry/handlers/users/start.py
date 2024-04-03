from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.filters.state import StatesGroup, State

from data import texts
from loader import dp, db
from states.order_form import Form, UserStates


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message, state: FSMContext):

    user_id = message.from_user.id

    user_exists = db.get_user_by_chat_id(user_id)

    if not user_exists:
        # If the user doesn't exist, add them to the database
        db.add_user(chat_id=user_id)

        # Set the state to IN_LANG and prompt the user to choose a language
        await UserStates.IN_LANG.set()

        keyboard_lang = types.ReplyKeyboardMarkup(resize_keyboard=True)
        lang_buttons = [texts.BTN_LANG_UZ, texts.BTN_LANG_RU]
        keyboard_lang.add(*lang_buttons)

        await message.answer(texts.WELCOME_TEXT)
        await message.answer(texts.CHOOSE_LANG, reply_markup=keyboard_lang)
    else:
        # If the user exists, set the state to IN_MENU
        await UserStates.IN_MENU.set()

        user_id = message.from_user.id
        lang_id = db.get_user_language_id(user_id)

        # Continue with your conversation flow for existing users
        keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

        # Add the first button separately
        keyboard_menu.add(texts.BTN_ORDER[lang_id])

        # Add the remaining buttons in pairs
        buttons_menu_row1 = [texts.BTN_MY_ORDERS[lang_id],texts.BTN_ABOUT_US[lang_id]]
        buttons_menu_row2 = [texts.BTN_SETTINGS[lang_id],texts.CONTENT[lang_id]]

        keyboard_menu.add(*buttons_menu_row1)
        keyboard_menu.add(*buttons_menu_row2)

        # Check if the user is an admin (you need to implement this check)

        await message.answer(text=texts.TEXT_MAIN_MENU[lang_id], reply_markup=keyboard_menu)
        await state.finish()

    # Check if the user exists in the database
    # user_exists = db.get_user_by_chat_id(user_id)
    # if not user_exists:
    #     # If the user doesn't exist, add them to the database
    #     db.add_user(chat_id=user_id)
    #
    #     keyboard_lang = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     lang_buttons = [texts.BTN_LANG_UZ, texts.BTN_LANG_RU]
    #     keyboard_lang.add(*lang_buttons)
    #
    #     await message.answer(texts.CHOOSE_LANG, reply_markup=keyboard_lang)
    #
    # else:
    #     user_id = message.from_user.id
    #     lang_id = db.get_user_language_id(user_id)
    #
    #     await message.answer(texts.TEXT_ENTER_FIRST_NAME[lang_id],reply_markup=types.ReplyKeyboardRemove())
    #
    #     await Form.name.set()

