#Busqueda lineal: Busca un elemento en una lista de forma secuencial.

#Cual es el peor de los casos?

import random

def busqueda_lineal(lista, objetivo):
    match = False 

    for elemento in lista:
        if elemento == objetivo:
            match = True
            break 

    return match #Siempre debemos de pensar en el peor d elos casos

if __name__ == "__main__": #Si este archivo se ejecuta desde la consola
    tamano_lista = int(input('Describe el tama;o de la lista:  '))
    objetivo = int(input('Que numero quieres encontrar:  '))

    lista = [random.randint(0, 100) for i in range(tamano_lista)] #Generamos una lista de numeros aleatorios entre 0 y 100
    encontrado = busqueda_lineal(lista, objetivo)
    print(lista)
    print(f'El elemento {objetivo} {"esta" if encontrado else "no esta"}')

