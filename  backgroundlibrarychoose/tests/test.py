import requests
import json

url = "http://10.131.129.128:8071/user/register"

payload = json.dumps({
  "username": "2016201125",
  "password": "2016201125",
  "email": "15525730080@163.com",
  "iphone": "15525730080",
  "name": "fbz"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

import requests
import json

url = "http://10.131.129.128:8071/user/login"

payload = json.dumps({
  "username": "2016201125",
  "password": "2016201125",
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


import requests

url = "http://10.131.129.128:8071/user/alluserinfo"

payload={}
headers = {
  'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjIwMTYyMDExMjUiLCJyb2xlX2lkIjoxLCJlbmRfdGltZSI6MTY0NzEwMDgwMC4wfQ._M1O_fzwfmUXKU4OTovcHmWbqelmQaWuM7t-R0qCYOk'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

import requests

url = "http://10.131.129.128:8071/user/userinfo"

payload={}
headers = {
  'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6IjIwMTYyMDExMjUiLCJyb2xlX2lkIjoxLCJlbmRfdGltZSI6MTY0NzEwMDgwMC4wfQ._M1O_fzwfmUXKU4OTovcHmWbqelmQaWuM7t-R0qCYOk'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

