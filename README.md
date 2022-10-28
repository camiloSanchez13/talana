# Prueba Tecnica Talana
Desarrollo de prueba técnica para postulación en Talana

### Clonar repositorio github

### Primer paso :
```
$ git clone https://github.com/camiloSanchez13/talana.git
```
## Istalar con Docker Composer
 Se asume que está instalado Docker y Docker Compose. \
 Ejecutar los siguientes comandos dentro del repositorio clonado.

### Construir imágenes

```
$ docker-compose build
```
### Eejecutar y levantar servicios Docker
```
$ docker-compose up -d
```

### Instalar Backend de forma manual
Se asume que está instalada la versión *3.9.1* de **Python**. \
Ejecutar los siguientes comandos dentro de **/backend**

### Primer paso: crear ambiente virtual venv
```
$ python -m venv ./venv
```
### Segundo paso: activar ambiente virtual

_En Windows_
```
$ source venv/Scripts/activate
```
_En Linux_
```
$ source venv/bin/activate
```

### Tercer paso: instalar requerimientos
```
(venv) $ pip install -r requirements.txt
```

### Cuarto paso: realizar migraciones
```
(venv) $ python manage.py migrate
```

### Quinto paso: ejecutar servidor de desarrollo
```
(venv) $ python manage.py runserver
