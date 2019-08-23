from setuptools import (
    find_packages,
    setup
)


setup(
    name='kartoshechka',
    version=__import__('kartoshechka').__VERSION__,
    packages=find_packages(exclude=('*.tests', '*.tests.*', 'tests.*', 'tests')),

    author='Maxim Kotyakov',
    author_email='m.a.kotyakov@yandex.ru',
    description='Configure applications with environment variables',
    url='https://github.com/kotyakov/envconf',

    zip_safe=True,

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
