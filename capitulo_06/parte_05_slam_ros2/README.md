# Parte 5 — SLAM con Cartographer en ROS 2

## Procedencia del código

El código base utilizado en esta actividad fue proporcionado por el docente del curso de Robótica como material de laboratorio.

Durante el desarrollo de la práctica se realizaron ajustes de configuración, integración con ROS 2 Jazzy y Gazebo Harmonic, pruebas de funcionamiento, diagnóstico de errores y una configuración experimental que incorpora odometría a Cartographer.

Los resultados, mapas generados y documentación corresponden a las pruebas realizadas durante el laboratorio.

La inclusión del material en este proyecto no implica que se conceda una licencia de redistribución del código original.

## Objetivo

Implementar y validar un sistema de mapeo y localización simultánea (SLAM) utilizando Cartographer, ROS 2 Jazzy, Gazebo Harmonic y un robot TurtleBot3 Burger simulado.

El propósito es generar un mapa de ocupación a partir de las mediciones del sensor LiDAR, visualizar los resultados en RViz2 y evaluar la incorporación de información de odometría al proceso SLAM.

## Entorno de trabajo

- **Sistema operativo:** Ubuntu 24.04 LTS.
- **ROS 2:** Jazzy Jalisco.
- **Simulador:** Gazebo Harmonic.
- **Robot:** TurtleBot3 Burger.
- **Algoritmo SLAM:** Cartographer 2D.
- **Visualización:** RViz2.
- **Lenguaje del controlador:** Python (`rclpy`).

## Organización de archivos

El directorio `localization_lab/` contiene el paquete ROS 2 desarrollado para esta actividad.

**Archivos principales:**

- [simple_controller.py](localization_lab/localization_lab/simple_controller.py): nodo encargado de publicar comandos de velocidad en `/cmd_vel`.
- [cartographer.launch.py](localization_lab/launch/cartographer.launch.py): inicia los nodos de Cartographer.
- [cartographer.lua](localization_lab/config/cartographer.lua): configuración experimental de SLAM con odometría.
- [cartographer_original.lua.bak](config_referencia/cartographer_sin_odometria.lua): respaldo de la configuración inicial del laboratorio.
- [slam.rviz](localization_lab/rviz/slam.rviz): configuración de visualización de RViz2.
- [slam_odom.pgm](resultados/slam_odom.pgm): mapa de ocupación generado.
- [slam_odom.yaml](resultados/slam_odom.yaml): metadatos del mapa.

## Desarrollo de la actividad

### 1. Creación del paquete ROS 2

Se creó el paquete `localization_lab` utilizando `ament_python` y se configuraron sus archivos `setup.py` y `package.xml`.

También se registró el ejecutable `simple_controller` para su ejecución mediante `ros2 run`.

### 2. Implementación del controlador

Se implementó un nodo que publica mensajes `geometry_msgs/msg/TwistStamped` en `/cmd_vel`.

El controlador establece las velocidades:

\[
v = 0.2\ \text{m/s},\qquad \omega = 0.1\ \text{rad/s}.
\]

Estas velocidades producen una trayectoria aproximadamente circular de radio teórico \(R=2\) metros.

El controlador no implementa evasión de obstáculos, por lo que debe utilizarse en un entorno seguro.

### 3. Configuración de Cartographer

Se configuró Cartographer para procesar las mediciones del LiDAR publicadas en `/scan` y construir mapas de ocupación mediante SLAM 2D.

Inicialmente se utilizó la configuración de la guía, sin incorporar mensajes de odometría.

Posteriormente se realizó una prueba experimental modificando tres parámetros:

| Parámetro | Configuración inicial | Configuración experimental |
|---|---|---|
| `published_frame` | `base_footprint` | `odom` |
| `provide_odom_frame` | `true` | `false` |
| `use_odometry` | `false` | `true` |

La configuración experimental utiliza los mensajes de `/odom` y permite aprovechar la transformación `odom → base_footprint` proporcionada por la simulación.

### 4. Validación de los sensores y transformaciones

Se comprobó la disponibilidad de los tópicos `/scan`, `/odom`, `/tf`, `/map` y `/submap_list`.

Las frecuencias observadas fueron aproximadamente:

- LiDAR `/scan`: 5 Hz.
- Odometría `/odom`: 48–49 Hz.

También se verificaron las transformaciones entre los marcos `map`, `odom`, `base_footprint`, `base_link` y `base_scan`.

### 5. Simulación y construcción del mapa

La simulación se realizó utilizando `empty_world.launch.py`, incorporando obstáculos estáticos para proporcionar referencias geométricas al LiDAR.

Se comprobó que Cartographer publicaba el mapa de ocupación y los submapas. Posteriormente se desplazó el TurtleBot3 mediante el controlador desarrollado y se observó la actualización del mapa en RViz2.

Se realizaron pruebas con y sin incorporación de odometría.

### 6. Guardado del mapa

Se utilizó `map_saver_cli` para guardar el mapa generado con la configuración experimental.

El mapa guardado tiene las siguientes características:

| Propiedad | Valor |
|---|---|
| Resolución | 0.05 m/celda |
| Ancho | 153 celdas |
| Alto | 176 celdas |
| Dimensiones | 7.65 m × 8.80 m |
| Formato | PGM y YAML |

El archivo `slam_odom.yaml` referencia la imagen `slam_odom.pgm`. Ambos archivos se encuentran en `resultados/`.

## Ejecución del laboratorio

Los siguientes comandos suponen que el paquete `localization_lab` está ubicado en `~/ros2_ws/src/` y que ha sido compilado correctamente.

**Terminal 1 — Gazebo**

```bash
source ~/ros2_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
QT_QPA_PLATFORM=xcb ros2 launch turtlebot3_gazebo empty_world.launch.py
```

Antes de iniciar Cartographer, colocar obstáculos en Gazebo para que el LiDAR disponga de referencias del entorno.

**Terminal 2 — Cartographer**

```bash
source ~/ros2_ws/install/setup.bash
ros2 launch localization_lab cartographer.launch.py
```

**Terminal 3 — RViz2**

```bash
source ~/ros2_ws/install/setup.bash
QT_QPA_PLATFORM=xcb rviz2 --ros-args -p use_sim_time:=true
```

Cargar `slam.rviz` desde el menú de configuraciones de RViz2, si no se carga automáticamente.

**Terminal 4 — Controlador**

```bash
source ~/ros2_ws/install/setup.bash
ros2 run localization_lab simple_controller
```

Antes de finalizar, detener el robot publicando velocidades cero en `/cmd_vel`.

## Problemas encontrados

Durante las pruebas se presentaron varias situaciones:

- **Problemas gráficos en Gazebo:** se utilizó `QT_QPA_PLATFORM=xcb`.
- **Colisión del robot:** el controlador de movimiento circular no incluía evasión de obstáculos.
- **Ausencia inicial del marco `map`:** las lecturas LiDAR del mundo vacío no proporcionaban referencias útiles.
- **Error `No map received` en RViz2:** se corrigió configurando correctamente el tópico `/map`.
- **Deformaciones del mapa:** se observaron durante la reconstrucción del entorno y motivaron una prueba adicional incorporando odometría.

La incorporación de odometría permitió generar un nuevo mapa, aunque no se realizó una evaluación cuantitativa de su precisión geométrica.

## Resultados y conclusiones

Se implementó y validó el funcionamiento de Cartographer en ROS 2 Jazzy con TurtleBot3 Burger simulado.

Se consiguió recibir información del LiDAR, generar submapas, publicar transformaciones TF, construir un mapa de ocupación y visualizarlo en RViz2.

También se verificó el funcionamiento de una configuración experimental que incorpora odometría al proceso SLAM.

Los resultados permiten observar la importancia de disponer de referencias geométricas suficientes y de configurar correctamente las transformaciones entre los marcos del robot.

El mapa guardado constituye una evidencia experimental de la ejecución del sistema, no una reconstrucción geométricamente validada del entorno.