import requests, time
from common.my_post import my_post

def my_get(url, headers=None):
    response = requests.get(
        url=url,
        headers=headers,
        verify=False
    )
    return response

def redfish_update_fw(bmc_ip, bmc_username, bmc_password, session_api, \
                    localFile_upload_api, file_path, \
                    update_api, update_target, ImageURI, \
                    task_api):
    # 1、先获取x-auth-token
    session_request_body = {
        "UserName": bmc_username,
        "Password": bmc_password
    }
    session_api = session_api.replace("ip", bmc_ip)
    post_result = my_post(session_api, session_request_body).json()
    token = post_result.get('Oem').get('Public').get('X-Auth-Token')
    print(f"获取token成功")

    # 2、上传FW文件到BMC OS下
    headers = {
        'X-Auth-Token': token
    }
    localFile_upload_api = localFile_upload_api.replace('ip', bmc_ip)
    with open(file_path, 'rb') as f:
        files = {
            'fwimage': f
        }
        my_post(localFile_upload_api, headers=headers, files=files)
        print(f"上传fw文件成功")
    
    # 3、更新BMC FW
    request_body = {
        "Targets":[
            update_target
        ],
        "ImageURI": ImageURI,
        "SaveConfig": True
    }
    update_api = update_api.replace('ip', bmc_ip)
    response = my_post(update_api, request_body=request_body, headers=headers)

    # 4、查看更新进度
    task_num = response.json().get("Name").split(' ')
    task_num = task_num[-1]
    task_api = task_api.replace('ip', bmc_ip)
    task_api = task_api.replace('task_num', task_num) 
    while my_get(task_api, headers=headers).json().get("PercentComplete") < 100:
        print(f"\rBMC固件更新中：{my_get(task_api, headers=headers).json().get("PercentComplete")} %", \
            end='', flush=True)
    print('\r')

    # 5、更新成功
    print("\r<--BMC固件成功更新-->")

    # 6、验证BMC是否恢复
    time.sleep(30)
    print("等待BMC恢复中...")
    from pythonping import ping
    def ping_with_pythonping(ip, count=3, timeout=1):
        result = ping(target=ip, count=count, timeout=timeout, verbose=True)
        # 检查至少有一个回复
        return result.success()
    time_wait, attempt = 10, 0
    while ping_with_pythonping(ip=bmc_ip) is False and attempt < (600/time_wait):
        time.sleep(time_wait)
    if attempt < (600/time_wait):
        print("BMC恢复成功")
        return True
    else:
        print("BMC恢复时间超时")
        return False

