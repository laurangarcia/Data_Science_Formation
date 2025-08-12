#Crecimiento asintotico

#no importan las variaciones 
#Su enfoque central es en lo que pasa conforme el tama;o del problema se acerca al infinito
#Importa mas el temino de mayor tama;o

#Ley de la suma

def f(n):
    for i in range(n):
        print(i)
    
    for i in range(n):
        print(i)

# O(n) + O(n) =O( n + n) = O(2n) = O(n) 

#Ley de la suma, lo que nos importa es le temino mas grande 

def f(n):
    for i in range(n):
        print(i)
    
    for i in range(n*n):
        print(i)

# O(n) + O(n*n) =O( n + n*n) = O(n + n^2) = O(n^2) 

#Ley de la multiplicacion

def f(n):
    for i in range(n):
        for j in range(n):
            print(i, j)

# O(n) * O(n) = O(n*n) = O(n^2)

#Recursividad multiple

def fibonacci(n):
    if n == 0 or n == 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2) #la estamos llamando dos veces|
# O(2^n) - Crece exponencialmente, cada llamada genera dos nuevas llamadas


