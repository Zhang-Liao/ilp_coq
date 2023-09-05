import matplotlib.pyplot as plt

k = list(range(0, 10))

ilp = [17.679, 23.638, 28.186, 30.207, 31.699, 32.466, 33.064, 33.517, 33.848, 34.144]

knn = [15.925, 20.513, 24.631, 26.484, 28.116, 29.899, 31.177, 32.24, 33.262, 34.144]

plt.plot(k, ilp, label = "ILP + kNN")
plt.plot(k, knn, label = "kNN")


# naming the x axis
plt.xlabel('top-k accuracy')
plt.ylabel('%')

plt.legend()
plt.savefig("results.pdf", bbox_inches='tight')

# plt.show()