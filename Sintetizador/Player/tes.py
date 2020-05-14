import numpy as np


arr1 = np.array([1, 2, 3, 4, 5])

print(arr1)

arr2 = np.array([6, 7, 8, 9, 10, 11, 12, 13, 14, 15])

print(arr2)


diff = len(arr2) - len(arr1)

print(diff)

ceros = np.zeros(diff)
sumar = np.append(arr1, ceros)

print(sumar)
print(len(sumar))
print(len(arr2))