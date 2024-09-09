from aiogram.types import KeyboardButton, ReplyKeyboardMarkup



def main_kb():
#/search_edition_isnb - search edition of book by isnb
#/search_work_name - search work by name
#/search_author_name - search author by name
    kb_list = [
        [KeyboardButton(text="search_edition_isnb")], 
        [KeyboardButton(text="search_work_name")],
        [KeyboardButton(text="search_author_name")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

