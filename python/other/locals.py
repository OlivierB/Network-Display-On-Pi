#encoding: utf-8

"""
@author: Olivier BLIN
"""

for i in range(5):
    locals()["moduleZ"+str(i)] = i

def p():
    print locals()

if __name__ == "__main__":
    print locals()