import os
from flask import Flask, render_template, request, redirect, url_for # เพิ่ม redirect และ url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Card Model (โครงสร้างฐานข้อมูลการ์ด) ---
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Card {self.name}>'

# --- Route หน้าแรก (แสดงรายการและการค้นหา) ---
@app.route('/')
def index():
    search_query = request.args.get('search')
    game_filter = request.args.get('game')
    
    query = Card.query
    if search_query:
        query = query.filter(Card.name.contains(search_query))
    if game_filter:
        query = query.filter(Card.game == game_filter)
        
    all_cards = query.all()
    return render_template('index.html', cards=all_cards)

# --- Commit 27: Route สำหรับเพิ่มการ์ดใหม่ ---
@app.route('/add', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        # รับค่าจากฟอร์มในหน้า add_card.html
        name = request.form.get('name')
        game = request.form.get('game')
        rarity = request.form.get('rarity')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        
        # สร้าง Object การ์ดใหม่และบันทึก
        new_card = Card(
            name=name, 
            game=game, 
            rarity=rarity, 
            price=int(price) if price else 0, 
            image_url=image_url
        )
        
        db.session.add(new_card)
        db.session.commit()
        
        # บันทึกเสร็จแล้วให้กลับไปหน้าแรกเพื่อดูผลลัพธ์
        return redirect(url_for('index'))
        
    # ถ้าเป็น GET (เปิดหน้าเว็บปกติ) ให้โชว์หน้าฟอร์ม
    return render_template('add_card.html')

# --- ฟังก์ชันสำหรับเตรียมข้อมูลเริ่มต้น ---
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

if __name__ == '__main__':
    seed_data()
    app.run(debug=True)