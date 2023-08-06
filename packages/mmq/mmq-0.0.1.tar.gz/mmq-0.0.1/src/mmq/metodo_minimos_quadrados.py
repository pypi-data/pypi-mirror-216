import numpy as np

def mmq(entradas: np.array, saidas: np.array, g: int) -> np.array:

    s_x = np.zeros(shape=(1, 2 * g + 1))
    for i in range(2 * g, -1, -1):
        s_x[0, i] = sum(entradas ** (2 * g - i))
    
    m = np.zeros(shape=(g + 1, g + 1))
    for j in range(g + 1):
        m[j, :] = s_x[0, j:j + g + 1]
    m_inv = np.linalg.inv(m)

    s_xy = np.zeros(shape=(g + 1, 1))
    for k in range(g, -1, -1):
        s_xy[g - k, 0] = sum((entradas ** k) * saidas)

    # coeficientes = m_inv @ s_xy # same as np.dot(m_inv, s_xy) or m_inv.dot(s_xy) or np.matmul(m_inv, s_xy) or np.linalg.solve(m, s_xy)
    coeficientes = m_inv @ s_xy

    return coeficientes.ravel()


if __name__ == "__main__":
    # x = np.array([0, 1, 2, 3, 4, 5])
    # f = np.array([11, -2, 7, 20, 19, -14])    # f(x) = -3x³ + 20x² - 30x¹ + 11x⁰
    # g = 3

    x = np.array([-1, 0, 1, 2])
    f = np.array([2, 3, 6, 11])             # f(x) = 1x² + 2x¹ + 3x⁰
    g = 2

    coef = mmq(entradas=x, saidas=f, g=g)

    print(f"Coeficientes (equação de {g}⁰):")
    print(dict(zip([chr(c) for c in range(97, 97 + g + 1, 1)], coef.T)))