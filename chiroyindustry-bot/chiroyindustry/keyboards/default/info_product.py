from aiogram import types
from aiogram.dispatcher import FSMContext

from data import texts
from loader import dp, db


@dp.message_handler(text=['Mahsulot haqida', 'О продукте'])
async def info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    if lang_id == 1:
        await message.answer(text="<b>Dermion qo’llanilishi:</b>\n\n"
                                  "Dermion paxta yostiqchasi yordamida kuniga 2 marta - ertalab va kechqurun toza teriga, husnbuzar bor joyga surting. "
                                  "Qo’llashdan oldin flakonni chayqatish kerak.Vositani ko'z va burun shilliq qavatiga tushishiga yo’l qo’ymang.\n\n"
                                  "<i>Mahsulotni qo'llaganingizdan so'ng quyosh nurlaridan saqlaning.</i>\n\n"
                                  "Preparatni 0 ° C dan + 25 ° C gacha haroratda, quruq, quyosh nurlaridan himoyalangan joyda saqlang.",parse_mode='html')
    else:
        await message.answer(text="<b>Способ применения Dermion:</b>\n\n"
                                  "Наносить с помощью ватного диска, локально на пораженные участки кожи лица и тела. Избегая попадания жидкости в глаза и слизистые носа. Наносить 2 раза в сутки утром и вечером после умывания. "
                                  "Избегать прямых попаданий солнечных лучей и не находиться у открытого огня. Перед применением взболтать флакон."
                                  "<b>Условия хранения:</b>\n\n"
                                  "Хранить при температуре не выше 25 °С , в сухом, защищенном от детей и света месте.",parse_mode='html')


@dp.message_handler(text=['Tarkibi','состав'])
async def info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    lang_id = db.get_user_language_id(user_id)
    if lang_id == 1:
        await message.answer(text="Dermion tarkibi: AHA-BHA, Bor kislotasi, Rezorsin, Salitsil kislotasi, Oltingugurt, Etanol,Distillagan suv.")
    else:
        await message.answer(text="Состав  Dermion: AHA-BHA, Борная кислота, Резорцин, Салициловая кислота, Сера, Этанол, Дистиллированная вода.")