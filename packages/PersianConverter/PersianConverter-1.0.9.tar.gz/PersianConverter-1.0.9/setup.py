from setuptools import setup

setup(
    name='PersianConverter',
    version='1.0.9',
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
    long_description='''
    A package for converting Persian text. This package provides functions to reshape and display Persian text.
    
    # PersianConverter
    
    [![PyPI version](https://img.shields.io/pypi/v/PersianConverter.svg)](https://pypi.org/project/PersianConverter/)
    [![License](https://img.shields.io/pypi/l/PersianConverter.svg)](https://github.com/your_username/PersianConverter/blob/main/LICENSE)

    PersianConverter is a Python package for converting Persian text. It provides functions to reshape Persian text, apply the bidirectional algorithm, and display Persian text using proper presentation forms.

    ## Installation

    You can install PersianConverter using pip:

    ```shell
    pip install PersianConverter
    ```

    ## Usage

    Here's an example of how to use PersianConverter:

    ```python
    from persian_converter import fprint

    text = "سلام من کمیلیان هستم"
    converted_text = fprint(text)
    print(converted_text)
    ```

    ```python
    from persian_converter import fprint

    def display_number(number):
        """
        Function display_number: This function takes a number as input and converts it to Persian text,
        then prints the converted number.
        """
        converted_number = fprint(number)
        print(converted_number)

    numbers = ["یک", "دو", "سه"]

    for number in numbers:
        # Calling the display_number function to display the converted number
        display_number(number)
    ```








    This will output the text in a properly reshaped and bidirectionally aligned format.

    ## How It Works
    PersianConverter utilizes the arabic_reshaper and python-bidi libraries to reshape and display Persian text. It takes input text in Persian and applies reshaping and bidirectional algorithms to ensure the correct rendering of the text.

    For more information and detailed documentation, please refer to the documentation (in Persian).



    # نصب و استفاده از کتابخانه PersianConverter



    ## نحوه نصب 

    بار نصب ار دستور pip به شرح ذیل استفاده کنید :

    ```shell
    pip install PersianConverter
    ```



    ## نمونه کد استفاده:
    ```python
    from persian_converter import fprint

    text = "سلام من کمیلیان هستم"
    converted_text = fprint(text)
    print(converted_text)
    ```


    ```python
    from persian_converter import fprint

    def display_number(number):
        """
        تابع display_number: این تابع یک عدد را دریافت می‌کند و آن را تبدیل به فارسی می‌کند،
        سپس عدد تبدیل شده را چاپ می‌کند.
        """
        converted_number = fprint(number)
        print(converted_number)

    numbers = ["یک", "دو", "سه"]

    for number in numbers:
        # فراخوانی تابع display_number برای نمایش عدد تبدیل شده
        display_number(number)

    ```



    ## برای تبدیل متن فارسی و نمایش آن با قالب مناسب و ترتیب صحیح، از این کتابخانه استفاده می‌شود.

    جهت مطالعه و مستندات بیشتر، به مستندات مراجعه کنید.


    ## Feel free to customize and enhance the text according to your specific needs and preferences.

   
    ''',
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
