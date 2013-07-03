#encoding: utf-8

class Base(object):
    def __init__(self):
        print "Base created"

class ChildA(Base):
    def __init__(self):
        Base.__init__(self)

class ChildB(Base):
    def __init__(self):
        super(ChildB, self).__init__()


# print ChildA(),ChildB()

class X(object):
  def __init__(self, x=1):
    print "init X", x

  def doit(self, bar):
    print "doit X", bar

class Y(X):
  def __init__(self):
    super(Y, self).__init__()
    print "init Y"

  def doit(self, foo):
    print "doit Y", foo
    return super(Y, self).doit(foo)

# a = Y(2)

class Parent(object):
    def __init__(self, a=11, b=12, bb=10, cc=20):
        print 'a', a
        print 'b', b
        print 'bb', bb
        print 'cc', cc

class Child(Parent):
    def __init__(self, c, d, *args, **kwargs):
        super(Child, self).__init__(*args, **kwargs)
        print 'c', c
        print 'd', d
        

# test = Child(1,2,8)
def is_ok(a):
    if a in ["Ethernet", "IPv4", "TCP", "HTTP", "DNS"]:
        return True
    else:
        return False

def is_protocol(*args):
        if len(args) > 0:
            print args[0]
            if args[0] == "*" or is_ok(args[0]):
                return is_protocol(*args[1:])
            else:
                return False
        else:
            return True

print is_protocol("Ethernet", "IPv4", "*", "DNS")