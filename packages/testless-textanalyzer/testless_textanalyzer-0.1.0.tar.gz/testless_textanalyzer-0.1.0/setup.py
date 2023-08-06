from setuptools import setup, find_packages

with open("/home/yousif/Downloads/GP/testless/Text_Analyzer/README.md", "r") as f:
    long_description = f.read()

setup(
  name = 'testless_textanalyzer' ,
  version='0.1.0',
  description='A text analyzer for test step sentences',
  packages=find_packages(),
  author='Youssef Ahmed',
  include_package_data=True,
  license='MIT',
  long_description=long_description,
  long_description_content_type="text/markdown",
  classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
  ],
  install_requires=["nltk>=3.8" , "numpy>=1.21.5" , "pandas>=1.5.3" , "sklearn_crfsuite>=0.3.6"],
)
  
  
    