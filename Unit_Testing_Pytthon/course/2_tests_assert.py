
# Código que va ir a producción
def calculate_total(products):
    total = 0
    for product in products:
        total += product["price"]
    return total

def discount(products, percentage):
    total = calculate_total(products)
    return total - (total * percentage / 100)

#  /// PRUEBAS ///
# assert es una declaración que prueba una condición, deteniendo el programa y generando un 
# AssertionError si la condición es falsa, y permitiendo la continuación si es verdadera.
# Sintaxis: assert <condición>, <mensaje_opcional>

def test_calculate_total_with_empty_list():
    assert calculate_total([]) == 0
 
def test_calculate_total_with_single_product():
    products = [
        {"name": "Product 1", "price": 10}
    ]
    assert calculate_total(products) == 10

def test_calculate_total_with_multiple_product():
    products = [
        {"name": "Product 1", "price": 10},
        {"name": "Product 2", "price": 50},
        {"name": "Product 3", "price": 20},
    ]
    assert calculate_total(products) == 80

#--------------------DISCOUNT FUNCTION TEST--------------------------------------
def test_discount_with_no_products():
    assert discount([], 10) == 0

def test_discount_with_multiple_products():
    products = [
        {"name": "Product 1", "price": 10, "discount": 50},
        {"name": "Product 2", "price": 20, "discount": 50},
    ]
    assert discount(products, 10) == 24

def test_discount():
    products = [
        {"name": "Product 1", "price": 10, "discount": 50}
    ]
    assert discount(products, 5) == 2

if __name__ == "__main__":
    test_calculate_total_with_empty_list()
    test_calculate_total_with_single_product()