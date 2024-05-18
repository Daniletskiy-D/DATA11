#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Для своего индивидуального задания лабораторной работы 2.23
# необходимо реализовать вычисление значений
# в двух функций в отдельных процессах.

import math
from multiprocessing import Process, Manager

E = 10e-7


def series1(x, eps, results):
    s = 0
    n = 1
    while True:
        term = (-1) ** (n + 1) * math.sin(n * x) / n
        if abs(term) < eps:
            break
        else:
            s += term
            n += 1
    results["series1"] = s


def series2(x, eps, results):
    s = 0
    n = 0
    term = x 
    while abs(term) >= eps:
        s += term
        n += 1
        term *= x ** 2 / ((2 * n) * (2 * n + 1))
    results["series2"] = s


def main():
    with Manager() as manager:
        results = manager.dict()

        x1 = -math.pi / 2
        control_value1 = math.sin(x1)

        x2 = 2
        control_value2 = (math.exp(x2) - math.exp(-x2)) / 2

        process1 = Process(target=series1, args=(x1, E, results))
        process2 = Process(target=series2, args=(x2, E, results))

        process1.start()
        process2.start()

        process1.join()
        process2.join()

        sum1 = results["series1"]
        sum2 = results["series2"]

        print(f"x1 = {x1}")
        print(f"Sum of series 1: {round(sum1, 7)}")
        print(f"Control value 1: {round(control_value1, 7)}")
        print(f"Match 1: {round(sum1, 7) == round(control_value1, 7)}")

        print(f"x2 = {x2}")
        print(f"Sum of series 2: {round(sum2, 7)}")
        print(f"Control value 2: {round(control_value2, 7)}")
        print(f"Match 2: {round(sum2, 7) == round(control_value2, 7)}")


if __name__ == "__main__":
    main()
