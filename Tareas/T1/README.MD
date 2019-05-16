# Tarea 1 Criptografía

## Input

Se espera que se entregue como input:
* la ubicación de un archivo con el formato igual a `quijote_misma_llave.txt`
* El número de discos que se espera procesar

Esto se debe entregar desde consola desde la siguiente manera:

`python3 main.py filepath number`

## Algoritmo

Se parte solucionando el disco más cerca al reflector, a través de ejemplos que solo usan un disco. Se realiza una hipótesis sobre hacia a dónde va *a*, y en base a eso se va deduciendo la posición de las demases letras.

Aquí dos cosas pueden pasar: o completamos el disco o encontramos una contradicción. Si encontramos una contradicción, nuestro supuesto sobre *a* fue incorrecto y buscamos otro valor. Si completamos el disco, encontramos la combinación que soluciona el problema.

Después de solucionar el primer disco más cercano al reflector, se continua con el disco que lo sigue. Ahora, se tiene el primer disco sabido, y la solución del problema es similar a la del primero, pero en vez de solo pasar por el reflector, se pasa por todos los discos, el reflector, y los discos nuevamente.

Se detiene cuando se obtienen todos los discos
