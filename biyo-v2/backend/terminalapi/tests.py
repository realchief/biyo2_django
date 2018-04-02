from django.test import TestCase
import requests
import json


class OrdersTests(TestCase):
    headers = {'content-type': 'application/json'}
    create_order_data = data = {
            "balance_remaining": 0,
            "discount_total": 0,
            "emp_open_id": 1,
            "frontend_id": 92,
            "grand_total": 2,
            "number": 0,
            "open_date": "2017-02-06T15:57:43Z",
            "status": 2,
            "subtotal": 2,
            "tax_total": 0
    }
    order_id = 1
    order_item_id = 1
    payment_id = 1

    def update_order(self, id):
        data = self.create_order_data
        data['subtotal'] = 6
        r = requests.put("http://localhost:8000/terminalapi/update/order/%s" % id, data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_create_order_open(self):
        data = self.create_order_data
        data['status'] = 1
        r = requests.post('http://localhost:8000/terminalapi/add/order', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)
        self.update_order(json.loads(r.text).get('id'))

    def test_create_order_closed(self):
        data = self.create_order_data
        data['status'] = 3
        r = requests.post('http://localhost:8000/terminalapi/add/order', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)

    def test_create_order_hold(self):
        data = self.create_order_data
        data['status'] = 2
        r = requests.post('http://localhost:8000/terminalapi/add/order', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)

    def test_create_order_cancelled(self):
        data = self.create_order_data
        data['status'] = 4
        r = requests.post('http://localhost:8000/terminalapi/add/order', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)

    def test_create_order_refunded(self):
        data = self.create_order_data
        data['status'] = 5
        r = requests.post('http://localhost:8000/terminalapi/add/order', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)

    def test_add_order_misc_item(self):
        data = {
            "cost": 0,
            "discount": 0,
            "employee": 1,
            "frontend_id": 1,
            "name": "Misc Item",
            "order_id": 1,
            "price": 0,
            "quantity": 1,
            "tax": 0,
            "product": 1,
        }
        r = requests.post('http://localhost:8000/terminalapi/add/order/item', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)

    def update_order_item(self, id):
        data = {
            "price": 9,
            "quantity": 2
        }
        r = requests.put("http://localhost:8000/terminalapi/update/order/item/%s" % id, data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_add_order_item(self):
        data = {
            "cost": 0,
            "discount": 0,
            "employee": 1,
            "frontend_id": 39,
            "name": "Cigar Borek",
            "order_id": self.order_id,
            "price": 8,
            "product": 1,
            "quantity": 1,
            "tax": "0.00",
            "terminal_id": 0
        }
        r = requests.post('http://localhost:8000/terminalapi/add/order/item', data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)
        self.update_order_item(json.loads(r.text).get('id'))

    def update_payment(self, id):
        data = {
            "amount": 11,
            "tips": 1
        }
        r = requests.put("http://localhost:8000/terminalapi/update/payments/%s" % id, data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_add_order_payment(self):
        data = {
            "amount": 10,
            "amount_paid": 0,
            "approval_code": 0,
            "batch_num": 0,
            "change_amount": 0,
            "employee_id": 1,
            "frontend_id": 3,
            "order_id": 1,
            "payment_date": "2014-05-13T15:47:01",
            "payment_form": "CASH",
            "payment_type": "Cash",
            "processor_response": "APPROVAL",
            "signature": "",
            "terminal_id": 0,
            "tips": 0,
            "transaction_id": "",
            "transaction_type": 1,
            "void_ref": 0
        }
        r = requests.post("http://localhost:8000/terminalapi/add/payments", data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)
        self.update_payment(json.loads(r.text).get('id'))

    def update_order_item_modifier(self, id):
        data = {
            "cost": 1,
            "price": 1
        }
        r = requests.put("http://localhost:8000/terminalapi/update/order/item/modifier/%s" % id, data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_add_order_item_modifier(self):
        data = {
            "item_id": 1,
            "name": "Mash Potatoes",
            "cost": 1,
            "price": 1,
            "oryginal_id": 1,
            "group_id": 1
        }
        r = requests.post("http://localhost:8000/terminalapi/add/order/item/modifier", data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 201)
        self.update_order_item_modifier(json.loads(r.text).get('id'))

    def test_update_table(self):
        data = {
            "x_value": 150,
            "y_value": 150,
            "table_name": "test"
        }
        r = requests.put("http://localhost:8000/terminalapi/update/table/1", data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def update_customer(self, id):
        data = {
            "last_name": "McQueen Jr",
            "rewards_points": 16
        }
        r = requests.post("http://localhost:8000/terminalapi/update/customer/%s" % id, data=json.dumps(data), headers=self.headers)
        self.assertEqual(r.status_code, 200)

    def test_add_customer(self):
        data = {
            "account_number": "1215212515215",
            "address": "LA, street",
            "email": "bobby_superstar@gmail.com",
            "first_name": "bobby",
            "last_name": "McQueen",
            "notes": "some notes, not required",
            "phone": "5556666123",
            "profile_key": "profile_key",
            "rewards_points": 15
        }
        r = requests.post("http://localhost:8000/terminalapi/add/customer", data=json.dumps(data), headers=self.headers)

        self.assertEqual(r.status_code, 201)
        self.update_customer(json.loads(r.text).get('id'))
