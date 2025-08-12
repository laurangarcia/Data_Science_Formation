# PCA, es lograr reducir la dimensionalidad de nuestros datos perdiendo la menor cantidad de información posible. Para esto, lo que se hace es encontrar un vector que pueda capturar la mayor varianza de los datos y proyectarlos en él para reducir la dimensionalidad.
import matplotlib.pyplot as plt

# Graficamos nuestros datos.
plt.plot(xy[:, 0], xy[:, 1], '.')
plt.show()

# Para partir, debemos centrar los datos en sus respectivos ejes.
# Esto lo hacemos restandoles su media.
# Buena práctica para simplificar el cómputo de los números.
# Aparte de lo anterior, veo que es porque en el siguiente paso
# obtenemos la matriz de covarianza, para obtener estas,
# necesitamos las distancias del dato hasta la media.
# y como ahora está centrado en la media, el valor del dato,,
# indica por si solo la distancia a la media.

xy_centrado = xy - np.mean(xy, axis=0)


# Graficamos nuestros datos centrados en la media.

plt.plot(xy_centrado[:, 0], xy_centrado[:, 1], '.')
plt.show()


# El siguiente paso es calcular nuestra matriz de covarianza
# y calcular sus autovectores y autovalores.
# la matriz de covarianza se resuelve así xy_centrado.T.dot(xy_centrado)
# falta dividirla por la cantidad de datos para obtener el promedio
# pero es un escalar y no nos afecta para obtener nuestros
# autovectores y autovalores, ya que obentemos un múltiplo del
# autovector, pero su dirección sigue siendo la misma.

autovalores, autovectores = np.linalg.eig(xy_centrado.T.dot(xy_centrado))
print(autovectores)

%run "../Funciones_auxiliares/graficarVectores.ipynb"


# Graficamos nuestros autovectores.
# juntos a los datos centrados en la media.

graficarVectores(autovectores.T, ['blue', 'red'])
plt.plot(xy_centrado[:, 0], xy_centrado[:, 1]/20, '.')
plt.show


# Vemos los autovalores.
# El autovalor mayor indica que el autovector asociado a este,
# captura la mayor varianza de los datos, 
# o sea la mayor cantidad de información, por lo que este
# es el autovector que debe ser elegido.
print(autovalores)


# luego de elegir debemos proyectar los datos perpendicularmente
# en el autovector, para esto podemos usar el producto punto.
# Lo que hace el profesor acá es proyectar los datos con cada
# autovector.
xy_nuevo = autovectores.T.dot(xy_centrado.T)



#Podemos ver acá que la nube de datos cambió y podemos ver que
# el eje y captura la mayor varianza, o sea la mayor información
# de los datos. Lo que calza con la elección de nuestro autovector.

plt.plot(xy_nuevo[0, :], xy_nuevo[1, :], '.')
plt.show()