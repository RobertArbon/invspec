"""
Unit and regression test for the invspec package.
"""

# Import package, test suite, and other packages as needed
import invspec
import numpy as np
import pytest
import sys


def test_invspec_imported():
    """Sample test, will always pass so long as import statement worked"""
    assert "invspec" in sys.modules


def test_eigenvalues():
    eigenvalues = np.array([0.9, 0.8])
    mat = next(invspec.stochastic_matrix(eigenvalues, num_matrices=1, seed=123))
    eigenvalues = np.concatenate([[1], eigenvalues])

    evs, _ = np.linalg.eig(mat)
    evs = np.sort(evs)[::-1]
    assert np.allclose(eigenvalues, evs)


def is_stochastic(matrix):
    row_sums_are_1 = np.allclose(np.sum(matrix, axis=1), np.ones(matrix.shape))
    is_non_negative = np.all(matrix >= 0)
    return row_sums_are_1 and is_non_negative


def test_is_stochastic():
    eigenvalues = np.array([0.9, 0.8])
    mat = next(invspec.stochastic_matrix(eigenvalues, num_matrices=1, seed=123))
    assert is_stochastic(mat)


def test_embiggen_eigenvalues():
    matrix = np.array([[0.9, 0.1],
                       [0.1, 0.9]])
    evs, _ = np.linalg.eig(matrix)
    new_ev = 0.7
    new_matrix = invspec.embiggen_matrix(new_ev, matrix, element_index=0)
    new_evs, _ = np.linalg.eig(new_matrix)
    new_evs_correct = np.allclose(np.sort(np.concatenate([evs, [new_ev]])),
                                  np.sort(new_evs))
    assert new_evs_correct


def test_embiggen_is_stochastic():
    matrix = np.array([[0.9, 0.1],
                       [0.1, 0.9]])
    new_ev = 0.7
    new_matrix = invspec.embiggen_matrix(new_ev, matrix, element_index=0)

    assert is_stochastic(new_matrix)



