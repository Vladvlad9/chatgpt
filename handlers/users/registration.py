from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.users.mainForms import main_cb, MainForms
from loader import dp


from states.users import UserStates


@dp.message_handler(commands=["start"], state=UserStates.all_states)
async def registration_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(text="Главное меню",
                         reply_markup=await MainForms.mainForm_ikb()
                         )


@dp.message_handler(commands="start")
async def registration_start(message: types.Message):
    await message.answer(text="Главное меню",
                         reply_markup=await MainForms.mainForm_ikb()
                         )


@dp.callback_query_handler(main_cb.filter())
@dp.callback_query_handler(main_cb.filter(), state=UserStates.all_states)
async def process_callback(callback: types.CallbackQuery, state: FSMContext = None):
    await MainForms.process(callback=callback, state=state)


@dp.message_handler(state=UserStates.all_states, content_types=["text"])
async def process_message(message: types.Message, state: FSMContext):
    await MainForms.process(message=message, state=state)







