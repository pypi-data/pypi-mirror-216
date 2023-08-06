from setuptools import setup

with open('README.md', 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='atc_easy_desktop',
    version='1.0.3',
    description='Thư viện sử dụng để code game trên màn hình desktop',
    long_description=long_description,
    author='Chienbg200',
    author_email='chienbg200400@gmail.com',
    packages=['atc_easy_desktop'],
    install_requires=[
        'pywin32',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Software Development :: Libraries',
    ],
)
