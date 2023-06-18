import requests
mydata = requests.get('http://127.0.0.1:8000/all_data/')
print(mydata.content)