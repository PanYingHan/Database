from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB 連接
client = MongoClient("mongodb://127.0.0.1:27017/")
db = client.hw3_database  # 資料庫名稱
collection = db.hw3_collection  # 集合名稱

# 首頁路由
@app.route('/')
def index():
    data = collection.find()  # 查詢所有資料
    return render_template('index.html', data=data)

# 新增資料的路由
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        try:
            name = request.form['name']  # 姓名
            product = request.form['product']  # 購買商品
            quantity = int(request.form['quantity'])  # 購買數量
            amount = int(float(request.form['amount']))  # 消費金額

            # 插入資料到 MongoDB
            collection.insert_one({
                "name": name,
                "product": product,
                "quantity": quantity,
                "amount": amount
            })
            return redirect('/')  # 新增完成後返回首頁
        except Exception as e:
            return f"Error: {str(e)}", 400
    return render_template('create.html')  # GET 請求時顯示表單

# 編輯資料的路由
@app.route('/edit', methods=['POST'])
def edit():
    try:
        item_id = request.form['id']
        name = request.form['name']
        product = request.form['product']
        quantity = int(request.form['quantity'])
        amount = int(float(request.form['amount']))

        # 在 MongoDB 中更新資料
        collection.update_one(
            {'_id': ObjectId(item_id)},  # 根據 ID 查找要更新的資料
            {'$set': {'name': name, 'product': product, 'quantity': quantity, 'amount': amount}}  # 設定新的資料
        )

        # 重新導向到首頁顯示更新後的資料
        return redirect('/')
    except KeyError as e:
        return f"Error: Missing key {e}", 400  # 如果表單中缺少某個字段，返回錯誤
    except Exception as e:
        return f"An error occurred: {str(e)}", 500  # 捕捉其他可能的錯誤

# 刪除資料的路由
@app.route('/delete', methods=['POST'])
def delete():
    item_id = request.form['id']  # 獲取要刪除的記錄的 ID
    collection.delete_one({'_id': ObjectId(item_id)})  # 從 MongoDB 刪除該記錄
    return redirect('/')  # 刪除後重定向到首頁

if __name__ == '__main__':
    app.run(debug=True)