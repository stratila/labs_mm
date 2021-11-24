import math
import numpy as np

E = 2 * 10 ** 11
CM = 4.9 * 10 ** 6
RO = 7800
DELTA = 1.2
SIGMA = 450 * 10 ** 6
VB = 10
F_MIN = 0.014
N_HITS = 5


def gen_rigidity(d_coll: list, l_coll: list):
    assert len(d_coll) == len(l_coll)  # lists lengths must be equal
    for d, l in zip(d_coll, l_coll):
        yield (E * math.pi * d ** 2) / (4 * l)  # C formula


def consolidated_rigidity(rigidity_data):
    return 1 / sum((1 / item for item in rigidity_data))


def sphere_diameter(d):
    return 4 / 3 * d / 2


def element_mass(d, l):
    return math.pi * d ** 2 * l * RO / 4


def sphere_mass(d, l):
    rc = (math.pow(d / 2, 2) + math.pow(l, 2)) / (2 * l)
    m = math.pi * math.pow(l, 2) * (rc - (l / 3)) * RO
    return m


def calculate_main_parameters(
        d2, d3, d4, d5, d8, d91, d90, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10
):
    # 1st and 6th elems are spheres
    d1 = sphere_diameter(d2)
    d6 = sphere_diameter(d5)

    rigidity_data = [
        c for c in gen_rigidity(
            [d1, d2, d3, d4, d5, d6], [l1, l2, l3, l4, l5, l6]
        )  # use generator to create tuple with results
    ]  # tuple comprehension

    c_b = consolidated_rigidity(rigidity_data)

    d7 = sphere_diameter(d8)
    d9 = d90 + (d91 - d90) / 2  # cone diameter
    d10 = sphere_diameter(d91)

    # extend tuple
    rigidity_data += (
        c for c in gen_rigidity(
        [d7, d8, d9, d10], [l7, l8, l9, l10]
    )
    )
    c_i = consolidated_rigidity(rigidity_data[6:])
    c_sum = 1 / (sum(1 / c for c in [c_b, c_i, CM]))

    m1 = sphere_mass(d2, l1)
    m2 = element_mass(d2, l2)
    m3 = element_mass(d3, l3)
    m4 = element_mass(d4, l4)
    m5 = element_mass(d5, l5)
    m6 = sphere_mass(d5, l6)

    m_b = m1 + m2 + m3 + m4 + m5 + m6

    m7 = sphere_mass(d8, l7)
    m8 = element_mass(d8, l8)
    m9 = (1 / 3) * math.pi * l9 * \
         ((math.pow(d91, 2) / 4) + ((d91 * d90) / 4) + (math.pow(d90, 2) / 4)) * RO
    m10 = sphere_mass(0.2, l10)

    m_i = m7 + m8 + m9 + m10
    m_sum = m_b + m_i / 3

    return c_sum, m_sum


def dissipation_coefficient(*args, **kwargs):
    x = []
    y = []

    c_sum, m_sum = calculate_main_parameters(*args, **kwargs)
    omega = math.sqrt(c_sum / m_sum)

    k = 0

    for n in range(0, N_HITS):
        x.append(n)
        y.append(k)
        k1 = math.sqrt(math.pow(omega, 2) + math.pow(k, 2))
        t = (2 * math.pi) / k1
        k = math.log(DELTA) / t

    return k, np.array(x), np.array(y)

