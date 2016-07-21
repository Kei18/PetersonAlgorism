#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Peterson Algorism
#
# created by Keisuke Okumura

from sympy import Symbol


class Peterson(object):
    """ Petersonのアルゴリズム、リードソロモン符号の復号化。行列計算は人間の手でやること。
        2元体の-0はこのプログラム内では-1として扱う
    """
    def __init__(self, a=Symbol('a')):
        self.F16 = [
            1, a, a**2, a**3, a+1, a**2+a, a**3+a**2, a**3+a+1, a**2+1,
            a**3+a, a**2+a+1, a**3+a**2+a, a**3+a**2+a+1, a**3+a**2+1, a**3+1
        ]
        self.exp_list = [0, 1, a, a**2, a**3]
        self.n = 15
        self.k = 9
        self.input = []
        self.syndrome = []
        self.q = []  # Q1_0, Q1_1, Q1_2, ... , Q1_t
        self.error_pos = []

    # =========================
    # 受信語の設定
    # =========================
    def set_input(self, input):
        self.input = input

    # =========================
    # Q1_0, ... , Q1_t を求める
    # =========================
    def set_q(self, q):
        self.q = q

    # =========================
    # 二元体の多項式の加算(式入力)
    # =========================
    def add(self, exp1, exp2):
        for exp in self.exp_list:
            if (" "+str(exp)+" " in " "+str(exp1)+" ") and (" "+str(exp)+" " in " "+str(exp2)+" "):
                exp1 -= exp
                exp2 -= exp
        result = exp1 + exp2
        return result if result is not None else -1

    # =========================
    # 二元体の多項式の加算(数字入力)
    # =========================
    def add_num(self, i, j):
        return self.get_num(self.add(self.get(i), self.get(j)))

    # =========================
    # a^iの多項式を取得
    # =========================
    def get(self, i):
        return self.F16[i % self.n] if i is not -1 else 0

    # =========================
    # 多項式からa^iを取得
    # =========================
    def get_num(self, val):
        for i in xrange(0, len(self.F16)):
            if val == self.get(i):
                return i

    # =========================
    # シンドロームの取得
    # =========================
    def get_syndrome(self):
        self.syndrome = []
        syndrome_exp = []
        for i in xrange(1, self.n-self.k+1):
            rx = [self.get((val+i*j) % self.n) if val != -1 else 0 for j, val in enumerate(self.input)]
            syndrome_exp.append(rx)
        for exp in syndrome_exp:
            result = self.get_num(reduce(self.add, exp))
            self.syndrome.append(result if result is not None else -1)

    # =========================
    # シンドロームを出力
    # =========================
    def print_syndrome(self):
        for i in xrange(0, len(self.syndrome)):
            print 'S(a^%02d) = ' % (i+1), 'a^{0:02d} ='.format(self.syndrome[i]), self.get(self.syndrome[i])

    # =========================
    # Qから誤り位置を取得する
    # =========================
    def get_error_pos(self):
        self.error_pos = []
        for x in xrange(0, len(self.F16)):
            exp = 0
            for t in xrange(0, len(self.q)):
                if self.q[t] == -1:
                    continue
                exp = self.add(exp, self.get(self.q[t]+x*(len(self.q)-t-1)))
            if exp == 0:
                self.error_pos.append(x)

    # =========================
    # 誤り位置の出力
    # =========================
    def print_error_pos(self):
        print "Error Position : ", self.error_pos


if __name__ == '__main__':
    peterson = Peterson()
    peterson.set_input([10, -1, -1, -1, -1, 10, -1, 11, -1, 15, 5, 13, -1, 14, 7])
    # シンドロームを求める
    peterson.get_syndrome()
    peterson.print_syndrome()
    # 最小次数の非零の多項式をセット
    peterson.set_q([-1, 0, 7, 9])
    # 誤り位置を取得
    peterson.get_error_pos()
    peterson.print_error_pos()
