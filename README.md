# Smart Canteen Management System

This is a web application built using **Flask** that allows students to pre-order food from the college canteen. It solves the issue of long queues and item availability by providing a real-time item listing with a pre-order system. Students can select food items, specify the quantity, and choose a pickup time. The system also manages real-time item availability and order history.

---

## Features

- **User Registration & Login**: Students can register, log in, and log out to place orders.
- **Item Listing**: Students can view available food items with real-time quantity updates.
- **Pre-ordering**: Students can select the items they want, specify the quantity, and set the pickup time.
- **Order Management**: Displays the order details including pickup time and order time.
- **Real-time Availability**: Updates item availability as orders are placed.
- **Responsive Design**: Designed with **Bootstrap 5** to be mobile-friendly and user-friendly.

---

## Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript (Bootstrap 5)
- **Database**: MySQL
- **Authentication**: Flask sessions (for login and order management)

---

## Installation

Follow the steps below to get the project up and running on your local machine.

### Prerequisites

- Python 3.x installed on your machine
- A MySQL database configured

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/smart-canteen.git
cd smart-canteen
```

### Step 2: Install Required Packages

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

### Step 3: Set Up the Database

Make sure MySQL is installed and running.

1. Open **MySQL Command Line** or **MySQL Workbench**.

2. Create a new database for the project:

```sql
CREATE DATABASE smart_canteen;
```

3. Switch to the newly created database:

```sql
USE smart_canteen;
```

4. Create the required tables for the system:

```sql
-- Table for users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    phone VARCHAR(15),
    role ENUM('admin', 'user') DEFAULT 'user',
    login_time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table for items
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    quantity INT NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

-- Table for orders
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    pickup_time TIME NOT NULL,
    order_time DATETIME NOT NULL,
    order_id VARCHAR(36) NOT NULL UNIQUE,   -- Updated order_id column
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (item_id) REFERENCES items(id)
);

CREATE TABLE order_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id VARCHAR(36) NOT NULL,
    user_id INT,
    item_name VARCHAR(100),
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    pickup_time TIME NOT NULL,
    order_time DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

```

### Step 4: Configuration

Configure your database connection in `app.py`:

```python
def get_db_connection():
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='password',
        db='smart_canteen',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn
```

### Step 5: Run the Application

```bash
flask run
```

The app will start on `http://127.0.0.1:5000/`.

---

## API Endpoints

- **GET /home**: Displays the list of available items in the canteen.
- **POST /order/<item_id>**: Allows the user to place an order for a specific item with quantity and pickup time.
- **GET /logout**: Logs out the current user session.
- **GET /contact**: Contact us page (can be customized for feedback or help).

---

## Project Structure

```
/smart-canteen
│
├── /static                # Static files (CSS, JS, Images)
│
├── /templates             # HTML templates
│   ├── admin.html         # Admin template
│   ├── home.html          # Home page template
│   ├── order.html         # Order confirmation page
│   └── login.html         # Login page
│
├── app.py                 # Main Flask application
├── requirements.txt       # List of dependencies
├── config.py              # Configuration file (optional)
└── README.md              # This README file
```

---

## Contributions

Contributions are welcome! If you find a bug or want to add a feature, feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-name`).
6. Create a new pull request.

---

## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Acknowledgements

- **Bootstrap 5**: For responsive and mobile-first design.
- **Flask**: For building the backend.
- **MySQL**: For storing and managing the canteen data.
- **FontAwesome**: For icons used in the UI.

---

Feel free to customize this further based on your project specifics!
