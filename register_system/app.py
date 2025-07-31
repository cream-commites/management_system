import pymysql
from flask import Flask, render_template, request, jsonify, redirect, url_for
from matplotlib.backend_tools import cursors

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template(
        'index1.html',
    )


# 注册路由
@app.route('/reg')
def reg():
    return render_template('reg.html')

# 前端index1中的新增用户路由：
@app.route('/add/user', methods=['GET', 'POST'])
def add_user():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        department = request.form.get('department')
        salary = request.form.get('salary')

        if not all([username, email, mobile, department, salary]):
            return jsonify({"code":1 ,"message":"所有字段都必须填写哦"}),400
        coon = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='root', charset="utf8", db="unicom")
        cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)

#         插入新增数据
        sql = "INSERT INTO admin (username, email, mobile, department, salary) VALUES (%s, %s, %s, %s, %s)"
        add_data = cursor.execute(sql, (username, email, mobile, department, salary))
        print(add_data)    #验证数据，前后端口的交互
        coon.commit()
        user_id = cursor.lastrowid
        cursor.close()
        coon.close()
        return jsonify({"code": 0, "message": "用户添加成功", "user_id": user_id})
    # 抛出异常
    except Exception as e:
        print(f"用户添加失败：{e}")
        return jsonify({"code": 1, "message": f"添加用户失败: {str(e)}"}), 500


# 删除信息
@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    try:
        coon = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='root', charset="utf8", db="unicom")
        cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # 根据用户名删除用户
        sql = "DELETE from admin where id = %s"
        cursor.execute(sql, (user_id,))
        coon.commit()

        cursor.close()
        coon.close()

        # 删除成功后重定向到管理页面
        return redirect(url_for('admin'))

    except Exception as e:
        # 处理数据库错误
        return jsonify({"error": f"删除用户失败: {str(e)}"}), 500


# 登录页面
@app.route('/login', methods=['GET', 'POST'])
def erollment():
    username = request.form.get('username')
    password = request.form.get('password')
    # print(request.form)
    print(username, password)
    try:
        coon = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='root', charset="utf8", db="unicom")
        cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)

        # 查询用户信息
        sql = "select * from admin where username = %s AND password = %s"
        cursor.execute(sql, (username, password))
        user = cursor.fetchone()

        cursor.close()
        coon.close()

        if user and user['username'] == username and user['password'] == password:
            return redirect(url_for('admin'))
        else:
            return render_template('index1.html', error="用户名或密码错误")

    except Exception as e:
        return jsonify({"error": f"数据库错误: {str(e)}"}), 500

        # 处理GET请求，返回登录页面
    return render_template('index1.html')


# 总效果页面
@app.route('/admin', methods=['GET'])
def admin():
    keyword = request.args.get('keyword', '').strip()

    try:
        with pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user='root',
                password='root',
                charset="utf8",
                db="unicom"
        ) as conn:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                if keyword:
                    sql = """
                        SELECT * FROM admin 
                        WHERE username LIKE %s 
                        OR email LIKE %s 
                        OR mobile LIKE %s 
                        OR department LIKE %s
                    """
                    like_keyword = f"%{keyword}%"
                    cursor.execute(sql, (like_keyword, like_keyword, like_keyword, like_keyword))
                else:
                    sql = "SELECT * FROM admin"
                    cursor.execute(sql)

                users = cursor.fetchall()

        return render_template('admin.html', users=users, keyword=keyword)

    except Exception as e:
        return jsonify({"error": f"获取用户列表失败: {str(e)}"}), 500


# 注册页面接口
@app.route('/register', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('confirmPassword')
    print(username, password, mobile, email)

    try:
        coon = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='root', charset="utf8", db="unicom")
        cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "INSERT INTO admin (username,email,mobile,password) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (username, email, mobile, password))
        coon.commit()
        cursor.close()
        coon.close()

        return render_template('index1.html')
    except Exception as e:
        print(f"注册失败: {e}")
        return "注册失败，请重试"

# 返回页面
@app.route('/index1')  # 对应我的前端href="/index1"
def index1():
    return render_template('index1.html')

# 修改数据
@app.route('/update', methods=['GET', 'POST'])
def update():
    # d第一步要先获取所有字段
    user_id = request.form.get('id')
    username = request.form.get('username')
    email = request.form.get('email')
    mobile = request.form.get('mobile')
    password = request.form.get('confirmPassword')
    department = request.form.get('department')
    salary = request.form.get('salary')
    print(username, password, mobile, email,department, salary)    #打印出来验证是否正确获取，前后端交互是否正常

    try:
        coon = pymysql.connect(host="127.0.0.1", port=3306, user='root', password='root', charset="utf8", db="unicom")
        cursor = coon.cursor(cursor=pymysql.cursors.DictCursor)
        sql = "update admin SET username = %s, email = %s, mobile = %s,department = %s,salary= %s WHERE id = %s"
        cursor.execute(sql, (username, email, mobile, department, salary, user_id))
        if cursor.rowcount == 0:
            coon.close()
            return jsonify({"code": 1, "message": "未找到该用户，或数据未变化"})

        coon.commit()
        cursor.close()
        coon.close()
        return jsonify({"code": 0,"message": "修改成功"})

    except Exception as e:
        print(f"Error: {e}")
        if coon:
            coon.rollback()
        return jsonify({"code": 1,"message": "修改失败"})


if __name__ == '__main__':
    app.run()
