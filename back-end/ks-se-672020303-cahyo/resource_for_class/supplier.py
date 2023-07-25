import falcon
import json
from connectDB import Databasequery as db
from datetime import datetime

# Kode di dibawah adalah implementasi endpoint API untuk operasi CRUD 
# (Create, Read, Update, Delete) pada tabel "_672020303_cahyo_supplier" pada database publik.

class Supplier:
    def on_get(self, req, resp):
        self.data = db.select('SELECT * FROM public._672020303_cahyo_supplier')
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
                        'id_supplier': row[0],
                        'supplier_name': row[1],
                        'address': row[2],
                        'phone_number': row[3],
                        'email': row[4],
                        'created_at': str(row[5]), # convert to string
                        'updated_at': str(row[6]) 
                    })
                media = returnData
                status = falcon.HTTP_200

            resp.media = media
            resp.status = status

    def on_post(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # rd = json.loads(req.stream.read())
        rd = json.load(req.bounded_stream)

        query = f"INSERT INTO public._672020303_cahyo_supplier (id_supplier, supplier_name, address, phone_number, email, created_at, updated_at) VALUES ('{rd.get('id_supplier')}', '{rd.get('supplier_name')}', '{rd.get('address')}', '{rd.get('phone_number')}', '{rd.get('email')}', '{formatDateNow}', '{formatDateNow}');"
        result = db.insert(query)
        if result[0]:
            message = "Insert Data to Table Supplier Success"
            resp.status = falcon.HTTP_201
        else:
            message = "Insert Data to Table Supplier Failed"
            resp.status = falcon.HTTP_500

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rd = json.load(req.bounded_stream)
        id_supplier = rd.get('id_supplier')
        supplier_name = rd.get('supplier_name')
        address = rd.get('address')
        phone_number = rd.get('phone_number')
        email = rd.get('email')

        check_id_query = f"SELECT * FROM public._672020303_cahyo_supplier WHERE id_supplier='{id_supplier}'"
        check_id_result = db.select(check_id_query)

        if check_id_result[0]:
            if not check_id_result[1]:
                message = "ID Supplier Not Found"
                resp.status = falcon.HTTP_404
            else:
                query = f"UPDATE public._672020303_cahyo_supplier SET supplier_name='{supplier_name}', address='{address}', phone_number='{phone_number}', email='{email}', updated_at='{formatDateNow}' WHERE id_supplier='{id_supplier}';"
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
        id_supplier = rd.get('id_supplier')

        check_id_query = f"SELECT * FROM public._672020303_cahyo_supplier WHERE id_supplier='{id_supplier}'"
        check_id_result = db.select(check_id_query)

        if check_id_result[0]:
            if not check_id_result[1]:
                message = "ID Supplier Not Found"
                resp.status = falcon.HTTP_404
            else:
                query = f"DELETE FROM public._672020303_cahyo_supplier WHERE id_supplier='{id_supplier}';"
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