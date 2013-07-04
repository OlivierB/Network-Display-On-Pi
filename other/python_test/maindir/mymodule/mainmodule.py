import sys
from mymodule.subdir import submodule
# import mymodule.subdir2.submodule2 as subdir2


def main():
    print "++in mainmodule"
    print submodule.teststring

    # print subdir2.teststring

    sys.exit(0)


if __name__ == "__main__":
    sys.exit(main())
