import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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



def check_statistic():
    list_user_report = []
    users_report = {}
    general_report = {}
    company_profit_report = {}

    company_profit_report = {}
    for items in trades_list:
        user = items['telegram_id']
        list_user_report.append(user)
    for user in set(list_user_report):
        sum = 0
        for items in trades_list:
            if items['telegram_id'] == str(user):
                sum = sum + float(items['realizedPnl'])
        users_report[str(user)] = round(sum, 2)

    for items in users_report:
        for it in users_list:
            if it['telegram_id'] == str(items):
                if users_report[str(items)]>0:
                    company_profit_report[str(items)] = round(float(users_report[str(items)]) * float(it['commission_percent']) / 100, 2)
                general_report[str(items)] = round(float(users_report[str(items)]) * (100 - float(it['commission_percent'])) / 100, 2)

    for items in referrals_list:
        items['referral_bonus'] = float(0)
        for it in company_profit_report:
            if items['telegram_id'] == str(it):
                items['referral_bonus'] = float(company_profit_report[str(it)]) * 0.05





# ------------Таблица зароботок по пользователям

    from tabulate import tabulate

    tb_trades = pd.DataFrame(trades_list)
    pdtabulate = lambda tb_trades: tabulate(tb_trades, headers='keys', tablefmt='psql')
    print(pdtabulate(tb_trades))

    tb_user_list = pd.DataFrame(users_list)
    pdtabulate = lambda tb_user_list: tabulate(tb_user_list, headers='keys', tablefmt='psql')
    print(pdtabulate(tb_user_list))



    

# ------------Гистограма зароботок по пользователям
    user_id = list(users_report.values())
    sum = list(users_report.keys())

    plt.style.use('ggplot')
    plt.title('Общий заработок по пользователям ')
    plt.xlabel('(dollar) $')
    plt.ylabel('user')

    plt.barh(sum, user_id)
    plt.show()
# ------------Гистограма зароботок компании
    user_id_comis=list(company_profit_report .keys())
    money_comis = list(company_profit_report .values())

    plt.title('Общий зароботок компании по пользователям ')
    plt.xlabel('(dollar) $')
    plt.ylabel('user')

    plt.barh(user_id_comis, money_comis)
    plt.show()
# ------------Чистый заработок юзеров
    user_id_sal=list(general_report.keys())
    money_sal = list(general_report.values())

    plt.title('Чистый заработок пользователей')
    plt.xlabel('(dollar) $')
    plt.ylabel('user')

    plt.barh(user_id_sal, money_sal)
    plt.show()

# ------------Реферальные бонусы
    from_user = []

    ref_bonus=[]
    for item in referrals_list:
        from_user.append(item['from_telegram_id'])

    for item in referrals_list:
        ref_bonus.append(item['referral_bonus'])

    plt.title('Реферальные бонусы')
    plt.xlabel('(dollar) $')
    plt.ylabel('user')

    plt.barh(from_user, ref_bonus)
    plt.show()

check_statistic()

