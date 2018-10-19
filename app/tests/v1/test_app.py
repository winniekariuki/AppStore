import unittest
from app import create_app
from instance.config import app_config
import json
from app.api.v1.views import clear_data
class TestProducts(unittest.TestCase):

    def setUp(self):
        self.app = create_app(config_name="testing")
        self.test_client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        product_data = json.dumps({
                "name":"del",
                "model_no":"1523",
                "price":"2516"
            })
        self.sale_data = json.dumps({
                "id":1

            })
        users_data = json.dumps({
                "username":"winnie",
                "password":"1234",
                "role":"Admin"

            })
        login_data = json.dumps({
                "username":"winnie",
                "password":"1234"

            })
        users_data_storeattendant = json.dumps({
                "username":"Ann",
                "password":"12",
                "role":"storeattendant"

            })
        login_data_storeattendant = json.dumps({
                "username":"Ann",
                "password":"12"

            })


        self.create_admin_user=self.test_client.post('api/v1/users',data=users_data,content_type='application/json')
        self.login_admin_user=self.test_client.post('api/v1/login',data=login_data,content_type='application/json')

        self.create_attendant__user=self.test_client.post('api/v1/users',data=users_data_storeattendant,content_type='application/json')
        self.login_attendant_user=self.test_client.post('api/v1/login',data=login_data_storeattendant,content_type='application/json')
        

        self.admin_token=json.loads(self.login_admin_user.data.decode())
        self.storeattendant_token=json.loads(self.login_attendant_user.data.decode())

        self.create_product=self.test_client.post('api/v1/products',data=product_data,headers={'content-type':'application/json','access-token':self.admin_token["token"]})
        self.create_sale=self.test_client.post('api/v1/sales',data=self.sale_data,headers={'content-type':'application/json','access-token':self.storeattendant_token["token"]})
        print(self.create_product.data)
        print(self.create_sale.data)

    def tearDown(self):
        clear_data()
        self.app_context.pop()

    def test_signup(self):
        user =  json.dumps({
              "username":"winnie",
              "password":"1234",
              "role":"Admin"
            })
        user =  json.dumps({
              "username":"Dee",
              "password":"0707",
              "role":"storeattendant"
            })

        response=self.test_client.post('/api/v1/users',data=user,content_type='application/json')
        
        self.assertEqual(response.status_code,201)
    def test_login(self):
        login = json.dumps({
                "username":"winnie",
                "password":"1234"
                 })
        response=self.test_client.post('/api/v1/login',data=login,content_type='application/json')

        self.assertEqual(response.status_code,200)
    def test_post_products(self):
        data2 = json.dumps({
                "name":"del",
                "model_no":"1523",
                "price":"2516",
                "role":"role"

            })
        
        response=self.test_client.post('api/v1/products',data=data2,headers={'content-type':'application/json','access-token':self.admin_token["token"]})
        self.assertEqual(response.status_code,201)
    def test_get_products(self):

        response=self.test_client.get('api/v1/products',content_type='application/json')
        self.assertEqual(response.status_code,200)
    def  test_get_single_products(self):
        
        response=self.test_client.get('api/v1/products/1',content_type='application/json')
        self.assertEqual(response.status_code,200)   
    