import matplotlib.pyplot as plt

N_shepherd = [1, 2, 3]
Tick_number_1 = [49530, 37171, 39336]
Tick_number_2 = [71770, 77716, 78348]
Tick_number_3 = [88746, 65977, 71155]

plt.plot(N_shepherd, Tick_number_1, 's-', color = 'r', label = "N_sheep = 50")
plt.plot(N_shepherd, Tick_number_2, '*-', color = 'cyan', label = "N_sheep = 75")
plt.plot(N_shepherd, Tick_number_3, 'o-', color = 'g', label = "N_sheep = 100")

plt.xticks([1,2,3], ["N = 1", "N = 2", "N = 3"])

plt.xlabel("Shepherd number")
plt.ylabel("Ticks in total")

plt.legend(loc = "best")
plt.savefig("result.png")
plt.show()


