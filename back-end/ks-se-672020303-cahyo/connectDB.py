import psycopg2

# Koneksi Database
instance_name = "sat-kapita-selekta-b:asia-southeast2:training-kapita-selekta"
port = 5432
db = "postgres"
user = "postgres"
password = "FwF6qfEA5AzlztzG"
param = f"host='/cloudsql/{instance_name}' port={port} dbname='{db}' user='{user}' password= '{password}'"
# param = f"host='localhost' port={port} dbname='{db}' user='{user}' password='{password}'"
conn = psycopg2.connect(param)

# Class Databasequery Baris code tersebut mendefinisikan sebuah class Python bernama Databasequery 
# yang berfungsi untuk melakukan operasi CRUD pada database PostgreSQL menggunakan library psycopg2. 
class Databasequery:
    def select(query='', data=()):
        try:
            conn = psycopg2.connect(param)
            cursor = conn.cursor()
            cursor.execute(query, data)
            data = cursor.fetchall()
            cursor.close()
            del(conn)
            return True, data
        except Exception as e:
            print(str(e))
            return False, "Data not found"
    def insert(query=''):
        try:
            conn = psycopg2.connect(param)
            cursor = conn.cursor()
            result = cursor.execute(query)
            conn.commit()
            cursor.close()
            del(conn)
            return True, "Insert data successfully"
        except psycopg2.errors.SyntaxError as e:
            print(str(e))
            return False, "Make sure there are no typing errors"
        except Exception as e:
            print(f"Unexpected {e=}, {type(e)=}")
            return False, "An unknown error has occurred :)"
    def update(query=''):
        try:
            conn = psycopg2.connect(param)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            del(conn)
            return True, "Update data successfully"
        except psycopg2.errors.SyntaxError as e:
            print(str(e))
            return False, "Make sure there are no typing errors"
        except Exception as e:
            print(str(e))
            return False, "An unknown error has occurred :)"
        
    def delete(query=''):
        try:
            conn = psycopg2.connect(param)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            cursor.close()
            del(conn)
            return True, "Delete data successfully"
        except psycopg2.errors.UndefineColumn:
            return False, "Delete failed, column not found"
        except Exception as e:
            print(str(e))
            return False, "An unknown error has occurred :)"
    
    # Baris code dibawah diPakai untuk proses Delete dan Update dibagian Frontend
    def selectID(id_item):
        conn=psycopg2.connect(param)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("SELECT * FROM public._672020303_cahyo_warehouse WHERE id_item = %s", (id_item,))
            rows = cur.fetchall()
            cur.close()
            item = []
            for row in rows:
                items = {
                    "id_item": row[0],
                    "item_name": row[1],
                    "quantity": row[2],
                    "id_supplier": row[3],
                    "id_expiration": row[4],
                    "category": row[5],
                    "status": row[6],
                    "created_at": str(row[7]),
                    "updated_at": str(row[8]),
                    "exp_date": str(row[9])
                }
                item.append(row)
            return items
        else:
            return None
        
    def selectSupp(id_supplier):
        con = psycopg2.connect(param)
        if con is not None:
            cur = con.cursor()
            cur.execute("SELECT * FROM public._672020303_cahyo_supplier WHERE id_supplier = %s", (id_supplier,))
            rows = cur.fetchall()
            cur.close()
            supp = []
            for row in rows:
                supplier = {
                    "id_supplier": row[0],
                    "supplier_name": row[1],
                    "address": row[2],
                    "phone_number": row[3],
                    "created_at": str(row[4]),
                    "updated_at": str(row[5])
                }
                supp.append(row)
            return supplier
        else:
            return None
        
    def updateBarang(id_item, item_name, quantity, id_supplier, id_expiration, category, status, exp_date):
        conn = psycopg2.connect(param)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("UPDATE public._672020303_cahyo_warehouse SET item_name = %s, quantity = %s, id_supplier = %s, id_expiration = %s, category = %s, status = %s, exp_date = %s WHERE id_item = %s", (item_name, quantity, id_supplier, id_expiration, category, status, exp_date, id_item))
            conn.commit()
            cur.close()
            return True
        else:
            return False
        
    def updateSupplier(id_supplier, supplier_name, address, phone_number, email):
        con = psycopg2.connect(param)
        if con is not None:
            cur = con.cursor()
            cur.execute("UPDATE public._672020303_cahyo_supplier SET supplier_name = %s, address = %s, phone_number = %s, email = %s WHERE id_supplier = %s", (supplier_name, address, phone_number, email, id_supplier))
            con.commit()
            cur.close()
            return True
        else:
            return False
        
    def deleteBarang(id_item):
        conn = psycopg2.connect(param)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM public._672020303_cahyo_warehouse WHERE id_item = %s", [id_item])
            conn.commit()
            cur.close()
            return True
        else:
            return False
    
    def deleteSupplier(id_supplier):
        conn = psycopg2.connect(param)
        if conn is not None:
            cur = conn.cursor()
            cur.execute("DELETE FROM public._672020303_cahyo_supplier WHERE id_supplier = %s", [id_supplier])
            conn.commit()
            cur.close()
            return True
        else:
            return False