import requests

#url = 'http://naver.com'
#rest_api_supporter.utils.get(url, json=payload) #json=사전
#rest_api_supporter.utils.get(url, data=json.dumps(payload)) #data=json 문자열
def get(url, headers=None, timeout=60, return_json=True):
    response = requests.get(url, headers=headers, timeout=timeout)
    if return_json:
        response = response.json()
    return response
