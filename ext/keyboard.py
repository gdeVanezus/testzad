from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram import types
async def start():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="📕 Просмотр книг", callback_data="viewbook"),
                InlineKeyboardButton(text="➕ Добавить книгу", callback_data="addbook"),
                InlineKeyboardButton(text="🪶 Управления книгами", callback_data="setbook"),
                # InlineKeyboardButton(text="Управления книгами", callback_data="setbook"),
            ]
        ]
    )
    return keyboard

async def usbooks(bookdata, ownid):
    inline_keyboard = [[InlineKeyboardButton(text="◀️ Вернуться назад", callback_data='main')]]
    books = bookdata.get('books', [])
    for book in books:
        if book:
            if book.get('ownerid', None) == ownid:
                inline_keyboard.append([InlineKeyboardButton(text=f"{book['title']} | {book['ownername']}", callback_data=f"vievset:{book['id']}")])
    
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard_markup

async def search(bookdata):
    inline_keyboard = [[InlineKeyboardButton(text="🔍 Поиск", callback_data='search')], [InlineKeyboardButton(text="◀️ Вернуться назад", callback_data='main')]]
    for book in bookdata:
        if book:
            inline_keyboard.append([InlineKeyboardButton(text=f"{book['title']} | {book['ownername']}", callback_data=f"book:{book['id']}")])
    
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard_markup

async def books(bookdata):
    inline_keyboard = [[InlineKeyboardButton(text="🔍 Поиск", callback_data='search')], [InlineKeyboardButton(text="◀️ Вернуться назад", callback_data='main')]]
    books = bookdata.get('books', [])
    for book in books:
        if book:
            inline_keyboard.append([InlineKeyboardButton(text=f"{book['title']} | {book['ownername']}", callback_data=f"book:{book['id']}")])
    
    keyboard_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return keyboard_markup

async def usbtns(id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete:{id}"),
                InlineKeyboardButton(text="◀️ Вернуться назад", callback_data='setbook'),
            ]
        ]
    )
    return keyboard

async def back(cbdata):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="◀️ Вернуться назад", callback_data=cbdata),
            ]
        ]
    )
    return keyboard