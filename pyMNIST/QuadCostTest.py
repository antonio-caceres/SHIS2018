import numpy as np

''' Different options to do the cost function.
** Pythagorean with squared sums -> square root, divide by two at the end
Pythagorean with squared sums -> square root, mean at the end
Pythagorean with squared sums -> square root, divide by two and mean at the end
Pythagorean with square sums -> no square root, divide by two, or mean, at the end
'''

ac = np.array([0.77, 0.6, 0.15])
exp = np.array([0.8, 0.45, 0.1])
print(ac, exp)


def quad_cost_func_test(actual, expected):
    delta_matrix = np.abs(expected - actual)
    print(delta_matrix, delta_matrix.size)
    vec_length = np.dot(delta_matrix, delta_matrix)
    return 0.5 * vec_length


print(quad_cost_func_test(ac, exp))
