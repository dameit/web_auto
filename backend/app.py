from inspect import cleandoc
from operator import is_
from flask import Flask, request, jsonify
from flask_cors import CORS  # 处理跨域请求
import mysql.connector
import hashlib
import os, sys
from common.config_read import *
from common.mysql_connect import *
from common.my_post import my_post
from common.ssh_connect import ssh_connect

global app 
app = Flask(__name__)
CORS(app)
config = ConfigRead()

def db_connect():    
    conn = MysqlConnect()
    conn = conn.get_connection()
    return conn

def read_redfish():
    return config.redfish_load()

def hash_password(password):
    """对密码进行哈希处理（生产环境应加盐）"""
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

    conn = db_connect()
    cursor = conn.cursor()

    try:
        # 1. 检查用户名是否已存在
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            return jsonify({'success': False, 'message': '用户名已存在'}), 400

        # 2. 插入新用户 (哈希密码)
        hashed_pw = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (%s, %s)
        """, (username, hashed_pw))
        conn.commit()

        return jsonify({'success': True, 'message': '注册成功'}), 201

    except Exception as e:
        conn.rollback()
        print(f"注册出错: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    if not username or not password:
        return jsonify({'success': False, 'message': '用户名和密码不能为空'}), 400

    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    try:
        # 查询用户
        cursor.execute("""
            SELECT id, username, password, 
                   bmc_ip, bmc_username, bmc_password,
                   os_ip, os_username, os_password
            FROM users WHERE username = %s
        """, (username,))
        # 读取结果集中的第一条记录
        user = cursor.fetchone()

        # 验证用户和密码
        if user and user['password'] == hash_password(password):
            # 登录成功，移除密码字段再返回用户信息
            user.pop('password')
            return jsonify({
                'success': True,
                'message': '登录成功',
                'user': user  # 包含所有用户信息（包括BMC/OS配置）
            })
        else:
            return jsonify({'success': False, 'message': '用户名或密码错误'}), 401

    except Exception as e:
        print(f"登录出错: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/api/home/bmc_save', methods=['POST'])
@app.route('/api/home/os_save', methods=['POST'])
def save_config():
    """保存BMC配置接口"""
    # 从请求体中获取数据
    data = request.get_json()
    username = data.get('username', '').strip()
    ip = data.get('ip', '').strip()
    _username = data.get('_username', '').strip()
    _password = data.get('_password', '').strip()
    print(f"用户{username}保存的配置为{ip}、{_username}、{_password}")

    if not username:
        return jsonify({'success': False, 'message': '用户名不能为空'}), 400

    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    try:
        # 插入bmc数据
        if request.path == '/api/home/bmc_save':
            cursor.execute("""
                UPDATE users 
                SET 
                bmc_ip = %s, 
                bmc_username = %s, 
                bmc_password = %s
                WHERE username = %s
            """, (ip, _username, _password, username,))
        # 插入os数据
        else:
            cursor.execute("""
                UPDATE users 
                SET 
                os_ip = %s, 
                os_username = %s, 
                os_password = %s
                WHERE username = %s
            """, (ip, _username, _password, username,))
        # 事务提交：执行UPDATE后调用 conn.commit()
        # 只有修改操作才需要事务控制和提交（commit），而查询操作（SELECT）不需要提交
        conn.commit()

        return jsonify({'success': True, 'message': '配置保存成功'}), 201

    except Exception as e:
        conn.rollback()
        print(f"配置保存出错: {e}")
        return jsonify({'success': False, 'message': '服务器内部错误'}), 500

@app.route('/api/home/os_test_connect', methods=['POST'])
@app.route('/api/home/bmc_test_connect', methods=['POST'])
def test_connect():
    # 从请求体中获取数据
    data = request.get_json()
    
    ip = data.get('ip', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if request.path == "/api/home/bmc_test_connect":
        redfish = read_redfish()
        session_post_api = redfish["session_post_api"].replace("ip", ip)
        request_body = {
            "UserName": username,
            "Password": password
        }
        print(f"BMC测试连接: api为{session_post_api}, 请求体为{request_body}")
        response = my_post(session_post_api, request_body=request_body)
        if int(response.status_code) in range(200, 210): 
            return jsonify({'success': True, 'message': 'BMC连接成功'}), 200
        else:
            return jsonify({'success': False, 'message': 'BMC连接失败'}), 400
    else:
        print(f"OS测试连接: IP为{ip}, 用户名为{username}, 密码为{password}")
        if ssh_connect(ip, username=username, password=password):
            return jsonify({'success': True, 'message': 'OS连接成功'}), 200
        else:
            return jsonify({'success': False, 'message': 'OS连接失败'}), 400

@app.route('/api/test_cases/file_upload', methods=['POST'])
def file_upload():
    file_upload_path = config.file_save_path()
    project_root = os.path.dirname(os.path.abspath(__file__))
    # 在项目根目录下创建file_upload文件夹
    file_upload_path = os.path.join(project_root, file_upload_path)
    try:
        os.makedirs(file_upload_path, exist_ok=True)
        print(f"目录已确认存在: {file_upload_path}")
    except Exception as e:
        print(f"创建目录失败: {str(e)}")
    file = request.files.get('file')
    username = request.form.get('username')

    # 验证必填字段
    if not file:
        return jsonify({
            "success": False,
            "message": "请选择文件"
        }), 400
    
    if not username:
        return jsonify({
            "success": False,
            "message": "用户名不能为空"
        }), 400
    
    try:
        # 拼接文件保存的完整路径（目录+原文件名）
        file_path = os.path.join(file_upload_path, file.filename)
        # 保存文件到服务器本地
        file.save(file_path)

        conn = db_connect()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE users 
            SET file_save_path = %s
            WHERE username = %s
        """, (file_path, username))
        conn.commit()
        # 返回成功响应（包含文件保存路径）
        return jsonify({
            "success": True,
            "message": "文件上传成功",
            "server_path": file_path  # 返回服务器上的保存路径
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"文件上传失败：{str(e)}"
        }), 500

from pages.test_syslog import *
from pages.test_snmp_trap import *
from pages.test_smtp import *
from pages.test_snmp_v1v2 import *
from pages.test_poweron_strategy import *
from pages.test_network import *
from pages.test_user_group import *
from pages.test_ldap import *
from pages.test_ad import *
from pages.test_bios import *
from pages.test_time import *
from pages.test_log import *
from pages.login import *
import base64
@app.route('/api/test_cases/start_test', methods=['POST'])
def start_test():
    # 配置字典，根据选中的配置执行相关函数
    config_dict = {
        "Syslog设置": (test_syslog, "syslog_config_auto"),
        "Trap设置": (test_snmp_trap, "snmp_trap_config_auto"),
        "SMTP设置": (test_smtp, "smtp_config_auto"),
        "SNMP V1/V2设置": (test_snmp_v1v2, "snmp_v1v2_config_auto"),
        "上电开机策略": (test_poweron_strategy, "poweron_strategy_auto"),
        "网络设置": (test_network, "network_config_auto"),
        "用户/用户组": (test_user_group, "user_group_config_auto"),
        "LDAP/E-directory": (test_ldap, "ldap_config_auto"),
        "Active Directory": (test_ad, "ad_config_auto"),
        "BIOS设置": (test_bios, "bios_config_auto"),
        "日期&时间": (test_time, "time_config_auto"),
        "日志设置": (test_log, "log_config_auto")
    }

    # 从请求体中获取数据
    data = request.get_json()
    
    ip = data.get('ip', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    test_cases = data.get('test_cases')
    is_before = data.get('is_before')

    # 创建截图保存的文件夹
    screenshot_save_path = config.screenshot_save_path()
    project_root = os.path.dirname(os.path.abspath(__file__))
    # 在项目根目录下创建screenshot_save文件夹
    screenshot_save_path = os.path.join(project_root, screenshot_save_path)
    try:
        os.makedirs(screenshot_save_path, exist_ok=True)
        print(f"目录已确认存在: {screenshot_save_path}")
    except Exception as e:
        print(f"创建目录失败: {str(e)}")

    screenshot_data_all, screenshot_name = [], []
    try:
        test_case = login_page(ip, username, password)
        shared_driver = test_case.login_auto()
        for case in test_cases:
            config_class, method_name = config_dict[case]
            # 实例化页面自动操作类
            config_instance = config_class(driver=shared_driver, is_before=is_before) if case != "日期&时间" \
                else config_class(ip, username, password, driver=shared_driver, is_before=is_before)
            # 动态获取方法并调用（getattr是核心）
            target_method = getattr(config_instance, method_name)
            shared_driver, screenshot_base64 = target_method()
            screenshot_base64 = screenshot_base64 if isinstance(screenshot_base64, list) else [screenshot_base64]
            screenshot_data_all.extend(screenshot_base64)
            screenshot_name.extend([f"{case}_截图{i+1}" for i in range(len(screenshot_base64))])
        test_case.driver_quit()
        return jsonify({
            'success': True, 
            'message': '自动配置执行成功',
            'screenshots': screenshot_data_all,
            'screenshots_name': screenshot_name
        }), 200
    except Exception as e:
        test_case.driver_quit()
        print(e)
        return jsonify({'success': False, 'message': '自动配置过程中出错'}), 400

from backend.redfish_update_fw import redfish_update_fw
@app.route('/api/test_cases/fw_update', methods=['POST'])
def fw_update():
    data = request.get_json()

    ## 从前端获取bmc_ip, bmc_username, bm_password
    bmc_ip = data.get('bmc_ip', '').strip()
    bmc_username = data.get('bmc_username', '').strip()
    bmc_password = data.get('bmc_password', '').strip()

    ## 从前端获取bmc用户名对应的FW文件存储路径
    username = data.get('username', '')
    conn = db_connect()
    cursor = conn.cursor()
    # 执行查询
    cursor.execute("""
        SELECT file_save_path
        FROM users
        WHERE username = %s
    """, (username,))  # 注意这里需要逗号，确保是元组
    # 获取查询结果
    result = cursor.fetchone()  # 获取单条记录
    if result:
        file_save_path = result[0]  # 获取第一列的值
        print(f"找到用户 {username} 的文件路径: {file_save_path}")
    else:
        file_save_path = None
        print(f"未找到用户 {username} 的记录")

    ## 从config文件中获取
    all_config = config.config_load()
    session_api = all_config.get("redfish_path", "session_post_api")
    localFile_upload_api = all_config.get("redfish_path", "local_file_upload_api")
    update_api = all_config.get("redfish_path", "bmc_file_update_api")
    update_target = all_config.get("redfish_path", "bmc_file_update_target")
    ImageURI = file_save_path.split('\\')
    ImageURI = f"/tmp/{ImageURI[-1]}"
    task_api = all_config.get("redfish_path", "task_api")
    try:
        if redfish_update_fw(bmc_ip, bmc_username, bmc_password, session_api, \
                        localFile_upload_api, file_save_path, \
                        update_api, update_target, ImageURI, \
                        task_api):
            return jsonify({
                'success': True, 
                'message': '更新BMC固件成功',
            }), 200
    except Exception as e:
        print(e)
        return jsonify({'success': False, 'message': '更新BMC固件失败'}), 400

@app.route('/api/monitor_update', methods=['POST'])
def monitor_update():
    data = request.get_json()

    # 从前端获取os_ip,os_username,os_password
    os_ip = data.get('os_ip', '').strip()
    os_username = data.get('os_username', '').strip()
    os_password = data.get('os_password', '').strip()

    is_ssh_connected, client = ssh_connect(os_ip, os_username, os_password)
    if is_ssh_connected:
        monitor_data = {}
        try:
            # 获取cpu资源信息
            # cpu占用率
            _, cpu_used, _ = client.exec_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
            cpu_used = cpu_used.read().decode()
            monitor_data["cpu_used"] = cpu_used
            # cpu型号
            _, cpu_model, _ = client.exec_command("cat /proc/cpuinfo | grep \"model name\" | uniq | awk -F': ' '{print $2}'")
            cpu_model = cpu_model.read().decode()
            monitor_data["cpu_model"] = cpu_model
            # cpu核数
            _, cpu_cores, _ = client.exec_command("grep 'physical id' /proc/cpuinfo | sort -u | wc -l")
            cpu_cores = cpu_cores.read().decode()
            monitor_data["cpu_cores"] = cpu_cores
            # cpu主频
            _, cpu_frequency, _ = client.exec_command("lscpu | grep \"MHz\" | awk '{print $3}' | cut -d. -f1")
            cpu_frequency = cpu_frequency.read().decode()
            monitor_data["cpu_frequency"] = cpu_frequency

            # 获取内存资源信息
            # 内存使用率
            _, mem_used, _ = client.exec_command("free | grep Mem | awk '{printf \"%.1f\", $3/$2 * 100}'")
            mem_used = mem_used.read().decode()
            monitor_data["mem_used"] = mem_used
            # 内存总容量
            _, mem_total, _ = client.exec_command("free | grep Mem | awk '{printf \"%.1f\", $2/1024/1024}'")
            mem_total = mem_total.read().decode()
            monitor_data["mem_total"] = mem_total
            # 内存已使用容量
            _, mem_isused, _ = client.exec_command("free | grep Mem | awk '{printf \"%.1f\", $3/1024/1024}'")
            mem_isused = mem_isused.read().decode()
            monitor_data["mem_isused"] = mem_isused

            # 获取硬盘资源信息
            # 硬盘使用率
            _, disk_used, _ = client.exec_command("df -h / | awk 'NR==2 {print $5}' | cut -d'%' -f1")
            disk_used = disk_used.read().decode()
            monitor_data["disk_used"] = disk_used
            # 硬盘总容量
            _, disk_total, _ = client.exec_command("df -h / | awk 'NR==2 {print $2}' | cut -d'G' -f1")
            disk_total = disk_total.read().decode()
            monitor_data["disk_total"] = disk_total
            # 硬盘已使用容量
            _, disk_isused, _ = client.exec_command("df -h / | awk 'NR==2 {print $3}' | cut -d'G' -f1")
            disk_isused = disk_isused.read().decode()
            monitor_data["disk_isused"] = disk_isused

            # 获取硬盘并使用iostat读取硬盘读写
            # sysstat下载网址: https://sysstat.github.io/
            _, is_iostat_exist, _ = client.exec_command("which iostat")
            is_iostat_exist = is_iostat_exist.read().decode()
            if is_iostat_exist == "":
                client.exec_command("mkdir -p /root/sysstat") 
                with client.open_sftp() as sftp:
                    # 上传本地文件到远程服务器
                    remote_path = "/root/sysstat/sysstat-12.7.9.tar.gz"
                    local_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "linux_package", "sysstat-12.7.9.tar.gz")
                    sftp.put(local_file_path, remote_path)
                    print(f"文件 {local_file_path} 已成功上传到 {remote_path}")
                    # 解压并安装sysstat
                    print("开始解压sysstat...")
                    stdin, stdout, stderr = client.exec_command("cd /root/sysstat && tar -zxvf sysstat-12.7.9.tar.gz", timeout=30)
                    unpack_error = stderr.read().decode()
                    print("解压错误:", unpack_error)
                    
                    # 检查解压是否成功
                    print("开始configure...")
                    stdin, stdout, stderr = client.exec_command("cd /root/sysstat/sysstat-12.7.9 && ./configure", timeout=60)
                    configure_error = stderr.read().decode()
                    print("configure错误:", configure_error)
                    
                    # 编译
                    print("开始编译...")
                    stdin, stdout, stderr = client.exec_command("cd /root/sysstat/sysstat-12.7.9 && make", timeout=120)
                    make_error = stderr.read().decode()
                    print("make错误:", make_error)
                    
                    # 安装
                    print("开始安装...")
                    stdin, stdout, stderr = client.exec_command("cd /root/sysstat/sysstat-12.7.9 && make install", timeout=120)
                    install_error = stderr.read().decode()
                    print("install错误:", install_error)
                    
                    # 创建软连接
                    print("创建软连接...")
                    _, stdout, _ = client.exec_command("ln -sf /usr/local/bin/iostat /usr/bin/iostat")
                    link_result = stdout.read().decode()
                    print("软连接结果:", link_result)
            else:
                _, disks, _ = client.exec_command("lsblk -d -n -o NAME")
                disks = disks.read().decode()
                disks = disks.strip().split('\n')
                _, disks_info, _ = client.exec_command("iostat -h  | awk '$8 ~/^[a-z]+[0-9]+/ {printf \"%s %s %s %s %s\\n\",  $8,  $2,  $3,  $5,  $6}'")
                disks_info = disks_info.read().decode()
                disks_info = disks_info.strip().split('\n')
                disks_info_all = {}
                for disk in disks_info:
                    disk = disk.split(' ')
                    disks_info_all[disk[0]] = disk[1:]
                monitor_data["disks_info_all"] = disks_info_all
                monitor_data["disks"] = list(monitor_data["disks_info_all"].keys())
                print(monitor_data["disks_info_all"])

            # 关闭ssh连接
            client.close()

            return jsonify({
                    'success': True, 
                    'message': '更新系统资源信息成功',
                    'monitor_data': monitor_data
                }), 200

        except Exception as e:
            return jsonify({'success': False, 'message': '获取系统资源信息失败', 'error': str(e)}), 400
    else:
        return jsonify({'success':False, 'message':"连接OS失败"}), 400
