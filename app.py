from chalice import Chalice

app = Chalice(app_name='bus-checker')


@app.route('/test')
def index():
    return {'hello': 'world'}


# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#

#from selenium import webdriver
from pyquery import PyQuery as pq
from datetime import datetime, timedelta  
import re
import requests
import json

@app.route('/{stop}', methods=['GET'])
def on_start(stop):
	#stop = input("Enter your bus stop: ")
	# deviceID = request.args.get('deviceID', None)
	# consentToken = request.args.get('consentToken', None)
	# stop = request.args.get('stop', None)
	#return [deviceID, consentToken, stop]
	url = "https://ltp.umich.edu/transit/BB.php"
	resp = requests.get(url)
	doc = pq(resp.text)
	for item in doc.find('.main table').eq(1).find('tr').items():
		if item.find("td").eq(1).text() == " ".join(stop.split("+")):
			print(stop)
			url = item.find("a").attr("href")
			break
	#stop = "+".join(stop.split())
	#location = '1770+Broadway+Street'
	# deviceID = request_json["deviceID"]
	# consentToken = request_json["consentToken"]
	#deviceID, consentToken
	#print(deviceID, consentToken)
	location = '+'.join(get_alexa_location().split())
	doc = pq(requests.get(url).text)
	url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='+ location + '&destinations='
	url += stop + '&mode=walking&key=AIzaSyBRJAYtJKPN0oRlWSz0dYOtB_OBEfcXi8I'
	print(url)
	data = requests.get(url).json()
	travel_time = round(data['rows'][0]['elements'][0]['duration']['value']/60)
	
	next_time = re.search('([0-9]*):([0-9]*) ([ap]).m', doc.find(".r2").eq(0).find('td').eq(1).text())
	if next_time is None:
		return {"can_catch": False, "time_to_walk": None, "next_bus_time": None}
	hour = int(next_time.group(1)) if next_time.group(3) == 'a' else int(next_time.group(1)) + 12
	minutes = int(next_time.group(2))

	if (datetime.now() - timedelta(hours=5)).hour * 60 + datetime.now().minute + travel_time < hour * 60 + minutes:
		return {"can_catch": True, "time_to_walk": travel_time, "next_bus_time": [hour, minutes], "datetime_now": [(datetime.now() - timedelta(hours=5)).hour, datetime.now().minute]}
	else:
		for i in range(2, 5):
			second_bus = re.search('([0-9]*):([0-9]*) ([ap]).m', doc.find(".r2").eq(0).find('td').eq(i).text())
			hour = int(second_bus.group(1)) if second_bus.group(3) == 'a' else int(second_bus.group(1)) + 12
			if (datetime.now() - timedelta(hours=5)).hour * 60 + datetime.now().minute + travel_time < hour * 60 + int(second_bus.group(2)):
				return {"can_catch": False, "time_to_walk": travel_time, "next_bus_time": [int(second_bus.group(1)), int(second_bus.group(2))], "datetime_now": [(datetime.now() - timedelta(hours=5)).hour, datetime.now().minute]}
	
	# if datetime.now().hour*60 + datetime.now().minute + travel_time < hour * 60 + minutes:
    #     return {"can_catch": True, "time_to_walk": travel_time, "next_bus_time": [hour, minute]}
	# else:
    #     second_bus = re.search('([0-9]*):([0-9]*) ([ap]).m', doc.find(".r2").eq(0).find('td').eq(2).text())
    #     return {"can_catch": False, "time_to_walk": travel_time, "next_bus_time": [second_bus.group(0), second_bus.group(1)]}
	

def get_alexa_location():
	return "1770 Broadway Street"
	# URL =  "https://api.amazonalexa.com/v1/devices/{}/settings" \
	# 		"/address".format(deviceID)
	# TOKEN =  consentToken
	# HEADER = {'Accept': 'application/json',
	# 			'Authorization': 'Bearer {}'.format(TOKEN)}
	# r = requests.get(URL, headers=HEADER)
	
	# if r.status_code == 200:
	# 	return(r.json()["addressLine1"])
	# else:
	# 	return "Invalid request"

#on_start()
