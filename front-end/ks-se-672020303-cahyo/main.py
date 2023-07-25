import json
import requests
import datetime
from flask import Flask, render_template, url_for, abort, redirect, request, session, flash, jsonify, Response
from functools import wraps
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = '672020303-cahyo'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=30)
URL_data = "https://backend-cahyo-5zn7xh2gqq-et.a.run.app"

# Login Check
# decorator check user is logged or not
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Silakan login terlebih dahulu')
            return redirect(url_for('login', next=request.url))
    return decorated_function

@app.route('/')
def login():
    session.clear()
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def do_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # check email and password validity
        url = f"{URL_data}/users"
        params = {'email': email}
        response = requests.get(url, params=params)
        result = json.loads(response.text)
        if result:
            if check_password_hash(result[0]['password'], password):
                session['logged_in'] = True
                session['username'] = result[0]['username']
                session.permanent = True
                session['login_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                flash('Anda berhasil login')
                return redirect(url_for('index'))
            else:
                flash('Password salah')
                return redirect(url_for('login'))
        else:
            flash('User tidak ditemukan')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Anda berhasil logout')
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/warehouse"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('index.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('login'))

@app.route('/kelola_barang', methods=['GET', 'POST'])
@login_required
def kelola_barang():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/warehouse"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('kelola-barang.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('login'))
        
@app.route('/kelola_supplier', methods=['GET', 'POST'])
@login_required
def kelola_supplier():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/supplier"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('kelola-supplier.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('login'))
        
@app.route('/data_user', methods=['GET', 'POST'])
@login_required
def data_user():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/users"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('data-user.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('login'))
        
@app.route('/tbl_masukkeluar', methods=['GET', 'POST'])
@login_required
def tbl_masukkeluar():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/warehouse"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('tables_brg-keluar-masuk.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('index'))
        
@app.route('/tbl_kadaluarsa', methods=['GET', 'POST'])
@login_required
def tbl_kadaluarsa():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        # retrieve data from URL
        url = f"{URL_data}/exp"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return render_template('tables_kadaluarsa.html', data=data)
        else:
            flash('Terjadi kesalahan saat mengambil data dari server')
            return redirect(url_for('index'))

# INSERT DATA 
@app.route('/kelola_barang/tambah_barang', methods=['GET', 'POST'])
@login_required
def tambah_barang():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            # retrieve data from form
            id_item = request.form['id_item']
            item_name = request.form['item_name']
            quantity = request.form['quantity']
            id_supplier = request.form['id_supplier']
            id_expiration = request.form['id_expiration']
            category = request.form['category']
            status = request.form['status']
            exp_date = request.form['exp_date']
            
            # create data payload
            data = {
                'id_item': id_item,
                'item_name': item_name,
                'quantity': quantity,
                'id_supplier': id_supplier,
                'id_expiration': id_expiration,
                'category': category,
                'status': status,
                'exp_date': exp_date
            }
            
            # send post request to API
            response = requests.post(f"{URL_data}/warehouse", json=data)
            
            if response.status_code == 201:
                flash('Data barang berhasil ditambahkan')
                return redirect(url_for('kelola_barang'))
            else:
                flash('Terjadi kesalahan saat menambahkan data barang')
                return redirect(url_for('tambah_barang'))
        else:
            return render_template('form-barang.html')
            
@app.route('/kelola_supplier/tambah_supp', methods=['GET', 'POST'])
@login_required
def tambah_supp():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            # retrieve data from form
            id_supplier = request.form['id_supplier']
            supplier_name = request.form['supplier_name']
            address = request.form['address']
            phone_number = request.form['phone_number']
            email = request.form['email']

            
            # create data payload
            data = {
                'id_supplier': id_supplier,
                'supplier_name': supplier_name,
                'address': address,
                'phone_number': phone_number,
                'email': email
            }
            
            # send post request to API
            response = requests.post(f"{URL_data}/supplier", json=data)
            
            if response.status_code == 201:
                flash('Data barang berhasil ditambahkan')
                return redirect(url_for('kelola_supplier'))
            else:
                flash('Terjadi kesalahan saat menambahkan data barang')
                return redirect(url_for('tambah_supp'))
        else:
            return render_template('form-supp.html')
    
@app.route('/regis_user', methods=['GET', 'POST'])
@login_required
def regis_user():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    login_time = datetime.datetime.strptime(session['login_time'], '%Y-%m-%d %H:%M:%S')
    if (datetime.datetime.strptime(now, '%Y-%m-%d %H:%M:%S') - login_time) > datetime.timedelta(minutes=30):
        flash('Sesi Anda telah berakhir, silakan login kembali')
        session.clear()
        return redirect(url_for('login'))
    else:
        if request.method == 'POST':
            # retrieve data from form
            # jadikan inputan password dihash
            
            email = request.form['email']
            username = request.form['username']
            password = request.form['password']
            level = request.form['level']
            
            # create data payload
            data = {
                'email': email,
                'username': username,
                'password': password,
                'level': level
            }
            
            # send post request to API
            response = requests.post(f"{URL_data}/users", json=data)
            
            if response.status_code == 201:
                flash('Data barang berhasil ditambahkan')
                return redirect(url_for('data_user'))
            else:
                flash('Terjadi kesalahan saat menambahkan data barang')
                return redirect(url_for('regis_user'))
        else:
            return render_template('register-user.html')

@app.route("/barang/update", methods=['GET', 'POST', 'PUT'])
def productDetail():
        if request.method == 'POST':
            id_item = request.form['id_item']
            item_name = request.form['item_name']
            quantity = request.form['quantity']
            id_supplier = request.form['id_supplier']
            id_expiration = request.form['id_expiration']
            category = request.form['category']
            status = request.form['status']
            exp_date = request.form['exp_date']
            
            data = {
                'id_item': id_item,
                'item_name': item_name,
                'quantity': quantity,
                'id_supplier': id_supplier,
                'id_expiration': id_expiration,
                'category': category,
                'status': status,
                'exp_date': exp_date}
            print(data)
            try:
                response = requests.post(f"{URL_data}/update", json=data)
                if response.status_code == 200:
                    print("update success")
                else:
                    print("ERROR |update product |", response.status_code)
            except Exception as e:
                print("ERROR | update product |", e)
            return redirect(url_for('kelola_barang'))
        return redirect(url_for('kelola_barang'))

@app.route("/supp/update", methods=['GET', 'POST', 'PUT'])
def supplierDetail():
    if request.method == 'POST':
        id_supplier = request.form['id_supplier']
        supplier_name = request.form['supplier_name']
        address = request.form['address']
        phone_number = request.form['phone_number']
        email = request.form['email']
        
        data = {
            'id_supplier': id_supplier,
            'supplier_name': supplier_name,
            'address': address,
            'phone_number': phone_number,
            'email': email}
        print(data)
    try:
        response = requests.post(f"{URL_data}/update_supp", json=data)
        if response.status_code == 200:
            print('update success')
        else:
            print("ERROR |update product |", response.status_code)
    except Exception as e:
            print("ERROR | update product |", e)
            return redirect(url_for('kelola_supplier'))
    return redirect(url_for('kelola_supplier'))

@app.route("/delete", methods=['GET', 'POST', 'DELETE'])
def productDelete():
        id_item = request.form['id_item']
        try:
            response = requests.post(f"{URL_data}/delete", json={'id_item': id_item})
            if response.status_code == 200:
                print("deleted successfully")
            else:
                print("ERROR | Delete product |", response.status_code)
        except Exception as e:
            print("ERROR | Delete product |", e)
        # Redirect ke halaman product setelah produk dihapus
        return redirect(url_for('kelola_barang'))

@app.route("/delete_supp", methods=['GET', 'POST', 'DELETE'])
def suppDelete():
        id_supplier = request.form['id_supplier']
        try:
            response = requests.post(f"{URL_data}/delete_supp", json={'id_supplier': id_supplier})
            if response.status_code == 200:
                print("deleted successfully")
            else:
                print("ERROR | Delete |", response.status_code)
        except Exception as e:
            print("ERROR | Delete |", e)
        return redirect(url_for('kelola_supplier'))
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)