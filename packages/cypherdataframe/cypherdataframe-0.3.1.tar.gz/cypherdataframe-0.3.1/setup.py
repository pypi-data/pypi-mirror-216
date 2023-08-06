from setuptools import find_packages, setup
setup(
    name='cypherdataframe',
    packages=find_packages(include=['cypherdataframe', 'cypherdataframe.model', 'cypherdataframe.garner_domain']),
    version='0.3.1',
    description='Cypher Query to df Toolkit',
    author='Attila Vanderploeg',
    license='MIT',
    install_requires=['py2neo>=2021.2.3', 'dacite>=1.6.0'],
    setup_requires=[],
    tests_require=[],
    test_suite='tests',
)
