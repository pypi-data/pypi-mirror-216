from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name="qlytix_package",
      version='4.0',
      description='User and Auth Data',
      long_description=readme(),
      author='Kranthi',
      author_email="kk@gmail.com",
      license='MIT',
      packages=['qlytix_package'],
      include_package_data=True
      )