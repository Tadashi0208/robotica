
import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped


class ReactiveNavigator(Node):

    def __init__(self):
        super().__init__('reactive_navigator')

        # Parámetros del controlador
        self.distancia_seguridad = 0.5
        self.velocidad_lineal = 0.15
        self.velocidad_angular = 0.8

        # Publicador de velocidades
        self.publisher_ = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        # Suscriptor del LiDAR
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        # Seguridad ante pérdida de datos del LiDAR
        self.ultima_lectura = time.monotonic()
        self.timer = self.create_timer(
            0.25,
            self.verificar_sensor
        )

        self.get_logger().info(
            'Controlador reactivo iniciado'
        )

    def scan_callback(self, msg):

        self.ultima_lectura = time.monotonic()

        distancias_frontales = []

        # Revisar un sector de +/- 30 grados
        for i, distancia in enumerate(msg.ranges):

            angulo = msg.angle_min + i * msg.angle_increment

            # Normalizar el ángulo a [-pi, pi]
            angulo = math.atan2(
                math.sin(angulo),
                math.cos(angulo)
            )

            if abs(angulo) > math.radians(30):
                continue

            if math.isfinite(distancia):
                if msg.range_min <= distancia <= msg.range_max:
                    distancias_frontales.append(distancia)

            elif math.isinf(distancia) and distancia > 0:
                # Sin obstáculo detectado dentro del alcance
                distancias_frontales.append(msg.range_max)

        # Si no tenemos lecturas utilizables, detener
        if not distancias_frontales:
            self.publicar_velocidad(0.0, 0.0)
            return

        distancia_minima = min(distancias_frontales)

        # Lógica reactiva de la Actividad E2
        if distancia_minima < self.distancia_seguridad:

            # Obstáculo próximo: detener avance y girar
            self.publicar_velocidad(
                0.0,
                self.velocidad_angular
            )

        else:

            # Camino libre: avanzar
            self.publicar_velocidad(
                self.velocidad_lineal,
                0.0
            )

    def publicar_velocidad(self, v, omega):

        cmd = TwistStamped()

        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'

        cmd.twist.linear.x = v
        cmd.twist.angular.z = omega

        self.publisher_.publish(cmd)

    def verificar_sensor(self):

        # Detener si pasa más de 1 segundo sin datos LiDAR
        if time.monotonic() - self.ultima_lectura > 1.0:
            self.publicar_velocidad(0.0, 0.0)


def main(args=None):

    rclpy.init(args=args)

    node = ReactiveNavigator()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.publicar_velocidad(0.0, 0.0)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
