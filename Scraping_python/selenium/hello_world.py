import unittest
from pyunitreport import HTMLTestrunner
from selenium import webdriver

class HelloWorld(unittest.TestCase):
    def setUp(self): #prepara el entorno antes de hacer la prueba 
        self.driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
        driver = self.driver
        driver.implicitly_wait(30)
        driver.maximize_window()
        driver.get('http://www.google.com')

    def test_hello_world(self):
        driver = self.driver
        search_box = driver.find_element_by_name('q')
        search_box.send_keys('Hello World')
        search_box.submit()
        print(driver.title)

    def tearDown(self): #cierra el entorno despues de hacer la prueba
        self.driver.quit() 

if __name__ == "__main__":
    unittest.main(testRunner=HTMLTestrunner(output='reportes', report_name='hello-world-report'))
