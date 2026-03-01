import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'guy-tcg-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# --- Models ---

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    balance = db.Column(db.Integer, default=0)
    cards = db.relationship('Card', backref='owner', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # เก็บว่าใครเป็นเจ้าของ

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    amount = db.Column(db.Integer)
    type = db.Column(db.String(20)) # 'topup' หรือ 'buy'
    date = db.Column(db.DateTime, default=db.func.now())

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    
    # เชื่อมความสัมพันธ์เพื่อให้ดึงข้อมูลการ์ดมาโชว์ในหน้า Wishlist ได้ง่ายๆ
    card = db.relationship('Card', backref='favorited_by')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
def index():
    game_filter = request.args.get('game')
    search_query = request.args.get('search')
    
    query = Card.query
    if game_filter:
        query = query.filter_by(game=game_filter)
    if search_query:
        query = query.filter(Card.name.contains(search_query))
        
    all_cards = query.all()
    return render_template('index.html', cards=all_cards)

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'POST':
        new_card = Card(
            name=request.form.get('name'),
            game=request.form.get('game'),
            rarity=request.form.get('rarity'),
            price=int(request.form.get('price') or 0),
            image_url=request.form.get('image_url'),
            user_id=current_user.id # บันทึกเจ้าของ
        )
        db.session.add(new_card)
        db.session.commit()
        flash('ลงขายการ์ดสำเร็จ!', 'success')
        return redirect(url_for('index'))
    return render_template('add_card.html')

@app.route('/buy/<int:id>')
@login_required
def buy_card(id):
    card = Card.query.get_or_404(id)
    if current_user.balance < card.price:
        flash('เงินไม่พอ กรุณาเติมเงิน!', 'danger')
        return redirect(url_for('topup'))
    
    # หักเงิน บันทึกประวัติ และลบการ์ด (เพราะถูกซื้อไปแล้ว)
    current_user.balance -= card.price
    new_tx = Transaction(user_id=current_user.id, amount=card.price, type='buy')
    db.session.add(new_tx)
    db.session.delete(card) 
    db.session.commit()
    
    flash(f'ซื้อ {card.name} สำเร็จ!', 'success')
    return redirect(url_for('history'))

@app.route('/delete/<int:id>')
@login_required
def delete_card(id):
    card = Card.query.get_or_404(id)
    if card.user_id != current_user.id:
        flash('คุณไม่มีสิทธิ์ลบการ์ดของคนอื่น!', 'danger')
        return

@app.route('/profile')
@login_required
def profile():
    my_cards_count = Card.query.filter_by(user_id=current_user.id).count()
    return render_template('profile.html', cards_count=my_cards_count)

@app.route('/my-cards')
@login_required
def my_cards():
    cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template('my_cards.html', cards=cards)