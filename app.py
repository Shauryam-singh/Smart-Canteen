from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from datetime import datetime
import json
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL connection configuration
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        database='smart_canteen',
        cursorclass=pymysql.cursors.DictCursor
    )

def load_items_from_json():
    with open('items.json') as f:
        return json.load(f)

@app.route('/')
def index():
    if 'user_id' in session:
        # Redirect based on role
        return redirect(url_for('home') if session.get('role') == 'user' else url_for('admin'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user['id']
                session['role'] = user['role']
                return redirect(url_for('admin') if user['role'] == 'admin' else url_for('home'))
    finally:
        conn.close()

    return "Invalid credentials!"

@app.route('/home')
def home():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('index'))

    # Load items from JSON
    item_images = {item['id']: item['image_url'] for item in load_items_from_json()}

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
            # Map image URLs to items
            for item in items:
                item['image_url'] = item_images.get(item['id'], None)  # Add image URL to item

    finally:
        conn.close()

    return render_template('home.html', items=items)

@app.route('/order/<int:item_id>', methods=['POST'])
def order(item_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    quantity = request.form['quantity']
    pickup_time = request.form.get('pickup_time', None)
    order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    order_id = str(uuid.uuid4())  # Generate unique order ID

    if not pickup_time:
        pickup_time = datetime.now().strftime('%H:%M')

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()

            if item:
                if int(quantity) <= item['quantity']:
                    total_price = float(item['price']) * int(quantity)

                    cursor.execute(""" 
                        INSERT INTO orders (order_id, user_id, item_id, quantity, total_price, pickup_time, order_time) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """, (order_id, session['user_id'], item_id, quantity, total_price, pickup_time, order_time))

                    new_quantity = item['quantity'] - int(quantity)
                    cursor.execute("UPDATE items SET quantity = %s WHERE id = %s", (new_quantity, item_id))

                    conn.commit()
                    return render_template('order.html', item=item, total_price=total_price, pickup_time=pickup_time, order_time=order_time, order_id=order_id)
                else:
                    return "Not enough stock available!"
    finally:
        conn.close()

    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('index'))

@app.route('/admin')
def admin():
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('index'))

    # Load items from JSON
    item_images = {item['id']: item['image_url'] for item in load_items_from_json()}

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
            # Map image URLs to items
            for item in items:
                item['image_url'] = item_images.get(item['id'], None)  # Add image URL to item
    finally:
        conn.close()

    return render_template('admin.html', items=items)

@app.route('/update_item', methods=['POST'])
def update_item():
    item_id = request.form['item_id']
    availability = request.form['availability']
    price = request.form['price']
    quantity = request.form['quantity']

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE items SET available = %s, price = %s, quantity = %s WHERE id = %s",
                           (availability == '1', price, quantity, item_id))
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for('admin'))

@app.route('/add_item', methods=['POST'])
def add_item():
    name = request.form['name']
    price = request.form['price']
    quantity = request.form['quantity']
    availability = request.form['availability']  # Get availability value

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO items (name, price, quantity, available) VALUES (%s, %s, %s, %s)", 
                           (name, price, quantity, availability == '1'))  # Convert to boolean
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for('admin'))

@app.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for('admin'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def send_contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    # Add logic here to save the message or send it via email

    return "Thank you for reaching out! We will get back to you shortly."

if __name__ == '__main__':
    app.run(debug=True)
