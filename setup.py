import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-populars",
    version="0.1",
    url='http://github.com/fireinthehole/django-populars',
    license='BSD',
    description="Django application that evaluates the popularity for chosen objects. Could work with django-hitcount, django-popularity or other view counting application.",
    long_description=read('README.rst'),
    author='Damian Daskalov',
    author_email='daskalov.damian@gmail.com',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
