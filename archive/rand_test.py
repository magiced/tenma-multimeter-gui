import random
import matplotlib.pyplot as plt
rand_x = [i for i in range(10)]
rand_y = [random.randint(0,10) for i in range(10)]
print(rand_x)
print(rand_y)
print(max(rand_y))
plt.plot(rand_x,rand_y)
plt.show()
