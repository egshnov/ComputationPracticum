import math

from tabulate import tabulate

class Function:
    def __init__(self, f, f_diff, f_2diff, func_str):
        self.f = f
        self.f_diff = f_diff
        self.f_2diff = f_2diff
        self.str = func_str


def f1(x):
    return math.exp(6 * x)  # 1.5 * ((13 % 5) + 1) = 6


def f1_diff(x):
    return 6 * math.exp(6 * x)


def f1_2diff(x):
    return 36 * math.exp(6 * x)


def f1_str():
    return "f(x) = exp(6x)"


def f2(x):
    return math.log(1 + x) - math.exp(x)


def f2_diff(x):
    return 1 / (1 + x) - math.exp(x)


def f2_2diff(x):
    return -1 / ((1 + x) ** 2) - math.exp(x)


def f2_str():
    return "f(x) = ln(1+x) – exp(x)"


def create_table_of_values(a, h, m_plus_one, func):
    table = []
    for i in range(m_plus_one):
        x_i = a + i * h
        f_x_i = func.f(x_i)
        table.append((x_i, f_x_i))
    return table


def first_derivative(table, h, i): #формулы 6 7 8
    if i == 0:
        return (-3 * table[i][1] + 4 * table[i + 1][1] - table[i + 2][1]) / (2 * h)
    if i == len(table) - 1:
        return (3 * table[i][1] - 4 * table[i - 1][1] + table[i - 2][1]) / (2 * h)
    return (table[i + 1][1] - table[i - 1][1]) / (2 * h)

def new_first_derivative(table, h, i):
    if i == 0:
        return (-25 * table[i][1] + 48 * table[i+1][1] - 36* table[i+2][1] + 16 * table[i+3][1] - 3 * table[i+4][1])/(12*h)
    if i == 1:
        return (-3 * table[i-1][1] - 10 * table[i][1] + 18 * table[i+1][1] - 6* table[i+2][1] + table[i+3][1])/(12*h)
    if i == len(table) - 2:
        return (3 * table[i+1][1] + 10 * table[i][1] - 18 * table[i-1][1] + 6* table[i-2][1] - table[i-3][1])/(12*h)
    if i == len(table) - 1:
        return (25 * table[i][1] - 48 * table[i-1][1] + 36* table[i-2][1] - 16 * table[i-3][1] + 3 * table[i-4][1])/(12*h)
    return (table[i-2][1] - 8 * table[i-1][1] + 8 * table[i+1][1] - table[i+2][1])/(12 * h)

def second_derivative(table, h, i):

    if i == 0:
        return (2 * table[i][1] - 5 * table[i+1][1] + 4 * table[i+2][1] - table[i+3][1]) / (h**2)
    if i == len(table) - 1:
        return (2 * table[i][1] - 5 * table[i-1][1] + 4 * table[i-2][1] - table[i-3][1]) / (h**2)
    return (table[i + 1][1] - 2 * table[i][1] + table[i - 1][1]) / (h ** 2)



def calculate_default(func):
    m_plus_one = int(input("Введите число значений в таблице (m + 1): "))

    a = float(input("Введите начало отрезка a: "))

    while True:
        h = float(input("Введите значение шага h > 0: "))
        if h > 0:
            break
        print("h должно быть > 0. Повторите ввод.")

    table = create_table_of_values(a, h, m_plus_one, func)

    values_table = [["x_i", "f(x_i)"]]
    for i, (x_i, f_x_i) in enumerate(table):
        values_table.append([f"x_{i}", f"{x_i:.6f}", f"{f_x_i:.6f}"])

    print("\nТаблица значений функции:")
    print(tabulate(values_table, headers="firstrow", tablefmt="grid"))

    derivatives_table = [
        ["x_i", "f(x_i)", "f'(x_i)чд", "|f'(x_i)_T - f'(x_i)чд|", "f1(x_i)чд до h^4", "|f'(x_i)_T - f'(x_i)чд|", "f''(x_i)чд", "|f''(x_i)_T - f''(x_i)чд|"]
    ]
    for i, (x_i, f_x_i) in enumerate(table):
        f_diff = first_derivative(table, h, i)
        f_2diff = second_derivative(table, h, i)
        f_n_diff = new_first_derivative(table,h,i)
        derivatives_table.append([
            f"{x_i:.10f}",
            f"{f_x_i:.10f}",
            f"{f_diff:.10f}",
            f"{abs(func.f_diff(x_i) - f_diff):.10f}",
            f"{f_n_diff:.10f}",
             f"{abs(func.f_diff(x_i) - f_n_diff):.10f}",
            f"{f_2diff:.10f}",
            f"{abs(func.f_2diff(x_i) - f_2diff):10f}"
        ])

    print("\nТаблица производных:")
    print(tabulate(derivatives_table, headers="firstrow", tablefmt="grid"))
   

def calculate_runge(func):
    m_plus_one = int(input("Введите число значений в таблице (m + 1): "))

    a = float(input("Введите начало отрезка a: "))

    while True:
        h = float(input("Введите значение шага h > 0: "))
        if h > 0:
            break
        print("h должно быть > 0. Повторите ввод.")

    table_h = create_table_of_values(a, h, m_plus_one, func)
    table_h2 = create_table_of_values(a, h/2, m_plus_one * 2, func)
    
    values_table = [["x_i", "f(x_i)"]]
    
    for i, (x_i, f_x_i) in enumerate(table_h):
        values_table.append([f"x_{i}", f"{x_i:.6f}", f"{f_x_i:.6f}"])

    print("\nТаблица значений функции:")
    print(tabulate(values_table, headers="firstrow", tablefmt="grid"))

    derivatives_table = [
        ["x_i", "f(x_i)", "J(h)", "|f'(x_i)_T - J(h)|", "J(h/2)", "|f'(x_i)_T - J(h/2)|", "J", "|f'(x_i)_T - J|", "J(h) для 2й", "J(h/2) для 2й", "|f''(x_i)_T - J|"]
    ]
    for i, (x_i, f_x_i) in enumerate(table_h):
        j_h = first_derivative(table_h, h, i)
        j_h_2 = first_derivative(table_h2, h/2, i*2)
        j = (4*j_h_2-j_h)/3
        j_h_d2 = second_derivative(table_h,h,i)
        j_h_2_d2 = second_derivative(table_h2, h/2, i*2)
        j_d2 = (4*j_h_2_d2-j_h_d2)/3
        # f_2diff = second_derivative(table, h, i)
        # f_n_diff = new_first_derivative(table,h,i)
        derivatives_table.append([
            f"{x_i:.10f}",
            f"{f_x_i:.10f}",
            f"{j_h:.10f}",
            f"{abs(func.f_diff(x_i) - j_h):.10f}",
            f"{j_h_2:.10f}",
             f"{abs(func.f_diff(x_i) - j_h_2):.10f}",
            f"{j:.10f}",
            f"{abs(func.f_diff(x_i) - j):10f}",
            f"{j_h_d2:.10f}",
            f"{j_h_2_d2:.10f}",
            f"{abs(func.f_2diff(x_i) - j_d2)}"
            
        ])

    print("\nТаблица производных:")
    print(tabulate(derivatives_table, headers="firstrow", tablefmt="grid"))

    
def calculate(func, runge):
    if(runge):
        calculate_runge(func)
        return
    calculate_default(func)

def main():
    print("Задача 3. Нахождение производных таблично-заданной функции по формулам численного дифференцирования")
    print("Вариант №13")

    runge = False
    while True:
        func_num = 0
        print("1. ", f1_str())
        print("2. ", f2_str())
        while True:
            func_num = int(input("Введите номер функции, которую вы хотите исследовать (1 или 2): "))
            if func_num in [1, 2]:
                break
            print("Вы ввели некорректное значение. Введите 1 или 2.")
        
        func = Function(f1, f1_diff, f1_2diff, f1_str) if func_num == 1 else Function(f2, f2_diff, f2_2diff, f2_str)

        print(f"Вы выбрали функцию: {func.str()}\n")
       
        ans = '0'
        while True:
            calculate(func, runge)
            runge = False
            while(True):
                ans = input("Выберите следующее действие:\n1. Выбрать другую функцию 2. Ввести новые значения для нынешней функции 3. Перейти к уточнению по Рунге 4. Завершить исполнение\n").lower()
                if ans in ["1", "2", "3", "4"]:
                    break
                print("Вы выбрали несуществующую опцию!!!!! Введите 1, 2, 3 или 4")
            if ans in ["1", "3", "4"]:
                break
        if ans == "3":
            runge = True
        if ans == "4":
            break
        
        
        
        
    
            
if __name__ == "__main__":
    main()
