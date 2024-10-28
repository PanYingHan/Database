from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 設定 MySQL 資料庫連接
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",  # 你的 MySQL 使用者名稱
    password="h2004930517",  # 你的 MySQL 密碼
    database="sales"  # 使用的資料庫名稱
)

# 建立資料庫游標
cursor = db.cursor(dictionary=True)

# 初始化：建立資料庫表格
def initialize_database():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Customer (
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255) NOT NULL,
        occupation VARCHAR(255)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Contact (
        id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT,
        phone VARCHAR(20),
        address VARCHAR(255),
        FOREIGN KEY (customer_id) REFERENCES Customer(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CustomerOrder (
        id INT PRIMARY KEY AUTO_INCREMENT,
        customer_id INT,
        product VARCHAR(255) NOT NULL,
        quantity INT NOT NULL,
        amount DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES Customer(id)
    );
    """)
    db.commit()

# 執行初始化
initialize_database()

# 路由到首頁，顯示購物紀錄
@app.route('/')
def index():
    # 分別查詢 Customer、Contact 和 CustomerOrder 表格的資料
    cursor.execute("SELECT * FROM Customer")
    customers = cursor.fetchall()
    
    cursor.execute("SELECT * FROM Contact")
    contacts = cursor.fetchall()
    
    cursor.execute("SELECT * FROM CustomerOrder")
    orders = cursor.fetchall()
    
    # 將每個表格的資料傳遞給模板
    return render_template('index.html', customers=customers, contacts=contacts, orders=orders)

# 路由處理表單提交，新增紀錄
@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    occupation = request.form['occupation']
    phone = request.form['phone']
    address = request.form['address']
    product = request.form['product']
    quantity = request.form['quantity']
    amount = request.form['amount']

    # 插入 Customer 資料
    cursor.execute("INSERT INTO Customer (name, occupation) VALUES (%s, %s)", (name, occupation))
    customer_id = cursor.lastrowid  # 取得插入的 Customer id

    # 插入 Contact 資料
    cursor.execute("INSERT INTO Contact (customer_id, phone, address) VALUES (%s, %s, %s)", (customer_id, phone, address))

    # 插入 CustomerOrder 資料
    cursor.execute("INSERT INTO CustomerOrder (customer_id, product, quantity, amount) VALUES (%s, %s, %s, %s)", (customer_id, product, quantity, amount))

    db.commit()
    return redirect(url_for('index'))

# 路由處理刪除紀錄
@app.route('/delete/<int:id>', methods=['POST'])
def delete_record(id):
    cursor.execute("DELETE FROM CustomerOrder WHERE customer_id = %s", (id,))
    cursor.execute("DELETE FROM Contact WHERE customer_id = %s", (id,))
    cursor.execute("DELETE FROM Customer WHERE id = %s", (id,))
    db.commit()
    return redirect(url_for('index'))

# 路由處理編輯紀錄
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    if request.method == 'POST':
        name = request.form['name']
        occupation = request.form['occupation']
        phone = request.form['phone']
        address = request.form['address']
        product = request.form['product']
        quantity = request.form['quantity']
        amount = request.form['amount']

        cursor.execute("UPDATE Customer SET name = %s, occupation = %s WHERE id = %s", (name, occupation, id))
        cursor.execute("UPDATE Contact SET phone = %s, address = %s WHERE customer_id = %s", (phone, address, id))
        cursor.execute("UPDATE CustomerOrder SET product = %s, quantity = %s, amount = %s WHERE customer_id = %s", (product, quantity, amount, id))
        
        db.commit()
        return redirect(url_for('index'))
    
    # 查詢要編輯的紀錄
    cursor.execute("""
    SELECT 
        Customer.name, Customer.occupation, Contact.phone, Contact.address, 
        CustomerOrder.product, CustomerOrder.quantity, CustomerOrder.amount 
    FROM Customer
    LEFT JOIN Contact ON Customer.id = Contact.customer_id
    LEFT JOIN CustomerOrder ON Customer.id = CustomerOrder.customer_id
    WHERE Customer.id = %s
    """, (id,))
    record = cursor.fetchone()
    return render_template('edit.html', record=record)

if __name__ == '__main__':
    app.run(debug=True)
