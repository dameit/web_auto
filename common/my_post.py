import requests
import urllib3

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def my_post(api, request_body=None, headers=None, files=None):
    try:
        response = requests.post(
            url=api,
            json=request_body,
            headers=headers,
            files=files,
            verify=False
        )
        return response
    
    except Exception as e:
        print(f"请求异常:{e}")