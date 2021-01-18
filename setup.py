from setuptools import find_packages, setup

setup(
    name='SimplexEd',
    packages=find_packages(include=['SimplexEd']),
    version='0.1.0',
    description='Educational Python library to demonstrate the Simplex Algorithm',
    author='Mathew Perez',
    license='Apache 2.0',
    install_requires=["numpy"],
    setup_requires=["pytest-runner"],
    tests_require=["pytest==4.4.1", "numpy"],
    test_suite="tests",
)