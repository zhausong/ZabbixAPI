# coding=utf8

from setuptools import setup

setup(
    name='ZabbixAPI',
    version='1.0.0',
    author='itnihao',
    author_email='admin@itnihao.com',
    description=('Zabbbix API'),
    keywords='Zabbix API',
    packages=['ZabbixAPI'],
    include_package_data=True,
    zip_safe=False,
    url='https://github.com/itnihao/ZabbixAPI',
    scripts=['zbx_tool'],
    install_requires=[
        'requests>=2.3.0'
    ],
    classifiers=[
        'Environment :: Console',
        'Development Status :: 2 - Production/Stable',
        'Topic :: System :: Monitoring',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
