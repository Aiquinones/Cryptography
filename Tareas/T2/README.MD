# Tarea 2

* Alumno: Alejandro Quiñones

## Cómo funciona

Se usa las librerías:

* **tkinter**: para la interfaz gráfica
* **gnupg**: para la encriptación
* **getpass**: para que el usuario ingrese su clave por consola

Su funcionamiento es el siguiente:

* Se espera que ambos _server_ y _client_ se corran desde el mismo dispositivo.
* Se espera que ambos se corran desde la carpeta T2 (por ej: ``python3 client/main.py``)
* Primero se debe iniciar el servidor, luego los clientes
* Al iniciar un cliente, se le pedirá por consola ingresar un usuario y luego su clave. **Se pide que se utilize uno de los clientes ya creados, especificados más adelante**
* Hay un máximo de 5 clientes a la vez, dado que la finalidad del problema no es escalabilidad si no seguridad
* Después de verificar al usuario y al servidor, se cargará una interfaz gráfica. Esta fue obtenida de internet, dado que la finalidad de la tarea no era la interfaz si no la seguridad. Las fuentes estarán citadas más adelante.

## Supuestos

### Usuarios

Se crearon a priori ciertos usuarios. Aunque se agregue el código para poder generar dichos usuarios (``gen_keys.py``), se espera que se usen los ya creados. Estos son, en un formato _mail_ : _passphrase_:

* _aiquinones@test.cl_ : _passaq_
* _alice@test.cl_ : _passalice_
* _bob@test.cl_ : _passbob_
* _charles@test.cl_ : _passcharles_
* _diana@test.cl_ : _passdiana_
* _ernest@test.cl_ : _passernest_
* _foxtrot@test.cl_ : _passfoxtrot_

### _Key Rings_

Para simular mejor la realidad, se optó por trabajar en diferentes directorios por usuario, y uno separado para el servidor.
Estos se encuentran en la carpeta _gpg_.
Los de usuarios están en ``gpg/client/{name}``, con "_name_" siendo el mail antes del "@". El servidor está en _gpg/server_

### Servidor

Se trabajó con el servidor _pgp.mit.edu_. Ninguno de los servidores encontrados tenía bastante confiabilidad, y es común que el servidor esté caído. El código está implementado de tal modo que la clave será buscada localmente y si no se encuentra será buscada en la nube. De esto se desprender dos consejos para un mejor uso:

* A veces el servidor está caído por lo que lo mejor sería intentar más tarde
* Una vez se consiga alguna llave pública desde el servidor, es recomendable no borrar la carpeta _gpg_ o ninguno de sus archivos, para no tener que volver a buscar la llave. Inicialmente, existen algunas llaves públicas localmente para ciertos usuarios.
* Si todo falla, se puede usar el ``LOCAL_MODE`` cambiando la variable de ``False`` a ``True`` en uno o ambos de las implementaciones. Al estar en ``LOCAL_MODE``, en vez de buscar las llaves en el servidor online, estas se van a buscar al directorio de los otros usuarios o del servidor, según corresponda. Esto puede que no sea lo deseado a evaluar, por lo que está apagado a menos que sea necesario. 

## Referencias

### Interfaz

La interfaz fue obtenida mayoritariamente desde https://medium.com/swlh/lets-write-a-chat-app-in-python-f6783a9ac170

Solo se varió en pequeñas cosas, además de, obviamente, agregar la encriptación.

### GPG

Si bien no hubo ninguna fuente en dónde basarse, sí se trabajo aprendiendo con la "documentación" de python-gnupg
https://pythonhosted.org/python-gnupg/