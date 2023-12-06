import matplotlib.pyplot as plt
import numpy as np

# plot the coordinate rate for different number of shepherds in different experiments
plt.figure(figsize=(8, 6), dpi=300)

Coordinate_rate_1 = [0.10322,   0.14568458, 0.13415542, 0.11903]
Coordinate_rate_2 = [0.08625375, 0.13505667, 0.128325,   0.10942042]
Coordinate_rate_3 = [0.09969167, 0.144556,   0.10324458, 0.09649833]
Coordinate_rate_4 = [0.116228,   0.15559208, 0.16120167, 0.15621125]
Coordinate_rate_5 = [0.09875022, 0.12494222, 0.187635,   0.18960333]
Coordinate_rate_6 = [0.09241111, 0.18385111, 0.26704667, 0.20782667]
Coordinate_rate_7 = [0.00746333, 0.15328,    0.19902111, 0.27475333]

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


