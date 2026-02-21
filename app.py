import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# ตั้งค่า Path สำหรับ Database
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Commit 15: Card Model ---
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

    def __repr__(self):
        return f'<Card {self.name}>'

# --- Commit 18: Index Route ---
@app.route('/')
def index():
    all_cards = Card.query.all()
    return render_template('index.html', cards=all_cards)

# --- Commit 16 & 17: Seed Data Function ---
def seed_data():
    with app.app_context():
        db.create_all()  # สร้างโต๊ะทำงาน (Database Tables)
        
        if not Card.query.first():
            # Commit 16: Pokemon Cards
            c1 = Card(name='Pikachu VMAX', game='Pokemon', rarity='Secret Rare', 
                      price=1200, image_url='https://images.pokemontcg.io/swsh4/44_hires.png')
            
            # Commit 17: Yu-Gi-Oh Cards
            c2 = Card(name='Dark Magician', game='Yu-Gi-Oh', rarity='Ultra Rare', 
                      price=800, image_url='https://images.ygoprodeck.com/images/cards/46986414.jpg')
            
            db.session.add_all([c1, c2])
            db.session.commit()
            print("Successfully Seeded TCG Data!")

if __name__ == '__main__':
    seed_data()
    app.run(debug=True)