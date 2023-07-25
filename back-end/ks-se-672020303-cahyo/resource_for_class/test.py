from connectDB import Databasequery as db 

# Cek COneection
class Testconnect:
    def on_get(self, req, resp):
        query = "SELECT current_date"
        result = db.select(query)
        result = str(result[1][0])
        resp.media = result
        resp.status = 200