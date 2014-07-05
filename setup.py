import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-clever-forms',
    version='0.1',
    packages=['clever_forms'],
    include_package_data=True,
    license='BSD License',  # example license
    description='A simple Django app providing useful form fields.',
    long_description=README,
    url='http://www.kingstonlabs.com/',
    author='Tom Kingston',
    author_email='tom@kingstonlabs.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    tests_require=["Django>=1.4.2"],
    test_suite='runtests.runtests'
)
