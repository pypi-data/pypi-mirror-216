# -*- coding: utf-8
# author: zarhin
# date: 2020/7/21 16:35

from setuptools import setup, find_packages
import re


# from Cython.Build import cythonize
def get_property(prop, project):
    result = re.search(r'{}\s*=\s*[\'"]([^\'"]*)[\'"]'.format(prop),
                       open(project + '/__init__.py').read())
    return result.group(1)


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='osbuilder',
    version=get_property('__version__', 'osbuilder'),
    description='The pre-& post-processing for openseespy.',
    author='zarhin',
    author_email='lizaixianvip@live.com',
    install_requires=[
        'numpy>=1.18.1', 'matplotlib>=3.1.3', 'scipy>=1.5.0',
        'openseespy>=3.2.2.6'
    ],
    packages=find_packages(exclude=('tests')),
    # ext_modules=cythonize(['osbuilder/preprocess/part/tools_cython.pyx'],
    #                       compiler_directives={'language_level': "3"}),
)
# setup(
#     name='osbuilder',
#     version='3.1.4',
#     description='The pre-& post-processing for openseespy.',
#     author='zarhin',
#     author_email='lizaixianvip@live.com',
#     install_requires=[
#         'numpy>=1.18.1', 'matplotlib>=3.1.3', 'scipy>=1.5.0',
#         'openseespy>=3.2.2.6'
#     ],
#     packages=find_packages(exclude=('tests', 'doc')),
#     # ext_modules=cythonize(['osbuilder/preprocess/part/tools_cython.pyx'],
#     #                       compiler_directives={'language_level': "3"}),
# )
