
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

    # Representación de ambas configuraciones
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    for i, (q1, q2) in enumerate(soluciones):

        # Posiciones de las articulaciones
        x0, y0 = 0.0, 0.0

        x1 = L1*np.cos(q1)
        y1 = L1*np.sin(q1)

        x2 = x1 + L2*np.cos(q1+q2)
        y2 = y1 + L2*np.sin(q1+q2)

        ax = axes[i]

        # Primer eslabón
        ax.plot(
            [x0, x1],
            [y0, y1],
            "o-",
            color="blue",
            linewidth=3,
            markersize=8,
            label="Eslabón 1"
        )

        # Segundo eslabón
        ax.plot(
            [x1, x2],
            [y1, y2],
            "o-",
            color="orange",
            linewidth=3,
            markersize=8,
            label="Eslabón 2"
        )

        # Posición objetivo
        ax.scatter(
            xd, yd,
            color="red",
            marker="x",
            s=100,
            label="Objetivo"
        )

        # Ejes coordenados
        ax.axhline(0, color="black", linewidth=1)
        ax.axvline(0, color="black", linewidth=1)

        ax.set_title(
            f"Solución {i+1}: "
            f"q1={np.rad2deg(q1):.2f}°, "
            f"q2={np.rad2deg(q2):.2f}°"
        )

        ax.set_xlabel("X [m]")
        ax.set_ylabel("Y [m]")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")
        ax.grid(True)
        ax.legend()

    plt.tight_layout()
    plt.show()
