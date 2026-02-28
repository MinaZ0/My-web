import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db = SQLAlchemy(app)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False) # ในงานจริงควรแฮชรหัสผ่าน
    balance = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    search_query = request.args.get('search')
    if search_query:
        all_cards = Card.query.filter(Card.name.contains(search_query)).all()
    else:
        all_cards = Card.query.all()
    return render_template('index.html', cards=all_cards)

@app.route('/add', methods=['GET', 'POST'])
def add_card():
    if request.method == 'POST':
        name = request.form.get('name')
        game = request.form.get('game')
        rarity = request.form.get('rarity')
        price = request.form.get('price')
        image_url = request.form.get('image_url')
        
        new_card = Card(name=name, game=game, rarity=rarity, 
                        price=int(price) if price else 0, 
                        image_url=image_url)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_card.html')

@app.route('/delete/<int:id>')
def delete_card(id):
    card_to_delete = Card.query.get_or_404(id) # หาการ์ดตาม ID
    db.session.delete(card_to_delete)           # สั่งลบ
    db.session.commit()                         # ยืนยันการลบ
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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