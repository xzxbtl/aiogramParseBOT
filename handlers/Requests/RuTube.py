import json
from aiogram import F
from aiogram.enums import ParseMode
from aiogrambot.base.TakeInfoBase import TakeInfo
from aiogrambot.handlers.Requests.ParseHTML.ParseRuTube import Parse
from aiogrambot.handlers.start_command import MainMenu
from aiogrambot.logs import logger
from aiogrambot.main import bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton


class UserInputs:
    def __init__(self):
        self.link = {}
        self.digit = {}
        self.authors = {}


obj_user = UserInputs()


def register_handlers(dp):
    @dp.callback_query(lambda query: query.data == 'RuTUBE')
    async def process_age_selection(query: CallbackQuery):
        username = query.from_user.first_name
        builder = InlineKeyboardBuilder()
        but = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu")
        but2 = InlineKeyboardButton(text="Последний Запрос", callback_data="last_request")
        builder.row(but2, but, width=1)
        reply_message = await bot.edit_message_text(message_id=query.message.message_id,
                                                    chat_id=query.message.chat.id,
                                                    text=f"*Здравствуйте* `{username}` \n введите `ссылку` на "
                                                         f"интересующий вас канал!",
                                                    reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
        dp['first_message'] = reply_message.message_id

    @dp.callback_query(lambda query: query.data == "last_request")
    async def last_request(query: CallbackQuery):
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu")
        but2 = InlineKeyboardButton(text="Названия", callback_data=f"last_names_request")
        but3 = InlineKeyboardButton(text="👀 Просмотры", callback_data=f"last_views_request")
        but4 = InlineKeyboardButton(text="🔗 Ссылка", callback_data=f"last_links_request")
        but5 = InlineKeyboardButton(text="📝 Описание", callback_data=f"last_description_request")
        await query.answer("Вы попали в последний запрос")
        builder.row(but2, but3, but4, but5, but1, width=2)
        await bot.delete_message(chat_id=query.message.chat.id,
                                 message_id=query.message.message_id)
        await bot.send_message(chat_id=query.message.chat.id,
                               reply_markup=builder.as_markup(),
                               text=f"Вы попали в *Меню последнего запроса* \n Выберите `интересующий` вас пункт",
                               parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "last_names_request")
    async def last_names_request(query: CallbackQuery):
        user_id = query.from_user.id
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_from_last_menu")
        builder.row(but1)
        titles = await TakeInfo.select_last_video_parse_titles_by_last_author(user_id)
        if titles is None or len(titles) == 0:
            titles_str = "Запросов не было"
        else:
            titles_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(titles)])

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=builder.as_markup(),
                                    text=f"*Названия видео последнего запроса* \n \n `{titles_str}`",
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "last_views_request")
    async def last_names_request(query: CallbackQuery):
        user_id = query.from_user.id
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_from_last_menu")
        builder.row(but1)
        titles = await TakeInfo.select_last_video_parse_views_by_last_author(user_id)
        if titles is None or len(titles) == 0:
            titles_str = "Запросов не было"
        else:
            titles_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(titles)])

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=builder.as_markup(),
                                    text=f"*Количество просмотров на видео последнего запроса* \n \n `{titles_str}`",
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "last_links_request")
    async def last_names_request(query: CallbackQuery):
        user_id = query.from_user.id
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_from_last_menu")
        builder.row(but1)
        titles = await TakeInfo.select_last_video_parse_link_by_last_author(user_id)
        if titles is None or len(titles) == 0:
            titles_str = "Запросов не было"
        else:
            titles_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(titles)])

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=builder.as_markup(),
                                    text=f"Ссылки на видео последнего запроса \n \n {titles_str}",
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "last_description_request")
    async def last_names_request(query: CallbackQuery):
        user_id = query.from_user.id
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_from_last_menu")
        builder.row(but1)
        titles = await TakeInfo.select_last_video_parse_description_by_last_author(user_id)
        if titles is None or len(titles) == 0:
            titles_str = "Запросов не было"
        else:
            titles_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(titles)])

        await bot.edit_message_text(chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    reply_markup=builder.as_markup(),
                                    text=f"*Описания видео последнего запроса* \n \n `{titles_str}`",
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "back_from_last_menu")
    async def last_menu_titles(query: CallbackQuery):
        await last_request(query)

    @dp.message(F.text.startswith("https://"))
    async def take_link(message: Message):
        user_id = message.from_user.id
        obj_user.link[user_id] = message.text
        builder = InlineKeyboardBuilder()
        but = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu")
        builder.row(but)
        reply_message = await bot.edit_message_text(message_id=dp['first_message'],
                                                    chat_id=message.chat.id,
                                                    text=f"введите `количество` видео для парсинга "
                                                         f"интересующий вас канал!",
                                                    reply_markup=builder.as_markup(), parse_mode=ParseMode.MARKDOWN)
        dp['second_message'] = reply_message.message_id
        await bot.delete_message(chat_id=message.chat.id,
                                 message_id=message.message_id)

    @dp.message(F.text.isdigit())
    async def take_digit_menu(message: Message):
        user_id = message.from_user.id
        obj_user.digit[user_id] = int(message.text)
        obj = Parse(obj_user.link[user_id], obj_user.digit[user_id], user_id)
        await obj.response_database()
        try:
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu")
            but2 = InlineKeyboardButton(text="🗑 Очистить", callback_data="delete_requests")
            last_authors = await TakeInfo.get_buttons_with_last_authors(user_id)
            if last_authors is not None:
                buttons = []
                if user_id not in obj_user.authors:
                    obj_user.authors[user_id] = []

                for author in last_authors:
                    formatted_string = str(author)[1:-1].strip("'").strip("'").strip(",")
                    formatted_string = formatted_string.rstrip("'")
                    obj_user.authors[user_id].append(formatted_string)
                    button = InlineKeyboardButton(text=formatted_string,
                                                  callback_data=f"{formatted_string}_authors")
                    buttons.append(button)
                if len(buttons) >= 5:
                    del buttons[0]
                    del obj_user.authors[user_id][0]
                builder.row(*buttons, width=2)
                builder.row(but1, but2, width=2)
            else:
                builder.row(but1)
            reply_message = await bot.edit_message_text(message_id=dp['second_message'],
                                                        chat_id=message.chat.id,
                                                        parse_mode=ParseMode.MARKDOWN,
                                                        reply_markup=builder.as_markup(),
                                                        text=f"Выберите ваш последний запрос")
            await bot.delete_message(chat_id=message.chat.id,
                                     message_id=message.message_id)
            dp['third_message'] = reply_message.message_id
        except Exception as err:
            await logger.info(f"Произошла ошибка при попытке вывести последние действия {err}")

    @dp.callback_query(lambda query: query.data == "back_to_menu")
    async def back_from_main_menu(query: CallbackQuery):
        try:
            await query.answer("Вы вернулись в главное меню")
            await bot.delete_message(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id)
            await MainMenu.main_menu_letter_query(query)
        except Exception as err:
            await logger.info(f"Произошла ошибка при перемещение в главное меню {err}")

    @dp.callback_query(lambda query: query.data == "delete_requests")
    async def delete_requests(query: CallbackQuery):
        user_id = query.from_user.id
        try:
            await TakeInfo.clean_parses_info(user_id)
            await query.answer("Вы удалили свои запросы")
        except Exception as err:
            await logger.info(f"Произошла ошибка при удалении записей {err}")

    @dp.callback_query(lambda query: query.data.endswith("_authors"))
    async def menu_author(query: CallbackQuery):
        try:
            callback_data = query.data
            author_name = callback_data.replace("_authors", "")
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu_requests")
            but2 = InlineKeyboardButton(text="Названия", callback_data=f"{author_name}_names_request")
            but3 = InlineKeyboardButton(text="👀 Просмотры", callback_data=f"{author_name}_views_request")
            but4 = InlineKeyboardButton(text="🔗 Ссылка", callback_data=f"{author_name}_links_request")
            but5 = InlineKeyboardButton(text="📝 Описание", callback_data=f"{author_name}_description_request")
            builder.row(but2, but3, but4, but5, width=2)
            builder.row(but1)
            reply_message = await bot.edit_message_text(message_id=dp['third_message'],
                                                        chat_id=query.message.chat.id,
                                                        text=f"Выберите нужную вам информацию \n"
                                                             f"На интересующем вас канале",
                                                        reply_markup=builder.as_markup(),
                                                        parse_mode=ParseMode.MARKDOWN)
            dp['four_message'] = reply_message.message_id

        except Exception as err:
            await logger.info(f"Произошла ошибка при изменении сообщения {err}")

    @dp.callback_query(lambda query: query.data.endswith("_names_request"))
    async def names_request(query: CallbackQuery):
        user_id = query.from_user.id
        callback_data = query.data
        author_name = callback_data.replace("_names_request", "")
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu_requests")
        builder.row(but1)
        titles = await TakeInfo.select_video_parse_titles(user_id, author_name)
        titles_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(titles)])
        await bot.edit_message_text(text=f"*Список Названия видео* \n \n `{titles_str}`",
                                    reply_markup=builder.as_markup(),
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data.endswith("_views_request"))
    async def views_request(query: CallbackQuery):
        user_id = query.from_user.id
        callback_data = query.data
        author_name = callback_data.replace("_views_request", "")
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu_requests")
        builder.row(but1)
        views = await TakeInfo.select_video_parse_views(user_id, author_name)
        views_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(views)])
        await bot.edit_message_text(text=f"*Список просмотров на видео* \n \n `{views_str}`",
                                    reply_markup=builder.as_markup(),
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data.endswith("_links_request"))
    async def links_request(query: CallbackQuery):
        user_id = query.from_user.id
        callback_data = query.data
        author_name = callback_data.replace("_links_request", "")
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu_requests")
        builder.row(but1)
        links = await TakeInfo.select_video_parse_links(user_id, author_name)
        links_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(links)])
        await bot.edit_message_text(text=f"*Список ссылок на видео* \n \n {links_str}",
                                    reply_markup=builder.as_markup(),
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data.endswith("_description_request"))
    async def description_request(query: CallbackQuery):
        user_id = query.from_user.id
        callback_data = query.data
        author_name = callback_data.replace("_description_request", "")
        builder = InlineKeyboardBuilder()
        but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu_requests")
        builder.row(but1)
        descriptions = await TakeInfo.select_video_parse_description(user_id, author_name)
        description_str = '\n'.join([f"{i + 1}. {title[0]}" for i, title in enumerate(descriptions)])
        await bot.edit_message_text(text=f"*Список описания видео* \n \n `{description_str}`",
                                    reply_markup=builder.as_markup(),
                                    chat_id=query.message.chat.id,
                                    message_id=query.message.message_id,
                                    parse_mode=ParseMode.MARKDOWN)

    @dp.callback_query(lambda query: query.data == "back_to_menu_requests")
    async def menu_request(query: CallbackQuery):
        user_id = query.from_user.id
        link = obj_user.link[user_id]
        digit = obj_user.digit[user_id]
        obj = Parse(link, digit, user_id)
        await obj.response_database()
        try:
            builder = InlineKeyboardBuilder()
            but1 = InlineKeyboardButton(text="⏪ Назад", callback_data="back_to_menu")
            but2 = InlineKeyboardButton(text="🗑 Очистить", callback_data="delete_requests")
            last_authors = await TakeInfo.get_buttons_with_last_authors(user_id)
            if last_authors is not None:
                buttons = []
                for author in last_authors:
                    formatted_string = str(author)[1:-1].strip("'").strip("'").strip(",")
                    formatted_string = formatted_string.rstrip("'")
                    button = InlineKeyboardButton(text=formatted_string, callback_data=f"{formatted_string}_authors")
                    buttons.append(button)
                if len(buttons) >= 5:
                    del buttons[0]
                builder.row(*buttons, width=2)
                builder.row(but1, but2, width=2)
            else:
                builder.row(but1)
            reply_message = await bot.send_message(chat_id=query.message.chat.id,
                                                   parse_mode=ParseMode.MARKDOWN,
                                                   reply_markup=builder.as_markup(),
                                                   text=f"Выберите ваш последний запрос")
            await bot.delete_message(chat_id=query.message.chat.id,
                                     message_id=query.message.message_id)
            dp['third_message'] = reply_message.message_id
        except Exception as err:
            await logger.info(f"Произошла ошибка при попытке вывести последние действия {err}")
