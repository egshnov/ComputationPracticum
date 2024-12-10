import numpy as np
import math

def constant_function(x,c):
    return c * np.ones_like(x)

def f(x):
    return constant_function(x,10)


def rho(x):
    return 1 #np.exp(x)

def F(x):
    return rho(x) * f(x)


def exact_integral(f, a, b):
    from scipy.integrate import quad
    result, _ = quad(f, a, b)
    return result

def composite_quadratures(f, a, b, m):
    h = (b - a) / m
    x = np.linspace(a, b, m + 1) # равномерно распределенная последовательность числе в отрезке с указанным шагом
    
    left_rect = sum(f(x[:-1])) * h # все кроме последнего
    
    right_rect = sum(f(x[1:])) * h # все кроме первого
    
    mid_points = (x[:-1] + x[1:]) / 2
    mid_rect = sum(f(mid_points)) * h
    
    trapezoid = (f(a) + f(b) + 2 * sum(f(x[1:-1]))) * h / 2
    
    # Всегда используем чётное количество отрезков
    m_simpson = 2 * m
    h_simpson = (b - a) / m_simpson
    x_simpson = np.linspace(a, b, m_simpson + 1)
    simpson = (f(a) + f(b) +
               4 * sum(f(x_simpson[1:-1:2])) +
               2 * sum(f(x_simpson[2:-2:2]))) * h_simpson / 3
    
    return left_rect, right_rect, mid_rect, trapezoid, simpson

def runge_correction_pair(j_h, j_h2, p):
    return j_h2 + (j_h2 - j_h) / (2**p - 1)


def main():
    from tabulate import tabulate

    print("Приближённое вычисление интеграла по составным квадратурным формулам.")
    a = float(input("Введите нижний предел интегрирования A: "))
    b = float(input("Введите верхний предел интегрирования B: "))
    m = int(input("Введите число промежутков деления m: "))
    
    j_exact = exact_integral(F, a, b)
    h = (b - a) / m
    print(f"\nТочное значение интеграла: J = {j_exact:.15f}")
    print(f"Параметры задачи: A={a}, B={b}, m={m}, h={h:.15f}\n")
    
    j_approx = composite_quadratures(F, a, b, m)
    j_approx_h2 = composite_quadratures(F, a, b, m * 2)
    
    methods = ["Левые прямоугольники", "Правые прямоугольники", 
               "Средние прямоугольники", "Трапеции", "Симпсона"]
    orders = [1, 1, 2, 2, 4]

    table = []
    for method, j in zip(methods, j_approx):
        abs_error = abs(j_exact - j)
        rel_error = abs_error / abs(j_exact)
        table.append([method, f"{j:.15f}", f"{abs_error:.15f}", f"{rel_error:.15f}"])
    
    print(f"Результаты для m = {m}:")
    print(tabulate(table, headers=["Метод", "J(h)", "Абс. погр.", "Отн. погр."], tablefmt='grid'))

    # Таблица результатов с уточнением по Рунге для m
    table_runge = []
    for method, j, j_h2, p in zip(methods, j_approx, j_approx_h2, orders):
        j_refined = runge_correction_pair(j, j_h2, p)
        abs_error_ref = abs(j_exact - j_refined)
        rel_error_ref = abs_error_ref / abs(j_exact)
        table_runge.append([method, f"{j_refined:.15f}", f"{abs_error_ref:.15f}", f"{rel_error_ref:.15f}"])
    
    print(f"\nУточнённые значения методом Рунге для m = {m}:")
    print(tabulate(table_runge, headers=["Метод", "J(точн.)", "Абс. погр.", "Отн. погр."],tablefmt='grid'))

    # Уточнение для m*l
    l = int(input("\nВведите параметр l для увеличения числа разбиений: "))
    j_approx_l = composite_quadratures(F, a, b, m * l)
    j_approx_h2l = composite_quadratures(F, a, b, m * 2 * l)

    # Таблица результатов без уточнения для m*l
    table_l = []
    for method, j_l in zip(methods, j_approx_l):
        abs_error_l = abs(j_exact - j_l)
        rel_error_l = abs_error_l / abs(j_exact)
        table_l.append([method, f"{j_l:.15f}", f"{abs_error_l:.15f}", f"{rel_error_l:.15f}"])
    
    print(f"\nРезультаты для m*l= {m*l}:")
    print(tabulate(table_l, headers=["Метод", "J(h/l)", "Абс. погр.", "Отн. погр."],tablefmt='grid'))

    # Таблица результатов с уточнением по Рунге для m*l
    table_runge_l = []
    for method, j_l, j_h2l, p in zip(methods, j_approx_l, j_approx_h2l, orders):
        j_refined_l = runge_correction_pair(j_l, j_h2l, p)
        abs_error_ref_l = abs(j_exact - j_refined_l)
        rel_error_ref_l = abs_error_ref_l / abs(j_exact)
        table_runge_l.append([method, f"{j_refined_l:.15f}", f"{abs_error_ref_l:.15f}", f"{rel_error_ref_l:.15f}"])
    
    print(f"\nУточнённые значения методом Рунге для m*l = {m*l}:")
    print(tabulate(table_runge_l, headers=["Метод", "J(точн. для m*l)", "Абс. погр.", "Отн. погр."],tablefmt='grid'))

if __name__ == "__main__":
    main()
