from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BadRequest

from config import CONFIG
from loader import bot
from states.users import UserStates
import openai

main_cb = CallbackData("main", "target", "action", "id", "editId")


class MainForms:
    @staticmethod
    async def back_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Назад",
                                         callback_data=main_cb.new("MainForm", "get_MainForm", 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def mainForm_ikb() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Задать вопрос",
                                         callback_data=main_cb.new("Question", "get_Question", 0, 0)
                                         )
                ]
            ]
        )

    @staticmethod
    async def process(callback: CallbackQuery = None, message: Message = None, state: FSMContext = None) -> None:
        if callback:
            if callback.data.startswith("main"):
                data = main_cb.parse(callback_data=callback.data)
                if data.get("target") == "MainForm":
                    if data.get("action") == "get_MainForm":
                        await state.finish()
                        await callback.message.edit_text(text="Главное меню",
                                                         reply_markup=await MainForms.mainForm_ikb()
                                                         )

                elif data.get("target") == "Question":
                    if data.get("action") == "get_Question":
                        await callback.message.edit_text(text="Введите ваш вопрос",
                                                         reply_markup=await MainForms.back_ikb()
                                                         )
                        await UserStates.Text.set()

        if message:
            await message.delete()

            try:
                await bot.delete_message(
                    chat_id=message.from_user.id,
                    message_id=message.message_id - 1
                )
            except BadRequest:
                pass

            if state:
                if await state.get_state() == "UserStates:Text":
                    await message.answer(text="Подожди немного сейчас я обработаю вопрос")
                    openai.api_key = CONFIG.OPENAI
                    response = openai.Completion.create(
                        model="text-davinci-003",
                        prompt=message.text,
                        temperature=0.7,
                        max_tokens=256,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )
                    await message.answer(text=response['choices'][0]['text'])