from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
from datetime import datetime

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
    
    # Connect to the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            if user:
                session['user_id'] = user['id']
                session['role'] = user['role']  # Store the role in the session
                if user['role'] == 'admin':
                    return redirect(url_for('admin'))
                else:
                    return redirect(url_for('home'))
    finally:
        conn.close()

    return "Invalid credentials!"

@app.route('/home')
def home():
    if 'user_id' not in session or session.get('role') != 'user':
        return redirect(url_for('index'))

    # Connect to the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
    finally:
        conn.close()

    return render_template('home.html', items=items)

@app.route('/order/<int:item_id>', methods=['POST'])
def order(item_id):
    if 'user_id' not in session:
        return redirect(url_for('index'))

    # Get the values from the form
    quantity = request.form['quantity']
    pickup_time = request.form.get('pickup_time', None)  # Get the pickup time, defaults to None if not provided
    order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current time for the order

    # If no pickup_time is provided, set it to the current time
    if not pickup_time:
        pickup_time = datetime.now().strftime('%H:%M')  # Current time in "HH:MM" format

    print(f"Pickup Time: {pickup_time}, Order Time: {order_time}")  # Debugging output

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
            item = cursor.fetchone()

            if item:
                if int(quantity) <= item['quantity']:
                    total_price = float(item['price']) * int(quantity)

                    cursor.execute(""" 
                        INSERT INTO orders (user_id, item_id, quantity, total_price, pickup_time, order_time) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """, (session['user_id'], item_id, quantity, total_price, pickup_time, order_time))

                    new_quantity = item['quantity'] - int(quantity)
                    cursor.execute("UPDATE items SET quantity = %s WHERE id = %s", (new_quantity, item_id))

                    conn.commit()

                    # Pass order_time to the template
                    return render_template('order.html', item=item, total_price=total_price, pickup_time=pickup_time, order_time=order_time)
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

    # Connect to the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM items")
            items = cursor.fetchall()
    finally:
        conn.close()

    return render_template('admin.html', items=items)

@app.route('/update_item', methods=['POST'])
def update_item():
    item_id = request.form['item_id']
    availability = request.form['availability']
    price = request.form['price']
    quantity = request.form['quantity']

    # Connect to the database
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # Update item availability, price, and quantity
            cursor.execute("UPDATE items SET available = %s, price = %s, quantity = %s WHERE id = %s",
                           (availability == '1', price, quantity, item_id))
            conn.commit()
    finally:
        conn.close()

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
