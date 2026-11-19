
import numpy as np
import matplotlib.pyplot as plt
from roboticstoolbox import ET2

# Longitudes de los eslabones
L1 = 0.6
L2 = 0.4

# Modelo cinemático con transformaciones elementales
robot = (
    ET2.R()
    * ET2.tx(L1)
    * ET2.R()
    * ET2.tx(L2)
)

# Configuración articular
q = np.deg2rad([0, 0])

# Cinemática directa con Robotics Toolbox
T = robot.fkine(q)

print("Transformación homogénea:")
print(T)

# Posiciones de las articulaciones
q1, q2 = q

x0, y0 = 0.0, 0.0

x1 = L1*np.cos(q1)
y1 = L1*np.sin(q1)

x2 = x1 + L2*np.cos(q1 + q2)
y2 = y1 + L2*np.sin(q1 + q2)

# Espacio de trabajo (código de la guía)
theta = np.linspace(0, 2*np.pi, 500)

r_min = abs(L1-L2)
r_max = L1+L2

plt.figure(figsize=(7, 7))

plt.plot(
    r_max*np.cos(theta),
    r_max*np.sin(theta),
    label="Límite exterior"
)

plt.plot(
    r_min*np.cos(theta),
    r_min*np.sin(theta),
    label="Límite interior"
)

# Primer eslabón
plt.plot(
    [x0, x1],
    [y0, y1],
    "o-",
    color="blue",
    linewidth=3,
    markersize=8,
    label="Eslabón 1"
)

# Segundo eslabón
plt.plot(
    [x1, x2],
    [y1, y2],
    "o-",
    color="orange",
    linewidth=3,
    markersize=8,
    label="Eslabón 2"
)

# Ejes coordenados
plt.axhline(y=0, color="black", linewidth=1)
plt.axvline(x=0, color="black", linewidth=1)

plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Espacio de trabajo del manipulador 2R")
plt.axis("equal")
plt.grid(True)
plt.legend()

plt.show()
