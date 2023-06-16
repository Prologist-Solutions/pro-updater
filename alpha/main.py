import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

bot_token = 'token'  # Replace with your Telegram bot token
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Welcome to the logistics automation bot! Please use the /manual command to enter the details.")


@dp.message_handler(commands=['manual'])
async def manual_command(message: types.Message):
    await message.reply("Please enter the load number:")
    await dp.current_state().set_state("waiting_for_load_number")

@dp.message_handler(state="waiting_for_load_number")
async def process_load_number(message: types.Message, state: FSMContext):
    load_number = message.text
    await message.reply("Please enter the trailer number:")
    await state.set_state("waiting_for_trailer_number")
    await state.update_data(load_number=load_number)


@dp.message_handler(state="waiting_for_trailer_number")
async def process_trailer_number(message: types.Message, state: FSMContext):
    trailer_number = message.text
    await message.reply("Please enter the pickup (PU) address:")
    await state.set_state("waiting_for_pickup_address")
    await state.update_data(trailer_number=trailer_number)


@dp.message_handler(state="waiting_for_pickup_address")
async def process_pickup_address(message: types.Message, state: FSMContext):
    pickup_address = message.text
    await message.reply("Please enter the delivery (DEL) address:")
    await state.set_state("waiting_for_delivery_address")
    await state.update_data(pickup_address=pickup_address)


@dp.message_handler(state="waiting_for_delivery_address")
async def process_delivery_address(message: types.Message, state: FSMContext):
    delivery_address = message.text
    await message.reply("Please enter the pickup (PU) time:")
    await state.set_state("waiting_for_pickup_time")
    await state.update_data(delivery_address=delivery_address)


@dp.message_handler(state="waiting_for_pickup_time")
async def process_pickup_time(message: types.Message, state: FSMContext):
    pickup_time = message.text
    async with state.proxy() as data:
        load_number = data['load_number']
        trailer_number = data['trailer_number']
        pickup_address = data['pickup_address']
        delivery_address = data['delivery_address']

    await state.reset_state()
    await message.reply(
        f"Load: #  {load_number}\n"
        f"Trailer: # {trailer_number}\n"
        f"______________________________\n"
        f"PU:   \n\n{pickup_address}\n\n⏰:  {pickup_time}\n"
        f"________________________________\n"
        f"DEL:  \n\n{delivery_address}\n\n⏰: straight\n"
        f"________________________________\n"
        f"SEND SEAL, TRAILER and PAPERWORK pictures\n"
        f"Do not forget to do SCALE, if load's weight more than 33k'"
    )


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
