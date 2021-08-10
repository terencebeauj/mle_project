import requests

api_adddress = "172.50.0.2"
api_port = "8000"
patient = "10"

r = requests.get(url=f"http://{api_adddress}:{api_port}/decision/{patient}")
response = r.json()["score"]

output = f"""
==========
Decision Test
==========

requests done at "/decision/{patient}"

expected result must be == 0 or == 1 or == 2
actual result is: {response}
"""

print(output)
