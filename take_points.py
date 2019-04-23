import numpy as np
from numpy import random

image = np.random.randint(0, 255, (25, 50), dtype=np.int)
print(image%100)
