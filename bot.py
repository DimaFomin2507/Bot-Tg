import asyncio
import json

from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from envparse import Env
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext



env = Env()

env.read_envfile(".env")
TOKEN = env.str('TOKEN')

dp = Dispatcher()

class Profile(StatesGroup):
    name = State()
    age = State()
    color = State()
    group = State()

@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer("Привет!")
    await message.answer("Представься пожалуйста!")
    await state.set_state(Profile.name)


@dp.message(Profile.name)
async def name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=message.text)
    await message.answer("Хорошо, сколько тебе лет?")
    await state.set_state(Profile.age)

@dp.message(Profile.age)
async def age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Это не число!")
        return
    await state.update_data(age=message.text)
    await message.answer("Хорошо, какой твой любимый цвет?")
    await state.set_state(Profile.color)


@dp.message(Profile.color)
async def color(message: Message, state: FSMContext):
    await state.update_data(color=message.text)
    await message.answer("Хорошо, в какой ты группе?")
    await state.set_state(Profile.group)


@dp.message(Profile.group)
async def group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer("Спасибо!")
    data = await state.get_data()
    await state.clear()
    id = message.from_user.id
    with open(f"{id}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f)



# @dp.message(Command("start"))
# async def start(message: Message) -> None:
#     text = message.text
#     username = message.from_user.username
#     full_name = message.from_user.full_name
#     await  message.answer(
#         text=f"Привет, {full_name}!\n"
#              f"Твой username - {username}"
#     )
#
#
# @dp.message(F.text.lower().contains("кошка"))
# async def cat(message: Message) -> None:
#     await message.answer(text="Здесь есть кошка")
#
#
# @dp.message(F.text.lower().contains("собака"))
# async def dog(message: Message) -> None:
#     await message.answer(text="Здесь есть собака")


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
