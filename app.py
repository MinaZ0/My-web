import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model การ์ด TCG
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

# Route หลัก รองรับ Search และ Filter
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

# ฟังก์ชัน Seed ข้อมูลเบื้องต้น
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