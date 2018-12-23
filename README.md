# Votaciones_Ulacit
Sistema de votaciones desarrollado por el Tech Club para las elecciones estudiantiles de la Universidad Latinoamericana de Ciencia y Tecnología 2017

## Instrucciones para ejecutar:

1- Utilizar una máquina virtual con Ubuntu (Desktop o Server).

2- Instalar apache2, mysql, python 3.5 (en linux por general se instala pip junto con python, de lo contrario isntalar "pip" manualmente).

3- Un la terminal de comandos ejecutar el siguiente comando: pip install virtualenv

4- Descargar el codigo de este repositorio y en la terminal de comando poner: cd Votaciones_Ulacit

5- Buscar la carpeta en /var/www/html y pegar ahí el contenido de la carpeta Frontend (solo el contenido no la carpeta "Frondend").

6- Ejecutar el siguiente comando estando dentro de Votaciones_Ulacit:
    virtualenv votaciones_env
y asegurarse de que se crea el entorno virtual con python3

7- ejecutar source ./votaciones_env/bin/activate

8- Hacer cd a Votaciones_Ulacit/Votaciones_Code/Backend/ y ejecutar pip install requirements.txt

9- Luego ejecutar python main.py para inciar el servidor, en un navegador poner localhost y se podrá acceseder a la página inicial.
