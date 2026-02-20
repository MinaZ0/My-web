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

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(200), default='https://via.placeholder.com/150')

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/')
def index():
    # ดึงข้อมูลสินค้าทั้งหมดจาก Database
    all_products = Product.query.all()
    return render_template('index.html', products=all_products)

# 5. Helper Function: สั่งสร้าง Database และเพิ่มข้อมูลตัวอย่าง (Seeding)
# คุณสามารถรันฟังก์ชันนี้เพื่อ