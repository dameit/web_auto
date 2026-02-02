import paramiko

def ssh_connect(ip:str, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.load_system_host_keys()
    try:
        client.connect(hostname=ip, username=username, password=password)
        return True, client
    except Exception as e:
        print(f"连接失败:{e}")
        return False