import numpy as np

"""
stochastic.py
Generates stochastic matrices with given properties

Handles the primary functions
"""

def stochastic(eigenvalues):
    eigenvalues = get_valid_spectrum(eigenvalues)




def get_valid_spectrum(eigenvalues):
    eigenvalues = np.sort(eigenvalues)[::-1]
    if np.max(eigenvalues) >= 1:
        raise ValueError('Eigenvalues must be strictly less that 1. Eigenvalue of 1 is included by default.')
    if np.any(eigenvalues < 0):
        raise NotImplemented('Negative eigenvalues not implemented yet.')
    if np.any(np.iscomplex(eigenvalues)):
        raise ValueError('Eigenvalues must be real.')
    return eigenvalues


def r_min(eigenvalue, matrix_element):
    return np.max(0, eigenvalue/(eigenvalue+matrix_element))


def r_max(eigenvalue, matrix_element):
    return np.min(1, matrix_element/(eigenvalue + matrix_element))


def split_element(eigenvalue, matrix_element):
    if matrix_element > np.abs(eigenvalue):
        raise ValueError('Matrix element to be split must be larger than proposed eigenvalue.')

    min_val = r_min(eigenvalue, matrix_element)
    max_val = r_max(eigenvalue, matrix_element)
    r = np.random.uniform(min_val, max_val, size=1)[0]

    split = (matrix_element/max_val)*np.array([[r, max_val-r],
                                           [r-min_val, 1-r]])
    return split, r


def split_matrix(eigenvalue, matrix, matrix_element_ix):

    A11 = matrix[:matrix_element_ix, :matrix_element_ix]
    c1k = matrix[:matrix_element_ix, [matrix_element_ix]]
    A12 = matrix[:matrix_element_ix, matrix_element_ix + 1:]

    r1k = matrix[[matrix_element_ix], :matrix_element_ix]
    r2k = matrix[[matrix_element_ix], matrix_element_ix + 1:]

    A21 = matrix[matrix_element_ix + 1:, :matrix_element_ix]
    c2k = matrix[matrix_element_ix + 1:, [matrix_element_ix]]
    A22 = matrix[matrix_element_ix + 1:, matrix_element_ix + 1:]

    matrix_element = matrix[matrix_element_ix, matrix_element_ix]
    S, r = split_element(matrix_element, eigenvalue)

    new_r1 = np.concatenate([A11, r * c1k, (1 - r) * c1k, A12], axis=1)
    new_rk = np.concatenate([np.concatenate([r1k, r1k], axis=0), S, np.concatenate([r2k, r2k], axis=0)], axis=1)
    new_r2 = np.concatenate([A21, r * c2k, (1 - r) * c2k, A22], axis=1)
    new_A = np.concatenate([new_r1, new_rk, new_r2], axis=0)
    return new_A