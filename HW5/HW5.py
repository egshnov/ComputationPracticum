from tabulate import tabulate
import numpy as np
from math import factorial, tan, sqrt

# Точное решение (вариант 13)
def exact_solution(x):
    sqrt_7 = sqrt(7)
    return 0.25 + sqrt_7 / 4 * tan(sqrt_7 / 2 * x)

# Функция, определяющая правую часть уравнения
def f(x, y):
    return -y + 2 * y**2 + 1

# Метод Тейлора (6 слагаемых)
def taylor_method(x0, y0, h, N):
    def derivatives(y):
        d1 = -y + 2 * y**2 + 1
        d2 = -d1 + 4 * y * d1
        d3 = -d2 + 4 * (d1**2 + y * d2)
        d4 = -d3 + 4 * (3 * d1 * d2 + y * d3)
        d5 = -d4 + 4 * (3 * d2**2 + 4 * d1 * d3 + y * d4)
        #d6 = -d5 + 4 * (4 * d1 * d4 + 6 * d2 * d3 + y * d5)
        return [d1, d2, d3, d4, d5]#, d6]

    x_vals = [x0]
    y_vals = [y0]
    for k in range(-2, N+1):
        x_k = x_vals[-1] + h
        y_k = y_vals[-1]
        d = derivatives(y_k)
        y_next = y_k + sum(d[i] * (h**(i + 1)) / factorial(i + 1) for i in range(5))
        x_vals.append(x_k)
        y_vals.append(y_next)
    return x_vals, y_vals

# Метод Рунге-Кутты 4-го порядка
def runge_kutta_4(x0, y0, h, N):
    x_vals = [x0]
    y_vals = [y0]
    for k in range(N):
        x_k = x_vals[-1]
        y_k = y_vals[-1]
        k1 = h * f(x_k, y_k)
        k2 = h * f(x_k + h / 2, y_k + k1 / 2)
        k3 = h * f(x_k + h / 2, y_k + k2 / 2)
        k4 = h * f(x_k + h, y_k + k3)
        y_next = y_k + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        x_vals.append(x_k + h)
        y_vals.append(y_next)
    return x_vals, y_vals

# Метод Эйлера
def euler_method(x0, y0, h, N):
    x_vals = [x0]
    y_vals = [y0]
    for k in range(N):
        x_k = x_vals[-1]
        y_k = y_vals[-1]
        y_next = y_k + h * f(x_k, y_k)
        x_vals.append(x_k + h)
        y_vals.append(y_next)
    return x_vals, y_vals

# Метод Эйлера I (средний прямоугольник)
def euler_method_1(x0, y0, h, N):
    x_vals = [x0]
    y_vals = [y0]
    for k in range(N):
        x_k = x_vals[-1]
        y_k = y_vals[-1]
        y_half = y_k + (h / 2) * f(x_k, y_k)
        y_next = y_k + h * f(x_k + h / 2, y_half)
        x_vals.append(x_k + h)
        y_vals.append(y_next)
    return x_vals, y_vals

# Метод Эйлера II (трапеция)
def euler_method_2(x0, y0, h, N):
    x_vals = [x0]
    y_vals = [y0]
    for k in range(N):
        x_k = x_vals[-1]
        y_k = y_vals[-1]
        y_predict = y_k + h * f(x_k, y_k)
        y_next = y_k + (h / 2) * (f(x_k, y_k) + f(x_k + h, y_predict))
        x_vals.append(x_k + h)
        y_vals.append(y_next)
    return x_vals, y_vals

# Экстраполяционный метод Адамса 4-го порядка
# Экстраполяционный метод Адамса 4-го порядка
def adams_4th_order(x0, y0, h, N):
    # Получаем начальные значения из метода Тейлора
    x_taylor, y_taylor = taylor_method(x0, y0, h, 5)
    
    # Инициализация для метода Адамса
    x_vals = x_taylor[:5]
    y_vals = y_taylor[:5]

    # Экстраполяция методом Адамса 4-го порядка
    for i in range(5, N + 1):
        # Последние 4 значения
        f_3 = f(x_vals[-4], y_vals[-4])
        f_2 = f(x_vals[-3], y_vals[-3])
        f_1 = f(x_vals[-2], y_vals[-2])
        f_0 = f(x_vals[-1], y_vals[-1])

        # Вычисление следующего значения
        y_next = y_vals[-1] + h * (55 / 24 * f_0 - 59 / 24 * f_1 + 37 / 24 * f_2 - 9 / 24 * f_3)
        x_next = x_vals[-1] + h

        # Добавление нового значения
        x_vals.append(x_next)
        y_vals.append(y_next)

    return x_vals, y_vals


# Основная программа
def main():
    while True:
        try:
            print("\nВведите параметры задачи:")
            h = float(input("Введите шаг h: "))
            N = int(input("Введите количество шагов N: "))
            x0, y0 = 0, 0.25

            # Вычисление результатов методами
            x_t, y_taylor = taylor_method(x0, y0, h, N)
            x_rk, y_rk4 = runge_kutta_4(x0, y0, h, N)
            x_e, y_euler = euler_method(x0, y0, h, N)
            x_e1, y_euler1 = euler_method_1(x0, y0, h, N)
            x_e2, y_euler2 = euler_method_2(x0, y0, h, N)
            x_adams, y_adams = adams_4th_order(x0, y0, h, N)

            # Приведение всех массивов к минимальной длине
            min_len = min(len(y_taylor), len(y_rk4), len(y_euler), len(y_euler1), len(y_euler2), len(y_adams))
            y_taylor = y_taylor[:min_len]
            y_rk4 = y_rk4[:min_len]
            y_euler = y_euler[:min_len]
            y_euler1 = y_euler1[:min_len]
            y_euler2 = y_euler2[:min_len]
            y_adams = y_adams[:min_len]
            x_t = x_t[:min_len]

            # Формирование данных для таблицы
            table_data = []
            for i in range(min_len):
                exact = exact_solution(x_t[i])
                table_data.append([
                    i, x_t[i], exact,
                    y_taylor[i], y_rk4[i], y_euler[i],
                    y_euler1[i], y_euler2[i], y_adams[i]
                ])

            # Погрешности для последнего шага
            last_idx = min_len - 1
            exact = exact_solution(x_t[last_idx])
            table_data.append([
                "Погрешности",
                x_t[last_idx], None,
                abs(y_taylor[last_idx] - exact),
                abs(y_rk4[last_idx] - exact),
                abs(y_euler[last_idx] - exact),
                abs(y_euler1[last_idx] - exact),
                abs(y_euler2[last_idx] - exact),
                abs(y_adams[last_idx] - exact)
            ])

            # Заголовки таблицы
            headers = [
                "Шаг", "x", "Точное",
                "Тейлор", "Рунге-Кутта", "Эйлер", "Эйлер I", "Эйлер II", "Адамс 4-го порядка"
            ]

            # Вывод таблицы
            print("\nТаблица решений:")
            print(tabulate(table_data, headers=headers, floatfmt=".6f", tablefmt="grid"))

            # Запрос следующего действия у пользователя
            choice = input("\nВыберите действие:\n1. Ввести новые параметры N и h.\n2. Завершить программу.\nВаш выбор: ")
            if choice == "1":
                continue
            elif choice == "2":
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}. Попробуйте снова.")

# Запуск программы
if __name__ == "__main__":
    main()
