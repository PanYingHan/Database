from flask import Flask, request, jsonify, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# 連接 MySQL 資料庫
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",  # 根據你的設定
        password="h2004930517",  # 根據你的設定
        database="employees"
    )

# 查詢所有員工
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employee")
    employees = cursor.fetchall()
    conn.close()
    return render_template('index.html', employees=employees)

# 新增員工
@app.route('/add', methods=['POST'])
def add_employee():
    name = request.form['name']
    position = request.form['position']
    salary = request.form['salary']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employee (name, position, salary) VALUES (%s, %s, %s)", 
                   (name, position, salary))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

# 編輯員工
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        salary = request.form['salary']
        cursor.execute("UPDATE employee SET name = %s, position = %s, salary = %s WHERE id = %s",
                       (name, position, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM employee WHERE id = %s", (id,))
    employee = cursor.fetchone()
    conn.close()
    return render_template('edit.html', employee=employee)

# 刪除員工
@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employee WHERE id = %s", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
