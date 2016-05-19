from setuptools import setup

setup(
    name='lektor-markdown-table-of-contents',
    version='0.1',
    author='David Baumgold',
    author_email='david@davidbaumgold.com',
    license='MIT',
    py_modules=['lektor_markdown_table_of_contents'],
    url='http://github.com/lektor/lektor',
    entry_points={
        'lektor.plugins': [
            'markdown-table-of-contents = lektor_markdown_table_of_contents:MarkdownTOCPlugin',
        ]
    }
)
