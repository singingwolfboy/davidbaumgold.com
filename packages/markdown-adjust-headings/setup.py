from setuptools import setup

setup(
    name='lektor-markdown-adjust-headings',
    version='0.1',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    license='MIT',
    py_modules=['lektor_markdown_adjust_headings'],
    url='http://github.com/lektor/lektor',
    entry_points={
        'lektor.plugins': [
            'markdown-adjust-headings = lektor_markdown_adjust_headings:MarkdownAdjustHeadingsPlugin',
        ]
    }
)
