#! /usr/bin/env python
# -*- coding: utf-8 -*-

import profile



def main():
    """
    main function
    """
    # server.main()

    return 0


if __name__ == "__main__":
    # pr = profile.Profile()
    # for i in range(5):
    #     your_computed_bias = pr.calibrate(10000)

    # pr = profile.Profile(bias=your_computed_bias)


    # profile.run('main()')

    profile.run("import server; server.main()")

