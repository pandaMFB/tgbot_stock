# import json
# import requests
# from time import sleep
#
# index_names_dict = {}
# index_name_moex_list = []
# index_moex_list = []
#
# #перебор индексов списка биржи
# for i in range(0, 5214, 1):
#   url_all_index = f"https://iss.moex.com/iss/securities.json?engine=stock&market=shares&limit=1&securities.columns=secid,shortname&iss.meta=off&start={i}"
#   response_url_all_index = requests.request("GET", url_all_index)
#   items_index = json.loads(response_url_all_index.text)
#
#   for el in items_index['securities']['data']:
#     index_stock = el[0]
#     name_stock = el[1]
#     index_names_dict[index_stock] = name_stock
#     index_name_moex_list.append(name_stock)
#     index_moex_list.append(index_stock)
#
# with open('all_index_moex.txt', 'w') as file:
#   for key, val in index_names_dict.items():
#     file.write('{}:{}\n'.format(key, val))
#
# with open('all_index_moex_list.txt', 'w') as file:
#   for line in index_moex_list:
#     file.write(f'{line}\n')
#
# with open('all_index_name_moex_list.txt', 'w') as file:
#   for line in index_name_moex_list:
#     file.write(f'{line}\n')
