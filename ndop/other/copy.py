#encoding: utf-8

import time


class ManageData():
    def __init__(self, data, start=0):
        self.data = data
        self.start = start

    def data(self, start=None):
        if start is not None:
            return self.data[self.start+start:]
        return self.data[self.start:]

    def range(self, start, end):
        return self.data[self.start+start:self.start+end]

    def rangeN(self, start, nb):
        pos = self.start+start
        return self.data[pos:pos+nb]

    def at(self, pos):
        return self.data[self.start+pos]

    def inc(self, inc):
        self.start += inc

    def copy(self, inc=0):
        return ManageData(self.data, self.start + inc)

    def __getitem__(self, *args):
        return self.data[args[0]]

    def test(self, a, b):
        return self.data[a:b]


class useless():
    def __init__(self, cdata):
        self.cdata = cdata


def deeps(s, p):
    if p > 0:
        r = s[p:]
        deeps(s[1:], p-1)

def deep(s, p):
    if p > 0:
        r = s[p:]
        deep(s, p-1)

def deepc(c, p):
    if p > 0:
        r = c.at(1)
        deepc(c.copy(1), p-1)


var = str("QWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBNQWERTYUIOPASDFGHJKLZXCVBN")

varC = ManageData(var)

varU = useless(varC)

# a = time.time()
# # for j in range(100000):
# #     for i in range(6):
# #         # tmp = ManageData(var)
# #         # tmp = var[1:]
# #         tmp = varC.copy(5)
# print "Time :", time.time() - a


# a = time.time()
# for j in range(1000000):
#     for i in range(6):
#         # tmp = ManageData(var)
#         # tmp = var[1:]
#         # tmp = varC[5]
#         # tmp = varC.at(5)
#         # tmp = varC.data[5]

#         tmp = varC[5:6]
#         # tmp = varC.test(5, 6)
#         # tmp = varC.rangeN(5, 1)
#         # tmp = varC.range(5, 6)
#         # tmp = varC.data[5:6]
#         # tmp = varU.cdata.rangeN(5,1)
# print "Time :", time.time() - a

# lll = range(100000)
# a = time.time()
# # before
# for j in lll:
#     # for i in range(6):
#     deeps(var, 15)
#         # tmp = varC.data[10:]

#         # tmp = varC.data[5]
#         # tmp = varC.data[5]
#         # tmp = varC.data[5]
#         # tmp = varC.data[5]

#         # tmp = varC.data[4:6]
#         # tmp = varC.data[4:6]
#         # tmp = varC.data[4:6]
#         # tmp = varC.data[4:6]
# print "Time Before :", time.time() - a

# a = time.time()
# # after
# for j in lll:
#     # for i in range(6):
#     deepc(varC, 15)
#         # tmp = ManageData(var)

#         # tmp = varC.at(5)
#         # tmp = varC.at(5)
#         # tmp = varC.at(5)
#         # tmp = varC.at(5)

#         # tmp = varC.range(4, 6)
#         # tmp = varC.range(4, 6)
#         # tmp = varC.range(4, 6)
#         # tmp = varC.range(4, 6)
# print "Time After :", time.time() - a


# varC[5:6]

# varCc = varC.copy(5)
# print varC.start
# print varCc.start
# varC.inc(2)
# print varC.start
# print varCc.start
