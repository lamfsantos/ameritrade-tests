import requests
import urllib
import json
import datetime
import pandas as pd

ameritrade_api_callback = "https://localhost/"
account_id = "12345678"

def refresh_ameritrade_token(refresh_token: str):
	url = r'https://api.tdameritrade.com/v1/oauth2/token'

	headers = {
		"Content-type":"application/x-www-form-urlencoded"
	}

	payload = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
		"client_id": "ID HERE",
		"redirect_uri": ameritrade_api_callback
	}

	authReply = requests.post(url, headers= headers, data= payload)

	decoded_content = authReply.json()
	return(decoded_content)

def get_orders(refresh_token: str):
	access_token = refresh_ameritrade_token(refresh_token)['access_token']

	today = datetime.date.today()
	year = str(today.year)

	fromEnteredTime = "fromEnteredTime=" + "2020" + "-01-01"
	toEnteredTime = "toEnteredTime=" + year + "-12-31"
	status = "status=FILLED"

	url = "https://api.tdameritrade.com/v1/accounts/"+ account_id +"/orders?"+fromEnteredTime+"&"+toEnteredTime+"&"+status

	headers = {
	    "Content-type": "application/x-www-form-urlencoded",
	    "Authorization": "Bearer " + access_token

	}

	payload={}

	authReply = requests.get(url, headers=headers, data=payload)

	decoded_content = authReply.json()

	#print(decoded_content)

	parse_decoded_content = parse_orders(decoded_content)

	return parse_decoded_content

def get_company_names(orders: list):
	symbols = ''

	for a in orders:
		symbols += (a["orderLegCollection"][0]["instrument"]["symbol"]) + ","

	symbols = symbols[:][:-1]

	url = create_companies_request_link(symbols)

	companies = request_symbol_companies(url)

	return companies

def request_symbol_companies(url):
	response = requests.request("GET", url, headers={}, data={})

	df = pd.read_json(response.text)
	df = df.transpose()

	df = df[['description', 'symbol']]

	#companies = df.values.tolist()

	return df

def save_csv(df):
	df.to_csv('result.csv', encoding='utf-8')

def create_companies_request_link(list_symbols):
	url = 'https://api.tdameritrade.com/v1/marketdata/quotes?'
	api_key = 'apikey=AAAAAAAA'
	symbol = 'symbol='+list_symbols

	url = url + api_key + "&" +symbol
	url = url.replace(" ", "")

	return url

def parse_orders(orders: list):
	return_list = []
	companies = get_company_names(orders)	

	#print(companies)


	for a in orders:
		dict_index = {}
		dict_index["stock"] = (a["orderLegCollection"][0]["instrument"]["symbol"])

		for index, row in companies.iterrows():
			if row['symbol'] == a["orderLegCollection"][0]["instrument"]["symbol"]:
				dict_index["company"] = row['description']
		
		dict_index["quantity"] = a["quantity"]	
		dict_index["quantity"] = a["orderActivityCollection"][0]["executionLegs"][0]["price"]

		return_list.append(dict_index)

	return(return_list)

if __name__ == '__main__':
	result = refresh_ameritrade_token(refresh_token)['access_token']
	print(result)