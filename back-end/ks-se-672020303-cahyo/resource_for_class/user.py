import falcon
import json
from connectDB import Databasequery as db
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Kode di dibawah adalah implementasi endpoint API untuk operasi CRUD 
# (Create, Read, Update, Delete) pada tabel "_672020303_cahyo_user" pada database publik.

class User:
    def on_get(self, req, resp):
        self.data = db.select('SELECT * FROM public._672020303_cahyo_user')
        media = []
        status = falcon.HTTP_500
        if self.data[0] == False:
            print(self.data[1])
        else:
            returnData = []
            if not self.data[1]:
                media = []
                status = falcon.HTTP_404
            else:
                for row in self.data[1]:
                    returnData.append({
                        'email': row[0],
                        'username': row[1],
                        'password': row[2],
                        'level': row[3],
                        'created_at': str(row[4]), # convert to string
                        'updated_at': str(row[5]) 
                    })
                media = returnData
                status = falcon.HTTP_200

        resp.media = media
        resp.status = status
        
    def on_post(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rd = json.load(req.bounded_stream) 
        
        hashPassword = generate_password_hash(rd.get('password'))
        query = f"INSERT INTO public._672020303_cahyo_user(email, username, password, level, created_at, updated_at) VALUES('{rd.get('email')}', '{rd.get('username')}', '{hashPassword}', '{rd.get('level')}', '{formatDateNow}', '{formatDateNow}');"
        result = db.insert(query)
        if result[0]:
            message = "Insert Data Success"
        else:
            message = "Insert Data Failed"
            
        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_201

    def on_put(self, req, resp):
        formatDateNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        rd = json.load(req.bounded_stream)

        hashPassword = generate_password_hash(rd.get('password'))
        query = f"UPDATE public._672020303_cahyo_user SET username = '{rd.get('username')}', password = '{hashPassword}', level = '{rd.get('level')}', updated_at = '{formatDateNow}' WHERE email = '{rd.get('email')}';"
        result = db.update(query)
        if result[0]:
            message = "Update Data Success"
        else:
            message = "Update Data Failed"

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        rd = json.load(req.bounded_stream)

        query = f"DELETE FROM public._672020303_cahyo_user WHERE email = '{rd.get('email')}';"
        result = db.delete(query)
        if result[0]:
            message = "Delete Data Success"
        else:
            message = "Delete Data Failed"

        resp.media = [{'message': message}]
        resp.status = falcon.HTTP_200
