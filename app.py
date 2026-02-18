from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-key-123'

@app.route('/')
def index():
    return "<h1>E-Commerce Project is Running!</h1>"

if __name__ == '__main__':
    app.run(debug=True)