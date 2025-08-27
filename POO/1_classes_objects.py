"""
Clase

Una clase es una plantilla o molde que define cómo deben ser los objetos.
 -> Describe atributos (datos o propiedades) y métodos (funciones que operan sobre esos datos).r.

Un objeto es una instancia concreta de una clase.
"""

class Celular():
    marca = "Samsung" #Atributo estático
    modelo = "Galaxy S21"
    ano = 2021

celular1 = Celular()
celular2 = Celular()

print(celular1.marca) #Acceder a un atributo



class Celular():
    def __init__(self, marca, modelo, ano): # Constructor/ Método inicializador
        self.marca = marca # Atributo dinámico / Propiedades
        self.modelo = modelo 
        self.ano = ano
# Metodo: funcion dentro de una clase
    def mostrar_info(self):
        print("Marca:", self.marca)
        print("Modelo:", self.modelo)
        print("Año:", self.ano)

celular1 = Celular("Samsung", "Galaxy S21", 2021)
