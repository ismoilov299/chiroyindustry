from datetime import datetime

from aiogram import types

from data import texts
from loader import db, dp


@dp.message_handler(text=['🛍 Buyurtmalarim', '🛍 Мои заказы'])
async def view_orders(message: types.Message):

    user_id = message.from_user.id
    print(user_id)
    lang_id = db.get_user_language_id(user_id)

    # Fetch orders using db.get_orders_by_user_and_status
    orders = db.get_orders_by_user_and_status(user_id)  # Assuming status 1 is for processed orders
    print(orders)
    if orders:
        # Initialize a message to send order details
        orders_message = (f"<b>{texts.TEXT_MY_ORDERS[lang_id]}</b>\n\n"
                          f"<i>{texts.TEXT_ORDER_ACTIVE[lang_id]}</i>\n\n")

        for order in orders:
            print(orders)
            # Process each order
            amount = order['amount']
            order_status = order['status']
            created_at_datetime = datetime.strptime(order['created_at'], '%Y-%m-%d %H:%M:%S')
            created_at_without_seconds = created_at_datetime.strftime('%Y-%m-%d %H:%M')
            orders_message += (f"Buyurtma  soni {amount} ta \nberilgan sanasi {created_at_without_seconds}\n")

        orders_message += (f"\n<b>{texts.ALL[lang_id]}</b>")

        await message.answer(text=orders_message, parse_mode='html')
    else:
        await message.answer(text=texts.NO_ORDERS[lang_id])