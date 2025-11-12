import pytest 
import sys
import pathlib
from decimal import Decimal

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src.transaction import TransactionType, TransactionStatus, Transaction, Account


def test_hello_world():
    assert "Hello World" == "Hello World"


def test_account_deposit():
    """Test that depositing money to an account increases balance and creates a completed transaction."""
    # Arrange
    account = Account("ACC001", Decimal("100.00"))
    initial_balance = account.balance
    deposit_amount = Decimal("50.00")
    
    # Act
    transaction = account.deposit(deposit_amount, "Test deposit")
    
    # Assert
    assert account.balance == initial_balance + deposit_amount
    assert transaction.status == TransactionStatus.COMPLETED
    assert transaction.transaction_type == TransactionType.DEPOSIT
    assert transaction.amount == deposit_amount
    assert len(account.transactions) == 1
    assert account.transactions[0] == transaction
