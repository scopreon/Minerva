from termcolor import colored
import requests
import json
import datetime

JSESSIONID = ''
cookies = {
    'JSESSIONID': '{}'.format(JSESSIONID)
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:103.0) Gecko/20100101 Firefox/103.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-GB,en;q=0.5',
    'X-CSRF-TOKEN': '948b22de-174e-450d-896b-05d4e5d74c55',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive',
    'Referer': 'https://mytimetable.leeds.ac.uk/m/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
}

params = {
    'start': '2022-10-17T00:00:00.000+01:00',
    'limit': '50',
}

numberOfDays = int(input('Days: '))

response = requests.get('https://mytimetable.leeds.ac.uk/m/api/timetable', params=params, cookies=cookies, headers=headers)
with open("studentWithPrettyPrint3.json", "w") as write_file:
    json.dump(response.json(), write_file, indent=4, sort_keys=True)

epoch_time = response.json()['data'][0]['startDate']/1000
date_time = datetime.datetime.fromtimestamp(epoch_time)

dates=[]

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
        print(colored(date_time.strftime("%H:%M:"),'red'),end=' ')
        print(colored(x['name'],'blue'), end=' ')
        print(colored('in ' + x['locations'][0]['name'],'green'))
