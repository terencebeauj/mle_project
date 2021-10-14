import requests
import os

api_adddress = "fastapi_container"
api_port = "8000"
patient = "0"
username = os.environ.get("username")
password = os.environ.get("password")
params = {"user": username, "password": password}

r = requests.get(url=f"http://{api_adddress}:{api_port}/duration/{patient}", params=params)
status_code = r.status_code
if status_code == 200:
    test_status = "SUCCESS"
else:
    test_status = "FAILURE"
response = r.json()["score"]

output = f"""
==========
Duration Test
==========

requests done at "/duration/{patient}"

==> {test_status}

expected result must be >= 0
actual result is: {response}
"""

print(output)

if os.environ.get("LOG") == "1":
    with open("/home/logs/api_test.log", "a") as file:
        file.write(output)
