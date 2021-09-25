import requests

r = requests.post("http://127.0.0.1:5000/user/get_coins/", data={'email': 'a@ufv.br'})
print(r.json())
