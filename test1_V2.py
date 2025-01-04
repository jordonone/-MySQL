from datetime import datetime, time

from flask import Flask, render_template, request, redirect, url_for, flash, session
from product_pack import ProductManager
import os

#创建一个Flask对象
test = Flask(__name__)
test.secret_key = '527821'  # 设置会话密钥

manager = ProductManager()

def check_permission():
    """检查用户是否具有管理员权限"""
    if 'role_new' not in session or session['role_new'] == 'user':
        return False
    return True

@test.route("/",methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        print(f"Attempting login: username={uname}, password={pwd}")  # 调试信息
        flag, message= manager.check_login(uname, pwd)
        if flag:
            print("Login successful")  # 调试信息
            session["role_new"] = message
            return redirect(url_for("main_page"))
        else:
            print(f"Login failed: {message}")  # 调试信息
            return render_template("login.html", error=message)
    return render_template("login.html")

@test.route("/register",methods = ['GET','POST'])
def regist():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        pwd2 = request.form['confirm_password']
        flag,message = manager.register(uname,pwd,pwd2)
        if flag:
            return redirect(url_for("login"))
        else:
            return render_template("regist.html",error=message)
    return render_template("regist.html")
from flask import Flask, session, redirect, url_for, Response



@test.route("/logout")
def logout():
    # 清除所有会话信息
    print("Session data before logout:", session)
    session.clear()
    print("Session data after logout:", session)

    # 创建重定向响应
    return redirect(url_for('login'))

@test.route("/ok")
def main_page():
    return render_template("index.html")

@test.route("/ok/items")
def show_all_items():
    items = manager.show_all_items()
    print(items)  # 打印 items 数据结构
    return render_template("items.html",items = items)

@test.route("/ok/insert",methods = ['GET', 'POST'])
def insert_item():
    if not check_permission():
        message = "无权限"
        return redirect(url_for('main_page'))
    if request.method == "POST":
        item_id = request.form['item_id']
        name3 = request.form['name3']
        count = request.form['count']
        price = request.form['price']
        brand_name = request.form['brand_name']
        people = request.form['people']
        provider_name = request.form['provider_name']
        phone = request.form['phone']
        address = request.form['address']
        flag,message = manager.insert_3(item_id,name3,count,price,brand_name,people,provider_name,phone,address)
        flash(message,"success" if flag else "error")
        return redirect(url_for('show_all_items'))
    return render_template('insert.html')

@test.route("/ok/provider_stats")
def show_provider_price_stats():
    result = manager.show_provider_price_stats();
    return render_template("provider_stats.html",stats = result)

@test.route("/ok/low")
def show_low_stock_items():
    result = manager.show_low_stock_items()
    return render_template("low_stock.html",items = result)

@test.route('/ok/brands')
def show_all_brands():
    brands = manager.show_all_brands()
    return render_template('brands.html', brands=brands)

@test.route('/ok/providers')
def show_all_providers():
    providers = manager.show_all_providers()
    return render_template('providers.html', providers=providers)

@test.route("/ok/price",methods = ['GET', 'POST'])
def show_items_by_price_range():
    if request.method == 'POST':
        min_price = request.form['min_price']
        max_price = request.form['max_price']
        result = manager.show_items_by_price_range(min_price,max_price)
        return render_template("price_range.html",items = result)
    return render_template("price_range.html")

@test.route("/ok/search_brand",methods = ['GET','POST'])
def show_items_by_brand():
    if request.method =='POST':
        name = request.form['brand_name']
        items = manager.show_items_by_brand(name)
        return render_template("brand_items.html",items = items)
    return render_template("brand_items.html")

@test.route("/ok/search_provider",methods = ['GET','POST'])
def show_items_by_provider():
    if request.method =='POST':
        name = request.form['provider_name']
        items = manager.show_items_by_provider(name)
        return render_template("provider_items.html",items = items)
    return render_template("provider_items.html")

@test.route('/ok/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    if not check_permission():
        message = "无权限"
        return redirect(url_for('show_all_items'))

    if request.method == 'POST':
        new_price = request.form['price']
        new_count = request.form['count']
        success, message = manager.update_items(item_id, new_price, new_count)
        flash(message, 'success' if success else 'error')
        return redirect(url_for('show_all_items'))
    items = manager.show_all_items()
    item = next((item for item in items if item['item_id'] == item_id), None)
    return render_template('update.html', item=item)

@test.route('/ok/delete_by_id/<int:item_id>')
def delete_item_by_id(item_id):
    if not check_permission():
        message = "无权限"
        return redirect(url_for('show_all_items'))
    success, message = manager.delete_items_id(item_id)
    flash(message, 'success' if success else 'error')
    return redirect(url_for('show_all_items'))

@test.route('/ok/search', methods=['GET', 'POST'])
def search_items():
    if request.method == 'POST':
        search_type = request.form['search_type']
        search_value = request.form['search_value']
        if search_type == 'id':
            success, results = manager.search_id(int(search_value))
        else:
            success, results = manager.search_name(search_value)
        if not success:
            flash(results, 'error')
            return redirect(url_for('search_items'))
        return render_template('search.html', results=results)
    return render_template('search.html')

if __name__ == "__main__":
    #同一局域网1可访问，设置host  app.run(host="0.0.0.0", port=5000)
    test.run(port=8000,debug=True)


