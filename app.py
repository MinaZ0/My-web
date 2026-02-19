from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

@app.route('/')
def index():
    products = [
        {'id': 1, 'name': 'MacBook Pro', 'price': 45900, 'img': 'https://via.placeholder.com/150'},
        {'id': 2, 'name': 'iPhone 15', 'price': 32900, 'img': 'https://via.placeholder.com/150'},
        {'id': 3, 'name': 'iPad Air', 'price': 23900, 'img': 'https://via.placeholder.com/150'}
    ]
    return render_template('index.html', products=products)

if __name__ == '__main__':
    app.run(debug=True)