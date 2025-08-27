""""
Un unit test (prueba unitaria) es un fragmento de código que verifica que una unidad aislada de software (como una función, método o clase) 
funciona correctamente por sí sola, asegurando que cumple con la lógica esperada por el desarrollador. Estas pruebas automatizadas se escriben
al mismo tiempo que el código principal, permitiendo identificar errores de forma temprana y garantizando la calidad y eficiencia del software individualmente. 

1. Crear entorno virtual 
2. Instalar la libreria: pip install ipdb -> Se utiliza para inspeccionar el código línea por línea, establecer puntos de interrupción y examinar variables en tiempo real,
lo que facilita la detección y corrección de errores en programas Python. 
3. Separar los archivos de prueba del código fuente.
4. Crear el gitignore para evitar que el entorno virtual se vaya  al repositorio
5. Comando para ejecutar las pruebas: python -m unittest discover
6. Comando para ejecutar una prueba en específico: python -m unittest tests/test_calculator.py -v
7. Comando para ejecutar la prueba y saber cual está ejecutando: python -m unittest discover -v  -s tests 
"""