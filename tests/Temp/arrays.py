import timeit
import math
import numpy as np
import numexpr as ne


def damped_sine_func(x, A, lbda, omega, phi):
    return A * math.exp(-lbda * x) * math.sin(omega * x + phi)

def calc_py_external_func(x_array, A, lbda, omega, phi):
    y_array = []
    for x in x_array:
        y_array.append(damped_sine_func(x, A, lbda, omega, phi))
    return y_array

def calc_py_internal_func(x_array, A, lbda, omega, phi):
    y_array = []
    for x in x_array:
        y_array.append(A * math.exp(-lbda * x) * math.sin(omega * x + phi))
    return y_array

def calc_py_list_compreh(x_array, A, lbda, omega, phi):
    return [A * math.exp(-lbda * x) * math.sin(omega * x + phi) for x in x_array]

def calc_numpy(x_array, A, lbda, omega, phi):
    return A * np.exp(-lbda * x_array) * np.sin(omega * x_array + phi)

def calc_numexpr(x_array, A, lbda, omega, phi):
    return ne.evaluate("A * exp(-lbda * x_array) * sin(omega * x_array + phi)")

if __name__ == '__main__':
    num = 50_000

    x_nparray = np.linspace(0, 1, num=num)
    x_pylist = x_nparray.tolist()

    A = 1
    lbda = 1
    omega = 8 * np.pi
    phi = 0.5 * np.pi

    loop = 10

    print(f'calc_py_external_func for {num} points:', timeit.timeit(lambda: calc_py_external_func(x_pylist, A, lbda, omega, phi), number=loop)/loop)
    print(f'calc_py_internal_func for {num} points:', timeit.timeit(lambda: calc_py_internal_func(x_pylist, A, lbda, omega, phi), number=loop)/loop)
    print(f'calc_py_list_compreh for {num} points:', timeit.timeit(lambda: calc_py_list_compreh(x_pylist, A, lbda, omega, phi), number=loop)/loop)
    print(f'calc_numpy for {num} points:', timeit.timeit(lambda: calc_numpy(x_nparray, A, lbda, omega, phi), number=loop)/loop)
    print(f'calc_numexpr for {num} points:', timeit.timeit(lambda: calc_numexpr(x_nparray, A, lbda, omega, phi), number=loop)/loop)
