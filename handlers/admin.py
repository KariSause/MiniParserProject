from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data_base.db import add_user, add_keyword, get_keywords, delete_keyword

router = Router()

@router.message(Command("start"))
async def start_cmd(message: types.Message):
    add_user(message.from_user.id)
    await message.answer("👋 Привіт! Надішли мені ключові слова через кому, і я шукатиму їх у групах.\n\nПереглянути /keywords")

@router.message(Command("keywords"))
async def list_keywords(message: types.Message):
    keywords = get_keywords(message.from_user.id)
    if not keywords:
        return await message.answer("У тебе ще немає ключових слів.")
    
    buttons = [
        [InlineKeyboardButton(text=f"❌ {kw}", callback_data=f"delkw:{kw}")]
        for kw in keywords
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("🔑 Твої ключові слова:", reply_markup=markup)

@router.message(F.text)
async def add_keywords(message: types.Message):
    add_user(message.from_user.id)
    words = [kw.strip().lower() for kw in message.text.split(",") if kw.strip()]
    for kw in words:
        add_keyword(message.from_user.id, kw)
    await message.answer(f"✅ Додано слів: {len(words)}\nПодивитися: /keywords")

@router.callback_query(F.data.startswith("delkw:"))
async def delete_kw_cb(callback: types.CallbackQuery):
    keyword = callback.data.split(":", 1)[1]
    delete_keyword(callback.from_user.id, keyword)
    await callback.answer(f"❌ Видалено: {keyword}")
    await list_keywords(callback.message)
