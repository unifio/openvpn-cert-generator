#!/usr/bin/env python
from setuptools import setup, find_packages

requires = [
    'awscli>=1.10.0',
    'boto>=2.34.0',
    'jinja2>=2.8',
    'plumbum>=1.6.1',
]

setup_options = dict(
    name='openvpn-cert-generator',
    description='Fun description here',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    package_data={'openvpn_cert_generator': ['templates/*', ]},
    install_requires=requires,
    scripts=['bin/openvpn-cert-generator'],
)

setup(**setup_options)
