
import csv
import telebot
from telebot import types

bot = telebot.TeleBot('1578481362:AAGq61UVSjdhyhiMNhl7I0r38Q8akjZomxk')

chatId = 389484326

list_user_report = []
users_report = {}
general_report = {}
company_profit_report = {}

# ------------------Открываем файлы и записываем в масив

with open('./data/referrals.csv') as f:
    referrals = csv.DictReader(f)
    referrals_list = []
    for row in referrals:
        referrals_list.append(row)

with open('./data/trades.csv') as f:
    trades = csv.DictReader(f)
    trades_list = []
    for row in trades:
        trades_list.append(row)

with open('./data/users.csv') as f:
    users = csv.DictReader(f)
    users_list = []
    for row in users:
        users_list.append(row)


# -------------------Общий зароботок по каждому юзеру --------------------------------------

def user_report(user_id):
    print(user_id)
    for items in trades_list:
        user = items['telegram_id']
        list_user_report.append(user)
    for user in set(list_user_report):
        sum = 0
        for items in trades_list:
            if items['telegram_id'] == str(user):
                sum = sum + float(items['realizedPnl'])
        users_report[str(user)] = round(sum, 2)
    return users_report[str(user_id)]

# -------------------Общий зароботок компании по каждому юзеру --------------------------------------
def company_profit(user_id):
    for items in users_report:

        for it in users_list:
            if it['telegram_id'] == str(items):
                company_profit_report[str(items)] = round(
                    float(users_report[str(items)]) * float(it['commission_percent']) / 100, 2)
                general_report[str(items)] = round(
                    float(users_report[str(items)]) * (100 - float(it['commission_percent'])) / 100, 2)

    return company_profit_report[str(user_id)]

# -------------------Список % комисий по каждому юзеру --------------------------------------
def comision_persent(user_id):
    for item in users_list:
        if item['telegram_id'] == str(user_id):
            return item['commission_percent']

# -------------------Реферальные бонусы по юзерам --------------------------------------
def referal_bonus(user_id):
    for items in referrals_list:
        items['referral_bonus'] = float(0)
        for it in company_profit_report:
            if items['telegram_id'] == str(it):
                items['referral_bonus'] = float(company_profit_report[str(it)]) * 0.05
# -------------------Записываем информацию в файл --------------------------------------
    with open('./data/referrals_bonus.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(referrals_list[1].keys())

        for line in referrals_list:
            writer.writerow(line.values())

    for items in referrals_list:
        for it in users_report:
            if items['from_telegram_id'] == str(it):
                users_report[str(it)] = +items['referral_bonus']

    return users_report[str(user_id)]


msg = f' Привет друг.\n Вместе мы заработали: {user_report(389484326)} \n Благодарность для меня составляет {comision_persent(389484326)} % или {company_profit(389484326)} $ ' \
      f'\n Реферальный бонус {referal_bonus(389484326)}'

bot.send_message(chatId, text=msg)




# # ------------------------Вариант бота с кнопками ____________________________
#
# @bot.message_handler(content_types=['text'])
# def get_text_messages(message):
#
#     bot.send_message(message.from_user.id, "Привет, хочешь узнать сколько ты заработал?")
#     keyboard = types.InlineKeyboardMarkup()
#     key_yes = types.InlineKeyboardButton(text='Да!!!!', callback_data='money' )
#     keyboard.add(key_yes)
#     bot.send_message(message.from_user.id, text='***нажми да', reply_markup=keyboard)
#
# @bot.callback_query_handler(func=lambda call: True)
# def callback_worker(call):
#
#     list_user_report = []
#     users_report = {}
#     general_report = {}
#     company_profit_report = {}
#
#
#     if call.data == "money":
#         # ---------------------------------------------Open files------------
#         with open('./data/referrals.csv') as f:
#             referrals = csv.DictReader(f)
#             referrals_list = []
#             for row in referrals:
#                 referrals_list.append(row)
#
#         with open('./data/trades.csv') as f:
#             trades = csv.DictReader(f)
#             trades_list = []
#             for row in trades:
#                 trades_list.append(row)
#
#         with open('./data/users.csv') as f:
#             users = csv.DictReader(f)
#             users_list = []
#             for row in users:
#                 users_list.append(row)
#
#         # ---------------------------------------------------------
#
#         def user_report(user_id):
#             print(user_id)
#             for items in trades_list:
#                 user = items['telegram_id']
#                 list_user_report.append(user)
#             for user in set(list_user_report):
#                 sum = 0
#                 for items in trades_list:
#                     if items['telegram_id'] == str(user):
#                         sum = sum + float(items['realizedPnl'])
#                 users_report[str(user)] = round(sum, 2)
#             return users_report[str(user_id)]
#
#
#
#
#         def company_profit(user_id):
#             for items in users_report:
#
#                 for it in users_list:
#                     if it['telegram_id'] == str(items):
#
#                         company_profit_report[str(items)] = round(
#                             float(users_report[str(items)]) * float(it['commission_percent']) / 100, 2)
#                         general_report[str(items)] = round(
#                             float(users_report[str(items)]) * (100 - float(it['commission_percent'])) / 100, 2)
#
#             return company_profit_report[str(user_id)]
#
#
#         def comision_persent(user_id):
#             for item in users_list:
#                 if item['telegram_id']==str(user_id):
#                     return item['commission_percent']
#
#
#         def referal_bonus(user_id):
#
#             for items in referrals_list:
#                 items['referral_bonus'] = float(0)
#                 for it in company_profit_report:
#                     if items['telegram_id'] == str(it):
#                         items['referral_bonus'] = float(company_profit_report[str(it)]) * 0.05
#
#
#             with open('./data/referrals_bonus.csv', "w", newline='') as csv_file:
#                 writer = csv.writer(csv_file, delimiter=',')
#                 writer.writerow(referrals_list[1].keys())
#
#                 for line in referrals_list:
#                     writer.writerow(line.values())
#
#             for items in referrals_list:
#                 for it in users_report:
#                     if items['from_telegram_id']==str(it):
#
#                         users_report[str(it)]=+items['referral_bonus']
#
#             return users_report[str(user_id)]
#
#         msg = f' Привет друг.\n Вместе мы заработали: {user_report(389484326)} \n Благодарность для меня составляет {comision_persent(389484326)} % или {company_profit(389484326) } $ ' \
#               f'\n Реферальный бонус {referal_bonus(389484326)}'
#
#         # Отправляем текст в Телеграм
#         bot.send_message(call.message.chat.id, msg)



bot.polling(none_stop=True, interval=0)

