from setuptools import setup, find_packages


setup(
    name='mkdocs-plugin-rzk',
    version='0.1.1',
    description='A MkDocs plugin for Literate Rzk',
    long_description='This plugin automates the generation of SVG renderings for code snippets in Literate Rzk Markdown files rendered using MkDocs.',
    keywords='mkdocs',
    author='Abdelrahman Abounegm',
    author_email='a.abounegm@innopolis.university',
    license='MIT',
    install_requires=[
        'mkdocs>=1.4.0'
    ],
    packages=find_packages(),
    entry_points = {
        'mkdocs.plugins': [
            'rzk = rzk.generate_svgs:RzkPlugin',
        ]
    }
)
