from termcolor import colored
import requests
import json
import datetime
import sys

JSESSIONID = ''
cookies = {
    'JSESSIONID': '{}'.format(JSESSIONID)
}

headers = {
    'User-Agent': '',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.5',
    'X-CSRF-TOKEN': '',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://mytimetable.leeds.ac.uk/m/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

time = (datetime.datetime.today()).strftime('%Y-%m-%dT00:00:00.000+01:00')
params = {
    'start': '{}'.format(time),
    'limit': '50',
}

numberOfDays = 0

if len(sys.argv) > 1:
    numberOfDays = sys.argv[1]
else:
    numberOfDays = input('Days: ')

try:
    numberOfDays = int(numberOfDays)
    assert numberOfDays > 0
except AssertionError:
    print("Error {}: number must be greater than 0".format(numberOfDays))
    exit(0)
except ValueError:
    print("Error {}: must be a number".format(numberOfDays))
    exit(0)

response = requests.get('https://mytimetable.leeds.ac.uk/m/api/timetable', params=params, cookies=cookies,
                        headers=headers)
with open("studentWithPrettyPrint3.json", "w") as write_file:
    json.dump(response.json(), write_file, indent=4, sort_keys=True)

epoch_time = response.json()['data'][0]['startDate'] / 1000
date_time = datetime.datetime.fromtimestamp(epoch_time)

dates = []

# implement so you can ask for lots and it will keep making requests until you are done


for x in response.json()['data']:
    epoch_time = x['startDate'] / 1000
    date_time = datetime.datetime.fromtimestamp(epoch_time)
    repDateTime = datetime.datetime.fromtimestamp(epoch_time).replace(hour=0, minute=0, second=0)
    if repDateTime not in dates:
        dates.append(repDateTime)
        if len(dates) > numberOfDays:
            break
        print(date_time.strftime("%a %d %b:"))
    if len(dates) <= numberOfDays:
        print(colored(date_time.strftime("%H:%M:"), 'red'), end=' ')
        print(colored(x['name'], 'blue'), end=' ')
        print(colored('in ' + x['locations'][0]['name'], 'green'))
