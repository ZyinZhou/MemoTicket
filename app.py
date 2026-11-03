from flask import Flask, request, jsonify
from flask_cors import CORS  # 新增：解决跨域
import pyodbc
from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer  # 新增：生成Token

app = Flask(__name__)
# 解决跨域问题，允许前端所有请求（包含 OPTIONS 预检请求）
CORS(app, supports_credentials=True)

# 用于生成 Token 的秘钥（实际项目要放环境变量，这里写死）
app.config['SECRET_KEY'] = 'memo_ticket_secret_key_123'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ================= 数据库连接配置 =================
DB_CONFIG = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=InterestDB;'
    'UID=sa;'
    'PWD=JohnTitor488;'  # <--- 改成你的密码
)

def get_db_connection():
    return pyodbc.connect(DB_CONFIG)

# ================= 1. 预设兴趣查询接口 =================
@app.route('/api/interests', methods=['GET'])
def get_interests():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT InterestId, Name FROM Interests")
        rows = cursor.fetchall()
        # 返回中文，防止 unicode 转义 (ensure_ascii=False)
        return jsonify({"code": 200, "data": [{"id": r.InterestId, "name": r.Name} for r in rows]}), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 2. 用户注册接口 =================
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    interest_ids = data.get('interests', [])

    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    pw_hash = pbkdf2_sha256.hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (Username, PasswordHash) OUTPUT INSERTED.UserId VALUES (?, ?)", 
            (username, pw_hash)
        )
        new_user_id = cursor.fetchone()[0]
        
        for i_id in interest_ids:
            cursor.execute(
                "INSERT INTO UserInterests (UserId, InterestId) VALUES (?, ?)",
                (new_user_id, i_id)
            )
        
        conn.commit()
        return jsonify({"code": 200, "msg": "注册成功"}), 200

    except pyodbc.IntegrityError:
        return jsonify({"code": 400, "msg": "用户名已存在"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 3. 用户基础登录接口 =================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"code": 400, "msg": "用户名和密码不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT UserId, PasswordHash FROM Users WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"code": 400, "msg": "用户名或密码错误"}), 400

        user_id, pw_hash = row
        if pbkdf2_sha256.verify(password, pw_hash):
            # 登录成功，生成 Token（有效期 24 小时）
            token = serializer.dumps({"user_id": user_id})
            
            # ⚠️ 注意这里：多返回了一个 token 字段
            return jsonify({
                "code": 200, 
                "msg": "登录成功", 
                "user_id": user_id,
                "token": token 
            }), 200
        else:
            return jsonify({"code": 400, "msg": "用户名或密码错误"}), 400

    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 4. 票根管理接口（E） =================
from ticket_api import ticket_bp
app.register_blueprint(ticket_bp)

if __name__ == '__main__':
    app.run(debug=True, port=5000)