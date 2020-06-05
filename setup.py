from setuptools import find_packages, setup

version = '1.1.1'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='best_python_logger',
      version=version,
      description="A great python logger to fulfill your needs ",
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Unix",
      ],
      python_requires='>=3.6',
      keywords='logging handler concurrent logger log',
      author='Teodoro B. Mendes',
      author_email='teobmendes@gmail.com',
      url='https://github.com/herzog0/best_python_logger',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=[]
      )
