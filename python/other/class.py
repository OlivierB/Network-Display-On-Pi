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
        

test = Child(1,2,8)
