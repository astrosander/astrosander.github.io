import numpy as np
import matplotlib.pyplot as plt

m = 0.1   
L = 0.681   
g = 9.8   

def vertical_displacement(M, m, L):

    ratio = M / (2.0*m)
    if ratio >= 1:
        return np.nan

    numerator = (L * M) / 4.0 / m
    denominator = np.sqrt(1.0 - ratio**2)
    y = numerator / denominator
    return y

M_values = np.linspace(0, 1.99*m, 200)

y_values = [vertical_displacement(M, m, L) for M in M_values]

# print(
#     vertical_displacement(0.2, m, L)
#     )

plt.figure()
plt.plot(M_values, y_values, marker='', linestyle='-')
plt.xlabel('Mass of central object, M (kg)')
plt.ylabel('Vertical displacement, y (m)')
plt.title('Vertical Displacement of Object B vs. Its Mass')
plt.grid(True)
plt.show()
