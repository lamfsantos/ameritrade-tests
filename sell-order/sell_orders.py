import requests
import json

account_id = "123"
refresh_token = 'aaaaa'
ameritrade_api_callback = "https://localhost"

def refresh_ameritrade_token(refresh_token: str):
	url = r'https://api.tdameritrade.com/v1/oauth2/token'

	headers = {
		"Content-type":"application/x-www-form-urlencoded"
	}

	payload = {
		"grant_type": "refresh_token",
		"refresh_token": refresh_token,
		"client_id": "AAAAAA",
		"redirect_uri": ameritrade_api_callback
	}

	authReply = requests.post(url, headers= headers, data= payload)

	decoded_content = authReply.json()
	return(decoded_content)

def place_order_payload(symbol: str, quantity: str, instruction:str):
	payload = {
	  "orderType": "MARKET",
	  "session": "NORMAL",
	  "duratio": "DAY",
	  "orderStrategyType": "SINGLE",
	  "orderLegCollection": [
	    {
	      "instruction": instruction,
	      "quantity": quantity,
	      "instrument": {
	        "symbol": symbol,
	        "assetType": "EQUITY"
	      }
	    }
	  ]
	}

	return json.dumps(payload)

def place_order(symbol:str):
	#accound_id = service_ameritrade.get_account_id(user)
	access_token = refresh_ameritrade_token(refresh_token)['access_token']

	place_order_link = "https://api.tdameritrade.com/v1/accounts/" + account_id + "/orders"

	headers = {
	    "Content-type": "application/json",
	    "Authorization": "Bearer " + access_token.strip(),
	}

	payload = place_order_payload(symbol, str(1), "SELL")

	#print(place_order_link)
	#print("\n")
	#print(headers)
	#print("\n")
	#print(payload)
	#print("\n")

	authReply = requests.post(place_order_link, headers=headers, data=payload)

	decoded_content = authReply #.json()

	return decoded_content
	#return ":)"

if __name__ == '__main__':
	response = place_order("ZNGA")
	print(response)
	print(response.text)

	#x = refresh_ameritrade_token(refresh_token)['access_token']
	#print(x)