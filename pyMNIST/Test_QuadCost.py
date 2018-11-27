import numpy as np

ac = np.array([0.77, 0.6, 0.15])
exp = np.array([0.8, 0.45, 0.1])


def quad_cost_func_test(actual, expected):
    delta_matrix = np.abs(expected - actual)
    print(delta_matrix, delta_matrix.size)
    vec_length = np.dot(delta_matrix, delta_matrix)
    return 0.5 * vec_length


if __name__ == "__main__":
    print(ac, exp)
    print(quad_cost_func_test(ac, exp))
