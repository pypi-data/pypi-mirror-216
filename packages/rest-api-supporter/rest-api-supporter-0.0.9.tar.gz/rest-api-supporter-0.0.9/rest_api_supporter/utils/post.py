import requests

#url = 'http://localhost:8000/apis/auto-bell-token-api-pynecone/api'
#payload = {'data': []}
#rest_api_supporter.utils.post(url, json=payload) #json=사전
#rest_api_supporter.utils.post(url, data=json.dumps(payload)) #data=json 문자열
def post(url, json=None, data=None, headers=None, timeout=60, return_json=True):
    response = requests.post(url, json=json, data=data, headers=headers, timeout=timeout)
    if return_json:
        response = response.json()
    return response
