import pandas as pd
import os
import requests
import json

#os.chdir(os.path.dirname(__file__))

path = os.getcwd()
path += "/symbols.csv"

def read_csv():
	df = pd.read_csv(path)

	return df

def parse_csv_to_list_of_strings(df):
	list_size = 135

	symbol = df.columns.values
	symbol = list(symbol[0])


	list_symbols = []

	for x in range(0,list_size):
		list_symbols.append("") 

	list_symbols.append(str(symbol[0]) + ",")


	df_len = len(df.index)/list_size
	df_len = round(df_len)

	for index, row in df.iterrows():
		if index <= df_len:
			list_symbols[0] += str(row['A']) + ","
		# elif index <= df_len * 2:
		# 	list_symbols[1] += str(row['A']) + ","
		# elif index <= df_len * 3:
		# 	list_symbols[2] += str(row['A']) + ","
		# elif index <= df_len * 4:
		# 	list_symbols[3] += str(row['A']) + ","
		# elif index <= df_len * 5:
		# 	list_symbols[4] += str(row['A']) + ","
		# else:
		# 	list_symbols[5] += str(row['A']) + ","

	for x in range(0,list_size):
		list_symbols[x] = list_symbols[x][:-1]

	return list_symbols[0]


def create_request_link(list_symbols):
	url = 'https://api.tdameritrade.com/v1/marketdata/quotes?'
	api_key = 'apikey=AAAAAAAA'
	symbol = 'symbol='+list_symbols

	url = url + api_key + "&" +symbol
	url = url.replace(" ", "")

	return url

def request_symbol_quotes(url):
	response = requests.request("GET", url, headers={}, data={})

	df = pd.read_json(response.text)
	df = df.transpose()

	return df

def save_csv(df, x):
	df.to_csv('result-'+ str(x+1) +'.csv', encoding='utf-8')

def filter_df_by_price(df, price):
	for index, row in df.iterrows():
		df.drop(df.index[df['bidPrice'] > 10], inplace = True)

	return df

if __name__ == '__main__':
	df = read_csv()


	result_list = []

	list_symbols = parse_csv_to_list_of_strings(df)

	#for x in range(0,6):
	url = create_request_link(list_symbols)

	df = request_symbol_quotes(url)

	print(df.to_dict('index'))

	result_list.append(df)	
	
	for x in range(0,1):
		#result_list[x] = filter_df_by_price(result_list[x], 10)

		save_csv(result_list[x], x)

	# result_list = filter_df_by_price(result_list, 10)

	# save_csv(result_list, x)
