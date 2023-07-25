import falcon
from resource_for_class.test import Testconnect
from resource_for_class.user import User
from resource_for_class.warehouse import Warehouse, Wlist, UpdateBarang, DeleteBarang, UpdateSupplier, DeleteSupplier
from resource_for_class.login import Login
from resource_for_class.supplier import Supplier
from resource_for_class.expiration import Expiration


# Route for each class
app = falcon.App()
app.add_route('/test', Testconnect())
app.add_route('/users', User())
app.add_route('/warehouse', Warehouse())
app.add_route('/login', Login())
app.add_route('/supplier', Supplier())
app.add_route('/exp', Expiration())
app.add_route('/wlist', Wlist())
app.add_route('/update', UpdateBarang())
app.add_route('/delete', DeleteBarang())
app.add_route('/update_supp', UpdateSupplier())
app.add_route('/delete_supp', DeleteSupplier())