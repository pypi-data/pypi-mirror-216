from setuptools import find_packages, setup


NAME = 'scrapy_samwe'
DESCRIPTION = 'Smawe scrapy notes'
EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.5.0'

about = {"__version__": "0.01"}


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description="help(DefineDownloaderMiddleware)",
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(exclude=('tests',)),
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
