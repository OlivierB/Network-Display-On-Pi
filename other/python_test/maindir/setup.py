from setuptools import setup, find_packages
print find_packages()
setup(
    name = "mytestmodule",
    version = "0.0.1",
    description = ("A simple module."),
    packages=find_packages(),
    entry_points={"console_scripts": ["mymodule=mymodule.mainmodule:main"]},
)