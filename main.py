import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
import ext.keyboard as keyboard
import asyncio
import motor.motor_asyncio
from aiogram.types import WebAppInfo
import json

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://gdevanezus:K2zqV1R1fqWwJGIA@cluster0.zqwmzbt.mongodb.net/?retryWrites=true&w=majority')
db = client['testiki']


TOKEN = '7178622994:AAExkLidcT37FJsXKv3EpA1xJtQwZG3mc4c'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def mainmsg(msg, type):
    if type == 2:
        message: types.Message = msg.message
    else:
        message: types.Message = msg
    await message.delete()
    kb = await keyboard.start()

    await message.answer(f"Привет! Я бот для книг да пон.", reply_markup=kb)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await mainmsg(message, 1)

@dp.callback_query(F.data == "main")
async def send_random_value(callback: types.CallbackQuery):
    await mainmsg(callback, type=2)

dp.callback_query()

@dp.callback_query(F.data == "viewbook")
async def send_random_value(callback: types.CallbackQuery):
    dbdata = await db['books'].find_one({"_id": 1})
    kb = await keyboard.books(dbdata)
    await callback.message.delete()
    await callback.message.answer('Просмотр книг: ', reply_markup=kb)

@dp.callback_query(F.data == "addbook")
async def send_random_value(callback: types.CallbackQuery):
    dbdata = await db['books'].find_one({"_id": 1})
    await callback.message.delete()
    kbs = [
        [types.KeyboardButton(text="Добавить книгу", web_app=WebAppInfo(url='https://bookweb-kappa.vercel.app/'))],
    ]
    kbb = types.ReplyKeyboardMarkup(keyboard=kbs)
    await callback.message.answer('Чтоб создать книгу нажмите на кнопку ниже и заполните форму.', reply_markup=kbb)

@dp.callback_query(F.data == "search")
async def send_random_value(callback: types.CallbackQuery):
    dbdata = await db['books'].find_one({"_id": 1})
    await callback.message.delete()
    kbs = [
        [types.KeyboardButton(text="Добавить книгу", web_app=WebAppInfo(url='https://bookweb-kappa.vercel.app/search.html'))],
    ]
    kbb = types.ReplyKeyboardMarkup(keyboard=kbs)
    await callback.message.answer('Чтоб найти книгу нажмите на кнопку ниже и вибирите критерии.', reply_markup=kbb)


@dp.callback_query(F.data == "setbook")
async def send_random_value(callback: types.CallbackQuery):
    dbdata = await db['books'].find_one({"_id": 1})
    kb = await keyboard.usbooks(dbdata, callback.from_user.id)
    await callback.message.delete()
    await callback.message.answer('Вашие книги: ', reply_markup=kb)


@dp.message(~F.message.via_bot)
async def web_app2(message: types.Message):
    if message.web_app_data is not None:
        
        dbdata = await db['books'].find_one({"_id": 1})
        jsondata = json.loads(message.web_app_data.data)
        if jsondata['type'] == "create":
            doc = {
                "id": len(dbdata['books']),
                "ownername": message.from_user.username,
                "ownerid": message.from_user.id,
                "title": jsondata['title'],
                "author": jsondata['author'],
                "description": jsondata['description'],
                "tags": jsondata['tags']
            }
            await db['books'].update_one({}, {"$addToSet": {"books": doc}}, upsert=True)
            await message.answer(f"Добавлено 👌", reply_markup=types.ReplyKeyboardRemove())
        elif jsondata['type'] == "search":
            await message.answer(f"Ожидайте ⏱️", reply_markup=types.ReplyKeyboardRemove())
            search_query = jsondata['query'].lower()
            found_books = []
            for book in dbdata['books']:
                if book and (search_query in book['title'].lower() or search_query in book['author'].lower() or search_query in book['tags']):
                    found_books.append(book)
            if found_books:
                await message.delete()
                await message.answer(f"Нашел: ", reply_markup=await keyboard.search(found_books))
            else:
                await message.delete()
                await message.answer(f"Ничего не нашел", reply_markup=await keyboard.back('viewbook'))
        
@dp.callback_query()
async def books(callback: types.CallbackQuery):
    id = callback.data
    print(id)
    parts = [id]
    if ":" in id:
        parts = id.split(":", 1)
    match parts[0]:
        case "book":
            dbdata = await db['books'].find_one({"_id": 1})
            bookid = parts[1]
            for book in dbdata['books']:
                if book:
                    if int(book['id']) == int(bookid):
                        await callback.message.delete()
                        await callback.message.answer(f'ID книги: {book['id']}\n💬 Название: {book['title']}\n🪶 Описание: {book['description']}\n 🪧 Автор: {book['author']}\n👌 Выложил: {book['ownername']}', reply_markup=await keyboard.back('setbook'))
        case "vievset":
            dbdata = await db['books'].find_one({"_id": 1})
            bookid = parts[1]
            for book in dbdata['books']:
                if book:
                    if int(book['ownerid']) == int(callback.from_user.id):
                        await callback.message.delete()
                        await callback.message.answer(f'ID книги: {book['id']}\n💬 Название: {book['title']}\n🪶 Описание: {book['description']}\n👀 Теги: {book['tags']}\n 🪧 Автор: {book['author']}', reply_markup=await keyboard.usbtns(book['id']))
        case "delete":
            dbdata = await db['books'].find_one({"_id": 1})
            bookid = parts[1]
            for book in dbdata['books']:
                if book:
                    if int(book['id']) == int(bookid):
                        await db['books'].update_one({"_id": 1}, {"$unset": {f"books.{book.get('id')}": {}}})
                        await callback.message.answer(f'Удалено', reply_markup=await keyboard.back('setbook'))

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())