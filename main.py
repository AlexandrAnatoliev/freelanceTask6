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

# Решение нелинейного уравнения типа (𝑥 − 𝑎)(𝑥 − 𝑏)(𝑥 − 𝑐) + d = 0
# *********************************************************************************************************************
from sympy import *


def coeff_before_x(function):
    # функция, определяющая коэффициент перед первым 'x' в уравнении
    fl_sign = 'plus'  # флаг знака числа
    f_string = str(function)
    x_index = f_string.index('x')
    if ' ' in f_string[:x_index]:  # если есть пробел перед 'x'
        space_count = f_string.count(' ', 0, x_index)  # число пробелов до 'x'
        space_index = 0
        for i in range(space_count):
            space_index = f_string.find(' ', space_index + 1, x_index)  # последний пробел - пробел перед числом
        if x_index == len(f_string) - 1:  # если 'x' крайний справа
            fl_sign = 'plus' if '+' == f_string[space_index - 1] else 'minus'
    else:
        space_index = -1

    if x_index == 0:
        coefficient = 1
    else:
        # если выражение типа 56789 - 98765*x, то коэффициент с отрицательным знаком
        coefficient = int(f_string[space_index + 1:x_index - 1]) if fl_sign == 'plus' else -int(
            f_string[space_index + 1:x_index - 1])
    return coefficient


def degree_x(function):
    # функция, определяющая степень первого 'x' в уравнении
    f_string = str(function)
    if 'x' in f_string:
        x_index = f_string.index('x')
        if x_index == len(f_string) - 1:  # если 'x' крайний справа
            degree_x = 1
        else:
            if f_string[x_index + 1] == '*' and f_string[x_index + 2] == '*':
                degree_x = int(f_string[x_index + 3])
            else:
                degree_x = 1
    else:
        degree_x = 0
    return degree_x


def residue_func(func0, func1):
    # функция приводящая две функции к одному виду и опредяляющая остаток их разности
    f0_reduction = expand(func0 * coeff_before_x(func1))
    f1_reduction = expand(func1 * coeff_before_x(func0) * (x ** (degree_x(func0) - degree_x(func1))))
    func2 = f0_reduction - f1_reduction
    return func2


def calculate_residue(func1, func2):
    # функция, определяющая нужно ли дальше вычислять остаток
    if degree_x(func2) < degree_x(func1):  # если степень остатка меньше степени функции, на которую делят
        residue = -func2
    else:
        residue = -residue_func(func2, func1)  # иначе - еще раз вычисляем
    return residue


# ввод данных для решения уравнения и получение системы Штурма
# **********************************************************************************************************************

print("Решаем нелинейное уравнения типа (x - a)(x - b)(x - c) + d  = 0")
a, b, c, d = map(int, input("Введите коэффициенты уравнения в формате: a b c d: ").split())
x = Symbol('x')  # объясняем программе что 'x' это символ, а не переменная

f = (x - a) * (x - b) * (x - c) + d  # заданная функция из задания
f0 = expand(f)  # раскрываем скобки и приводим функцию к виду f0 = x ** 3 - 52 * x + 96
f1 = diff(f0, x)  # дифференцируем

f_list = []  # создаем список функций (система Штурма)

f_list.append(f0)
f_list.append(f1)

fl = True  # начало цикла занесения формул в список
i = 0
while fl == True:
    f_list.append(calculate_residue(f_list[i + 1], residue_func(f_list[i], f_list[i + 1])))
    if diff(f_list[i + 2], x) == 0:  # пока остаток не является функцией (производная числа = 0)
        fl = False  # стоп цикл
    i += 1


# Создание таблицы Штурма
# **********************************************************************************************************************

# Определим знаки  многочленов при плюс и при минус бесконечность. Вычислять  ничего не нужно.
# Достаточно посмотреть только на коэффициенты при старших степенях и на сами эти степени.
# определим количество изменений знака системы штурма при плюс\минус бесконечности
# Определим количество действительных корней как разницу между ними


def define_sign_infinity(func):
    # функция опеделяющая знак функции при плюс/минус-бесконечности
    if degree_x(func) == 0:  # если функция - число
        if define_sign_before_number(func) == 'plus':  # если знак перед числом 'плюс'
            sign_plus_inf = '+'
            sign_minus_inf = '-'
        else:
            sign_plus_inf = '-'
            sign_minus_inf = '+'
    else:
        if degree_x(func) % 2 == 0:  # если функция четная
            sign_plus_inf = '+'  # знак функции при плюс-бесконечности
            sign_minus_inf = '+'  # знак функции при минус-бесконечности
        else:
            sign_plus_inf = '+'
            sign_minus_inf = '-'
    return sign_plus_inf, sign_minus_inf


def create_shturm_table(lst):
    # создание таблицы Штурма при минус\плюс бесконечности
    table = []
    for i in range(len(lst)):
        table.append(define_sign_infinity(lst[i]))
    return table


def define_sign_before_number(func):
    # функция, определяющая знак перед первым числом
    func = str(func)
    if func[0] == '-':
        fl = 'minus'
    else:
        fl = 'plus'
    return fl


def count_sign_change(lst, index):
    # функция, считающая число изменений знака в системе Штурма (для бесконеччностей)
    fl = lst[0][index]  # начальное значение флага
    count = 0
    for i in range(len(lst)):
        if lst[i][index] != 0:  # если знак = 0, то значение флага не изменяется и проверяется следующее значение
            if lst[i][index] != fl:
                fl = lst[i][index]
                count += 1
    return count


def calculation_func_value(func, x_value):
    # вычисление значения функции при заданном аргументе 'x_value'
    y = func.subs({x: x_value})
    return y


def define_sign_func_value(func_value):
    # функция, определяющая знак вычисленного значения функции
    if func_value < 0:
        fl = 'minus'
    elif func_value > 0:
        fl = 'plus'
    else:
        fl = 0
    return fl


def count_sign_func_change(lst):
    # функция, считающая число изменений знака в системе Штурма (для вычисленных значений функций)
    fl = lst[0]  # начальное значение флага
    count = 0
    for i in range(len(lst)):
        if lst[i] != 0:  # если знак = 0, то значение флага не изменяется и проверяется следующее значение
            if lst[i] != fl:
                fl = lst[i]
                count += 1
    return count


def create_sign_list(lst, arg_x):
    # функция, вычисляющая значение функции при заданном аргументе 'x' и создающая список знаков(+\-)
    sign_list = []  # список знаков вычисленных значений функции
    for i in range(len(lst)):
        sign_list.append(define_sign_func_value(calculation_func_value(lst[i], arg_x)))
    return sign_list


# определим количество изменений знака системы штурма при плюс\минус бесконечности
# Определим количество действительных корней как разницу между ними
inf_table = create_shturm_table(f_list)  # таблица Штурма для плюс\минус бесконечности
valid_roots = abs(count_sign_change(inf_table, 0) - count_sign_change(inf_table, 1))  # количество действительных корней

# определим диапазон, в котором будем искать корни.
# Вычисляем количество изменений знака системы Штурма при разных значениях аргумента 'x'.
# Искомый диапазон от '0' изменений до числа, равного количествку действительных корней.
# !!! разобраться!!!
max_root_list = []  # список количеств изменений знака системы Штурма при разных значениях аргумента 'x'.
max_root_list.append(count_sign_func_change(create_sign_list(f_list, -12)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, -9)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, -6)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, -3)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 0)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 3)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 6)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 9)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 12)))  # x = 0
max_root_list.append(count_sign_func_change(create_sign_list(f_list, 15)))  # x = 0
print(f_list[0].subs({x: -9}))  # вычисляет значение функции из списка с x=0
print(f_list[0].subs({x: -6}))  # вычисляет значение функции из списка с x=0
print(f_list[0].subs({x: 0}))  # вычисляет значение функции из списка с x=0
print(f_list[0].subs({x: 3}))  # вычисляет значение функции из списка с x=0
print(f_list[0].subs({x: 6}))  # вычисляет значение функции из списка с x=0
print(f_list[0].subs({x: 9}))  # вычисляет значение функции из списка с x=0
x_arg = 1  # начальное значение х
# while (0 not in max_root_list):
# пока не найдены значения изменений системы штурма: '0' и 'количество действительных корней'
#    print(max_root_list)
#    max_root_list.append(count_sign_func_change(create_sign_list(f_list, x_arg)))
#    max_root_list.append(count_sign_func_change(create_sign_list(f_list, -x_arg)))
#    x_arg += 1
# print(0 not in max_root_list)
print(max_root_list)

print(calculation_func_value(f_list[3], 0))
print(define_sign_func_value(calculation_func_value(f_list[3], 0)))
print(f_list)
print(inf_table)
print(valid_roots)

# print(f_list[0].subs({x: 0}))  вычисляет значение функции из списка с x=0
