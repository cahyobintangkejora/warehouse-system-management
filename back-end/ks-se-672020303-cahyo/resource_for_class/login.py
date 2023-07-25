import falcon
import json
from connectDB import Databasequery as db
from werkzeug.security import check_password_hash

class Login:
    def on_post(self, req, resp):
        rd = json.load(req.bounded_stream)
        result = db.select(f"SELECT * FROM public._672020303_cahyo_user WHERE email = %s;", (rd.get('email'),))
        if result[0]:
            if not result[1]:
                resp.media = [{'message': 'User Not Found'}]
                resp.status = falcon.HTTP_404
            else:
                if check_password_hash(result[1][0][2], rd.get('password')):
                    resp.media = [{'message': 'Login Success'}]
                    resp.status = falcon.HTTP_200
                else:
                    resp.media = [{'message': 'Password Wrong'}]
                    resp.status = falcon.HTTP_401
        else:
            resp.media = [{'message': 'Login Failed'}]
            resp.status = falcon.HTTP_500

class Logout:
    def on_post(self, req, resp):
        resp.media = [{'message': 'Logout Success'}]
        resp.status = falcon.HTTP_200
        
    def on_get(self, req, resp):
        resp.media = [{'message': 'Logout Failed'}]
        resp.status = falcon.HTTP_500