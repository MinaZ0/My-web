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
    balance = db.Column(db.Integer, default=10000) # เริ่มต้นหมื่นนึง
    cards = db.relationship('Card', backref='owner', lazy=True)

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    game = db.Column(db.String(50), nullable=False)
    rarity = db.Column(db.String(50))
    price = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    card = db.relationship('Card', backref='favorited_by')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---
@app.route('/')
def index():
    all_cards = Card.query.all()
    return render_template('index.html', cards=all_cards)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.password == request.form.get('password'):
            login_user(user)
            flash('ยินดีต้อนรับกลับมา!', 'success')
            return redirect(url_for('index'))
        flash('ชื่อผู้ใช้หรือรหัสผ่านผิด', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/buy/<int:id>')
@login_required
def buy_card(id):
    card = Card.query.get_or_404(id)
    if current_user.balance >= card.price:
        current_user.balance -= card.price
        card.user_id = current_user.id # เปลี่ยนเจ้าของ
        db.session.commit()
        flash(f'ซื้อ {card.name} สำเร็จ!', 'success')
    else:
        flash('เงินไม่พอ กรุณาเติมเงิน!', 'danger')
    return redirect(url_for('index'))

@app.route('/wishlist/add/<int:card_id>')
@login_required
def add_wishlist(card_id):
    exists = Favorite.query.filter_by(user_id=current_user.id, card_id=card_id).first()
    if not exists:
        new_fav = Favorite(user_id=current_user.id, card_id=card_id)
        db.session.add(new_fav)
        db.session.commit()
        flash('เพิ่มในรายการที่ชอบแล้ว ❤️', 'success')
    return redirect(url_for('index'))

@app.route('/wishlist')
@login_required
def wishlist():
    favs = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', favorites=favs)

@app.route('/inventory')
@login_required
def inventory():
    # ดึงการ์ดที่เป็นของ current_user (ที่เราซื้อมาแล้ว)
    my_cards = Card.query.filter_by(user_id=current_user.id).all()
    return render_template('inventory.html', cards=my_cards)

@app.route('/history')
@login_required
def history():
    # ดึงประวัติการทำรายการ (ซื้อ/เติมเงิน) ของ user นี้
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    return render_template('history.html', transactions=transactions)

# --- Database Setup ---
def seed_data():
    with app.app_context():
        db.drop_all() # เพิ่มบรรทัดนี้ชั่วคราวเพื่อล้างตารางเก่า
        db.create_all()
        
        # สร้าง User 'guy'
        user = User(username='guy', password='123', balance=10000)
        db.session.add(user)
        
        # เพิ่มการ์ดตัวอย่าง 3 ใบ
        cards = [
            Card(name='Charizard G', game='Pokemon', rarity='Ultra Rare', price=2500, 
                 image_url='https://images.pokemontcg.io/pl3/1_hires.png'),
            Card(name='Blue-Eyes White Dragon', game='Yu-Gi-Oh', rarity='Ultra Rare', price=3500, 
                 image_url='https://images.ygoprodeck.com/images/cards/89631139.jpg'),
            Card(name='Dark Magician', game='Yu-Gi-Oh', rarity='Super Rare', price=1800, 
                 image_url='https://images.ygoprodeck.com/images/cards/46986414.jpg')
        ]
        db.session.bulk_save_objects(cards)
        db.session.commit()
        print("✅ สร้างข้อมูลการ์ดตัวอย่างเรียบร้อยแล้ว!")

if __name__ == '__main__':
    seed_data()
    app.run(debug=True, port=5001)