import random 

def ordenamiento_mezcla(lista):
    if len(lista) > 1:
        medio = len(lista) // 2
        izquierda = lista[:medio]
        derecha = lista[medio:]

        # Llamada recursiva en cada mitad
        ordenamiento_mezcla(izquierda)
        ordenamiento_mezcla(derecha)

        # Iteradores para recorrer las dos sublistas
        i, j = 0, 0
        # Iterador para la lista principal
        k = 0

        while i < len(izquierda) and j < len(derecha):
            if izquierda[i] < derecha[j]:
                lista[k] = izquierda[i]
                i += 1
            else:
                lista[k] = derecha[j]
                j += 1
            k += 1

        while i < len(izquierda):
            lista[k] = izquierda[i]
            i += 1
            k += 1

        while j < len(derecha):
            lista[k] = derecha[j]
            j += 1
            k += 1
        
        print(f"izquierda: {izquierda}, derecha: {derecha} ")
        print(f"Lista combinada: {lista}")
        print("-" * 60)

    return lista


if __name__ == "__main__":
    tamano_lista = int(input("De que tamano sera la lista: "))

    lista = [random.randint(0, 100) for i in range(tamano_lista)]
    print(f"Lista original: {lista}")
    print("-" * 60)


    lista_ordenada = ordenamiento_mezcla(lista)
    print(f"Lista ordenada: {lista_ordenada}")