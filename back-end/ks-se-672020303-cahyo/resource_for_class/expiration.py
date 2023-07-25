import falcon
import json
from connectDB import Databasequery as db
import datetime

# MEnampilkan data kadaluarsa per 12 April 2023
class Expiration:
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
                    # filter data based on exp_date before 13 April 2023
                    exp_date_str = str(row[9])
                    if datetime.datetime.strptime(exp_date_str, '%Y-%m-%d').date() < datetime.date(2023, 4, 13):
                        returnData.append({
                            'id_item': row[0],
                            'item_name': row[1],
                            'quantity': row[2],
                            'id_supplier': row[3],
                            'id_expiration': row[4],
                            'category': row[5],
                            'status': row[6],
                            'created_at': str(row[7]), # convert to string
                            'updated_at': str(row[8]),
                            'exp_date': exp_date_str
                        })
                
                media = returnData
                status = falcon.HTTP_200

            resp.media = media
            resp.status = status