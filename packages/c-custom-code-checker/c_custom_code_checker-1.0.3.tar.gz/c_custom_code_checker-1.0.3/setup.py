from setuptools import setup, find_packages


setup(
    name='c-custom-code-checker',
    version='1.0.3',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'c-validator= c_custom_code_checker:main',
        ],
    },
    install_requires=["art>=6.0","clang>=16.0.1.1","colorama>=0.4.4","libclang>=16.0.0","tqdm>=4.65.0"],
)