from setuptools import setup

setup(
    name='PersianConverter',
    version='1.0.1',
    packages=['persian_converter'],
    install_requires=[
        'arabic_reshaper',
        'python-bidi'
    ],
    author='Hamidreza Komeylian',
    author_email='komeylian@gmail.com',
    description='A package for converting Persian text',
    python_requires='>=3.6',
    url='https://github.com/komeylian/PersianConverter',
    license='MIT',
    keywords=['Persian', 'text conversion'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    long_description='A package for converting Persian text. This package provides functions to reshape and display Persian text.',
    long_description_content_type='text/markdown',
    package_data={
        'persian_converter': ['data/*.txt']
    },
    entry_points={
        'console_scripts': [
            'persian_convert=persian_converter:main',
        ],
    },
)
