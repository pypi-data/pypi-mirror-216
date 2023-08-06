from .boxprocessing import var_less_equal


def list_a(m, n, k, i):
    l_a = list(range(0, var_less_equal(m, k) + 1))
    return l_a


def list_b(m, n, k, i):
    l_b = list(range(0, var_less_equal(n, i) + 1))
    return l_b


def value_c(m, n, k, i, a):
    v_c = var_less_equal(m - a * k, i)
    return v_c


def list_d(m, n, k, i, b):
    y = var_less_equal(b * i, k)
    x = var_less_equal(n, k)
    l_d = list(range(y, x + 1))
    return l_d


def value_f(m, n, k, i, d):
    y = n - d * k
    x = i
    v_f = var_less_equal(y, x)
    return v_f


def list_e(m, n, k, i, c):
    y = var_less_equal(c * i, k)
    x = var_less_equal(m, k)
    l_e = list(range(y, x + 1))
    return l_e


def value_g(m, n, k, i, e):
    v_g = var_less_equal(m - e * k, i)
    return v_g


def value_h(m, n, k, i, b):
    y = n - b * i
    x = k
    v_h = var_less_equal(y, x)
    return v_h
