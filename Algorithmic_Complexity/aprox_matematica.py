#La aproximacion matematica basicamente se basa en contar que pasa
# en el programa 


def f(x):
    respuesta = 0 # un paso, una asignacion ---> 1

    for i in range(1000): # 1000 pasos, 1000 asignaciones ---> 1000
        respuesta += 1

    for i in range(x): # x pasos, x asignaciones ---> x
        respuesta += x
    
    for i in range(x): 
        for j in range(x): 
            respuesta += 1 # x^2 pasos, x^2 asignaciones ---> x^2
            respuesta += 1 # x^2 pasos, x^2 asignaciones ---> x^2
    return respuesta # un paso, una asignacion ---> 1

# 1002 + x + 2x^2 -> Para el polinomio nos damos cuenta que el termino
#que mas pesa es la cuadratica, por lo que esta es mas grande


