
from flask_restful import Api
from flask import Blueprint

from .views import Products,SingleProduct,SaleRecords,SingleSaleRecord,UserAccount,LoginUsers

version1 = Blueprint('api',__name__,url_prefix='/api/v1')

api=Api(version1)

api.add_resource(LoginUsers,'/login')
api.add_resource(UserAccount,'/users')
api.add_resource(Products,'/products')
api.add_resource(SingleProduct,'/products/<productID>')
api.add_resource(SaleRecords,'/sales')
api.add_resource(SingleSaleRecord,'/sales/<saleID>')
