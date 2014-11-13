"""
Flask-SQLite3
-------------

This is the description for that library
"""
from setuptools import setup


setup(
    name='Flask-Settings',
    version='0.9',
    url='#',
    license='BSD',
    author='John Paskalis - Theseas Maroulis',
    author_email='j.paskal@coding-labs.eu, info@theseas.eu',
    description='This is an extensions that lets you add custom settings variable without initiallizing everything at the conf.py file. It is designed to be quite simple and fast at extracting and referensing custom variables',
    long_description=__doc__,
    py_modules=['flask_settings'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)