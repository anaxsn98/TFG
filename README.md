# TFG
Tecnologias desarrolladas
APP Móvil: Hemos utilizado Android Studio y Java además de muchas librerías para poder proporcionarle más características.

Aplicació Web : Está compuesta y hecha en Angular 13 con lenguajes de marcas como HTML, CSS y TypeScript.

Base de datos: Hemos utilizado Mysql y AWS para subir nuestra base de datos a la nube. Y poder acceder a ella desde la App, desde la Web y desde el Script del invernadero.

Servicio Rest: Tecnologías usadas Java 11, Spring, Spring Boot, Spring JPA Data, Hibernate, MySQL, JWT, Maven, Postman y los patrones de diseño: DAO, MVC.

Invernadero: El cableado son elementos de arduino que están conectados a una Raspberry el cual su programación está hecha por python.

Otras Herramientas:Git, MobaXterm,Figma, Adobe XD, PhpAdmin,Eclipse,Visual Studio.


Instalación y ejecución del proyecto Angular

Para poder ejecutar la aplicación en local será necesario instalar nvm siguiendo las instrucciones de este enlace, pero es importante que la versión de node sea la 14.19.0
https://content.breatheco.de/es/how-to/nvm-install-windows

Después deberemos instalar angular cli con el comando:
npm install -g @angular/cli@13.3.4
'-g' significa que se instalará globalmente y estará disponible desde cualquier parte del sistema. Y con @ indicamos la versión deseada de angular que en este caso se ha utilizado la 13.3.4
Después nos situaremos desde la terminal en la carpeta que contenga el proyecto
Quedando la ruta de este modo.

Y a continuación deberemos poner el comando:  npm install

Este comando sirve para instalar todas las dependencias y librerías del proyecto para que pueda ser ejecutado.

Después deberemos arrancar el proyecto con el comando : npm start 

Se utiliza este comando en concreto ya tiene configurada la ruta con el proxy, que consiste en un json que aplica los permisos necesarios para poder acceder a la url de amazon web services porque si no saltan errores del tipo cors.
