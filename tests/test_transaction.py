import pytest 
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src.transaction import TransactionType, TransactionStatus, Transaction, Account
from decimal import Decimal


def test_hello_world():
    assert "Hello World" == "Hello World"


def test_transaction_creation_and_completion():
    """Test that a Transaction is created with PENDING status and can be completed"""
    # Create a transaction
    account_id = "ACC123"
    amount = Decimal("100.00")
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        transaction_type=TransactionType.DEPOSIT,
        description="Test deposit"
    )
    
    # Verify initial state
    assert transaction.account_id == account_id
    assert transaction.amount == amount
    assert transaction.transaction_type == TransactionType.DEPOSIT
    assert transaction.description == "Test deposit"
    assert transaction.status == TransactionStatus.PENDING
    assert transaction.id is not None
    assert transaction.timestamp is not None
    
    # Complete the transaction
    transaction.complete()
    assert transaction.status == TransactionStatus.COMPLETED
