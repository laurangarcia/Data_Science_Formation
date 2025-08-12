import time


# Necesitamos conocer la complejidad algoritmica, por lo que lo podemos realzar midiendo el tiempo:
#Implementacion iteractiva, medir el tiempo nos permite ver la complejidad del algoritmo
def factorial(n):
    respuesta = 1 

    while n > 1:
        respuesta = respuesta * n 
        n = n-1
    return respuesta



def factorial_recursivo(n):
    if n == 1: 
        return 1
    return n * factorial_recursivo(n-1) 

if __name__ == "__main__": # Medir el tiempo de ejecución
    n = 1000000

    inicio = time.time()
    #print(f"Factorial de {n} (iterativo): {factorial(n)}")
    fin = time.time()
    print(f"Tiempo de ejecución (iterativo): {fin - inicio} segundos")

    inicio = time.time()
    #print(f"Factorial de {n} (recursivo): {factorial_recursivo(n)}")
    fin = time.time()
    print(f"Tiempo de ejecución (recursivo): {fin - inicio} segundos") 


