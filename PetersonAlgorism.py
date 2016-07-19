#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# created by Keisuke Okumura

import math
from sympy import *


class Peterson(object):
    def __init__(self, a):
        self.F16 = [
            1, a, a**2, a**3, a+1, a**2+a, a**3+a**2, a**3+a+1, a**2+1,
            a**3+a, a**2+a+1, a**3+a**2+a, a**3+a**2+a+1, a**3+a**2+1, a**3+1
        ]
        self.exp_list = [0, 1, a, a**2, a**3]
        self.n = 15
        self.k = 9
        self.input = []
        self.syndrome = []
        self.q = [-1, 0, 7, 9]  # Q1_0, Q1_1, Q1_2, ... , Q1_t
        self.error_pos = []

    def set_input(self, input):
        self.input = input

    def set_q(self, q):
        self.q = q

    def add(self, exp1, exp2):
        for exp in self.exp_list:
            if (" "+str(exp)+" " in " "+str(exp1)+" ") and (" "+str(exp)+" " in " "+str(exp2)+" "):
                exp1 -= exp
                exp2 -= exp
        result = exp1 + exp2
        return result if result != None else -1

    def add_num(self, i, j):
        return self.get_num(self.add(self.get(i), self.get(j)))

    def get(self, i):
        return self.F16[i%self.n]

    def get_num(self, val):
        for i in xrange(0, len(self.F16)):
            if val == self.get(i):
                return i

    def get_syndrome(self):
        syndrome_exp = []
        for i in xrange(1, self.n-self.k+1):
            rx = [self.get((val+i*j)%self.n) if val!=0 else 0 for j, val in enumerate(self.input)]
            syndrome_exp.append(rx)
        for exp in syndrome_exp:
            val = reduce(self.add, exp)
            self.syndrome.append(self.get_num(val))
      
    def print_syndrome(self):
        for i in xrange(0, len(self.syndrome)):
            print 'S(%02d):'%(i+1), 'a^{0:02d} ='.format(i), self.syndrome[i]

    def get_error_pos(self):
        for x in xrange(1, len(self.F16)):
            exp = 0
            for t in xrange(0, len(self.q)):
                if self.q[t] == -1:
                    continue
                exp = self.add(exp, self.get(self.q[t]+x*(len(self.q)-t-1)))
            if exp == 0:
                self.error_pos.append(x)

    def print_error_pos(self):
        print self.error_pos


if __name__ == '__main__':
    a = Symbol('a')
    gause = Peterson(a)
    gause.set_input([10, 0, 0, 0, 0, 10, 0, 11, 0, 15, 5, 13, 0, 14, 7])
    gause.get_syndrome()
    gause.print_syndrome()
    gause.get_error_pos()
    gause.print_error_pos()