from setuptools import setup

with open("requirements.txt", "r") as req:
      required=req.read().splitlines()

files = ["data/*"]

setup(
      name='variational_principle_gui',
      version='1.0',
      description='A Graphical User Interface for the Variational Principle method for computing bound energy eigenstates.',
      url='https://github.com/tiernan8r/variational_principle_gui',
      author='Tiernan8r',
      author_email='tiernan8r@pm.me',
      license='MIT',
      install_requires=required,
      include_package_data=True,
      packages=['variational_principle_gui'],
      package_data={"variational_principle_gui": files},
      zip_safe=True,
)
