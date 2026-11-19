
import numpy as np
import matplotlib.pyplot as plt

L1 = 0.6
L2 = 0.4

q1 = np.deg2rad(30)
q2 = np.deg2rad(45)

# Jacobiano de posición
J = np.array([
    [
        -L1*np.sin(q1)-L2*np.sin(q1+q2),
        -L2*np.sin(q1+q2)
    ],
    [
        L1*np.cos(q1)+L2*np.cos(q1+q2),
        L2*np.cos(q1+q2)
    ]
])

print("Jacobiano:")
print(J)

print("Determinante:")
print(np.linalg.det(J))

# Evaluación del determinante
q2_values = np.linspace(-np.pi, np.pi, 400)

det_values = L1*L2*np.sin(q2_values)

plt.figure(figsize=(8, 5))

plt.plot(
    np.rad2deg(q2_values),
    det_values
)

plt.axhline(0, color="black", linestyle="--")

plt.xlabel("q2 [°]")
plt.ylabel("Determinante del jacobiano [m²]")
plt.title("Singularidades del manipulador 2R")
plt.grid(True)

plt.show()
