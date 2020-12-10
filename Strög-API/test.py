import requests
base_url = "http://127.0.0.1:5000/"

# Så här ger man parametrar tille en api.
# Skicka data som dict enligt rad nedan.

response = requests.get(base_url + "measurements/data1")
print(response.json())

