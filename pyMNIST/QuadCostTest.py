import numpy as np

''' Different options to do the cost function.
Pythagorean with squared sums -> square root, divide by two at the end
Pythagorean with squared sums -> square root, mean at the end
Pythagorean with squared sums -> square root, divide by two and mean at the end
Pythagorean with square sums -> no square root, divide by two, or mean, at the end
'''

ac = np.array([4, 6, 2])
exp = np.array([8, 2, 0])
print(ac, exp)


def quad_cost_func_test(actual, expected):
    delta_matrix = np.abs(expected - actual)
    print(delta_matrix, delta_matrix.size)


quad_cost_func_test(ac, exp)
