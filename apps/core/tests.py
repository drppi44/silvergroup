from django.test import TestCase
from plaid import Client, errors as plaid_errors
from .utils import process_account_creation, process_transaction
from .models import Account
import traceback
import stripe


Client.config({
    'url': 'https://tartan.plaid.com'
})
account_type = 'bofa'
stripe.api_key = 'sk_test_OnePfOj1vtFbKqW96gTIrhSy'


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
            self.assertEqual(response.json()['type'], 'questions')
            self.assertEqual(response.status_code, 201)
            response = client.connect_step(account_type, 'tomato')
            self.assertEqual(response.status_code, 200)
            response = client.connect_get()
            accounts = response.json()["accounts"]
            transactions = response.json()["transactions"]
            for account in accounts:
                process_account_creation(account)
            for transaction in transactions:
                process_transaction(transaction)
            print Account.objects.values_list('_id', 'pend_transfer')
        except plaid_errors.UnauthorizedError:
            traceback.print_exc()


class TestStripe(TestCase):
    def test_connection(self):
        print stripe.Charge.retrieve(
          "ch_190wZVHXVG5gpinqOcGu0Uvw", expand=['customer']
        )
        print stripe.Customer.list(limit=3)
        print stripe.Balance.retrieve()
