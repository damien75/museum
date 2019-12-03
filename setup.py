import os
from setuptools import setup, find_packages

version = os.environ.get('PACKAGE_VERSION', '0.0.0')

INSTALL_REQUIRES = [
    'attrs'
]

EXTRAS_REQUIRE = {}


def setup_package():
    setup(
        name='museum',
        version=version,
        author='Damien Goblot',
        description='Museum visits analysis package',
        packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
        install_requires=INSTALL_REQUIRES,
        extras_require=EXTRAS_REQUIRE,
        package_dir={'visits': 'visits'},
        include_package_data=True,
        entry_points={
            'console_scripts': [
                'visits = visits.main:main'
            ]
        }
    )


if __name__ == '__main__':
    setup_package()
