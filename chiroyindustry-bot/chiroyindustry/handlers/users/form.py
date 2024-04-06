from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from datetime import datetime

from aiogram.utils.exceptions import MessageNotModified

from data import texts
from loader import dp, db, bot
from states.order_form import Form


@dp.message_handler(lambda message: message.text in [texts.BTN_ORDER[1],texts.BTN_ORDER[2]])
async def handle_language_selection(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    regions = [texts.BTN_TEXT_UZUM_1[lang_id], texts.BTN_TEXT_UZUM_2[lang_id]]
    keyboard.add(*regions)
    await message.answer(f"{texts.DELIVER_TEXT[lang_id]}",reply_markup=keyboard)
    await Form.market.set()

@dp.message_handler(lambda message: message.text in [texts.BTN_TEXT_UZUM_1[1], texts.BTN_TEXT_UZUM_1[2]],state=Form.market)
async def uzum_order(message:types.Message,state: FSMContext):
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    url_button = InlineKeyboardMarkup()
    button = InlineKeyboardButton('Uzum marketdan buyurtma berish', url='https://uzum.uz/uz/product/husnbuzarga-qarshi-vosita-dermion-408631?skuid=740300')
    url_button.add(button)
    await message.answer("Uzum marketdan buyurtma berish uchun tugmani bosing",reply_markup=url_button)
    keyboard_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Add the first button separately
    keyboard_menu.add(texts.BTN_ORDER[lang_id])

    # Add the remaining buttons in pairs
    buttons_menu_row1 = [texts.BTN_MY_ORDERS[lang_id], texts.BTN_ABOUT_US[lang_id]]
    buttons_menu_row2 = [texts.BTN_SETTINGS[lang_id], texts.CONTENT[lang_id]]

    keyboard_menu.add(*buttons_menu_row1)
    keyboard_menu.add(*buttons_menu_row2)

    # Check if the user is an admin (you need to implement this check)

    await message.answer(text=texts.TEXT_MAIN_MENU[lang_id], reply_markup=keyboard_menu)
    await state.finish()
    await state.finish()

@dp.message_handler(lambda message: message.text in [texts.BTN_TEXT_UZUM_2[1], texts.BTN_TEXT_UZUM_2[2]],state=Form.market)
async def bot_order(message:types.Message,state: FSMContext):
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    await message.answer(texts.TEXT_ENTER_FIRST_NAME[lang_id], reply_markup=types.ReplyKeyboardRemove())
    await Form.name.set()

@dp.message_handler(state=Form.name)
async def phone_number(message: types.Message, state: FSMContext):
    name = message.text
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    await state.update_data(name=name)
    user_id = message.from_user.id
    db.update_user_field(user_id, "first_name", name)
    button_phone = types.KeyboardButton(text=f"{texts.BTN_SEND_CONTACT[lang_id]}", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button_phone)

    await message.answer(f"{texts.TEXT_ENTER_CONTACT[lang_id]}", reply_markup=keyboard)
    await Form.phone.set()


@dp.message_handler(state=Form.phone, content_types=[types.ContentType.TEXT, types.ContentType.CONTACT])
async def process_phone_number(message: types.Message, state: FSMContext):
    user_id = message.chat.id
    lang_id = db.get_user_language_id(user_id)

    if message.content_type == types.ContentType.CONTACT:
        phone_number = message.contact.phone_number
    else:
        if message.text.startswith("+998"):
            phone_number = message.text
        else:
            await message.answer(f"{texts.TEXT_ERROR_PHONE[lang_id]}")
            return

    await state.update_data(phone_number=phone_number)
    db.update_user_field(chat_id=user_id, key='phone_number', value=phone_number)
    await message.answer(f"{texts.ASK_PRODUCT[lang_id]}",reply_markup=types.ReplyKeyboardRemove())
    await Form.product.set()

@dp.message_handler(state=Form.product,content_types=types.ContentType.TEXT)
async def product_count(message: types.Message,state: FSMContext):
    amount = message.text
    await state.update_data(product_count=amount)
    keyboard_region = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_id = message.chat.id
    lang_id = db.get_user_language_id(user_id)

    regions = [texts.TEXT_REGION_1[lang_id], texts.TEXT_REGION_2[lang_id]]
    keyboard_region.add(*regions)
    await message.answer(f"{texts.TEXT_REGION_ASK[lang_id]}",reply_markup=keyboard_region)
    await Form.region.set()

@dp.message_handler(state=Form.region)
async def region(message: types.Message,state: FSMContext):
    user_id = message.chat.id
    lang_id = db.get_user_language_id(user_id)
    if message.text == texts.TEXT_REGION_1[lang_id]:

        location_button = KeyboardButton(text=f"{texts.SEND_LOCATION[lang_id]}", request_location=True)

        Keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(location_button)
        await message.answer(f"{texts.TEXT_ASK_LOCATION[lang_id]}",reply_markup=Keyboard)

        await Form.location.set()

    if message.text == texts.TEXT_REGION_2[lang_id]:
        await message.answer("Buyurtma to'g'ri yetib borishi uchun manzilingizni to'liq kiriting!",reply_markup=types.ReplyKeyboardRemove())
        await Form.location.set()

@dp.message_handler(state=Form.location, content_types=types.ContentType.LOCATION)
async def process_location(message: types.Message, state: FSMContext):
    print(message.location)
    location = message.location

    user_id = message.chat.id
    lang_id = db.get_user_language_id(user_id)


    await state.update_data(admin_location=location)

    user_data = await state.get_data()

    name = user_data.get('name', 'Unknown')
    phone_number = user_data.get('phone_number', 'Unknown')
    product_count = user_data.get('product_count', 'Unknown')


    confirmation_message = (
        f"{texts.INFO_USER_ORDER[lang_id]}\n"
        f"{texts.INFO_USER_ORDER_NAME[lang_id]} {name}\n"
        f"{texts.INFO_USER_ORDER_PHONE[lang_id]} {phone_number}\n"
        f"{texts.INFO_USER_ORDER_PRODUCT[lang_id]} {product_count}\n"
        f"{texts.INFO_USER_ORDER_ASK[lang_id]}"
    )

    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_button = InlineKeyboardButton(text=f"{texts.CONFIRMATION_YES[lang_id]}", callback_data="confirm_yes")
    no_button = InlineKeyboardButton(text=f"{texts.CONFIRMATION_NO[lang_id]}", callback_data="confirm_no")
    keyboard.add(yes_button, no_button)

    await message.answer(confirmation_message, reply_markup=keyboard)

@dp.callback_query_handler(lambda query: query.data == 'confirm_yes', state=Form.location)
async def confirm_yes(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang_id = db.get_user_language_id(user_id)
    user_data = await state.get_data()
    location = user_data.get('admin_location', None)


    name = user_data.get('name', 'Unknown')
    phone_number = user_data.get('phone_number', 'Unknown')
    product_count = user_data.get('product_count', 'Unknown')
    latitude = location.latitude
    longitude = location.longitude
    max_order_id = db.get_max_order_id()
    if max_order_id != "001":
        order_id = str(int(max_order_id) + 1).zfill(3)
    else:
        order_id = max_order_id

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    db.add_order(user_id=user_id, status='1', amount=product_count, order_id=order_id, created_at=created_at)

    # await bot.send_message(user_id, "Buyurtmangiz qabul qilindi. Tez orada siz bilan bog'lanamiz")
    #
    # await callback_query.answer("Buyurtmangiz qabul qilindi. Tez orada siz bilan bog'lanamiz")

    await state.finish()

    message_to_admin = (
        f"Yangi buyurtma\n"
        f"ID raqami: {order_id}\n"
        f"Ism: {name}\n"
        f"Telefon raqami: {phone_number}\n"
        f"Mahsulotlar soni: {product_count}\n"

    )


    admin_id = 1161180912  #-4199719807
    keyboard_send_message = InlineKeyboardMarkup()
    deactivate_button = InlineKeyboardButton(
        "Yetkazib berildi",
        callback_data=f"deactivate_{order_id}"
    )
    user = db.get_user_by_chat_id(user_id)

    # Add both buttons to the keyboard
    keyboard_send_message.add( deactivate_button)


    await bot.send_message(admin_id, message_to_admin,reply_markup=keyboard_send_message)
    await bot.send_location(admin_id, latitude=latitude, longitude=longitude)

    # Notify the user that their order has been received
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, f"{texts.NOTIFY_OREDER[lang_id]}")

    # Respond to the user's confirmation query
    await callback_query.answer(f"{texts.ACCEPT_ORDER[lang_id]}")

    # Clear the state
    await state.finish()

@dp.callback_query_handler(lambda query: query.data.startswith('deactivate_'))
async def process_deactivate_callback(query: CallbackQuery, state: FSMContext):
    # Extract user_id from the callback_data
    user_id = int(query.data.split('_')[1])

    # Deactivate orders for the specified user_id
    db.deactivate_orders_by_user_id(user_id)

    # Send a response to the user
    try:
        await bot.answer_callback_query(query.id, text="Ajoyib yana bitta buyurtmani yetkazib berdik 🎉 ", show_alert=True)
    except MessageNotModified:
        pass
    delivery_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    await query.message.delete_reply_markup()
    await query.message.reply(f'Buyurtma yetkazildi ✅ \n'
                              f'yetkazib berilgan vaqt: {delivery_time}\n'
                              f'yetkazib beruvchi {query.from_user.full_name}')



