# optimizacion-turnos

## Instrucciones de uso:

Primero lo primero, deben entrar al DBeaver (gestor de bases de datos) y conectarse a la base de datos de primos signup, cuando encuentren la tabla con los turnos deben seleccionar todos los datos, dar click derecho y seleccionar *advanced copy* y luego *copiar como csv*.

Una vez copiados los datos, diríjanse al directorio raíz del programa y creen un archivo (si es que no existe) y llámenlo *input.csv*.

Ya tenemos todo preparado para comenzar a correr el script siguiendo estos pasos:
En una consola...
```
python primos.py
```
```
python opti.py
```
Verán que después de correr esto aparecen lso turnos en consola, si se fijan detenidamente, en el directorio raíz se creó otro archivo llamado *primos.csv* el cual contiene la información de los nuevos turnos.

Finalmente, para subir estos nuevos turnos al checkins tenemos que meter todo esto en una sentencia SQL e ingresarla en el contenedor con la base de datos del checkins, para facilitar un poco la tarea hay un script que crea la sentencia SQL para copiar y pegar:
```
python buffer_sql.py
```

## Pasar los datos al checkins

### Forma fácil
El DBeaver les deja importar datos de un csv, que suerte que tenemos uno con todos los nuevos turnos.
Conéctense a la base de datos del checkins en el DBeaver, búsquen la tabla *tracks_primo* en el menú de la derecha y háganle un click derecho, selecciones *import data* y buscan el csv.

El mismo DBeaver también les deja utilizar sentencias SQL, en el menú de arriba dice SQL bien grande y tiene un pequeño menú desplegable, de ese menú seleccionen la opción *open SQL console*, pegan la sentencia SQL que está en *salida.txt* y luego la corren, ya deberíua funcionar, para checkear solo revisen la tabla en el DBeaver

### Forma difícil
Teniendo la sentencia SQL solo resta ponerla en la base de datos del checkins, para eso van a buscar el contenedor de la base de datos con

```
docker ps -a
```
El contenedor se llama *primos-checkins-backend* y la imagen se llama *postgres*, copien el id del contenedor y ejecuten el siguiente comando:
```
docker exec -it <id_contenedor> bash
```
Una vez dentro del contenedor, deben darle permisos de root al usuario postgres y conectarse a la base de datos
```
su - postgres
psql
\c primos-checkins-backend
```

Puede que me haya equivocado con la última línea, esa es la que conecta a la base de datos, para listar las bases de datos escriban ``` \l ```, luego escriban el mismo comando de arriba pero con el nombre correcto. Ahora si pueden tirar la sentencia SQL, solamente copien y peguen

```
INSERT INTO .....
```

El output debiese decirles si es que hubieron lineas afectadas en la base de datos, para verificar pueden tirar un ```SELECT * ...```
