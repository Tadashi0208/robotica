# Actividad E1 — Navegación con Nav2

## Objetivo

Implementar y comprobar la navegación autónoma de un robot TurtleBot3 en un entorno simulado, utilizando ROS2, Gazebo y Navigation2.

## Herramientas utilizadas

- Ubuntu 24.04
- ROS2 Jazzy
- Gazebo Harmonic
- TurtleBot3 Burger
- Navigation2 (Nav2)
- RViz2
- Cartographer, para la creación previa del mapa

## Archivos del mapa

La carpeta `mapas/` contiene el mapa de ocupación generado previamente mediante Cartographer:

- `map.pgm`: imagen del mapa.
- `map.yaml`: configuración del mapa, incluyendo su resolución y origen.

## Ejecución

### Terminal 1. Iniciar Gazebo

```bash
export TURTLEBOT3_MODEL=burger
source ~/turtlebot3_ws/install/setup.bash
QT_QPA_PLATFORM=xcb ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

Este comando inicia el TurtleBot3 Burger en el mundo con obstáculos.

### Terminal 2. Iniciar Navigation2

Primero, ingresar a la carpeta `E1_nav2` del repositorio:

```bash
cd ~/Documentos/GitHub/Unal/robotica/capitulo_05/parte_E_ros2/E1_nav2
```

Después, configurar el entorno:

```bash
export TURTLEBOT3_MODEL=burger
source ~/turtlebot3_ws/install/setup.bash
```

Finalmente, ejecutar Navigation2:

```bash
QT_QPA_PLATFORM=xcb ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:="$(pwd)/mapas/map.yaml"
```

**Importante:** este comando utiliza `$(pwd)` para obtener el directorio actual. Por tanto, debe ejecutarse desde la carpeta `E1_nav2`, donde se encuentra el subdirectorio `mapas/`.

Las rutas del espacio de trabajo y del repositorio corresponden a la instalación utilizada en esta práctica y deben adaptarse si se trabaja desde otra ubicación.

### Navegación en RViz

1. Comprobar que `Navigation` y `Localization` estén activos.
2. Verificar la posición estimada del robot.
3. Seleccionar la herramienta `Nav2 Goal`.
4. Indicar una posición libre del mapa y la orientación deseada.
5. Observar el desplazamiento del robot en Gazebo y la trayectoria en RViz.

## Resultados

El TurtleBot3 logró desplazarse de forma autónoma hasta el objetivo seleccionado desde RViz.

En la grabación realizada se observaron los siguientes resultados:

- Estado final: `reached`.
- Tiempo de navegación: 29 segundos.
- Distancia restante: 0,07 metros.
- Maniobras de recuperación: 0.

El robot alcanzó el destino dentro de las tolerancias establecidas por Navigation2, sin necesidad de ejecutar maniobras de recuperación.

La práctica permitió comprobar el funcionamiento conjunto de Gazebo, RViz, AMCL y Navigation2.

## Evidencias

Se realizó una grabación de pantalla donde se observa el movimiento del TurtleBot3 en Gazebo y el resultado de la navegación en RViz.

**Video de la simulación:** pendiente de agregar el enlace de YouTube.

La carpeta `evidencias/` está destinada a almacenar capturas representativas del resultado.
