from setuptools import setup
from geometrical_layout import version


def get_version() -> str:
    """
    read version from VERSION file
    """
    return version.__version__


setup(
    name='geometrical-layout',
    version=get_version(),
    description='This client library is designed to help query endpoints of the "Dowell Geometrical Layout of Big Data API"',
    maintainer='Abdullahi Abdulwasiu',
    maintainer_email='abdullahiabdulwasiu1@gmail.com',
    url='https://github.com/DoWellUXLab/DoWell-Geometrical-layout-of-Big-Data',
    license='Apache',
    packages=["geometrical_layout"],
    package_dir={
        'geometrical_layout': 'geometrical_layout'},
    long_description=open("README.rst").read(),
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=['requests'],
)
