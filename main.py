import csv

with open('./data/referrals.csv') as f:
    referrals = csv.DictReader(f)
    referrals_list=[]
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

list_user_report = []
users_report={}
general_report={}

# Profit and Loss for each user
def user_report(user):
    for items in trades_list:
        user=items['telegram_id']
        list_user_report.append(user)
    for user in set(list_user_report):
        sum = 0
        for items in trades_list:
            if items['telegram_id']==str(user):
                sum=sum+float(items['realizedPnl'])
        users_report[str(user)]=round(sum, 2)
        # print(f'{str(user)} : {round(sum, 2)} ')
    print(f'Total profit {users_report}')

user_report(101151807)

company_profit_report={}
# Company profit
def company_profit(user):
    for items in users_report:
        for it in users_list:
            if it['telegram_id'] == str(items):
                company_profit_report[str(items)]=round(float(users_report[str(items)])*float(it['commission_percent'])/100, 2)
                general_report[str(items)] = round(float(users_report[str(items)]) * (100-float(it['commission_percent'])) / 100, 2)

    print(f'Company profit {company_profit_report}')
    print(f'User profit {general_report}')
    # print(company_profit_report[str(user)])

company_profit(101151807)


# with open(r'./data/referrals.csv', 'a') as f:
#     writer = csv.writer(f)
#     writer.writerow('***')


ref_list=[]
def add_refer():
    for items in referrals_list:
        items['referral_bonus'] = float(0)
        for it in company_profit_report:
            if items['telegram_id']==str(it):
                items['referral_bonus']=float(company_profit_report[str(it)])*0.05
                print(items)

    with open('./data/referrals_bonus.csv', "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(referrals_list[1].keys())

        for line in referrals_list:


            writer.writerow(line.values())

add_refer()