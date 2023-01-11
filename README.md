# Turtlebot Segurata

Se trata de un proyecto para la asignatura de Robots Móviles de la Universidad de Alicante. Consiste en un robot Turtlebot que es capaz de patrullar un espacio y detectar obstáculos y personas. En caso de detectar una persona, el robot envía una notificación a un bot de telegram.

## Características

- Trazado de patrullas de forma gráfica a partir del mapa actual
- Importación y exportación de patrullas en formato JSON
- Detección de obstáculos y detección de personas en tiempo real
- Envio de notificaciones mediante un bot de telegram 
- Interfaz gráfica alojada en un servidor web para su control desde caulquier dispositivo y lugar
- Simulación de todas sus características mediante gazebo

## Guia de uso e instalación

En la carpeta catkin_ws se encuentran los paquetes necesarios para el funcionamiento del robot. Para su instalación, se debe clonar el repositorio dirigirse al directorio y compilarlo. Para ello, se debe ejecutar los siguientes comandos:

```bash
git clone 
cd catkin_ws
catkin_make
source devel/setup.bash
```

Para la ejecución del robot en el entorno de simulacion, se debe ejecutar el siguiente comando:

```bash
roslaunch TurtleMadero turtlebot3_simulation.launch
```

El servidor web se ejecuta mediante el siguiente comando:

```bash
cd www
python3 -m http.server
```

A continuación, se debe abrir un navegador web y dirigirse a la dirección http://localhost:8001

