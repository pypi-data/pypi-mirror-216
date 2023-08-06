from setuptools import setup, find_packages

setup(
    name='netautomate.netorca',
    version='1.0.7',
    author='Scott Rowlandson',
    author_email='scott@netautomate.org',
    description='Ansible modules to interact with NetOrca',
    packages=find_packages(),
    install_requires=[
        'ansible-base',
    ],
)