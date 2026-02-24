import os
from flask import Flask, render_template, request # เพิ่มการ import request
from flask_sqlalchemy import SQLAlchemy

# ตั้งค่า Path สำหรับ Database
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key' #
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Card Model ---
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Card {self.name}>'

# --- Commit 22: Index Route with Search Logic ---
@app.route('/')
def index():
    # รับค่า 'search' จาก URL (เช่น /?search=pikachu)
    search_query = request.args.get('search')
    
    if search_query:
        # ค้นหาการ์ดที่ชื่อมีคำที่ระบุ (Case-insensitive ใน SQLite)
        all_cards = Card.query.filter(Card.name.contains(search_query)).all()
    else:
        # ถ้าไม่มีการค้นหา ให้ดึงข้อมูลทั้งหมดตามปกติ
        all_cards = Card.query.all()
        
    return render_template('index.html', cards=all_cards)

# --- Seed Data Function ---
def seed_data():
    with app.app_context():
        db.create_all()
        if not Card.query.first():
            c1 = Card(name='Pikachu VMAX', game='Pokemon', rarity='Secret Rare', 
                      price=1200, image_url='https://images.pokemontcg.io/swsh4/44_hires.png')
            c2 = Card(name='Dark Magician', game='Yu-Gi-Oh', rarity='Ultra Rare', 
                      price=800, image_url='https://images.ygoprodeck.com/images/cards/46986414.jpg')
            db.session.add_all([c1, c2])
            db.session.commit()
            print("Successfully Seeded TCG Data!")

if __name__ == '__main__':
    seed_data()
    app.run(debug=True)