from aiogram.enums import ParseMode
from aiogrambot.base.main.core import async_engine
from aiogrambot.base.main.models import users_table
from aiogrambot.logs import logger
from aiogrambot.main import bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


def register_handlers(dp):
    @dp.message(Command("start"))
    async def cmd_start(message: Message):
        user_id = message.from_user.id
        async with async_engine.connect() as conn:
            query = users_table.select().where(users_table.c.user_id == user_id)
            result = await conn.execute(query)
            row = result.fetchone()
            if row is not None:
                await MainMenu.main_menu_letter(message)
            else:
                builder = InlineKeyboardBuilder()
                builder.add(InlineKeyboardButton(
                    text="Нажмите на кнопку, если готовы продолжить ✅",
                    callback_data="message_second",
                )
                )
                reply_message = await message.answer(
                    "Здравствуйте, рады вас видеть",
                    reply_markup=builder.as_markup(),
                )
                dp['initial_message_id'] = reply_message.message_id

    @dp.callback_query(lambda query: query.data == 'message_second')
    async def process_age_selection(callback: CallbackQuery):
        user_id = callback.from_user.id
        username = callback.from_user.first_name
        async with async_engine.connect() as conn:
            stmt = users_table.insert().values(
                username=username,
                user_id=user_id,
            )
            await conn.execute(stmt)
            await conn.commit()

        await callback.answer(f"Вы успешно прошли регистрацию")
        await bot.delete_message(chat_id=callback.message.chat.id, message_id=dp['initial_message_id'])
        await MainMenu.main_menu_letter_query(callback)

    @dp.callback_query(lambda query: query.data == 'Menu')
    async def handle_main_menu_callback(query: CallbackQuery):
        await query.answer("Вы вернулись в главное меню", show_alert=False)

        try:
            await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        except Exception as err:
            logger.info(f"start.py - Ошибка при удалении сообщения: {err}")

        await MainMenu.main_menu_letter_query(query)


class MainMenu:
    @staticmethod
    async def main_menu_letter(message: Message):
        builder = InlineKeyboardBuilder()
        but_first = InlineKeyboardButton(text="☰ Главное меню", callback_data="Menu")
        but_second = InlineKeyboardButton(text="🎥 RuTUBE", callback_data="RuTUBE")
        but_third = InlineKeyboardButton(text="📋 Инфо", callback_data="Info")
        builder.row(but_first, but_second, but_third, width=2)
        user_id = message.from_user.id
        username = message.from_user.first_name

        await bot.send_message(chat_id=message.chat.id,
                               text=f" 📕 *Главное меню* `{username}` \n "
                                    f"Ваш ID: `{user_id}` \n ",
                               reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)

    @staticmethod
    async def main_menu_letter_query(callback: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but_first = InlineKeyboardButton(text="☰ Главное меню", callback_data="Menu")
        but_second = InlineKeyboardButton(text="🎥 RuTUBE", callback_data="RuTUBE")
        but_third = InlineKeyboardButton(text="📋 Инфо", callback_data="Info")
        builder.row(but_first, but_second, but_third, width=2)
        user_id = callback.from_user.id
        username = callback.from_user.first_name

        await bot.send_message(chat_id=callback.message.chat.id,
                               text=f" 📕 *Главное меню* `{username}` \n "
                                    f"Ваш ID: `{user_id}` \n ",
                               reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
