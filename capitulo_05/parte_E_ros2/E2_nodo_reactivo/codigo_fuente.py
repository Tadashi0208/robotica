import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import numpy as np

class ReactiveNavigator(Node):
    def __init__(self):
        super().__init__('reactive_navigator')
        
        # Suscriptor al LiDAR (/scan)
        self.sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )
        
        # Publicador de velocidades (/cmd_vel)
        self.pub = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

    def scan_callback(self, msg):
        ranges = np.array(msg.ranges)
        # Reemplazar valores no válidos (inf / nan)
        ranges = np.where(np.isfinite(ranges), ranges, msg.range_max)
        n = len(ranges)
        if n == 0:
            return

        # EN TURTLEBOT3:
        # 0° es el FRENTE (índices cercanos a 0 y a n)
        # 90° es IZQUIERDA | 270° es DERECHA
        
        # 1. Sector Frontal: Cono de ±30° al frente
        front_left = ranges[0:30]
        front_right = ranges[n-30:n]
        front_sector = np.concatenate((front_left, front_right))
        front_distance = np.min(front_sector)

        # 2. Sectores laterales para elegir el giro inteligente
        left_distance = np.min(ranges[30:90])     # Izquierda
        right_distance = np.min(ranges[270:330])  # Derecha

        cmd = TwistStamped()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'

        # Lógica de evasión
        if front_distance < 0.5:
            cmd.twist.linear.x = 0.0
            # Girar hacia el lado con mayor espacio libre
            if left_distance > right_distance:
                cmd.twist.angular.z = 0.5   # Giro a la izquierda
            else:
                cmd.twist.angular.z = -0.5  # Giro a la derecha
            self.get_logger().warn(f"Obstáculo a {front_distance:.2f} m. Evadiendo...")
        else:
            cmd.twist.linear.x = 0.2
            cmd.twist.angular.z = 0.0

        self.pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ReactiveNavigator()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
