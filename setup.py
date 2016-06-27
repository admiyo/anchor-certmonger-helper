from setuptools import setup, find_packages

desc='''\
anchor-certmonger-helper
========================

Helper program that enables Certmonger to communicate with an OpenStack Anchor CA
'''


setup(
    name = "anchor-certmonger-helper",
    version = "0.1",
    url='https://github.com/admiyo/anchor-certmonger-helper',
    
    packages = find_packages(),
)
