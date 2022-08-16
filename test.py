import requests
import csv
url = 'http://localhost:8000/users/files/measurements/?building=Inspehtorinkatu 1_A'

mycsv = r'C:\\Users\\Nicho\\Documents\\testData\\test.csv'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJuaWNrbmF2OTgiLCJleHAiOjE2NTkzNDQwMjd9.8uNx3DRyQ24BvhWqAZ1r4gBEfaOs5jDAdl-o8bPx_60'


with open(mycsv, 'rb') as f:
    r = requests.post(url, files={'file': ('test.csv', f, 'text/csv')}, headers={'Authorization': 'Bearer ' + token})
    print(r.text)

