botnet = 1000
botnet_loss = 2
botnet_add = 3
time_period = 30

result_loss = botnet - botnet_loss*time_period
result_add = botnet - botnet_loss*time_period + botnet_add*time_period

print(result_loss, 'ботов будет у Василия, если он не будет добавлять новых')
print(result_add, 'ботов будет у Василия, если он будет добавлять новых')