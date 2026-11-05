from roboticstoolbox import *
import numpy as np
import matplotlib.pyplot as plt
from math import pi

# ==============================
# Covarianza de odometría
# ==============================

V = np.diag([
    0.02,
    np.deg2rad(0.5)
])**2

# ==============================
# Robot
# ==============================

robot = Bicycle(
    covar=V,
    animation=None
)

robot.control = RandomPath(workspace=10)

# ==============================
# Mapa real
# ==============================

mapa = LandmarkMap(20, workspace=10)

# ==============================
# Sensor
# ==============================

W = np.diag([
    0.1,
    np.deg2rad(1)
])**2

sensor = RangeBearingSensor(
    robot=robot,
    map=mapa,
    covar=W,
    angle=[-pi/2, pi/2],
    range=4
)

# ==============================
# Covarianza inicial
# ==============================

P0 = np.diag([
    0.05,
    0.05,
    np.deg2rad(0.5)
])**2

# ==============================
# EKF SLAM
# ==============================

slam = EKF(
    robot=(robot, V),
    P0=P0,
    sensor=(sensor, W),
    map=None
)

# ==============================
# Ejecutar simulación
# ==============================

slam.run(T=40)

print("Tamaño inicial de P:", slam.history[0].P.shape)
print("Tamaño final de P:", slam.history[-1].P.shape)

plt.close('all')

# ==============================
# Graficar resultados
# ==============================

plt.subplots(figsize=(10, 8))

# Mapa real
mapa.plot()

# Trayectoria real
robot.plot_xy(
    color='blue',
    label='Trayectoria real'
)

# Trayectoria estimada
slam.plot_xy(
    color='red',
    label='Trayectoria estimada'
)

# Elipses de confianza
slam.plot_ellipse()

plt.title('SLAM usando EKF')
plt.grid(True)
plt.axis('equal')

# ==============================
# Incertidumbre
# ==============================

plt.figure(figsize=(8, 6))

sigma_x = np.array([
    np.sqrt(h.P[0, 0]) for h in slam.history
])

sigma_y = np.array([
    np.sqrt(h.P[1, 1]) for h in slam.history
])

plt.plot(slam.get_t(), sigma_x, label='Incertidumbre en x')
plt.plot(slam.get_t(), sigma_y, label='Incertidumbre en y')

plt.xlabel('Tiempo [s]')
plt.ylabel('Desviación estándar [m]')
plt.title('Incertidumbre de posición del robot')
plt.grid(True)
plt.legend()

plt.show()