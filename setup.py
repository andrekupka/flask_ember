"""
Flask-Ember
-------------

An extension that generates JSON API compatible apis for Flask.
"""
from setuptools import setup


setup(
    name='Flask-Ember',
    version='0.0.1',
    url='http://example.com/flask-sqlite3/',
    license='BSD',
    author='Andre Kupka',
    author_email='kupka@in.tum.de',
    description='Ember compatible JSON API generation for Flask',
    long_description=__doc__,
    py_modules=['flask_ember'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    test_suite='nose.collector',
    setup_requires=[
        'nose>=1.0'
    ],
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
