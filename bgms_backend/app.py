from flask import Flask, render_template, request, jsonify, redirect, url_for
from models.models import db, Admin  # 导入模型
import os

app = Flask(__name__)

# 配置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@127.0.0.1:3306/unicom?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭跟踪修改，提升性能

# 初始化数据库
db.init_app(app)

# 创建数据库表（首次运行时需要）
with app.app_context():
    db.create_all()  # 如果表不存在则创建


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    return render_template('index1.html')


@app.route('/reg')
def reg():
    return render_template('reg.html')


@app.route('/add/user', methods=['GET', 'POST'])
def add_user():
    try:
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        department = request.form.get('department')
        salary = request.form.get('salary')

        if not all([username, email, mobile, department, salary]):
            return jsonify({"code": 1, "message": "所有字段都必须填写哦"}), 400

        # 创建新用户对象
        new_user = Admin(
            username=username,
            email=email,
            mobile=mobile,
            department=department,
            salary=salary,
            password=''  # 新增用户默认密码为空（根据实际需求调整）
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "code": 0,
            "message": "用户添加成功",
            "user_id": new_user.id
        })

    except Exception as e:
        db.session.rollback()  # 出错时回滚
        print(f"用户添加失败：{e}")
        return jsonify({"code": 1, "message": f"添加用户失败: {str(e)}"}), 500


@app.route('/delete/<int:user_id>', methods=['GET', 'POST'])
def delete(user_id):
    try:
        user = Admin.query.get(user_id)
        if not user:
            return jsonify({"error": "用户不存在"}), 404

        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin'))

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"删除用户失败: {str(e)}"}), 500


@app.route('/login', methods=['GET', 'POST'])
def erollment():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            user = Admin.query.filter_by(username=username, password=password).first()
            if user:
                return redirect(url_for('admin'))
            else:
                return render_template('index1.html', error="用户名或密码错误")

        except Exception as e:
            return jsonify({"error": f"数据库错误: {str(e)}"}), 500

    return render_template('index1.html')


@app.route('/admin', methods=['GET'])
def admin():
    keyword = request.args.get('keyword', '').strip()

    try:
        if keyword:
            # 模糊查询
            users = Admin.query.filter(
                db.or_(
                    Admin.username.like(f'%{keyword}%'),
                    Admin.email.like(f'%{keyword}%'),
                    Admin.mobile.like(f'%{keyword}%'),
                    Admin.department.like(f'%{keyword}%')
                )
            ).all()
        else:
            users = Admin.query.all()

        return render_template('admin.html', users=users, keyword=keyword)

    except Exception as e:
        return jsonify({"error": f"获取用户列表失败: {str(e)}"}), 500


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        password = request.form.get('confirmPassword')

        try:
            new_user = Admin(
                username=username,
                email=email,
                mobile=mobile,
                password=password  # 注意：实际项目需要加密存储
            )
            db.session.add(new_user)
            db.session.commit()
            return render_template('index1.html')

        except Exception as e:
            db.session.rollback()
            print(f"注册失败: {e}")
            return "注册失败，请重试"

    return render_template('reg.html')


@app.route('/index1')
def index1():
    return render_template('index1.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        user_id = request.form.get('id')
        username = request.form.get('username')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        department = request.form.get('department')
        salary = request.form.get('salary')

        try:
            user = Admin.query.get(user_id)
            if not user:
                return jsonify({"code": 1, "message": "未找到该用户"})

            # 更新字段
            user.username = username
            user.email = email
            user.mobile = mobile
            user.department = department
            user.salary = salary

            # 如果有密码更新需求，可以在这里添加
            # if password:
            #     user.password = password

            db.session.commit()
            return jsonify({"code": 0, "message": "修改成功"})

        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")
            return jsonify({"code": 1, "message": "修改失败"})


if __name__ == '__main__':
    app.run(debug=True)