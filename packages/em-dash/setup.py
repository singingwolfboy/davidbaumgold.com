from setuptools import setup

setup(
    name='lektor-em-dash',
    version='0.1',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    license='MIT',
    py_modules=['lektor_em_dash'],
    entry_points={
        'lektor.plugins': [
            'em-dash = lektor_em_dash:EmDashPlugin',
        ]
    },
)
