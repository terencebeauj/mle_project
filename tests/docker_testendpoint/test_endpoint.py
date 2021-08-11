import requests

address = "172.50.0.2"
port = "8000"

r = requests.get(url=f"http://{address}:{port}/")
response = r.json()["response"]

output = f"""
==========
Endpoint Test
==========

requests done at "/"

result {response}
"""
print(output)
