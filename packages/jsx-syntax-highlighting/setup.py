from setuptools import setup

setup(
    name='lektor-jsx-syntax-highlighting',
    version='0.1',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    license='MIT',
    py_modules=['lektor_jsx_syntax_highlighting'],
    entry_points={
        'lektor.plugins': [
            'jsx-syntax-highlighting = lektor_jsx_syntax_highlighting:JsxSyntaxHighlightingPlugin',
        ]
    },
    install_requires=['pygments-lexer-babylon'],
)
