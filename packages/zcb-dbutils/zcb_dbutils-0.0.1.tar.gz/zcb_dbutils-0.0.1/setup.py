from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'DBUtils with pymysql by chzcb'

setup(
    name="zcb_dbutils",
    version=VERSION,
    author="chzcb",
    author_email="chzcb.04@163.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open('README.md',encoding="UTF8").read(),
    packages=find_packages(),
    install_requires=['pymysql'],
    keywords=['python', 'pymysql', 'zcb_dbutils'],
    data_files=[],
    entry_points={
    'console_scripts': [
    ]
    },
    license="MIT",
    url="https://github.com/chzcb/dbutils",
    scripts=['dbutils.py'],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows"
    ]
)