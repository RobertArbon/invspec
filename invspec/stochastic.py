import numpy as np
TOL = 1E-10
"""
stochastic.py
Generates stochastic matrices with given properties

Handles the primary functions
"""


def stochastic_matrix(eigenvalues, seed=None):
    if seed is not None:
        np.random.seed(seed)
    eigenvalues = get_valid_spectrum(eigenvalues)
    matrix = build_matrix(eigenvalues)
    rmsd = eigenvalues_rmsd(eigenvalues, matrix)
    if rmsd > TOL:
        raise RuntimeError(f'Something has gone wrong! RMSD between requested and actual eigenvalues is {rmsd:4.2f}.')
    else:
        return matrix


def eigenvalues_rmsd(eigenvalues, matrix):
    new_eigenvalues = np.sort(np.linalg.eig(matrix)[0])[::-1]
    new_eigenvalues_excl_1 = new_eigenvalues[1:]
    rmsd = np.sqrt(np.mean((new_eigenvalues_excl_1 - eigenvalues) ** 2))
    return rmsd


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
    return max(0, eigenvalue/(eigenvalue + matrix_element))


def r_max(eigenvalue, matrix_element):
    return min(1, matrix_element/(eigenvalue + matrix_element))


def split_element(eigenvalue, matrix_element):
    if matrix_element < np.abs(eigenvalue):
        raise ValueError(f'Matrix element ({matrix_element}) to be split must be larger than proposed eigenvalue '
                         f'({eigenvalue}).')

    min_val = r_min(eigenvalue, matrix_element)
    max_val = r_max(eigenvalue, matrix_element)
    r = np.random.uniform(min_val, max_val, size=1)[0]

    split = (matrix_element/max_val)*np.array([[r,         max_val-r],
                                               [r-min_val,       1-r]])
    return split, r


def embiggen_matrix(eigenvalue, matrix, element_index):
    A11 = matrix[:element_index, :element_index]
    c1k = matrix[:element_index, [element_index]]
    A12 = matrix[:element_index, element_index + 1:]
    r1k = matrix[[element_index], :element_index]
    r2k = matrix[[element_index], element_index + 1:]
    A21 = matrix[element_index + 1:, :element_index]
    c2k = matrix[element_index + 1:, [element_index]]
    A22 = matrix[element_index + 1:, element_index + 1:]

    matrix_element = matrix[element_index, element_index]
    S, r = split_element(eigenvalue, matrix_element)

    new_r1 = np.concatenate([A11, r * c1k, (1 - r) * c1k, A12], axis=1)
    new_rk = np.concatenate([np.concatenate([r1k, r1k], axis=0), S, np.concatenate([r2k, r2k], axis=0)], axis=1)
    new_r2 = np.concatenate([A21, r * c2k, (1 - r) * c2k, A22], axis=1)
    new_A = np.concatenate([new_r1, new_rk, new_r2], axis=0)
    return new_A


def choose_element_to_split(eigenvalue, matrix):
    matrix_diag = np.diag(matrix)
    element_indices = np.where(matrix_diag > eigenvalue)[0]
    element_index = np.random.choice(element_indices)
    return element_index


def build_matrix(eigenvalues):
    matrix, _ = split_element(eigenvalues[0], 1)
    for i in range(1, eigenvalues.shape[0]):
        eigenvalue = eigenvalues[i]
        element_index = choose_element_to_split(eigenvalue, matrix)
        matrix = embiggen_matrix(eigenvalue, matrix, element_index)
    return matrix
