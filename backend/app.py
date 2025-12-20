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
        "上电开机策略": (test_poweron_strategy, "poweron_strategy_auto")
    }

    # 从请求体中获取数据
    data = request.get_json()
    
    ip = data.get('ip', '').strip()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    test_cases = data.get('test_cases')

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

    screenshot_data_all = []
    try:
        test_case = login_page(ip, username, password)
        shared_driver = test_case.login_auto()
        for case in test_cases:
            config_class, method_name = config_dict[case]
            # 实例化页面自动操作类
            config_instance = config_class(driver=shared_driver)
            # 动态获取方法并调用（getattr是核心）
            target_method = getattr(config_instance, method_name)
            shared_driver, screenshot_base64 = target_method()
            screenshot_data_all.append(screenshot_base64)
        test_case.driver_quit()
        return jsonify({
            'success': True, 
            'message': '自动配置执行成功',
            'screenshots': screenshot_data_all
        }), 200
    except Exception as e:
        test_case.driver_quit()
        print(e)
        return jsonify({'success': False, 'message': '自动配置过程中出错'}), 400