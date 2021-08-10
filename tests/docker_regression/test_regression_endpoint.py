import requests

api_adddress = "172.50.0.2"
api_port = "8000"
patient = "0"

r = requests.get(url=f"http://{api_adddress}:{api_port}/duration/{patient}")
response = r.json()["score"]

output = f"""
==========
Duration Test
==========

requests done at "/duration/{patient}"

expected result must be >= 0
actual result is: {response}
"""

print(output)
