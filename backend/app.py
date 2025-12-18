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
    os.makedirs(file_upload_path, exist_ok=True)
    file = request.files.get('file')
    
    try:
        # 拼接文件保存的完整路径（目录+原文件名）
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        # 保存文件到服务器本地
        file.save(file_path)
        # 返回成功响应（包含文件保存路径）
        return jsonify({
            "code": 0,
            "msg": "文件上传成功",
            "server_path": file_path  # 返回服务器上的保存路径
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 2,
            "msg": f"文件上传失败：{str(e)}"
        }), 500
    
