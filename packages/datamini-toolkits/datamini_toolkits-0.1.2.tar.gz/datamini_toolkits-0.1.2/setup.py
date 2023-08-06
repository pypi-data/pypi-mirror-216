from setuptools import setup, find_packages

setup(
    name='datamini_toolkits',
    version='0.1.2',
    description='A toolkit for Data Using AI(e.g. LLM) by DataMini',
    author='DataMini',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sql-data-maker = datamini_toolkits.mock_data.cli:main',
            'cmysql = datamini_toolkits.cmysql.cli:main',
        ]
    }
)