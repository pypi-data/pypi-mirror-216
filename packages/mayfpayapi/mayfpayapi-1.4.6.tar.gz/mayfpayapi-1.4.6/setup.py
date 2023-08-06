from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='mayfpayapi',
    version='1.4.6',
    author='MayfPay.top',
    author_email='support@mayfpay.top',
    description='MayfPayApi is a Python library for interacting with the MayfPay payment system API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/MAYFPAY/MayfPayApi',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls={
        'Source': 'https://github.com/MAYFPAY/MayfPayApi',
        'Documentation': 'https://mayfpay.top/docs',
        'Bug Reports': 'https://github.com/MAYFPAY/MayfPayApi/issues',
    },
    python_requires='>=3.6',
    install_requires=[
        'requests',
    ],
)
