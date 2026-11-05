# Actividad E2 — Nodo Reactivo de Evasión de Obstáculos

## Objetivo
Implementar y validar un nodo en ROS 2 utilizando Python (`rclpy`) que procese en tiempo real las lecturas del sensor LiDAR (`/scan`) para controlar de manera reactiva la navegación y evasión de obstáculos de un robot TurtleBot3 Burger en el entorno de simulación Gazebo.

## Herramientas utilizadas
* **Sistema Operativo:** Ubuntu 24.04 LTS[cite: 13]
* **Entorno ROS:** ROS 2 Jazzy Jalisco[cite: 13]
* **Simulador:** Gazebo Sim / Gazebo Harmonic[cite: 13]
* **Modelo del Robot:** TurtleBot3 Burger
* **Lenguaje:** Python 3 (librerías `rclpy`, `numpy`)
* **Mensajes ROS 2:** `sensor_msgs/msg/LaserScan`, `geometry_msgs/msg/TwistStamped`[cite: 49]

## Estructura de archivos
La carpeta del paquete `lab_robotica` contiene la siguiente estructura:

```text
lab_robotica/
├── lab_robotica/
│   ├── __init__.py
│   └── reactive_navigator.py    # Nodo ROS 2 de evasión reactiva con LiDAR
├── package.xml                   # Dependencias del paquete (rclpy, sensor_msgs, geometry_msgs)
├── setup.cfg
└── setup.py                     # Configuración del paquete y puntos de entrada (console_scripts)

Lógica de control implementada
El script reactive_navigator.py ejecuta las siguientes operaciones:   
Suscripción y filtrado de datos: Se suscribe al tópico /scan y limpia las lecturas no 
válidas (inf, nan) reemplazándolas por el rango máximo permitido (msg.range_max).   
Segmentación del frente y laterales: En el TurtleBot3, el índice 0° corresponde al frente[cite: 49]. 
Se evalúa un cono frontal de ±30° (ranges[0:30] y ranges[n-30:n]) así como los sectores izquierdo (30° a 90°) y derecho (270° a 330°).   
Toma de decisiones reactiva:Obstáculo cercano ($d_{\text{frontal}} < 0.5\text{ m}$):
Se detiene la marcha lineal ($v = 0.0\text{ m/s}$) y se ejecuta un giro rotacional ($\omega = \pm 0.5\text{ rad/s}$) hacia el lado que presente mayor espacio libre.  
Camino despejado ($d_{\text{frontal}} \ge 0.5\text{ m}$): El robot avanza en línea recta a una velocidad constante de $v = 0.2\text{ m/s}$.   
Publicación: Envía mensajes de control con estampa de tiempo (Header) a través del tópico /cmd_vel mediante la estructura TwistStamped[cite: 49, 50].
