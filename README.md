# clap

    Sistema para caracterizar a los integrantes de un comité local de abastecimiento productivo CLAP

# Pasos para crear el entorno de desarrollo

    Cuando somos un usuario normal del sistema, en el terminal se mostrará el siguiente símbolo: ~$

    Cuando accedemos al usuario root del sistema, en el terminal se mostrará el siguiente símbolo: ~#

Probado en últimas versiones de Debian y Ubuntu. Instalar los siguientes programas

    ~# apt install curl git graphviz graphviz-dev libfreetype6-dev libjpeg-dev libz-dev postgresql phppgadmin python3-dev python3-setuptools virtualenv

Para instalar npm hacer lo siguiente

    ~# curl -sL https://deb.nodesource.com/setup_10.x | bash -

    ~# apt install -y nodejs

Crear las siguientes carpetas

    ~$ mkdir Programación

Desde el terminal, moverse a la carpeta Programación y ejecutar

    ~$ cd Programación/

    ~$ mkdir python

Entrar a la carpeta python y hacer lo siguiente

    ~$ cd python/

    ~$ mkdir entornos_virtuales proyectos_django

Entrar a EntornosVirtuales

    ~$ cd entornos_virtuales/

    ~$ mkdir django

Desde el terminal, moverse a la carpeta django y ejecutar

    ~$ cd django/

    ~$ virtualenv -p python3 clap

Para activar el entorno

    ~$ source clap/bin/activate

Nos movemos a la carpeta proyectos_django, descargamos el sistema y entramos a la carpeta con los siguientes comandos

    (clap) ~$ cd ../../proyectos_django/

    (clap) ~$ git clone https://gitlab.com/willez/clap.git

    (clap) ~$ cd clap/

    (clap) ~$ cp clap/settings.py_example clap/settings.py

Tendremos las carpetas estructuradas de la siguiente manera

    // Entorno virtual
    Programación/python/entornos_virtuales/django/clap

    // Servidor de desarrollo
    Programación/python/proyectos_django/clap

Instalar las dependencias de css y js: moverse a la carpeta static y ejecutar

    (clap) ~$ cd static/

    // Usa el archivo package.json para instalar lo que ya se configuro allí
    (clap) ~$ npm install

    // Terminado el proceso volver a la carpeta raíz del proyecto
    (clap) ~$ cd ../

Crear la base de datos para __clap__ usando PostgresSQL

    // Acceso al usuario postgres
    ~# su postgres

    // Acceso a la interfaz de comandos de PostgreSQL
    postgres@xxx:$ psql

    // Creación del usuario de a base de datos
    postgres=# CREATE USER admin WITH LOGIN ENCRYPTED PASSWORD '123' CREATEDB;
    postgres=# \q

    // Desautenticar el usuario PostgreSQL y regresar al usuario root
    postgres@xxx:$ exit

    // Salir del usuario root
    ~# exit

Puedes crear la base de datos usando la interfaz gráfica phppgadmin

    // Desde algún navegador ir al siguiente sitio y entrar con el usuario que se acaba de crear
    localhost/phppgadmin

    // Nombre de la base de datos: clap

Instalamos los requemientos que el sistema necesita en el entorno virtual

    (clap) ~$ pip install -r requirements/dev.txt

Hacer las migraciones y cargar los datos iniciales

    (clap) ~$ python manage.py makemigrations base user beneficiary

    (clap) ~$ python manage.py migrate

    (clap) ~$ python manage.py loaddata 1_country.json 2_state.json 3_municipality.json 4_city.json 5_parish.json

Crear usuario administrador

    (clap) ~$ python manage.py createsuperuser

Correr el servidor de django

    (clap) ~$ python manage.py runserver

Poner en el navegador la url que sale en el terminal para entrar el sistema

Llegado hasta aquí el sistema ya debe estar funcionando

Para salir del entorno virtual se puede ejecutar desde cualquier lugar del terminal: deactivate

Generar modelo de datos relacional del __clap__ completo. Crea la imagen en la raíz del proyecto

    (clap) ~$ python manage.py graph_models -a -g -o clap.svg

Generar modelo de datos relacional de las aplicaciones del proyecto

    (clap) ~$ python manage.py graph_models base -g -o base.svg

    (clap) ~$ python manage.py graph_models user -g -o user.svg

    (clap) ~$ python manage.py graph_models beneficiary -g -o beneficiary.svg