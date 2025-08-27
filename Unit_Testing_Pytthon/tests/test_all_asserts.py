import unittest

class AllAssertsTests(unittest.TestCase): 
    def test_assert_equal(self):
        self.assertEqual(10,10)
        self.assertEqual("Hola", "Hola")
    
    def test_assert_tue_or_false(self):
        self.assertTrue(True)
        self.assertFalse(False)

# Queremos validar que dentro de un meétodo se está utilizando una excepción
    def test_assert_raises(self):
        with self.assertRaises(ValueError):
            int("no_soy_un_numero")

    def test_assert_in(self):
        self.assertIn(10, [2, 4, 5, 10]) #Validar que 10 está en la lista
        self.assertNotIn(5, [2, 4, 10])

    def test_assert_dicts(self):
        self.assertIn(10, [2, 4, 5, 10])
        self.assertNotIn(5, [2, 4, 10])
    
    def test_assert_dicts(self):
        user = {"nombre": "Juan", "edad": 30}
        self.assertDictEqual(user, {"nombre": "Juan", "edad": 30})
        self.assertSetEqual(
            {1, 2, 3},
            {1, 2, 3}
        )
    
    # A veces nos solicitan hacer cambios en sus funcionalidades, por lo que debemos de camiar las pruebas
    # podriamos comentar las pruebas que no son relevantes, sin embargo, init test nos da algunos decoradores
    # para saltarnos las pruebas y una vez terminemos con el feature, donde ya pueda corer las pruebas, sencillamente volver y quitarle ese decorador


    # Decorador: funcionalidades que nos permiten cambiar el comportamiento de un método o función
    @unittest.skip("Trabajo en progreso, será habilitado nuevamente")
    def test_skip(self):
        self.assertEqual(1, 2)

    @unittest.skipIf(True, "Saltado porque no estamos en el servidor") #Recibe una condicion y una razón
    def test_skip_if(self):
        self.assertEqual(100,100)
    
    @unittest.expectedFailure #Esperamos que falle
    def test_expected_failure(self):
        self.assertEqual(100, 150)
