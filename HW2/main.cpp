#include <iostream>
#include <vector>
#include <cmath>
long double function(long double x)
{
    return std::log(1 + x) - std::exp(x);
}

long double lagrange_interpol(const std::vector<std::pair<long double, long double>> &interpol_table, int n, long double x)
{
    std::vector<long double> numerators(n - 1, 1);
    std::vector<long double> denumerators(n - 1, 1);
    long double res = 0;
    for (int i = 0; i < n; i++)
    {
        long double term = interpol_table[i].second;
        for (int j = 0; j < n; j++)
        {
            if (j != i)
            {
                term = term * (x - interpol_table[j].first) / (interpol_table[i].first - interpol_table[j].first);
            }
        }
        res += term;
    }
    return res;
}
int main()
{
    int m, n; // m это m+1 в терминах методички
    long double a, b, x;
    std::cout << "Задача 2: алгебраическое интерполирование\nВариант 13\nВведите число значений в таблице (m+1):" << std::endl;
    std::cin >> m;
    std::cout << "Введите степень интерполяционного многочлена:\n";
    std::cin >> n;
    while (n > m - 1)
    {
        std::cout << "n не должно превосходить m!!!!\n Введите значение n повторно:";
        std::cin >> n;
    }
    std::cout << "Введите края отрезка:\n";
    std::cin >> a >> b;
    std::cout << "Введите точку интерполирования:\n";
    std::cin >> x;

    std::vector<std::pair<long double, long double>> interpol_table(m);
    // x_j возрастает, можно не сортировать.

    for (int j = 0; j < m; j++)
    {

        interpol_table[j].first = a + j * (b - a) / (m - 1);
        interpol_table[j].second = function(interpol_table[j].first);
    }
    for (auto &i : interpol_table)
    {
        std::cout << i.first << " ";
    }
    std::cout << std::endl;

    for (auto &i : interpol_table)
    {
        std::cout << i.second << " ";
    }
    std::cout << std::endl;

    long double approximate = lagrange_interpol(interpol_table, n, x);
    std::cout << "Полученное значение:" << approximate << std::endl;
    std::cout << "Ожидаемое значение:" << function(x) << std::endl;
    std::cout << "Отклонение:" << std::fabs(function(x) - approximate) << std::endl;
}