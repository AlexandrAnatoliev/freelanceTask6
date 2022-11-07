# freelanceTask6

# Написать программу на языке Python

# Имея алгебраическое уравнение вида: (x-a)*(x-b)*(x-c)+d=0.
# Написать программу на языке Python, которая будет отделять корни с помощью метода Штурма,
# выводить таблицу с переменами знаков и интервалы, в которых лежат корни.
# В условие уже дано уравнение, например x^3-52x+d.
# Код должен быть написан таким образом, чтобы пользователь сам мог ввести d и получить результат.
# Аналитическое решение данной задачи на бумаге уже имеется, нужно лишь автоматизировать с помощью кода.
# Также нужно реализовать программный код, который будет высчитывать приближенный корень методом половинного деления
# и методом простых итераций.
#
# Обязательно с комментариями к коду и с описанием алгоритма в виде блок-схемы/по пунктам.

# pip install sympy

from sympy import *

x = Symbol('x')  # объясняем программе что 'x' это символ, а не переменная

f = (x - 2) * (x - 6) * (x + 8)  # заданная функция из задания
f0 = expand(f)  # раскрываем скобки
# f0 = x ** 3 - 52 * x + 96  # заданная функция из задания
f_list = []
f_list.append(f0)

f1 = diff(f0, x)  # дифференцируем
f_list.append(f1)


def coeff_before_x(function):
    # функция, определяющая коэффициент перед первым 'x' в уравнении
    f_string = str(function)
    x_index = f_string.index('x')
    if x_index == 0:
        coefficient = 1
    else:
        coefficient = int(f_string[:x_index - 1])
    return coefficient


def degree_x(function):
    # функция, определяющая степень первого 'x' в уравнении
    f_string = str(function)
    x_index = f_string.index('x')
    if f_string[x_index + 1] == '*' and f_string[x_index + 2] == '*':
        degree_x = int(f_string[x_index + 3])
    else:
        degree_x = 1
    return degree_x


f2 = expand(f1 * x / 3)
# print(solve(Eq(f), x))  # решить уравнение f=0, выводит [ответ1,ответ2,...]
# print(diff(f, x))  # найти производную функции F=0
print(f0)
print(f_list)
print(coeff_before_x(f1))
print(degree_x(f1))
