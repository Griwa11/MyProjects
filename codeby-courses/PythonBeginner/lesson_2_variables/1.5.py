car_price = 11000
bank_deposit = 0.25
money_spent = 0.15

cash_total = car_price/0.25
cash_bank_deposit = cash_total*bank_deposit
cash_money_spent = cash_total*money_spent

cash_left = cash_total - car_price - cash_bank_deposit - cash_money_spent

print('$', cash_left, '- осталось у Пети')