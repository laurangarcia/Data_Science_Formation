import random 

def ordenamiento_borbuja(lista):
    n = len(lista)

    for i in range(n):
        for j in range(0, n-i-1): # O(n) * O(n) = O(n^2) -> Crecimiento cuadratico, no es eficiente 
            #inicia desde 0 hasta la lista menos lo que ya recorrimos menos 1 porque lo queremos usar atraves de indices
            
            if lista[j] > lista[j+1]:
                # Intercambia si el elemento encontrado es mayor que el siguiente elemento
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista


if __name__ == "__main__":
    tamano_lista = int(input("De que tama;os sera la lista: "))
    lista = [random.randint(0, 100) for i in range(tamano_lista)]
    print(f"Lista original: {lista}")


lista_ordenada = ordenamiento_borbuja(lista)
print(f"Lista ordenada: {lista_ordenada}")

