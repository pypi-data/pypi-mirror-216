from xml.etree.ElementInclude import include

from setuptools import setup, find_packages

setup(
    name='LogTranslate',
    version='0.2。1',
    author='5hmlA',
    author_email='jonas.jzy@gmail.com',
    # packages=find_packages(),
    packages=['log_translate','log_translate/business'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='tools log translate',
    url='https://github.com/5hmlA/PyTools',
    description='A Python library for translate log from log files'
)

# python -m pip install --upgrade twine
# python -m build /  python setup.py sdist bdist_wheel
# twine upload --repository testpypi dist/*
# twine upload dist/*
