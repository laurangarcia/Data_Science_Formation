import unittest
from src.bank_account import BankAccount
import os

class BankAccountTests(unittest.TestCase):
    def setUp(self) -> None:
        self.account = BankAccount(balance=1000, log_file="transaction_log.txt")
    
    def tearDown(self) -> None: 
        if os.path.exists(self.account.log_file):
            os.remove("transaction_log.txt")
    
    def _count_lines(self, filename):
        with open(filename, "r") as f:
            return len(f.readlines())

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, "El balance no es igual")

    def test_withdraw(self):
        new_balance = self.account.withdraw(300)
        self.assertEqual(new_balance, 700, "El balance no es igual")

    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)
    
    def test_transfer(self):
        target_account = BankAccount(balance=500)
        result = self.account.transfer(300, target_account)
        assert result is True
        assert self.account.get_balance() == 700
        assert target_account.get_balance() == 800

    def test_transaction_log(self):
        self.account.deposit(200)
        self.assertTrue(os.path.exists("transaction_log.txt"))

    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1  # Account created
        self.account.deposit(500)
        assert self._count_lines(self.account.log_file) == 2  # Account created
  
