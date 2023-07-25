import falcon
import json
from connectDB import Databasequery as db
from datetime import datetime

# Kode di dibawah adalah implementasi endpoint API untuk operasi CRUD 
# (Create, Read, Update, Delete) pada tabel "_672020303_cahyo_warehouse" pada database publik.

class Warehouse:
    def on_get(self, req, resp):
        self.data = db.select('SELECT * FROM public._672020303_cahyo_warehouse')
        media = []
        status = falcon.HTTP_500
        if not self.data[0]:
            resp.media = [{'message': self.data[1]}]
            resp.status = falcon.HTTP_500
        else:
            returnData = []
            if not self.data[1]:
                media = []
                status = falcon.HTTP_404
            else:
                for row in self.data[1]:
                    returnData.append({
                        'id_item': row[0],
                        'item_name': row[1],
                        'quantity': row[2],
                        'id_supplier': row[3],
                        'id_expiration':row[4],
                        'category': row[5],
                        'status':row[6],
                        'created_at': str(row[7]), # convert to string
                        'updated_at': str(row[8]),
                        'exp_date': str(row[9]) 
                    })
                media = returnData
                status = falcon.HTTP_200

            resp.media = media
            resp.status = status

# def on_post(self, req, resp): CODE CHECK FK THE TABLE, CODE ERROR
#     formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     rd = json.load(req.bounded_stream)

#     # Check if id_supplier exists
#     query_supplier = f"SELECT COUNT(*) FROM public._672020303_cahyo_supplier WHERE id_supplier='{rd.get('id_supplier')}'"
#     result_supplier = db.select(query_supplier)

#     if result_supplier[0][0] == 0:
#         resp.media = [{'message': "Please input valid id_supplier"}]
#         resp.status = falcon.HTTP_400
#         return

#     # Check if id_expiration exists
#     query_expiration = f"SELECT COUNT(*) FROM public._672020303_cahyo_expiration_list WHERE id_expiration='{rd.get('id_expiration')}'"
#     result_expiration = db.select(query_expiration)

#     if result_expiration[0][0] == 0:
#         resp.media = [{'message': "Please input valid id_expiration"}]
#         resp.status = falcon.HTTP_400
#         return

#     # Insert data to warehouse table
#     query = f"INSERT INTO public._672020303_cahyo_warehouse (id_item, item_name, quantity, id_supplier, id_expiration, category, status, created_at, updated_at) VALUES ('{rd.get('id_item')}', '{rd.get('item_name')}', '{rd.get('quantity')}', '{rd.get('id_supplier')}', '{rd.get('id_expiration')}', '{rd.get('category')}', '{rd.get('status')}', '{formatDateNow}', '{formatDateNow}');"
#     result = db.insert(query)

#     if result[0]:
#         message = "Insert Data to Table Warehouse Success"
#         resp.status = falcon.HTTP_201
#     else:
#         message = "Insert Data to Table Warehouse Failed"
#         resp.status = falcon.HTTP_500

#     resp.media = [{'message': message}]
#     resp.status = falcon.HTTP_201

    def on_post(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rd = json.load(req.bounded_stream)
        query = f"INSERT INTO public._672020303_cahyo_warehouse (id_item, item_name, quantity, id_supplier, id_expiration, category, status, created_at, updated_at, exp_date) VALUES ('{rd.get('id_item')}', '{rd.get('item_name')}', '{rd.get('quantity')}', '{rd.get('id_supplier')}', '{rd.get('id_expiration')}', '{rd.get('category')}', '{rd.get('status')}', '{formatDateNow}', '{formatDateNow}', '{rd.get('exp_date')}');"

        result = db.insert(query)
        if result[0]:
            message = "Insert Data to Table Warehouse Success"
            resp.status = falcon.HTTP_201
        else:
            message = "Insert Data to Table Warehouse Failed"
            resp.status = falcon.HTTP_500

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rd = json.load(req.bounded_stream)
        id_item = rd.get('id_item')
        item_name = rd.get('item_name')
        quantity = rd.get('quantity')
        id_supplier = rd.get('id_supplier')
        id_expiration = rd.get('id_expiration')
        category = rd.get('category')
        status = rd.get('status')
        exp_date = rd.get('exp_date')

        check_id_query = f"SELECT * FROM public._672020303_cahyo_warehouse WHERE id_item='{id_item}'"
        check_id_result = db.select(check_id_query)

        if check_id_result[0]:
            if not check_id_result[1]:
                message = "ID Supplier Not Found"
                resp.status = falcon.HTTP_404
            else:
                query = f"UPDATE public._672020303_cahyo_warehouse SET item_name='{item_name}', quantity='{quantity}', id_supplier='{id_supplier}', id_expiration='{id_expiration}', category='{category}', status='{status}',updated_at='{formatDateNow}', exp_date='{exp_date}' WHERE id_item='{id_item}';"
                result = db.update(query)
                if result[0]:
                    message = "Update Data to Table Supplier Success"
                    resp.status = falcon.HTTP_200
                else:
                    message = "Update Data to Table Supplier Failed"
                    resp.status = falcon.HTTP_500
        else:
            message = "Update Data to Table Supplier Failed"
            resp.status = falcon.HTTP_500

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        rd = json.load(req.bounded_stream)
        id_item = rd.get('id_item')

        check_id_query = f"SELECT * FROM public._672020303_cahyo_warehouse WHERE id_item='{id_item}'"
        check_id_result = db.select(check_id_query)

        if check_id_result[0]:
            if not check_id_result[1]:
                message = "ID Supplier Not Found"
                resp.status = falcon.HTTP_404
            else:
                query = f"DELETE FROM public._672020303_cahyo_warehouse WHERE id_item='{id_item}';"
                result = db.delete(query)
                if result[0]:
                    message = "Delete Data to Table Supplier Success"
                    resp.status = falcon.HTTP_200
                else:
                    message = "Delete Data to Table Supplier Failed"
                    resp.status = falcon.HTTP_500
        else:
            message = "Delete Data to Table Supplier Failed"
            resp.status = falcon.HTTP_500

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_200

class Wlist:
    def on_post(self, req, resp):
        id_item = req.media.get('id_item')
        if not id:
            resp.status = falcon.HTTP_BAD_REQUEST
            return
        item = db.selectID(id_item)
        if item:
            resp.status = falcon.HTTP_200
            resp.media = { "item": item}
        else:
            resp.status = falcon.HTTP_401
            resp.media = {'message': ' not found'}

# Baris Code dibawah merupakan Class untuk memanggil Tampilan saat UPDATE dan DELETE DATA
# Memakai post post karena ditampilan memakai Modal

class UpdateBarang:
    def on_post(self, req, resp):
        data = req.media
        id_item = data['id_item']
        item_name = data['item_name']
        quantity = data['quantity']
        id_supplier = data['id_supplier']
        id_expiration = data['id_expiration']
        category = data['category']
        status = data['status']
        exp_date = data['exp_date']
        if not item_name or not quantity or not id_supplier or not id_expiration or not category or not status or not exp_date:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'Not found'}
            return
        if db.updateBarang(id_item, item_name, quantity, id_supplier, id_expiration, category, status, exp_date):
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'success updated hhhh'}
        else:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'not updated'}

class UpdateSupplier:
    def on_post(self, req, resp):
        data = req.media
        id_supplier = data['id_supplier']
        supplier_name = data['supplier_name']
        address = data['address']
        phone_number = data['phone_number']
        email = data['email']
        if not supplier_name or not address or not phone_number or not email:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'not found'}
            return
        if db.updateSupplier(id_supplier, supplier_name, address, phone_number, email):
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'success updated hhhh'}
        else:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'not updated'}
    
class DeleteBarang:
    def on_post(self, req, resp):
        data = req.media
        id_item = data['id_item']
        if not id_item:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'not found'}
            return
        if db.deleteBarang(id_item):
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'success deleted'}
        else:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'item not deleted'}

class DeleteSupplier:
    def on_post(self,req, resp):
        data = req.media
        id_supplier = data['id_supplier']
        if not id_supplier:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'not found'}
            return
        if db.deleteSupplier(id_supplier):
            resp.status = falcon.HTTP_200
            resp.media = {'message': 'success deleted'}
        else:
            resp.status = falcon.HTTP_400
            resp.media = {'message': 'data not deleted'}