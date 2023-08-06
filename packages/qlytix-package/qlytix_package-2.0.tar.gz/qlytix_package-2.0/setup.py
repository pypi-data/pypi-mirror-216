from setuptools import setup

def readme():
      with open('README.rst') as f:
            return f.read()

setup(name="qlytix_package",
      version='2.0',
      description='User and Auth Data',
      long_description=readme(),
      author='Kranthi',
      author_email="k@Gmail.com",
      license='MIT',
      packages=['qlytix_pack'],
      include_package_data=True
      )