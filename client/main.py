import requests

r = requests.post("http://127.0.0.1:5000/", data={'foo': 'bar'})
print(r.json())

s = requests.put("http://127.0.0.1:5000/", data={'foo': 'bar'})
print(s.json())
