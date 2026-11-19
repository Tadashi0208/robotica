
import numpy as np
import matplotlib.pyplot as plt

L1 = 0.6
L2 = 0.4

# Posición objetivo
xd = 1.20
yd = 0.20

# Cálculo del coseno de q2
c2 = (
    xd**2 + yd**2 - L1**2 - L2**2
) / (2*L1*L2)

if abs(c2) > 1:
    print("Posición no alcanzable")

else:
    # Soluciones de la segunda articulación
    q2_a = np.arccos(c2)
    q2_b = -np.arccos(c2)

    soluciones = []

    for q2 in [q2_a, q2_b]:

        q1 = (
            np.arctan2(yd, xd)
            - np.arctan2(
                L2*np.sin(q2),
                L1 + L2*np.cos(q2)
            )
        )

        soluciones.append([q1, q2])

    # Verificación mediante cinemática directa
    for i, (q1, q2) in enumerate(soluciones):

        x = (
            L1*np.cos(q1)
            + L2*np.cos(q1+q2)
        )

        y = (
            L1*np.sin(q1)
            + L2*np.sin(q1+q2)
        )

        error = np.hypot(xd-x, yd-y)

        print(f"Solución {i+1}")
        print("Articulaciones [°]:",
              np.rad2deg([q1, q2]))
        print("Posición:", x, y)
        print("Error:", error)
