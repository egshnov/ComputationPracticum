#include <iostream>
#include <cmath>
#include <vector>

using segment = std::pair<long double, long double>;
/*
0 - last segment
1 - cnt
2 - x
*/

// TODO: setpricision(100)
// TODO: ошибка в секущих
// TODO: запрос эпсилона

using method_func = std::tuple<segment, int, long double>(const segment &, long double);

long double cmp_eps = 1e-10;

long double function(long double x)
{
    return std::sin(x) + x * x * x - 9 * x + 3;
}

long double function_derivative(long double x)
{
    return std::cos(x) + 3 * x * x - 9;
}

std::vector<segment> root_separation(long double A, long double B, int N)
{
    long double h = (B - A) / N;
    long double x1 = A;
    long double x2 = x1 + h;
    long double y1 = function(x1);
    std::vector<segment> res;

    while (x2 < B || std::fabs(B - x2) < cmp_eps)
    {
        long double y2 = function(x2);
        if (y2 * y1 <= 0) // TODO: normal float comparison
        {
            res.emplace_back(x1, x2);
        }
        x1 = x2;
        x2 = x1 + h;
        y1 = y2;
    }
    return res;
}

std::tuple<segment, int, long double> bisection(const segment &inp, long double eps)
{
    long double a = inp.first;
    long double b = inp.second;
    int cnt = 0;
    while (b - a > 2 * eps)
    {
        cnt++;
        long double c = (a + b) / 2;
        if (function(a) * function(c) <= 0)
            b = c;
        else
            a = c;
    }
    return {{a, b}, cnt, (a + b) / 2};
}

std::tuple<segment, int, long double> newton(const segment &inp, long double eps)
{
    long double x_k_1 = (inp.first + inp.second) / 2;
    long double x_k = x_k_1 - function(x_k_1) / function_derivative(x_k_1);
    int cnt = 1;
    while (std::fabs(x_k - x_k_1) >= eps)
    {
        x_k_1 = x_k;
        x_k = x_k_1 - function(x_k_1) / function_derivative(x_k_1);
        cnt++;
    }
    return {{x_k_1, x_k}, cnt, x_k};
}

std::tuple<segment, int, long double> mod_newton(const segment &inp, long double eps)
{
    long double x_0 = (inp.first + inp.second) / 2;
    long double x_k_1 = x_0; // x_k-1
    long double x_k = x_k_1 - function(x_k_1) / function_derivative(x_0);
    int cnt = 1;
    while (std::fabs(x_k - x_k_1) >= eps)
    {
        x_k_1 = x_k;
        x_k = x_k_1 - function(x_k_1) / function_derivative(x_0);
        cnt++;
    }
    return {{x_k_1, x_k}, cnt, x_k};
}

std::tuple<segment, int, long double> secant(const segment &inp, long double eps)
{
    long double x_k_2 = (inp.first + inp.second) / 2;
    long double x_k_1 = (x_k_2 + inp.second) / 2;
    long double x_k = x_k_1 - function(x_k_1) / (function(x_k_1) - function(x_k_2)) * (x_k_1) - (x_k_2);
    int cnt = 1;
    while (std::fabs(x_k - x_k_1) >= eps)
    {
        x_k_2 = x_k_1;
        x_k_1 = x_k;
        x_k = x_k_1 - function(x_k_1) / (function(x_k_1) - function(x_k_2)) * (x_k_1 - x_k_2);
        cnt++;
    }
    return {{x_k_1, x_k}, cnt, x_k};
}

int main()
{
    std::cout << "Задание 1: Численные методы решения нелинейных уравнений" << std::endl;

    long double A, B, eps = 1e-8;
    int N;
    std::cout << "f(x) = sin(x) + x^3 - 9x + 3" << std::endl;
    // std::cout << "eps = " << eps << std::endl;
    std::cout << "Введите края отрезка [A,B]:" << std::endl;
    std::cin >> A >> B;
    bool end_input = false;
    std::vector<segment> segments;

    while (!end_input)
    {
        std::cout << "Введите значение N:" << std::endl;
        std::cin >> N;
        segments = root_separation(A, B, N);

        std::cout << "Число отрезков: " << segments.size() << std::endl;
        for (auto &i : segments)
        {
            std::cout << "[" << i.first << "," << i.second << "], ";
        }
        std::cout << std::endl;
        std::cout << "Прекратить отделение?\n";
        std::cin >> end_input;
    }

    auto helper = [](const segment &inp, long double eps, method_func *method)
    {
        auto [seg, cnt, x] = method(inp, eps);
        std::cout << "число шагов: " << cnt << std::endl;
        std::cout.precision(16);
        std::cout << "приближенное решение:" << x << std::endl;
        std::cout.precision(16);
        std::cout << "|x_m - x_(m-1)| = " << std::fabs(seg.first - seg.second) << std::endl;
        std::cout.precision(16);
        std::cout << "|f(x_m) - 0| = " << std::fabs(function(x)) << std::endl;
    };

    for (auto &i : segments)
    {
        std::cout << "Введите для eps нового отрезка:\n";
        std::cin >> eps;
        bool change_eps = false;
        do
        {

            std::cout << "Метод бисекции:" << std::endl;
            std::cout << "[" << i.first << ", " << i.second << "]" << std::endl;
            helper(i, eps, bisection);
            std::cout << "\n\n\n";
            std::cout << "Метод ньютона:\n";
            std::cout << "[" << i.first << ", " << i.second << "]" << std::endl;
            helper(i, eps, newton);
            std::cout << "\n\n\n";
            std::cout << "Модифицированный метод ньютона:\n";
            std::cout << "[" << i.first << ", " << i.second << "]" << std::endl;
            helper(i, eps, mod_newton);
            std::cout << "\n\n\n";
            std::cout << "Метод секущих:\n";
            std::cout << "[" << i.first << ", " << i.second << "]" << std::endl;
            helper(i, eps, secant);
            std::cout << "\n\n\n";
            std::cout << "Поменять eps?\n";
            std::cin >> change_eps;
            if (change_eps)
            {
                std::cout << "Введите eps:\n";
                std::cin >> eps;
            }
            if (!change_eps)
                break;

        } while (true);
    }
}
