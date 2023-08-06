from setuptools import find_packages, setup
setup(
    name='cypherdataframe',
    packages=find_packages(
        include=[
            'cypherdataframe',
            'cypherdataframe.model',
            'cypherdataframe.garner_domain',
            'cypherdataframe.garner_domain.logistics',
            'cypherdataframe.garner_domain.measure',
            'cypherdataframe.garner_domain.queries',
            'cypherdataframe.garner_domain.reference',
            'cypherdataframe.garner_domain.status'
        ]
    ),
    version='0.3.2',
    description='Cypher Query to df Toolkit',
    author='Attila Vanderploeg',
    license='MIT',
    install_requires=['py2neo>=2021.2.3', 'dacite>=1.6.0'],
    setup_requires=[],
    tests_require=[],
    test_suite='tests',
)
