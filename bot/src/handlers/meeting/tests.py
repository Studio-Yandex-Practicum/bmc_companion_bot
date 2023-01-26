# from core.constants import BotState
# from handlers.admin.root_handlers import back_to_admin
# from telegram import ReplyKeyboardMarkup, Update
# from telegram.ext import ContextTypes, ConversationHandler
# from ui.buttons import (
#     BTN_ADD_TEST,
#     BTN_ADMIN_MENU,
#     BTN_CHANGE_TEST,
#     BTN_DELETE_TEST,
#     BTN_SHOW_TESTS,
#     BTN_TESTS_MENU,
# )
# from utils import make_message_handler, make_text_handler
#
# MENU_TESTS_SELECTING_LEVEL = "MENU_TESTS_SELECTING_LEVEL"
# MENU_TESTS_LIST_SELECTING_LEVEL = "MENU_TESTS_LIST_SELECTING_LEVEL"
# TYPING_TEST_NAME_FOR_CHANGE_TEST = "TYPING_TEST_NAME_FOR_CHANGE_TEST"
# TYPING_TEST_ID_FOR_CHANGE_TEST = "TYPING_TEST_ID_FOR_CHANGE_TEST"
# TYPING_TEST_ID_FOR_DELETE_TEST = "TYPING_TEST_ID_FOR_DELETE_TEST"
# TYPING_CONFIRM_FOR_DELETE_TEST = "TYPING_CONFIRM_FOR_DELETE_TEST"
#
# CREATING_NEW_TEST = "CREATING_NEW_TEST"
#
# SCRIPT_CREATING_NEW_TEST, SCRIPT_CHANGE_TEST, SCRIPT_DELETE_TEST = range(3)
#
#
# async def menu_tests(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     text = "Раздел редактирования тестов"
#     buttons = [
#         [BTN_SHOW_TESTS, BTN_ADD_TEST],
#         [BTN_ADMIN_MENU],
#     ]
#     keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
#
#     await update.message.reply_text(text, reply_markup=keyboard)
#
#     return MENU_TESTS_SELECTING_LEVEL
#
#
# async def menu_tests_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     text = "Список всех тестов:"
#
#     # TODO: получить и вывести все тесты в формате
#     #  НомерПоПорядку. Название теста (id)
#     #  Например:
#     #   1. Тест о наличии НДО (99)
#     #   2. Токсичные ли у вас родители (100)
#
#     buttons = [
#         [BTN_ADD_TEST, BTN_CHANGE_TEST, BTN_DELETE_TEST],
#         [BTN_TESTS_MENU],
#     ]
#     keyboard = ReplyKeyboardMarkup(buttons, one_time_keyboard=True)
#
#     await update.message.reply_text(text, reply_markup=keyboard)
#
#     return MENU_TESTS_LIST_SELECTING_LEVEL
#
#
# def ask_for_input_test_id(script: int = SCRIPT_CHANGE_TEST):
#     async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#         text = "Введите ID теста:"
#
#         await update.message.reply_text(text=text)
#
#         if script == SCRIPT_DELETE_TEST:
#             return TYPING_TEST_ID_FOR_DELETE_TEST
#
#         return TYPING_TEST_ID_FOR_CHANGE_TEST
#
#     return inner
#
#
# def ask_for_input_test_name(script: int = SCRIPT_CREATING_NEW_TEST):
#     async def inner(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#         text = "Введите новое название теста (или -, чтобы ничего не делать):"
#
#         if script == SCRIPT_CHANGE_TEST:
#             user_data = context.user_data
#             test_id = update.message.text
#
#             # TODO: найти тест по test_id
#             test = "not_none"
#             if test is not None:
#                 user_data["test"] = test
#                 await update.message.reply_text(text=text)
#                 return TYPING_TEST_NAME_FOR_CHANGE_TEST
#
#             text = f"Тест с ID {test_id} не найден"
#             await update.message.reply_text(text=text)
#
#             await menu_tests(update, context)
#
#             return MENU_TESTS_SELECTING_LEVEL
#
#         await update.message.reply_text(text=text)
#         return CREATING_NEW_TEST
#
#     return inner
#
#
# async def create_new_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     test_name = update.message.text
#
#     # TODO: создать тест с названием test_name, если такого еще нет
#     test_exists = False
#     if test_exists:
#         text = f"Тест '{test_name}' уже существует"
#     elif test_name == "-":
#         text = "Ок, я ничего не сделал"
#     else:
#         text = f"Тест '{test_name}' успешно создан"
#     await update.message.reply_text(text=text)
#
#     await menu_tests(update, context)
#
#     return MENU_TESTS_SELECTING_LEVEL
#
#
# async def change_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     # user_data = context.user_data
#     test_name = update.message.text
#
#     if test_name and test_name.strip() != "-":
#         # test = user_data["test"]
#
#         # TODO: изменить название теста на test_name
#         text = "Название теста успешно изменено!"
#     else:
#         text = "Название теста не изменилось!"
#
#     await update.message.reply_text(text=text)
#
#     await menu_tests(update, context)
#
#     return MENU_TESTS_SELECTING_LEVEL
#
#
# async def ask_confirmation_for_test_deletion(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> str:
#     user_data = context.user_data
#     test_id = update.message.text
#
#     # TODO: найти тест по test_id
#     test = "not_none"
#     if test is not None:
#         user_data["test"] = test
#         text = "Вы точно хотите удалить тест? (y/n)"
#         await update.message.reply_text(text=text)
#         return TYPING_CONFIRM_FOR_DELETE_TEST
#
#     text = f"Тест с ID {test_id} не найден"
#     await update.message.reply_text(text=text)
#
#     await menu_tests(update, context)
#
#     return MENU_TESTS_SELECTING_LEVEL
#
#
# async def delete_test(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
#     user_data = context.user_data
#     test = user_data["test"]
#     confirm_deletion = update.message.text
#
#     if confirm_deletion.lower() == "y":
#         # TODO: удалить тест
#         text = f"Тест {test} удален!"
#     else:
#         text = f"Тест {test} остался без изменений. Он не удален!"
#
#     await update.message.reply_text(text=text)
#
#     await menu_tests(update, context)
#
#     return MENU_TESTS_SELECTING_LEVEL
#
#
# tests_section = ConversationHandler(
#     entry_points=[
#         make_message_handler(BTN_TESTS_MENU, menu_tests),
#     ],
#     states={
#         MENU_TESTS_SELECTING_LEVEL: [
#             make_message_handler(BTN_SHOW_TESTS, menu_tests_list),
#             make_message_handler(BTN_ADD_TEST, ask_for_input_test_name(SCRIPT_CREATING_NEW_TEST)),
#         ],
#         MENU_TESTS_LIST_SELECTING_LEVEL: [
#             make_message_handler(BTN_ADD_TEST, ask_for_input_test_name(SCRIPT_CREATING_NEW_TEST)),
#             make_message_handler(BTN_CHANGE_TEST, ask_for_input_test_id(SCRIPT_CHANGE_TEST)),
#             make_message_handler(BTN_DELETE_TEST, ask_for_input_test_id(SCRIPT_DELETE_TEST)),
#         ],
#         CREATING_NEW_TEST: [
#             make_text_handler(create_new_test),
#         ],
#         TYPING_TEST_ID_FOR_CHANGE_TEST: [
#             make_text_handler(ask_for_input_test_name(SCRIPT_CHANGE_TEST))
#         ],
#         TYPING_TEST_NAME_FOR_CHANGE_TEST: [
#             make_text_handler(change_test),
#         ],
#         TYPING_TEST_ID_FOR_DELETE_TEST: [
#             make_text_handler(ask_confirmation_for_test_deletion),
#         ],
#         TYPING_CONFIRM_FOR_DELETE_TEST: [
#             make_text_handler(delete_test),
#         ],
#     },
#     fallbacks=[
#         make_message_handler(BTN_ADMIN_MENU, back_to_admin),
#         make_message_handler(BTN_TESTS_MENU, menu_tests),
#     ],
#     map_to_parent={
#         BotState.STOPPING: BotState.MENU_ADMIN_SELECTING_LEVEL,
#     },
# )
