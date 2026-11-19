
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
q = np.deg2rad([0, 180])

# Cinemática directa con Robotics Toolbox
T = robot.fkine(q)

print("Transformación homogénea:")
print(T)

# Posiciones de las articulaciones
q1, q2 = q


# Determinante del Jacobiano
det_J = L1*L2*np.sin(q2)

print("Determinante del Jacobiano:")
print(det_J)


x0, y0 = 0.0, 0.0

x1 = L1*np.cos(q1)
y1 = L1*np.sin(q1)

x2 = x1 + L2*np.cos(q1 + q2)
y2 = y1 + L2*np.sin(q1 + q2)

# Representación gráfica
plt.figure(figsize=(7, 7))


# Primer eslabón
plt.plot(
    [x0, x1],
    [y0, y1],
    "o-",
    color="blue",
    linewidth=3,
    markersize=8
)

# Segundo eslabón
plt.plot(
    [x1, x2],
    [y1, y2],
    "o-",
    color="orange",
    linewidth=3,
    markersize=8
)


plt.xlabel("X [m]")
plt.ylabel("Y [m]")
plt.title("Manipulador plano 2R")
plt.grid(True)
plt.axis("equal")
plt.xlim(-1.1, 1.1)
plt.ylim(-1.1, 1.1)

# Ejes coordenados
plt.axhline(y=0, color="black", linewidth=1.5)
plt.axvline(x=0, color="black", linewidth=1.5)

plt.show()
