import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()
setuptools.setup(
    name="python-hello",
    version="0.0.1",
    author="james.lee",
    author_email="james.lee2015@gmail.com",
    description="PyPI Example",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    install_requires=[
        'pymysql>=0.10.0',
        'retrying==1.3.3',
        'xlrd>=1.2.0',
        'openpyxl>=3.0.5'
    ],
    python_requires=">=3"
)
