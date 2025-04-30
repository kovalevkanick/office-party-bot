import asyncio
import logging
import os
import random
from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, InlineKeyboardMarkup, InlineKeyboardButton,
    InputMediaPhoto, FSInputFile, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command

API_TOKEN = '7797337410:AAHVV-D9AA7b4-U_-d0xV7zTtfnDsXoU3X0'
YOUR_TELEGRAM_ID = 428454164

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(storage=MemoryStorage())

class Quiz(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    WaitForName = State()

characters = ["normis", "skuuf", "nadomashnem", "nefor", "gorpkor"]

descriptions = {
    "nefor": "<b>Ты — офисный нефор!</b>\nШирокие брюки, таби, огромный галстук и пара колец точно твоё всё. Обязательно перед вечеринкой зайди за настойками в «Селёдку» и за бургером в «Салют»",
    "skuuf": "<b>Ты — офисный скуф!</b>\nКостюм у тебя пылится на антресолях, но ботинки всё ещё хранят тепло «Этажей». Надевай старую добрую классику: немного потертый пиджак, поло, брюки и лёгкую грусть в глазах.",
    "nadomashnem": "<b>Ты — фрилансер!</b>\nТвой вайб — клоунский нос от правок клиентов, энергетик и афобазол. Если ты не придёшь – мы не осудим. Но если придешь, то надевай то, что удобно и велит сердце.",
    "normis": "<b>Ты — офисный нормис!</b>\nЧистый костюм, зализанная челка и любовь к олд-мани стилю — всё при тебе. Скорее надевай черно-белый костюм, лоферы, и не забудь про уверенную улыбку: офисные девочки любят уверенных в себе.",
    "gorpkor": "<b>Ты — офисный горпкорщик!</b>\nУ тебя всегда с собой кружка, дождевик и связка карабинов, куда поместится еще одна пара Salomon. Надевай ветровку, карго-штаны и кроссовки для приключений: в джунглях open space выживают сильнейшие."
}

def answer_to_character(answer):
    return answer if answer in characters else "unknown"

@dp.message(Command("start"))
async def start_command(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Летсгоу 🚀", callback_data="letsgo")]
    ])
    await message.answer(
        "Привет! На связи корпоративник 5/2 – офисные джунгли в знакомом месте. Уже сегодня мы открываем двери для друзей и коллег. Но для начала тест – готов узнать какой лук подойдет тебе на вечеринку?",
        reply_markup=keyboard
    )

@dp.callback_query(F.data == "letsgo")
async def letsgo(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(Quiz.Q1)
    await state.update_data(scores={char: 0 for char in characters})
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Готов пить", callback_data="skuuf")],
        [InlineKeyboardButton(text="Готов танцевать", callback_data="normis")],
        [InlineKeyboardButton(text="На выгорании, но еще держусь", callback_data="nefor")],
        [InlineKeyboardButton(text="Одну текилу и две водки", callback_data="nadomashnem")],
        [InlineKeyboardButton(text="Сегодня нет цели, только путь", callback_data="gorpkor")]
    ])
    await callback_query.message.answer("🧠 На каком вайбе сегодня?", reply_markup=keyboard)

@dp.callback_query(F.data.in_(characters))
async def quiz_answer(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    current_state = await state.get_state()
    data = await state.get_data()
    scores = data.get("scores", {})

    answer = callback_query.data
    character = answer_to_character(answer)
    if character in scores:
        scores[character] += 1

    await state.update_data(scores=scores)

    if current_state == Quiz.Q1.state:
        await state.set_state(Quiz.Q2)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Комфорт плюс", callback_data="skuuf")],
            [InlineKeyboardButton(text="Комфорт", callback_data="normis")],
            [InlineKeyboardButton(text="Самокат", callback_data="nefor")],
            [InlineKeyboardButton(text="Пешком", callback_data="gorpkor")],
            [InlineKeyboardButton(text="ДИСКОмфорт", callback_data="nadomashnem")]
        ])
        await callback_query.message.answer("🚗 На чем поедешь на вечеринку?", reply_markup=keyboard)

    elif current_state == Quiz.Q2.state:
        await state.set_state(Quiz.Q3)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Завтра в 08:00", callback_data="gorpkor")],
            [InlineKeyboardButton(text="В понедельник", callback_data="nefor")],
            [InlineKeyboardButton(text="В отпуске", callback_data="normis")],
            [InlineKeyboardButton(text="Не работаю", callback_data="skuuf")],
            [InlineKeyboardButton(text="Не работаю, но и не зарабатываю", callback_data="nadomashnem")]
        ])
        await callback_query.message.answer("🧳 Когда на работу?", reply_markup=keyboard)

    elif current_state == Quiz.Q3.state:
        await state.set_state(Quiz.Q4)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Очки", callback_data="nadomashnem")],
            [InlineKeyboardButton(text="Часы", callback_data="skuuf")],
            [InlineKeyboardButton(text="Подвеска", callback_data="nefor")],
            [InlineKeyboardButton(text="Карабин", callback_data="gorpkor")],
            [InlineKeyboardButton(text="Деньги", callback_data="normis")]
        ])
        await callback_query.message.answer("🕶 Любимый аксессуар?", reply_markup=keyboard)

    elif current_state == Quiz.Q4.state:
        await state.set_state(Quiz.Q5)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Fred Again - Ten Days", callback_data="nefor")],
            [InlineKeyboardButton(text="Icegergert — Amsterdam", callback_data="normis")],
            [InlineKeyboardButton(text="Errortica — Psycho", callback_data="gorpkor")],
            [InlineKeyboardButton(text="Мурат Тхагалегов - Дианочка", callback_data="skuuf")],
            [InlineKeyboardButton(text="Люблю слушать голосовые", callback_data="nadomashnem")]
        ])
        await callback_query.message.answer("🎧 Любимый трек?", reply_markup=keyboard)

    elif current_state == Quiz.Q5.state:
        await state.clear()
        max_score = max(scores.values())
        top_characters = [char for char, score in scores.items() if score == max_score]
        final_char = "normis" if "normis" in top_characters else random.choice(top_characters)

        description = descriptions.get(final_char, "Описание не найдено.")
        await callback_query.message.answer(description)

        media = []
        for i in range(1, 6):
            filename = f"{final_char}{i}.jpg"
            if os.path.exists(filename):
                media.append(InputMediaPhoto(media=FSInputFile(filename)))

        if media:
            await bot.send_media_group(chat_id=callback_query.message.chat.id, media=media)

        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Да", callback_data="yes_signup"),
             InlineKeyboardButton(text="❌ Нет", callback_data="no_signup")]
        ])
        await callback_query.message.answer(
            "Спасибо за ответы!\nЕсли хочешь, можешь оставить свое ФИО, и мы внесем тебя в списки.",
            reply_markup=keyboard
        )

@dp.callback_query(F.data.in_({"yes_signup", "no_signup"}))
async def signup_decision(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    if callback_query.data == "yes_signup":
        await callback_query.message.answer("Ну тогда присылай!")
        await state.set_state(Quiz.WaitForName)
    else:
        await callback_query.message.answer("Понятно.")

@dp.message(Quiz.WaitForName)
async def get_name(message: Message, state: FSMContext):
    user_name = message.text
    await message.answer("Внесли!")
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    text = f"📝 Новая запись!\n👤 ФИО: {user_name}\n🕒 Время: {now}"
    try:
        await bot.send_message(chat_id=YOUR_TELEGRAM_ID, text=text)
    except Exception as e:
        logging.error(f"Ошибка при отправке ФИО в личку: {e}")
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
