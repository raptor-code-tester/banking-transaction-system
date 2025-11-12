#!/usr/bin/env python3
"""
Main script to demonstrate the transaction system with comprehensive test data.
"""

from decimal import Decimal
from transaction import Account, TransactionType, TransactionStatus

def print_account_summary(account):
    """Print account balance and transaction history."""
    print(f"\n--- Account {account.account_id} Summary ---")
    print(f"Balance: ${account.balance}")
    print(f"Total Transactions: {len(account.transactions)}")
    
    for tx in account.transactions:
        print(f"  {tx.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | "
              f"{tx.transaction_type.value.upper()} | "
              f"${tx.amount} | "
              f"{tx.status.value.upper()} | "
              f"{tx.description}")

def main():
    """Run comprehensive transaction tests."""
    print("=== Banking Transaction System Demo ===\n")
    
    # Create test accounts
    alice = Account("ACC001", Decimal('2500.00'))
    bob = Account("ACC002", Decimal('1200.00'))
    charlie = Account("ACC003", Decimal('800.00'))
    merchant = Account("MERCH001", Decimal('5000.00'))
    
    print("Initial account balances:")
    for acc in [alice, bob, charlie, merchant]:
        print(f"  {acc.account_id}: ${acc.balance}")
    
    # Test deposits
    print("\n--- Testing Deposits ---")
    alice.deposit(Decimal('500.00'), "Monthly salary")
    bob.deposit(Decimal('300.00'), "Freelance payment")
    charlie.deposit(Decimal('150.00'), "Birthday gift")
    
    # Test withdrawals
    print("\n--- Testing Withdrawals ---")
    alice.withdraw(Decimal('200.00'), "ATM cash withdrawal")
    bob.withdraw(Decimal('50.00'), "Coffee shop")
    
    # Test transfers
    print("\n--- Testing Transfers ---")
    alice.transfer(bob, Decimal('250.00'), "Rent split payment")
    bob.transfer(charlie, Decimal('75.00'), "Dinner payment")
    charlie.transfer(alice, Decimal('25.00'), "Book loan repayment")
    
    # Test payments to merchant
    print("\n--- Testing Merchant Payments ---")
    alice.transfer(merchant, Decimal('120.00'), "Online shopping")
    bob.transfer(merchant, Decimal('85.00'), "Grocery purchase")
    charlie.transfer(merchant, Decimal('45.00'), "Gas station")
    
    # Test multiple small transactions
    print("\n--- Testing Multiple Small Transactions ---")
    for i in range(3):
        alice.deposit(Decimal('10.00'), f"Cashback reward #{i+1}")
        bob.withdraw(Decimal('5.00'), f"Vending machine #{i+1}")
    
    # Test edge cases
    print("\n--- Testing Edge Cases ---")
    try:
        alice.withdraw(Decimal('10000.00'), "Large withdrawal attempt")
    except ValueError as e:
        print(f"Expected error: {e}")
    
    try:
        bob.deposit(Decimal('-50.00'), "Negative deposit attempt")
    except ValueError as e:
        print(f"Expected error: {e}")
    
    # Final account summaries
    print("\n" + "="*60)
    print("FINAL ACCOUNT SUMMARIES")
    print("="*60)
    
    for account in [alice, bob, charlie, merchant]:
        print_account_summary(account)
    
    # Transaction statistics
    total_transactions = sum(len(acc.transactions) for acc in [alice, bob, charlie, merchant])
    total_volume = sum(tx.amount for acc in [alice, bob, charlie, merchant] for tx in acc.transactions)
    
    print(f"\n--- System Statistics ---")
    print(f"Total Transactions Processed: {total_transactions}")
    print(f"Total Transaction Volume: ${total_volume}")
    print(f"Average Transaction Size: ${total_volume / total_transactions:.2f}")

if __name__ == "__main__":
    main()