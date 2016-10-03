from django.test import TestCase
from plaid import Client, errors as plaid_errors
import traceback


Client.config({
    'url': 'https://tartan.plaid.com'
})
answer = 'tomato'
account_type = 'bofa'


class TestPaid(TestCase):
    def test_connection(self):
        client = Client(
            client_id='57f28ea8062e8c1d58ff9391',
            secret='580f72db7f49c97b4d279b504eda2d'
        )
        try:
            response = client.connect(account_type, {
                'username': 'plaid_test',
                'password': 'plaid_good'
            })
            data = response.json()
            print data
            if response.status_code == 200:
                pass
            elif response.status_code == 201:
                while data.get('type') == 'questions':
                    data = client.connect_step(account_type, answer).json()
                    print data
        except plaid_errors.UnauthorizedError:
            traceback.print_exc()
