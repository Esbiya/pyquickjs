from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
    long_description = f.read()

setup(
    name='pyquickjs',  # 包名
    version='1.1.9',  # 版本号
    description='a quickjs call package, used for eval javascript',
    long_description=long_description,
    author='esbiya',
    author_email='2995438815@qq.com',
    url='https://github.com/Esbiya/pyquickjs',
    install_requires=[],
    license='MIT',
    packages=find_packages(),
    platforms=["all"],
    include_package_data=True,
)
