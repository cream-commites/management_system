from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 初始化SQLAlchemy
db = SQLAlchemy()


class Admin(db.Model):
    """用户信息模型，对应admin表"""
    __tablename__ = 'admins'  # 表名

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='用户唯一ID')
    username = db.Column(db.String(50), unique=True, nullable=False, comment='用户名')
    password = db.Column(db.String(255), nullable=False, comment='密码')
    email = db.Column(db.String(100), unique=True, nullable=False, comment='邮箱')
    mobile = db.Column(db.String(20), unique=True, nullable=False, comment='手机号')
    department = db.Column(db.String(100), default='', comment='部门')
    salary = db.Column(db.Numeric(10, 2), default=0.00, comment='薪资')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')

    def __repr__(self):
        return f"<Admin {self.username}>"