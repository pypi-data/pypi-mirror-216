"""Procedures for LU decomposition.
"""


def ludcmp(mat_a, n, indices):
    """Replaces a real n-by-n matrix a with the LU decomposition of a
    row-wise permutation of itself. LUDCMP is based on the routine of the same
    name in Numerical Recipes in C: The Art of Scientific Computing, by
    Flannery, Press, Teukolsky, and Vetterling, Cambridge University Press,
    Cambridge, MA, 1988. It is used by permission.

    :param numpy.ndarray mat_a: A flatten n-by-n numpy array
    :param int n: The size of a row in our flatten array
    :param numpy.ndarray indices: An n-array to store the pivot indices

    :returns: (a, indices), defined by (1) a (numpy.ndarray) as an output, a is
        replaced by the LU decomposition of a row-wise permutation of itself
        and (2) indices (numpy.ndarray) as a vector which records the row
        permutation effected by the partial pivoting. The values returned for
        index are needed in the call to LUBKSB
    :return type: (numpy.ndarray, numpy.ndarray)
    """
    tiny = 1e-12
    i_max = 0
    tmp_vv = [0] * n

    for i in range(1, n):
        a_max = 0.0
        for j in range(1, n):
            if abs(mat_a[i * n + j]) > a_max:
                a_max = abs(mat_a[i * n + j])
        if a_max < tiny:
            return -1
        tmp_vv[i] = 1.0 / a_max

    for j in range(1, n):
        for i in range(1, j):
            summed = mat_a[i * n + j]
            for k in range(1, i):
                summed -= mat_a[i * n + k] * mat_a[k * n + j]
            mat_a[i * n + j] = summed

        a_max = 0.0
        for i in range(j, n):
            summed = mat_a[i * n + j]
            for k in range(1, j):
                summed -= mat_a[i * n + k] * mat_a[k * n + j]
            mat_a[i * n + j] = summed
            tmp = tmp_vv[i] * abs(summed)
            if tmp >= a_max:
                i_max = i
                a_max = tmp

        if j != i_max:
            for k in range(1, n):
                tmp = mat_a[i_max * n + k]
                mat_a[i_max * n + k] = mat_a[j * n + k]
                mat_a[j * n + k] = tmp
            tmp_vv[i_max] = tmp_vv[j]

        indices[j] = i_max
        if abs(mat_a[j * n + j]) < tiny:
            mat_a[j * n + j] = tiny

        if j != n - 1:
            tmp = 1 / mat_a[j * n + j]
            for i in range(j + 1, n):
                mat_a[i * n + j] *= tmp

    return mat_a, indices


def lubksb(mat_a, n, indices, mat_b):
    """Solves the set of n linear equations Ax = b, reusing the indices and
    matrix returned by ludcmp.

    TODO: Should be documented a bit more in depth

    :param numpy.ndarray mat_a: The permuted matrix returned by LUDCMP
        routine
    :param int n: The size of a row in our flatten array
    :param numpy.ndarray indices: The pivot indices returned by the LUDCMP
        routine
    :param numpy.ndarray mat_b: The final matrix to return with the results

    :returns: The rotated matrix
    :return type: numpy.ndarray
    """
    i2 = 0

    for i in range(1, n):
        idx = int(indices[i])
        summed = mat_b[idx]
        mat_b[idx] = mat_b[i]
        if i2 != 0:
            for j in range(i2, i):
                summed -= mat_a[i * n + j] * mat_b[j]
        elif summed != 0:
            i2 = i
        mat_b[i] = summed

    for i in range(n - 1, 0, -1):
        summed = mat_b[i]
        if i < n - 1:
            for j in range(i + 1, n):
                summed -= mat_a[i * n + j] * mat_b[j]
        mat_b[i] = summed / mat_a[i * n + i]

    return mat_b
