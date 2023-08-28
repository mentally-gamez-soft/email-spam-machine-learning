import requests
s = requests.session()
s.headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}
# response = s.post("http://127.0.0.1:5000/spam-email-control/api/v1.0", json={"email": "bar"})
response = s.post("http://127.0.0.1:5000/spam-email-refine/api/v1.0/redifine-email", json={"email": "this is an email of test","classification":"0"})
print(response.status_code)
print(response.request.headers)
print(response.json())