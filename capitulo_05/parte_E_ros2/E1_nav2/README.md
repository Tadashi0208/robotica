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

## Archivos

La carpeta `mapas/` contiene el mapa generado previamente mediante Cartographer:

- `map.pgm`: mapa de ocupación.
- `map.yaml`: configuración del mapa.

## Ejecución

**Terminal 1. Iniciar Gazebo**

```bash
export TURTLEBOT3_MODEL=burger
source ~/turtlebot3_ws/install/setup.bash
QT_QPA_PLATFORM=xcb ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

**Terminal 2. Iniciar Navigation2**

Desde la carpeta `E1_nav2/`:

```bash
export TURTLEBOT3_MODEL=burger
source ~/turtlebot3_ws/install/setup.bash
QT_QPA_PLATFORM=xcb ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:=$(pwd)/mapas/map.yaml
```

**Navegación en RViz**

1. Comprobar que Navigation y Localization estén activos.
2. Verificar la posición estimada del robot.
3. Seleccionar la herramienta `Nav2 Goal`.
4. Indicar una posición y orientación de destino.
5. Observar el desplazamiento del robot en Gazebo.

## Resultados

Durante la simulación, el TurtleBot3 se desplazó correctamente hasta el objetivo indicado mediante RViz.

En la prueba realizada se obtuvieron los siguientes resultados:

- Estado final: `reached`.
- Tiempo de navegación: 29 segundos.
- Distancia restante: 0,03 metros.
- Maniobras de recuperación: 0.

La prueba permitió comprobar el funcionamiento conjunto de Gazebo, RViz, el sistema de localización y Navigation2.

## Evidencias

La carpeta `evidencias/` contiene las capturas representativas de la navegación autónoma.
