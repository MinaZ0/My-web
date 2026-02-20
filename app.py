import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# 1. Setup Application & Directory
basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-super-secret-key-123'

# 2. Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# 4. Routes
@app.route('/')
def index():
    # ดึงข้อมูลสินค้าทั้งหมดจาก Database
    all_products = Product.query.all()
    return render_template('index.html', products=all_products)

# 5. Helper Function: สั่งสร้าง Database และเพิ่มข้อมูลตัวอย่าง (Seeding)
# คุณสามารถรันฟังก์ชันนี้เพื่อ