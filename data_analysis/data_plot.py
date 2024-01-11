import matplotlib.pyplot as plt
import numpy as np

# plot the coordinate rate for different number of shepherds in different experiments
plt.figure(figsize=(8, 6), dpi=300)

Coordinate_rate_1 = [0.27566821, 0.41870727, 0.43268498, 0.39779931]
Coordinate_rate_2 = [0.19009225, 0.30122245, 0.34001382, 0.32961186]
Coordinate_rate_3 = [0.12916332, 0.2203914,  0.19322434, 0.1768058 ]
Coordinate_rate_4 = [0.13176278, 0.22539609, 0.20774006, 0.19836793]
Coordinate_rate_5 = [0.10728878, 0.15610854, 0.20185862, 0.20313016]
Coordinate_rate_6 = [0.101035, 0.186179, 0.217867, 0.213464]
Coordinate_rate_7 = [0.064301, 0.151275, 0.156486, 0.261062]

x = np.arange(1, 5)

plt.plot(x, Coordinate_rate_1, '^-', color = 'orange', label = "N_sheep = 100")
plt.plot(x, Coordinate_rate_2, '^-', color = 'cyan', label = "N_sheep = 150")
plt.plot(x, Coordinate_rate_3, '^-', color = 'green', label = "N_sheep = 200")
plt.plot(x, Coordinate_rate_4, '^-', color = 'blue', label = "N_sheep = 250")
plt.plot(x, Coordinate_rate_5, '^-', color = 'purple', label = "N_sheep = 300")
plt.plot(x, Coordinate_rate_6, '^-', color = 'brown', label = "N_sheep = 400")
plt.plot(x, Coordinate_rate_7, '^-', color = 'grey', label = "N_sheep = 500")

plt.xticks(x, ["N = 2", "N = 3", "N = 4", "N = 5"])

plt.xlabel("Shepherd number")
plt.ylabel("Coordination Ratio")

plt.legend(loc = "best")
plt.savefig("./figures/Coordination_Ratio.png")
plt.show()


