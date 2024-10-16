from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Item, Order
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///canteen.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        session['user_id'] = user.id
        if user.role == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    return "Invalid credentials!"

@app.route('/home')
def home():
    items = Item.query.all()  # Fetch all items with availability
    return render_template('home.html', items=items)

@app.route('/order/<int:item_id>')
def order(item_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))
    item = Item.query.get(item_id)
    order = Order(user_id=session['user_id'], item_id=item.id)
    db.session.add(order)
    db.session.commit()
    return render_template('order.html', item=item)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    items = Item.query.all()
    return render_template('admin.html', items=items)

@app.route('/update_item', methods=['POST'])
def update_item():
    item_id = request.form['item_id']
    availability = request.form['availability']
    item = Item.query.get(item_id)
    item.available = availability == '1'
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
