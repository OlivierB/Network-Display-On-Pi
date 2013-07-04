from mymodule.subdir.subsubdir import subsubmodule
# import subsubdir.subsubmodule

print "++++in submodule"
print subsubmodule.teststring
# print subsubdir.subsubmodule.teststring

from mymodule.subdir2 import submodule2
# import mymodule.subdir2.submodule2 as subdir2
print "NON -", submodule2.teststring


teststring = "submodule"