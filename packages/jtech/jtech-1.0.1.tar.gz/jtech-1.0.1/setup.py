from setuptools import setup
import pkg_resources

with open('requirements.txt', 'r') as file:
    requirements = file.readlines()
    requirements = [req.strip() for req in requirements if req.strip()]

setup(
    name='jtech',
    version='1.0.1',
    packages=['jtech'],
    package_data={
        'jtech': ['resources/dependencies/dependencies.json', 'resources/tpl/*.tpl', 'resources/banner/banner.txt',
                  'resources/mock/*.tar.gz']},
    include_package_data=True,
    author='Angelo Vicente Filho',
    author_email='angelo.vicente@veolia.com',
    description='Jtech Project CLI',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.12'
    ],
    entry_points={
        'console_scripts': [
            'jtech = jtech.__main__:main'
        ]
    },
    install_requires=requirements
)
