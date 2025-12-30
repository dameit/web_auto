import requests, time
from common.my_post import my_post

def my_get(url, headers=None):
    try:
        response = requests.get(
            url=url,
            headers=headers,
            verify=False
        )
        return response
    except Exception as e:
        print(f"get请求异常: {e}")

def redfish_update_fw(bmc_ip, bmc_username, bmc_password, session_api, \
                    localFile_upload_api, file_path, \
                    update_api, update_target, ImageURI, \
                    task_api):
    # 1、先获取x-auth-token
    try:
        session_request_body = {
            "UserName": bmc_username,
            "Password": bmc_password
        }
        session_api = session_api.replace("ip", bmc_ip)
        post_result = my_post(session_api, session_request_body).json()
        token = post_result.get('Oem').get('Public').get('X-Auth-Token')
        print(f"获取token成功")
    except Exception as e:
        return f"获取token失败，错误信息为：{e}"

    # 2、上传FW文件到BMC OS下
    try:
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
    except Exception as e:
        return f"上传FW文件至BMC OS下失败，错误信息为：{e}"
    
    # 3、更新BMC FW
    try:
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
    except Exception as e:
        return f"更新BMC FW失败，错误信息为：{e}"

    # 5、更新成功
    print("\r<--BMC固件成功更新-->")

    # 6、验证BMC是否恢复
    try:
        time.sleep(5)
        print(my_post(session_api, request_body=session_request_body).status_code)
        while int(my_post(session_api, request_body=session_request_body).status_code) not in range(200, 210): 
            time.sleep(1)
        print("BMC恢复成功")
    except Exception as e:
        return f"等待BMC恢复失败，错误信息为：{e}"

