import requests
base_url = "http://127.0.0.1:5000/"

# Så här ger man parametrar tille en api.
# Skicka data som dict enligt rad nedan.

data = {'rpm': 10, 'kmh': 980, 'throttle': 9800, 'water': 980, 'oiltemp': 980, 'load': 980}

response = requests.patch(base_url + "measurements/data1", data)
print(response.json())
input()
response = requests.get(base_url + "measurements/data1")
print(response.json())

