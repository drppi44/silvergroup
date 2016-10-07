from .models import Transaction, Account


def _get_pending_delta(float_value):
    float_value = abs(float_value)
    value = int(float_value) - float_value
    return value or 1.


def process_account_creation(account_data_json):
    Account.objects.create(_id=account_data_json['_id'])


def process_transaction(transaction_data_json):
    account = Account.objects.get(_id=transaction_data_json['_account'])
    transaction = Transaction.objects.create(
        account=account,
        _id=transaction_data_json['_id'],
        amount=float(transaction_data_json['amount'])
    )
    if transaction.amount < 0:
        account.pend_transfer += _get_pending_delta(transaction.amount)
        account.save()
