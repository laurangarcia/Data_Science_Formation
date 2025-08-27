"""
Una test suite es como una carpeta que contiene varias pruebas (test cases), cada una diseñada para validar un aspecto específico del software.
Runner: Para ejecutar las suite, es algo que coge todas las pruebas y las va ejecutando una por una
"""

import unittest 
from tests.test_bank_account import BankAccountTests

def bank_account_suite():
    suite = unittest.TestSuite()
    suite.addTest(BankAccountTests("test_deposit"))
    suite.addTest(BankAccountTests("test_withdraw"))
    return suite

if __name__ == "__main__": # permite ejecutar la suite directamente
    runner = unittest.TextTestRunner()
    runner.run(bank_account_suite())

#para correr este archivo en el cmd: $env:PYTHONPATH='.'; python tests/test_suites.py