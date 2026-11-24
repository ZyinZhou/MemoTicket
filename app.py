from flask import Flask, request, jsonify
from flask_cors import CORS
import pyodbc
from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps

app = Flask(__name__)
CORS(app, supports_credentials=True)

# 秘钥
app.config['SECRET_KEY'] = 'memo_ticket_secret_key_123'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# ================= 数据库连接配置 =================
DB_CONFIG = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost\\SQLEXPRESS;'
    'DATABASE=InterestDB;'
    'UID=sa;'
    'PWD=JohnTitor488;'
)

def get_db_connection():
    return pyodbc.connect(DB_CONFIG)

# ================= 身份认证装饰器 =================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({"code": 401, "msg": "未登录或缺少 Token"}), 401
            
        token = auth_header.split(" ")[1]
        
        try:
            data = serializer.loads(token, max_age=86400) # 24小时过期
            user_id = data['user_id']
            token_nonce = data.get('nonce')
        except SignatureExpired:
            return jsonify({"code": 401, "msg": "登录已过期，请重新登录"}), 401
        except BadSignature:
            return jsonify({"code": 401, "msg": "无效的 Token"}), 401
        except Exception:
            return jsonify({"code": 401, "msg": "Token 验证失败"}), 401

        # 校验 nonce（防止退出后旧 token 还能用）
        if token_nonce:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT TokenNonce FROM Users WHERE UserId = ?", (user_id,))
            row = cursor.fetchone()
            conn.close()
            
            if not row or row[0] != token_nonce:
                return jsonify({"code": 401, "msg": "登录已失效，请重新登录"}), 401
                
        return f(user_id, *args, **kwargs)
    return decorated

# ================= 1. 预设兴趣查询接口 =================
@app.route('/api/interests', methods=['GET'])
def get_interests():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 只返回预设兴趣
        cursor.execute("SELECT InterestId, Name FROM Interests WHERE IsPreset = 1")
        rows = cursor.fetchall()
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
            cursor.execute("INSERT INTO UserInterests (UserId, InterestId) VALUES (?, ?)", (new_user_id, i_id))
        
        conn.commit()
        return jsonify({"code": 200, "msg": "注册成功"}), 200

    except pyodbc.IntegrityError:
        return jsonify({"code": 400, "msg": "用户名已存在"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 3. 用户登录接口 =================
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
        # 把 TokenNonce 也查出来
        cursor.execute("SELECT UserId, PasswordHash, TokenNonce FROM Users WHERE Username = ?", (username,))
        row = cursor.fetchone()

        if not row:
            return jsonify({"code": 400, "msg": "用户名或密码错误"}), 400

        user_id, pw_hash, token_nonce = row
        if pbkdf2_sha256.verify(password, pw_hash):
            # 生成 Token，把 nonce 塞进去
            token = serializer.dumps({"user_id": user_id, "nonce": token_nonce})
            
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

# ================= 4. 退出登录接口 =================
@app.route('/api/logout', methods=['POST'])
@token_required
def logout(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # 更新 nonce，让旧的 Token 立刻作废
        cursor.execute("UPDATE Users SET TokenNonce = CONVERT(NVARCHAR(64), NEWID()) WHERE UserId = ?", (user_id,))
        conn.commit()
        return jsonify({"code": 200, "msg": "已退出登录"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 5. 获取个人信息 =================
@app.route('/api/user/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Username, Nickname, AvatarUrl, Bio FROM Users WHERE UserId = ?", (user_id,))
        row = cursor.fetchone()
        if row:
            return jsonify({
                "code": 200,
                "data": {
                    "username": row[0],
                    "nickname": row[1],
                    "avatar_url": row[2],
                    "bio": row[3]
                }
            }), 200
        return jsonify({"code": 404, "msg": "用户不存在"}), 404
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 6. 修改个人信息 =================
@app.route('/api/user/profile', methods=['PUT'])
@token_required
def update_profile(user_id):
    data = request.get_json()
    nickname = data.get('nickname')
    avatar_url = data.get('avatar_url')
    bio = data.get('bio')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Users SET Nickname = ?, AvatarUrl = ?, Bio = ?, UpdatedAt = GETDATE() WHERE UserId = ?",
            (nickname, avatar_url, bio, user_id)
        )
        conn.commit()
        return jsonify({"code": 200, "msg": "个人信息更新成功"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 7. 搜索兴趣 =================
@app.route('/api/interests/search', methods=['GET'])
def search_interests():
    q = request.args.get('q', '')
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT InterestId, Name FROM Interests WHERE Name LIKE ?", (f'%{q}%',))
        rows = cursor.fetchall()
        return jsonify({"code": 200, "data": [{"id": r.InterestId, "name": r.Name} for r in rows]}), 200
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 8. 创建自定义兴趣 =================
@app.route('/api/interests', methods=['POST'])
@token_required
def create_interest(user_id):
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"code": 400, "msg": "兴趣名称不能为空"}), 400
        
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Interests (Name, IsPreset, CreatedBy) OUTPUT INSERTED.InterestId VALUES (?, 0, ?)", 
            (name, user_id)
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
        return jsonify({"code": 200, "msg": "创建成功", "interest_id": new_id}), 200
    except pyodbc.IntegrityError:
        return jsonify({"code": 400, "msg": "该兴趣已存在"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 9. 加入兴趣 =================
@app.route('/api/interests/<int:interest_id>/join', methods=['POST'])
@token_required
def join_interest(user_id, interest_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO UserInterests (UserId, InterestId) VALUES (?, ?)", (user_id, interest_id))
        conn.commit()
        return jsonify({"code": 200, "msg": "加入成功"}), 200
    except pyodbc.IntegrityError:
        return jsonify({"code": 400, "msg": "你已加入过该兴趣"}), 400
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 10. 退出兴趣 =================
@app.route('/api/interests/<int:interest_id>/quit', methods=['DELETE'])
@token_required
def quit_interest(user_id, interest_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM UserInterests WHERE UserId = ? AND InterestId = ?", (user_id, interest_id))
        conn.commit()
        return jsonify({"code": 200, "msg": "已退出该兴趣"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 11. 发布分享接口 =================
@app.route('/api/shares', methods=['POST'])
@token_required
def create_share(user_id):
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    interest_id = data.get('interest_id')  # 可选
    share_type = data.get('share_type', 0) # 0=体验, 1=推荐, 2=避雷
    rating = data.get('rating')            # 如果是推荐/避雷，可以附带评价数据

    if not title or not content:
        return jsonify({"code": 400, "msg": "标题和内容不能为空"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. 插入 Share 主表
        cursor.execute(
            """INSERT INTO Shares (UserId, Title, Content, InterestId, ShareType) 
               OUTPUT INSERTED.ShareId VALUES (?, ?, ?, ?, ?)""",
            (user_id, title, content, interest_id, share_type)
        )
        share_id = cursor.fetchone()[0]

        # 2. 如果是推荐(1)或避雷(2)且传了 rating，插入扩展表
        if share_type in [1, 2] and rating and rating.get('target_name'):
            cursor.execute(
                """INSERT INTO ShareRatings (ShareId, TargetName, Score) 
                   VALUES (?, ?, ?)""",
                (share_id, rating.get('target_name'), rating.get('score'))
            )

        conn.commit()
        return jsonify({"code": 200, "msg": "发布成功", "share_id": share_id}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

# ================= 12. 分享列表查询接口 =================
@app.route('/api/shares', methods=['GET'])
def get_shares():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    share_type = request.args.get('share_type') # 可选过滤
    
    offset = (page - 1) * page_size

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 基础 SQL
        sql = """
            SELECT s.ShareId, s.Title, s.Content, s.ShareType, s.CreatedAt, 
                   u.UserId, u.Username, u.Nickname,
                   r.TargetName, r.Score
            FROM Shares s
            JOIN Users u ON s.UserId = u.UserId
            LEFT JOIN ShareRatings r ON s.ShareId = r.ShareId
            WHERE s.IsDeleted = 0
        """
        params = []

        # 如果传了 share_type，加上过滤条件
        if share_type is not None:
            sql += " AND s.ShareType = ?"
            params.append(int(share_type))

        # 排序和分页 (SQL Server 语法)
        sql += " ORDER BY s.CreatedAt DESC OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, page_size])

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        data_list = []
        for r in rows:
            data_list.append({
                "share_id": r.ShareId,
                "title": r.Title,
                "content": r.Content,
                "share_type": r.ShareType,
                "created_at": r.CreatedAt.strftime("%Y-%m-%d %H:%M:%S"),
                "author": {
                    "user_id": r.UserId,
                    "username": r.Username,
                    "nickname": r.Nickname
                },
                "rating": {
                    "target_name": r.TargetName,
                    "score": r.Score
                } if r.TargetName else None
            })

        return jsonify({"code": 200, "data": data_list}), 200

    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)}), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)